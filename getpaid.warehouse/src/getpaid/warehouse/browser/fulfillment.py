"""
$Id: $
"""

from copy import copy

from Products.Five.browser import BrowserView
from Products.PloneGetPaid.browser import admin_order as order
from Products.Five.viewlet import manager
from zope import schema
from zope.formlib import form
from zc.table import column
from getpaid.core.interfaces import IShippableLineItem
from getpaid.warehouse.i18n import _
from getpaid.warehouse import interfaces

from warehouse import manager_template

class WarehouseFulfillment( BrowserView ):
    pass

class OrderFulfillment( BrowserView ):
    pass

### Viewlets for Warehouse Fulfillment

WarehouseFulfillmentVM = manager.ViewletManager(
    "WarehouseFulfillmentVM",
    interfaces.IWarehouseFulfillmentVM,
    manager_template,
    bases= (order.OrderAdminManagerBase, )
    )

def renderOrderId( order, formatter ):
    return '<a href="@@admin-manage-order/%s/@@fulfillment">%s</a>'%( order.order_id, order.order_id )

class FulfillmentOrderListing( order.OrderListingComponent ):

    columns = copy( order.OrderListingComponent.columns )
    columns.pop(0)
    columns.insert(0, column.GetterColumn( title=_(u"Order Id"), getter=renderOrderId ) )

    
class FulfillmentOrderSearch( order.OrderSearchComponent ):

    form_fields = form.Fields( 
        schema.Choice( **order.define( title=u"Created", __name__=u"creation_date",
                                       values=( [ d[0] for d in order.OrderSearchComponent.date_search_order ] ),
                                       default="last 7 days") ),
        schema.Choice( **order.define( title=u"Status", __name__=u"finance_state",
                                       values= order.OrderSearchComponent._finance_values ) ),
        schema.Choice( **order.define( title=u"Fulfillment",
                                       __name__=u"fulfillment_state",
                                       default="NEW",
                                       values= order.OrderSearchComponent._fulfillment_values ) ),
        schema.TextLine( **order.define( title=u"User Id", __name__=u"user_id") ),
        )
    

### Viewlets for Order Fulfillment

OrderFulfillmentVM = manager.ViewletManager(
    "OrderFulfillmentVM",
    interfaces.IOrderFulfillmentVM,
    manager_template,
    bases= (order.OrderAdminManagerBase, )
    )    

def getInventory( item ):
    if not IShippableLineItem.providedBy( item ):
        return None
    
    payable = item.resolve()
    if payable is None:
        return None

    return interfaces.IProductInventory( payable )

def renderPickBin( item, formatter ):
    if formatter.inventory is None:
        return u"N/A"
    return formatter.inventory.pickbin

def renderPallet( item, formatter ):
    inventory= getInventory( item )
    if inventory is None:
        formatter.inventory = None
        return u'N/A'
    formatter.inventory = inventory
    return inventory.pallet

class OrderPickList( order.OrderContentsComponent ):

    columns = copy( order.OrderContentsComponent.columns )
    columns.pop(5) # total
    columns.pop(3) # price
    columns.append( 
        column.GetterColumn( title=_(u"Pallet"), getter=renderPallet)
        )
    columns.append( 
        column.GetterColumn( title=_(u"Pickbin"), getter=renderPickBin)
        )

    actions = ()
    
    def update( self ):
        self.line_items = self.__parent__.context.shopping_cart.values()
        return super( order.OrderContentsComponent, self).update()
    
class OrderSummary( order.OrderSummaryComponent ):
    """ to be modified for sanity """

##    template = ZopeTwoPageTemplateFile('order-summary.pt')

##     def getShippingAddress( self ):
        
##         if not self.order.shipping_address.ship_same_billing:
##             return super( FulfillmentOrderSummary, self).getShippingAddress()

##         address = self.getBillingAddress()
##         for k in address.keys():
##             address[ k.replace('bill', 'ship') ] = address[k]
##         return address
            
