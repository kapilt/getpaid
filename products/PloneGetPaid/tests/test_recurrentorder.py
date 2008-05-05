"""Unit tests for setting type as shippable.
"""

import unittest

from Testing import ZopeTestCase
from Testing.ZopeTestCase import ZopeDocTestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from zope.app.testing import placelesssetup, ztapi
from Products.Five import zcml
from Products.Five import fiveconfigure

from getpaid.core.tests import base

from utils import optionflags

from base import baseAfterSetUp
from base import PloneGetPaidTestCase
from base import PloneGetPaidFunctionalTestCase


#ZopeTestCase.installProduct('five.intid')

class RecurrentOrderFunctionalTestCase(PloneGetPaidFunctionalTestCase):
    """Base class for functional integration tests for the 'PloneGetPaid' product.
    This may provide specific set-up and tear-down operations, or provide
    convenience methods.
    """

    def afterSetUp( self ):
#        placelesssetup.setUp()
        fiveconfigure.debug_mode = True
#        import Products.Five
#        import Products.GenericSetup
        import Products.PloneGetPaid
#        import pdb;pdb.set_trace()
#        zcml.load_config('meta.zcml', Products.Five)
#        zcml.load_config('configure.zcml', Products.Five)
#        zcml.load_config('meta.zcml', Products.Five.viewlet)
#        zcml.load_config('meta.zcml', Products.GenericSetup)
#        zcml.load_config('configure.zcml', Products.GenericSetup)
        zcml.load_config('configure.zcml', Products.PloneGetPaid)
        fiveconfigure.debug_mode = False

        baseAfterSetUp(self)
        self.portal.portal_quickinstaller.installProduct('PloneGetPaid')

def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite('test_recurrentorder.txt',
                                   package='Products.PloneGetPaid.tests',
                                   #setUp=base.coreSetUp,
                                   #tearDown=placelesssetup.tearDown,
                                   test_class=RecurrentOrderFunctionalTestCase),
        ))
