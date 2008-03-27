"""This is the setup for a doctest that tests a Zope 3 component.

There is really nothing too different from a "plain Python" test. We are not
parsing ZCML, for example. However, we use some of the helpers from Zope 3
to ensure that the Component Architecture is properly set up and torn down.
"""

import unittest

import zope.testing
import zope.component

from zope.app.testing import placelesssetup, ztapi

from getpaid.core.tests import base
from getpaid.core.interfaces import IStore, IPaymentProcessor, \
                                    ILineContainerTotals, IShippingMethod, \
                                    ITaxUtility
from getpaid.core.shipping import ShippingMethod
from getpaid.core.tax import TaxUtility

from getpaid.authorizedotnet.authorizenet import AuthorizeNetAdapter

def setUp(test):
    """This method is used to set up the test environment. We pass it to the
    DocFileSuite initialiser. We also pass a tear-down, but in this case,
    we use the tear-down from zope.component.testing, which takes care of
    cleaning up Component Architecture registrations.
    """
    base.coreSetUp(test)
    ztapi.provideAdapter(IStore,
                         IPaymentProcessor,
                         AuthorizeNetAdapter,
                         "Authorize.Net")
#    import pdb;pdb.set_trace()
    freeship=ShippingMethod()
    ztapi.provideUtility(IShippingMethod,
                         freeship)
    taxfree=TaxUtility()
    ztapi.provideUtility(ITaxUtility,
                         taxfree)

def test_suite():
    return unittest.TestSuite((

        # Here, we tell the test runner to execute the tests in the given
        # file. The setUp and tearDown methods employed make use of the Zope 3
        # Component Architecture, but really there is nothing Zope-specific
        # about this. If you want to test "plain-Python" this way, the setup
        # is the same.

        zope.testing.doctest.DocFileSuite('../readme.txt',
                                          setUp=setUp,
                                          tearDown=zope.component.testing.tearDown),
        ))