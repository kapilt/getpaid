"""Unit test for form schemas
"""

import unittest
from pprint import pprint

from zope.component import getUtility
from Testing.ZopeTestCase import ZopeDocTestSuite
from Products.Five.utilities.marker import mark

from utils import optionflags
from base import PloneGetPaidTestCase

from Products.PloneGetPaid import interfaces
from getpaid.core.interfaces import IShoppingCartUtility, IFormSchemas

class TestFormSchemas(PloneGetPaidTestCase):

    def mySetup(self):
        self.pprint = pprint
        self.setRoles(('Manager',))
        id = self.portal.invokeFactory('Document', 'doc')
        options = interfaces.IGetPaidManagementOptions(self.portal)
        options.buyable_types = ['Document']
        mark(self.portal.doc, interfaces.IBuyableMarker)
        self.cart_util = getUtility(IShoppingCartUtility)
        names = ['checkout-review-and-pay-form-schemas',
                 'checkout-address-form-schemas']
        self.formSchemas = [getUtility(IFormSchemas,
                                       name=x) for x in names]


    def test_named_utilities(self):
        """Test that a cart is not instantiated if not requested
        >>> self.mySetup()
        >>> self.pprint(self.formSchemas)
        [<Products.PloneGetPaid.preferences.CheckoutReviewAndPayFormSchemas instance at ...>,
         <Products.PloneGetPaid.tests.test_checkout.NewCheckoutAddressFormSchemas instance at ...>]

        """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=TestFormSchemas,
                             optionflags=optionflags),
        ))
