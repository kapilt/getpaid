"""Unit test for form schemas
"""

import unittest
from Testing import ZopeTestCase

from utils import optionflags
from base import PloneGetPaidTestCase

def test_suite():
    return unittest.TestSuite([
        ZopeTestCase.ZopeDocFileSuite(
            'parser.txt',
            package='getpaid.pxpay.tests',
            test_class=PloneGetPaidTestCase,
            optionflags=optionflags,
            ),
        ])
