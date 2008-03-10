"""

$Id$
"""

from zope.interface import implements
from getpaid.core import interfaces

class TaxUtility( object ):
    
    implements( interfaces.ITaxUtility )
    
    def getCost( self, order ):
        return 0


