"""Unit test for form schemas
"""

import unittest
from pprint import pprint

from zope.component import getUtility, getMultiAdapter
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implements
from zope import schema

from Testing.ZopeTestCase import ZopeDocTestSuite
from Products.Five.utilities.marker import mark

from utils import optionflags
from base import PloneGetPaidTestCase

from getpaid.core.interfaces import IShoppingCartUtility, IFormSchemas
from getpaid.core.item import LineItem
from getpaid.core import options
from Products.PloneGetPaid.preferences import CheckoutAddressFormSchemas
from Products.PloneGetPaid import interfaces

# a form schema override

# here we want to add in some gift options to the billing address form
# of the checkout and for these to be persisted in the order object.

class IGiftOptions(Interface):

    include_gift_card = schema.Bool(
        title=u"Tick here to include a gift card to the recipient",
        default=False)
    comment = schema.Text(title = u"Write any other special requests here")


class GiftOptions( options.PersistentBag ):
    title = "Gift Options"
    implements( IGiftOptions )
    __parent__ = None
    __name__ = None

GiftOptions.initclass(IGiftOptions)

class NewCheckoutAddressFormSchemas(CheckoutAddressFormSchemas):

    interfaces = dict(CheckoutAddressFormSchemas.interfaces)
    interfaces['gift_options']=IGiftOptions

    bags = dict(CheckoutAddressFormSchemas.bags)
    bags['gift_options']=GiftOptions

def override_address_schema_utility(context):
    """
    Usually you would do this in an overrides.zml

    <utility
        provides="getpaid.core.interfaces.IFormSchemas"
        factory=".overrides.NewCheckoutAddressFormSchemas"
        name="checkout-address-form-schemas"
        />
    """
    gsm = getGlobalSiteManager()
    gsm.registerUtility(NewCheckoutAddressFormSchemas(),
                        IFormSchemas,
                        name='checkout-address-form-schemas')


def reset_address_schema_utility(context):
    """
    We need to do this to put things back to normal for other tests.

    """
    gsm = getGlobalSiteManager()
    gsm.registerUtility(CheckoutAddressFormSchemas(),
                        IFormSchemas,
                        name='checkout-address-form-schemas')


# end form schema override

class TestCheckout(PloneGetPaidTestCase):

    def mySetup(self):
        self.pprint = pprint
        override_address_schema_utility(self.portal)
        self.setRoles(('Manager',))
        id = self.portal.invokeFactory('Document', 'doc')
        options = interfaces.IGetPaidManagementOptions(self.portal)
        options.buyable_types = ['Document']
        mark(self.portal.doc, interfaces.IBuyableMarker)
        self.load_line_items()
        self.set_and_prime_checkout_wizard()
        self.order_id = self.checkout.data_manager.get('order_id')


    def tearDown(self):
        reset_address_schema_utility(self.portal)

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

        Check that the added gift options schema and options have
        behaved and have been persisted on the order.

        >>> order.gift_options
        <Products.PloneGetPaid.tests.test_checkout.GiftOptions object at ...>
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
