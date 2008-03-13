"""Unit test for adding a payable type to a shopping cart.
"""

import unittest

from zope.component import getUtility
from Testing.ZopeTestCase import ZopeDocTestSuite
from Products.Five.utilities.marker import mark

from utils import optionflags
from base import PloneGetPaidTestCase

from Products.PloneGetPaid import interfaces
from getpaid.core.interfaces import IShoppingCartUtility

class TestCart(PloneGetPaidTestCase):

    def mySetup(self):
        self.setRoles(('Manager',))
        id = self.portal.invokeFactory('Document', 'doc')
        options = interfaces.IGetPaidManagementOptions(self.portal)
        options.buyable_types = ['Document']
        mark(self.portal.doc, interfaces.IBuyableMarker)
        self.cart_util = getUtility(IShoppingCartUtility)

    def test_doesNotCreateCartIfNotRequested(self):
        """Test that a cart is not instantiated if not requested

        >>> self.mySetup()
        >>> self.cart_util.get(self.portal, create=False)
        >>> 
        """
    def test_createsCartWhenRequsted(self):
        """

        >>> self.mySetup()
        >>> self.cart_util.get(self.portal, create=True)
        <getpaid.core.cart.ShoppingCart object at 0x...>

        """

    def test_destroyDestroysCart(self):
        """
        >>> self.mySetup()
        >>> self.cart_util.get(self.portal, create=True)
        <getpaid.core.cart.ShoppingCart object at 0x...>
        >>> self.cart_util.destroy(self.portal)
        >>> self.cart_util.get(self.portal, create=False)
        >>>
        """
    def test_destroyCopesWithNotHavingAnythingToDo(self):
        """
        >>> self.mySetup()
        >>> self.cart_util.destroy(self.portal)
        >>> self.cart_util.get(self.portal, create=False)
        >>>
        """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=TestCart,
                             optionflags=optionflags),
        ))
