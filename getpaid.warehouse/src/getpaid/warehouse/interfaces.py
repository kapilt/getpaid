"""
$Id: $
"""

from zope import interface, schema, component
from getpaid.core.interfaces import IAddress
from zope.app.container.interfaces import IContainer
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager
from zope.schema.interfaces import IContextSourceBinder
from zope.schema import vocabulary

_ = MessageFactory('getpaid')

class IWarehouse( interface.Interface ):
    name = schema.TextLine( title=_(u"Warehouse Name") )
    location = schema.Object( IAddress )

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
##
class IWarehouseContainerVM( IViewletManager ):
    """ warehouse utility's viewlet manager """
