"""Unit test for form schemas
"""

import unittest
from pprint import pprint

from zope.component import getUtility, getMultiAdapter
from Testing.ZopeTestCase import ZopeDocTestSuite
from Products.Five.utilities.marker import mark

from utils import optionflags
from base import PloneGetPaidTestCase

from Products.PloneGetPaid import interfaces
from getpaid.core.interfaces import IShoppingCartUtility, IFormSchemas
from getpaid.core.item import LineItem

class TestCheckout(PloneGetPaidTestCase):

    def mySetup(self):
        self.pprint = pprint
        self.setRoles(('Manager',))
        id = self.portal.invokeFactory('Document', 'doc')
        options = interfaces.IGetPaidManagementOptions(self.portal)
        options.buyable_types = ['Document']
        mark(self.portal.doc, interfaces.IBuyableMarker)
        self.load_line_items()
        self.set_and_prime_checkout_wizard()
        self.order_id = self.checkout.data_manager.get('order_id')

    def set_and_prime_checkout_wizard(self):
        self.checkout = getMultiAdapter((self.portal,
                                         self.app.REQUEST),
                                        name='getpaid-checkout-wizard')
        self.checkout.update()
        self.checkout()


    def load_line_items(self):
        item = LineItem()
        item.item_id = "jug-of-beer-1"
        item.name = "Jug of beer"
        item.cost = 5.00
        item.quantity = 5
        item.description = "Really nice beer"
        cart = self.get_cart()
        cart[ item.item_id ] = item

    def get_cart(self):
        cart_util = getUtility(IShoppingCartUtility)
        return cart_util.get(self.portal, create=True)

    def generate_order(self):
        create_transient_order = \
                interfaces.ICreateTransientOrder(self.checkout)
        return create_transient_order()

    def test_create_transent_order(self):
        """Test th creation of a transient order.
        >>> self.mySetup()
        >>> self.checkout
        <Products.Five.metaclass.CheckoutWizard object at ...>
        >>> order = self.generate_order()
        >>> order
        <getpaid.core.order.Order object at ...>
        >>> order.shopping_cart
        <getpaid.core.cart.ShoppingCart object at ...>
        >>> order.order_id == self.order_id
        True
        """

    def test_full_first_step(self):
        """Test that a first step with appropriate form data
        instantiates the schema adapters correctly and generates a
        nice looking transient order.

        XXX TODO
        """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=TestCheckout,
                             optionflags=optionflags),
        ))
