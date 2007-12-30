# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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

