"""Unit test for form schemas
"""

import unittest
import doctest
from Testing import ZopeTestCase

from utils import optionflags
from base import PloneGetPaidTestCase

def test_suite():
    return unittest.TestSuite([
        doctest.DocTestSuite(
            'getpaid.pxpay.parser',
            optionflags=optionflags,
            ),
        ZopeTestCase.ZopeDocFileSuite(
            'parser.txt',
            package='getpaid.pxpay.tests',
            test_class=PloneGetPaidTestCase,
            optionflags=optionflags,
            ),
        ZopeTestCase.ZopeDocFileSuite(
            'paymentprocessor.txt',
            package='getpaid.pxpay.tests',
            test_class=PloneGetPaidTestCase,
            optionflags=optionflags,
            ),
        ZopeTestCase.ZopeDocFileSuite(
            'callback.txt',
            package='getpaid.pxpay.tests',
            test_class=PloneGetPaidTestCase,
            optionflags=optionflags,
            ),
        ZopeTestCase.ZopeDocFileSuite(
            'utils.txt',
            package='getpaid.pxpay.tests',
            test_class=PloneGetPaidTestCase,
            optionflags=optionflags,
            ),

        ])
