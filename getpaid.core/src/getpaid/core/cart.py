"""
$Id$
"""

import decimal

from persistent import Persistent
from zope import component
from zope.interface import implements

from zope.app.container.ordered import OrderedContainer

import interfaces

class ShoppingCart( OrderedContainer ):
    """
    A shopping cart
    """
    implements( interfaces.IShoppingCart )

    def size( self ):
        return sum(i.quantity for i in self.values())


class CartItemTotals( object ):

    implements( interfaces.ILineContainerTotals )
    
    def __init__( self, context ):
        self.shopping_cart = context

    def getTotalPrice( self ):
        if not self.shopping_cart:
            return 0
        
        total = 0
        total += self.getSubTotalPrice()
        total += self.getShippingCost()
        total += self.getTaxCost()
        
        return float( str( total ) )            

    def getSubTotalPrice( self ):
        if not self.shopping_cart:
            return 0
        total = 0
        for item in self.shopping_cart.values():
            d = decimal.Decimal ( str(item.cost ) ) * item.quantity
            total += d        
        return total
        
    def getShippingCost( self ):
        shipping_method = component.getUtility( interfaces.IShippingMethod )
        return shipping_method.getCost( self )

    def getTaxCost( self ):
        tax_utility = component.getUtility( interfaces.ITaxUtility )
        return tax_utility.getCost( self )

