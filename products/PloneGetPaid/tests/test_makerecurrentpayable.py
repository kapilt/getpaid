"""Unit tests for setting type as shippable.
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from utils import optionflags

from base import PloneGetPaidTestCase
from base import PloneGetPaidFunctionalTestCase

def test_mark_object_recurrentpayable():
    """ test that we can designate a page as recurrentpayable

    >>> from Products.PloneGetPaid import interfaces
    >>> options = interfaces.IGetPaidManagementOptions(portal)
    >>> options.buyable_types = ['Document']

    Create a page to mark recurrent payable

    >>> self.setRoles(('Manager'),)
    >>> self.portal.invokeFactory('Document', 'testpage')
    'testpage'

    >>> testpage = self.portal.testpage
    >>> IRecurrentPaymentMarker = interfaces.IRecurrentPaymentMarker
    >>> from Products.Five.utilities.marker import mark
    >>> mark(testpage, IRecurrentPaymentMarker)
    >>> IRecurrentPaymentMarker(testpage)
    <ATDocument at ...>
    >>> IRecurrentPaymentMarker.providedBy( testpage )
    True
    """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
            FunctionalDocFileSuite('test_makerecurrentpayable_functional.txt',
                                   package='Products.PloneGetPaid.tests',
                                   test_class=PloneGetPaidFunctionalTestCase),
        ))
