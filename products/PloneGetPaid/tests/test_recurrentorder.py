"""Unit tests for setting type as shippable.
"""

import unittest

from Testing import ZopeTestCase
from Testing.ZopeTestCase import ZopeDocTestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Testing.ZopeTestCase import ZopeDocFileSuite
from zope.app.testing import placelesssetup, ztapi
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase

from getpaid.core.tests import base

from utils import optionflags

from base import baseAfterSetUp
from base import PloneGetPaidTestCase
from base import PloneGetPaidFunctionalTestCase


class RecurrentOrderFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for the 'PloneGetPaid' product.
    This may provide specific set-up and tear-down operations, or provide
    convenience methods.
    """
    def afterSetUp( self ):
#        placelesssetup.tearDown()
        fiveconfigure.debug_mode = True
        import five.intid
        zcml.load_config('configure.zcml', five.intid)
        import Products.PloneGetPaid
        zcml.load_config('configure.zcml', Products.PloneGetPaid)
        fiveconfigure.debug_mode = False

        baseAfterSetUp(self)
#        ZopeTestCase.installProduct('five.intid')
        self.portal.portal_quickinstaller.installProduct('PloneGetPaid')

def test_suite():
    return unittest.TestSuite((
            ZopeDocFileSuite('recurrent/test_recurrentorder.txt',
                             package='Products.PloneGetPaid.tests',
#                            setUp=base.coreSetUp,
                             #tearDown=placelesssetup.tearDown,
                             test_class=RecurrentOrderFunctionalTestCase),
        ))
