"""

sync options.

 - sync synchronously

 - sync async

benefit to async syncing, is any errors in sync won't hose an order.

$Id: $
"""

from getpaid.core import interfaces
from getpaid.warehouse.interfaces import IProductInventory
from zope import component, schema

import domain

def copyAddress( source_addr, target_addr, prefix=None):
    field_names = schema.getFields( interfaces.IAddress ).keys()
    for f in field_names:
        fn = prefix and "%s_%s"%(prefix, f) or f
        value = getattr( source_addr, fn, None)
        setattr( target_addr, f, value )

def copyItem( source, target ):
    
    i = interfaces.IShippableLineItem.providedBy( source ) \
        and interfaces.IShippableLineItem \
        or interfaces.IPayableLineItem
    
    field_names = set( schema.getFields( i ).keys() )
    field_names.remove('item_id')
    
    for f in field_names:
        value = getattr( source, f, None)
        setattr( target, f, value )

    target.item_zid = source.uid
    target.product_code = source.__name__

def copyCustomer( source, target ):
    for f in schema.getFields( interfaces.IUserContactInformation ).keys():
        value = getattr( source, f )
        setattr( target, f, value )

def copyProduct( source, target, item=None, uid=None ):
    payable = interfaces.IPayable( source )
    uid = item and item.uid or uid
    assert uid, "must pass in either item or uid"

    target.content_uid = uid
    target.supplier_uid = payable.made_payable_by
    target.product_code = payable.product_code or payable.context.UID()
    target.type = "payable"
    target.price = payable.price

    # copy inventory information if available
    inventory = component.queryAdapter( source, IProductInventory )
    if inventory:
        target.pick_bin = inventory.pickbin
        target.stock = inventory.stock
        target.stock_reserve= inventory.store_stock

def copyProductInventory( source, target ):
    target.stock = source.stock
    target.stock_reserve = source.store_stock
    
def copyState( source, target ):
    # handle workflow states
    target.finance_status = source.finance_state
    target.fulfillment_status = source.fulfillment_state

def copyOrder( _session, source, target ):

    # identity info
    target.order_zid = source.order_id
    
    target.creation_date = source.creation_date
    
    # handle workflow states
    target.finance_status = source.finance_state
    target.fulfillment_status = source.fulfillment_state
    
    # handle addresses
    billing_address = domain.Address()
    copyAddress( source.billing_address, billing_address, 'bill' )

    # ifpeople doesn't like the integrity constraint, as their
    # shipping free orders sans billing in some cases
    if billing_address.first_line:
        target.billing_address = billing_address
    
    shipping_address = domain.Address()
    if source.shipping_address.ship_same_billing:
        target.shipping_address = billing_address
    else:
        copyAddress( source.shipping_address, shipping_address, 'ship')
        target.shipping_address = shipping_address

    # handle customer/contact info
    customer = domain.Customer()
    copyCustomer( source.contact_information, customer )
    target.contact_information = customer
    target.contact_information.user_id = source.user_id
    
    # handle line items
    for _item in source.shopping_cart.values():
        item = domain.LineItem()
        copyItem( _item, item )
        target.items.append( item )
        
        if not interfaces.IPayableLineItem.providedBy( _item ):
            continue

        # try to find an existing record for this line item's product
        product = _session.query( domain.Product ).filter(
            domain.Product.content_uid == _item.uid ).first()
        
        # if we do find one, attach, continue
        if product is not None:
            item.product = product
            continue

        # else resolve item to product and serialize product
        payable = _item.resolve()
        if payable is None:
            continue
        
        product = domain.Product()
        copyProduct( payable, product, item=_item )
        _session.save( product )
        item.product = product
        
    
