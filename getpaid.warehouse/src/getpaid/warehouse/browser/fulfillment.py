"""

Fulfilling an Order.

- fufillment display

  item collection - available items 

    action - create shipment

    - if all items in order, then transition order to delivered
    
    - display form for entry of shipping info

  item collection - back order

  shipment summary listing -


  todo

   - shipping collection

   - on creating shipment, if we have all items, then transition order to delivered

   - if we only have backordered items remaining

   - generate create shipment event

   - add contained to shipment

$Id: $
"""

from copy import copy

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PloneGetPaid.browser import admin_order as order
from Products.Five.viewlet import manager, viewlet 

from zope import schema
from zope.formlib import form
from zc.table import column, table
from ore.viewlet import core

from getpaid.core.interfaces import IShippableLineItem, workflow_states, IShippableOrder, IShipment
from getpaid.warehouse.i18n import _
from getpaid.warehouse import interfaces, shipment

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

class FulfillmentManagerBase( order.AdminOrderManagerBase ):

    items_by_inventory = None

    def itemsByInventory( self, available=True ):
        # segment items into available, non available sets
        if self.items_by_inventory is not None:
            return self.items_by_inventory.get( available, () )

        items_by_inventory = {}
        
        for i in self.context.shopping_cart.values():
            inventory = getInventory( i )
            if not inventory:
                continue
            key = ( inventory.stock >= i.quantity )
            items_by_inventory.setdefault( key, [] ).append( i )

        self.items_by_inventory = items_by_inventory
        return items_by_inventory.get( available, () )
        
OrderFulfillmentVM = manager.ViewletManager(
    "OrderFulfillmentVM",
    interfaces.IOrderFulfillmentVM,
    manager_template,
    bases= ( FulfillmentManagerBase, )
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

class BackorderList( order.OrderContentsComponent ):

    columns = copy( order.OrderContentsComponent.columns )
    columns.pop(5) # total
    columns.pop(3) # price
    columns.pop(0) # selection
    
    collection_name = _(u"Backordered Items")
    
    def show( self, **kw ):
        self.line_items = self.manager.itemsByInventory( available=False )
        if len( self.line_items ) == 0:
            return False
        return True

    def update( self ):
        self.actions = ()
        return super( order.OrderContentsComponent, self).update()

class ShippedItems( order.OrderContentsComponent ):

    columns = copy( order.OrderContentsComponent.columns )
    columns.pop(5) # total
    columns.pop(3) # price
    columns.pop(0) # selection
    
    collection_name = _(u"Shipped Items")
    
    def show( self, inline=False, **kw ):
        if not inline:
            return True
        
        self.line_items = self.manager.itemsByStates(
            (workflow_states.item.SHIPPED,),
            )
        if len( self.line_items ) == 0:
            return False
        return True

    def render( self ):
        if self.show( inline=True ):
            return super( ShippedItems, self).render()
        return ''
    
    def update( self ):
        self.actions = ()
        return super( order.OrderContentsComponent, self).update()    
        
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

    actions = None  # reset standard container actions
    collection_name = _(u"Order Items") # fieldset label

    template = ZopeTwoPageTemplateFile('picklist.pt')
    
    form_fields = form.Fields( IShipment )
    form_fields = form_fields.omit('creation_date', 'service_code', 'service')
    
    form_name = _(u"Create Shipment") # inner fieldset form label
    form_description = _(u"Select Items to Ship, and Enter Shipping Details")
    
    def show( self, inline=False, **kw ):
        if not inline:
            return True
        
        self.line_items = self.filteredItems()
        if len(self.line_items):
            return True
        return False

    def render( self ):
        if self.show( inline=True ):
            return super( OrderPickList, self).render()
        return ''

    def filteredItems( self ):
        # we want only items in inventory that aren't shipped
        i_items =  self.manager.itemsByInventory( )
        s_items =  self.manager.itemsByStates( (workflow_states.item.NEW,) )
        filtered = []
        for i in s_items:
            if not i in i_items:
                continue
            filtered.append( i )
        return filtered
    
    def update( self ):
        # pop the selection if the order is already fulfilled
        if self.context.fulfillment_state == workflow_states.order.fulfillment.DELIVERED:
            columns = copy( self.columns )
            columns.pop(0)
            self.columns = columns
            
        return super( order.OrderContentsComponent, self).update()

    def condition_create_shipment( self, action ):
        if not IShippableOrder.providedBy( self.context._object ):
            return False
        if self.context.fulfillment_state == workflow_states.order.fulfillment.DELIVERED:
            return False
        if not self.line_items:
            return False
        return True
        
    @form.action(_(u"Create Shipment"), condition="condition_create_shipment" )
    def handle_create_shipment( self, action, data ):
        items = self.selection_column.getSelected( self.line_items, self.request )
        if not items:
            self.status = _(u"Please Select Items to Ship")
            return
        
        o_shipment = shipment.Shipment()
        
        order = self.context._object
        # this gets attached normally via the warehouse
        # event subscriber, we do it lazy here for existing orders
        if getattr( order, 'shipments', None) is None:
            order.shipments = shipment.OrderShipments()

        # modify shipment with supplied form fields
        adapters = { IShipment : o_shipment }
        form.applyChanges( None, self.form_fields, data, adapters )

        # store shipment
        sid = str( len( order.shipments ) + 1 )
        order.shipments[ sid ] = o_shipment

        # populate shipment with items
        for i in items:
            o_shipment[ i.item_id ] = i.clone()
            i.fulfillment_workflow.fireTransition('ship')

        # attempt to transition order
        self.transitionOrder()

        # clear manager item cache and fetch
        self.status = _(u"Shipment Created")

    def transitionOrder( self ):
        
        # clear manager item caches
        self.manager.items_by_state = None
        self.manager.items_by_inventory = None
        
        # if we have no more items         
        items = self.manager.itemsByStates( ( workflow_states.item.NEW, ) )
        if not len(items):
            if self.context.fulfillment_state == workflow_states.order.NEW:
                self.context.fulfillment_workflow.fireTransition('process-order')
                
            if self.context.fulfillment_state == workflow_states.order.PROCESSING:
                self.context.fulfillment_workflow.fireTransition('deliver-processing-order')                
        
def g_created( item, formatter ):
    return item.creation_date.isoformat()

def g_item( item, formatter ):
    return len(item)

def g_track( item, formatter ):
    return getattr( item, 'tracking_code', _(u'n/a'))

class OrderShipments( viewlet.ViewletBase ):

    __allow_access_to_unprotected_subobjects__ = 1
    
    template = ZopeTwoPageTemplateFile('item-collection.pt')
    
    columns = [
        column.GetterColumn( title=_(u"Created"), getter=g_created),
        column.GetterColumn( title=_(u"Item Count"), getter=g_item),
        column.GetterColumn( title=_(u"Tracking"), getter=g_track),
        ]
    
    collection_name = _(u"Shipments")
    order = 20

    def show( self, inline=False, **kw ):
        if not inline:
            return True
        if not IShippableOrder.providedBy( self.context._object ):
            return False
        shipments = getattr( self.context, 'shipments', ())
        if not len(shipments):
            return False
        return True
        
    def render( self ):
        if self.show( inline=True):
            return self.__of__( self.__parent__).template()
        return ''

    def listing( self ):
        values = self.context.shipments.values()
        formatter = table.StandaloneFullFormatter(
            self.context,
            self.request,
            values,
            prefix="ship",
            visible_column_names = [c.name for c in self.columns ],
            columns = self.columns
            )
        formatter.cssClasses['table'] = 'listing'
        return formatter()
    
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
            
