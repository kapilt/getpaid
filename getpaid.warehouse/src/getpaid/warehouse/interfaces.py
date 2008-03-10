"""
$Id: $
"""

from zope import interface, schema
from getpaid.core.interfaces import IAddress

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid')

class IWarehouse( interface.Interface ):
    name = schema.TextLine( title=_(u"Warehouse Name") )
    location = schema.Object( IAddress )
    
class IProductInventory( interface.Interface ):   
    pickbin = schema.TextLine( title=_(u"Pick Bin"), description=_("") )
    pallet = schema.TextLine( title=_(u"Pallet"), description=_(""))
    stock  = schema.Int( title=_(u"Quantity in Stock"))
    # so the notion is that we automatically adjust this value to give
    # update with incoming orders. stock value would always be manually updated.
    store_stock  = schema.Int( title=_(u"Quantity in Stock, minus existing orders"), )
