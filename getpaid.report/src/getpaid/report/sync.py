"""

sync options,

 - sync synchronously

 - sync async
 
we want to do several kinds of reports

$Id: $
"""

from getpaid.core import interfaces
from getpaid.warehouse import interfaces
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

    target.item_zid = source.item_id

def copyProduct( item, source, target ):

    #target.product_code = item.
    
    inventory = component.queryAdapter( source, interfaces.IProductInventory )
    target.pick_bin = target.pickbin
    target.stock = source.stock
    target.store_stock= source.store_stock

def handleOrderTransition( _order, event ):
    """
    """

def handleNewOrder( _order, event ):
    """
    """
    s = session.Session()
    
    order = domain.Order()

    # handle addresses
    billing_address = domain.Address()
    copyAddress( _order.billing_address, billing_address, 'bill' )
    order.billing_address = billing_address

    shipping_address = domain.Address()
    if _order.shipping_address.ship_same_billing:
        order.shipping_address = billing_address
    else:
        copyAddress( _order.shipping_address, shipping_address, 'ship')
        order.shipping_address = shipping_address
    
    # handle line items
    for _item in _order.shopping_cart.values():
        item = domain.LineItem()
        copyItem( _item, item )
        order.items.append( item )

        # serialize products if we haven't seen them.
        if not interfaces.IPayableLineItem.providedBy( _item ):
            continue        
        if s.query( domain.Product ).query( domain.Product.content_uid == _item.uid ).count():
            continue
        
        payable = _item.resolve()
        if payable is None:
            continue
        
        product = domain.Product()
        copyProduct( item, payable, product )
        

        
    s.begin()
    s.save( order )
    s.commit()

def sync( ):
    
    manager = component.getUtility( interfaces.IOrderManager )
    session = orm.Session()
    domain.Order

    s = session.Session()
    s.begin()
    s.save( order )
    s.commit()
    
    
