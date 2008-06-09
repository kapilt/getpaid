import doctest
from zope.app.tests import placelesssetup
from zope.configuration.xmlconfig import XMLConfig
from Products.PloneGetPaid.config import PLONE3

from zope.component import getMultiAdapter, getUtility
from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility, \
     IOrderWorkflowLog
from getpaid.core.order import Order
from getpaid.core.item import LineItem
from getpaid.pxpay.interfaces import IPXPayInvalidMessageError, \
     IPXPayNetworkError

# Standard options for DocTests
optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE)


def configurationSetUp(self):
    """Set up Zope 3 test environment
    """

    placelesssetup.setUp()

    # Ensure that the ZCML registrations in CMFonFive and PloneGetPaid are in effect
    # Also ensure the Five directives and permissions are available

    import Products.Five
    if not PLONE3:
        import Products.CMFonFive
    import Products.PloneGetPaid

    XMLConfig('configure.zcml', Products.Five)()
    XMLConfig('meta.zcml', Products.Five)()

    XMLConfig('configure.zcml', Products.PloneGetPaid)()

def configurationTearDown(self):
    """Tear down Zope 3 test environment
    """

    placelesssetup.tearDown()


class ContactInformation( object ):

    name = 'test user'
    email = 'test@xxx.xxx'


def create_test_order(context, order_id='1111111111'):
    """
    creates an order with a line item using a new cart.
    """
    item = LineItem()
    item.item_id = order_id
    item.name = "Jug of beer"
    item.cost = 5.00
    item.quantity = 5
    item.description = "Really nice beer"

    cart_util = getUtility(IShoppingCartUtility)
    cart = cart_util.get(context, create=True)
    cart[ item.item_id ] = item

    order = Order()
    order.order_id = order_id
    order.shopping_cart = cart
    order.processor_id = 'PXPay Processor'
    order.contact_information = ContactInformation()
    return order


def print_order_workflow_log(order):
    olog = IOrderWorkflowLog(order)
    for record in list(iter(olog)):
        print record.previous_state, ' --> ', record.new_state


def set_errors_to_raise_exceptions():
    invalidmessage_utility = getUtility(IPXPayInvalidMessageError)
    invalidmessage_utility.redirect = False
    networkerror_utility = getUtility(IPXPayNetworkError)
    networkerror_utility.redirect = False
