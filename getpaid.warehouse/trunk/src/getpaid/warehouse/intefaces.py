"""
$Id: $
"""

from zope import interface, schema
from getpaid.core.interfaces import IAddress

class IWarehouse( interface.Interface ):
    name = schema.TextLine( label=_(u"Warehouse Name") )
    location = schema.Object( IAddress )
    
class IProductInventory( interface.Interface ):   
    pickbin = schema.TextLine( label=_(u"Pick Bin"), description=_("") )
    pallet = schema.TextLine( label=_(u"Pallet"), description=_(""))
    stock  = schema.Int( label=_(u"Quantity in Stock"))
    store_stock  = schema.Int( label=_(u"Quantity in Stock, minus existing orders") )
