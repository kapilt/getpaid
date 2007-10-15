
"""

$Id$
"""

from zope.interface import implements
from getpaid.core import interfaces

class ShippingMethod( object ):
    
    implements( interfaces.IShippingMethod )
    
    def getCost( self, order ):
        return 0


