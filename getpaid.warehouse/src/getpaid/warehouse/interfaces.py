"""
$Id: $
"""

from zope import interface, schema, component
from getpaid.core import interfaces
from getpaid.core.interfaces import IAddress
from zope.component.interfaces import IObjectEvent
from zope.app.container.interfaces import IContainer
from zope.viewlet.interfaces import IViewletManager
from zope.schema.interfaces import IContextSourceBinder
from zope.schema import vocabulary

from i18n import _

class IWarehouse( interface.Interface ):
    name = schema.TextLine( title=_(u"Warehouse Name") )
    location = schema.Object( interfaces.IAddress )

class IWarehouseContainer( IContainer ):
    """
    warehouse container utility
    """

def WarehouseSource( *args ):
    container = component.getUtility( IWarehouseContainer )
    return vocabulary.SimpleVocabulary.fromValues( container.keys() )

interface.directlyProvides( WarehouseSource, IContextSourceBinder )

class IProductInventory( interface.Interface ):   
    pickbin = schema.TextLine( title=_(u"Pick Bin"), description=_("") )
    pallet = schema.TextLine( title=_(u"Pallet"), description=_(""))
    stock  = schema.Int( title=_(u"Quantity in Stock"), default=0)
    
    # so the notion is that we automatically adjust this value to give
    # update with incoming orders. stock value would always be manually updated.    
    store_stock  = schema.Int( title=_(u"Quantity Available For Sale"), description=_(u"Warehouse stock minus pending orders"), default=0)    
    warehouse = schema.Choice( title=_(u"Warehouse"), source=WarehouseSource,  )

class IInventoryModified( IObjectEvent ):
    """
    inventory modified, sent after the modification
    """
    product = schema.Object( interfaces.IShippableContent )
    stock_delta = schema.Int()

class IInventoryAvailabilityModified( IObjectEvent ):
    """
    inventory availability changed by an order
    """
    product = schema.Object( interfaces.IShippableContent )
    order = schema.Object( interfaces.IOrder )
    stock_delta = schema.Int()
    
class IInventoryOrderFulfilled( IObjectEvent ):
    """
    inventory stock changed by order fulfillment
    """
    product = schema.Object( interfaces.IShippableContent )
    order = schema.Object( interfaces.IOrder )
    stock_delta = schema.Int()

class IInventoryBackordered( IObjectEvent ):
    """
    when an item's available inventory ( store_stock ) goes below zero, this
    event is generated.
    """
    product = schema.Object( interfaces.IShippableContent )

class InventoryModified( object ):

    interface.implements( IInventoryModified )
    
    def __init__( self, inventory, product, stock_delta=0 ):
        self.object = inventory
        self.product = product
        self.stock_delta = stock_delta

class InventoryOrderModified( object ):
    
    def __init__( self, inventory, product, order, stock_delta=0 ):
        self.object = inventory
        self.product = product
        self.order = order
        self.stock_delta = stock_delta

class InventoryAvailabilityModified( InventoryOrderModified ):
    
    interface.implements( IInventoryAvailabilityModified )


class InventoryOrderFulfilled( InventoryOrderModified ):
    
    interface.implements( IInventoryOrderFulfilled )

    
class InventoryBackordered( object ):
    
    interface.implements( IInventoryBackordered )
    
    def __init__( self, inventory, product):
        self.object = inventory
        self.product = product

###
# UI Interfaces

class IWarehouseContainerVM( IViewletManager ):
    """ warehouse utility's viewlet manager """

class IWarehouseFulfillmentVM( IViewletManager ):
    """ warehouse fulfilmment viewlet manager """

class IOrderFulfillmentVM( IViewletManager ):
    """ order fulfillment viewlet manager """
