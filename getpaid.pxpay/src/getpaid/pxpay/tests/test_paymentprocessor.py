"""Unit test for form schemas
"""

import unittest
from pprint import pprint

from zope.component import getUtility, getMultiAdapter, getAdapter
from zope.component import getGlobalSiteManager
from zope.interface import Interface, implements
from zope import schema

from Testing.ZopeTestCase import ZopeDocTestSuite

from utils import optionflags
from base import PloneGetPaidTestCase

from getpaid.core.interfaces import IPaymentProcessor

from getpaid.core import options
from getpaid.core.order import Order
from Products.PloneGetPaid import interfaces

from getpaid.pxpay.interfaces import IPXPayStandardOptions
from getpaid.pxpay.config import *

class TestPaymentProcessor(PloneGetPaidTestCase):

    def mySetup(self):
        self.pprint = pprint
        self.set_test_payment_processor_options()

    def create_order(self):
        order = Order()
        order.order_id = 'order_1'
        return order

    def get_payment_processor_options(self):
        processor_options = getAdapter(self.portal,
                                       IPXPayStandardOptions)
        return processor_options

    def set_test_payment_processor_options(self):
        processor_options = self.get_payment_processor_options()
        processor_options.PxPayServerType = TEST_SERVER_TYPE
        processor_options.PxPayUserId = 'testid'
        processor_options.PxPayKey = 'testkey'
        processor_options.PxPaySiteCurrency = u"NZD"

    def get_payment_processor(self):
        processor = getAdapter(self.portal,
                               IPaymentProcessor,
                               name='PXPay Processor')
        return processor

    def test_payment_processor_options(self):
        """Test payment processor options.
        >>> self.mySetup()
        >>> processor_options = self.get_payment_processor_options()
        >>> processor_options
        <getpaid.core.options.PXPayStandardOptions object at ...>
        >>> processor_options.PxPayServerType
        u'TEST'
        >>> processor_options.PxPayUserId
        'testid'
        >>> processor_options.PxPayKey
        'testkey'
        >>> processor_options.PxPaySiteCurrency
        u'NZD'
        >>>
        """

    def test_payment_processor(self):
        """Test payment processor.
        >>> self.mySetup()
        >>> payment_processor = self.get_payment_processor()
        >>> payment_processor
        <getpaid.pxpay.pxpay.PXPayPaymentAdapter object at ...>

        Make sure we have picked up the pxpay settings

        >>> payment_processor.settings.PxPayServerType
        u'TEST'
        >>> payment_processor.settings.PxPayUserId
        'testid'

        >>> order = self.create_order()
        >>> order
        <getpaid.core.order.Order object at ...>
        """



def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=TestPaymentProcessor,
                             optionflags=optionflags),
        ))
