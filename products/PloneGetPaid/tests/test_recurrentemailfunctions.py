"""Unit tests for setting type as shippable.
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from utils import optionflags

from base import PloneGetPaidTestCase
from base import PloneGetPaidFunctionalTestCase

def test_recurrentemailfunctions():
    """
    Nothing here, tested at Products.PloneGetPaid.notifications
    """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
            ZopeDocTestSuite(module='Products.PloneGetPaid.notifications',
                             test_class=PloneGetPaidTestCase,
                             optionflags=optionflags),
            FunctionalDocFileSuite('test_recurrentemailfunctions_functional.txt',
                                   package='Products.PloneGetPaid.tests',
                                   test_class=PloneGetPaidFunctionalTestCase),
        ))
