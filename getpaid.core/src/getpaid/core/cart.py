"""
$Id$
"""

from zope.app.container.ordered import OrderedContainer
from zope.interface import implements
from persistent import Persistent

import interfaces

class ShoppingCart( OrderedContainer ):
    """
    A shopping cart
    """
    implements( interfaces.IShoppingCart )

    def size( self ):
        return sum(i.quantity for i in self.values())
