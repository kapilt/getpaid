import unittest, datetime, doctest

from Testing import ZopeTestCase as ztc
from zope.app.testing import placelesssetup, ztapi
from zope.testing.doctestunit import DocFileSuite
from zope import component

from getpaid.core.tests import base
from getpaid.core import order
from getpaid.core.interfaces import IOrderManager, IOrderWorkflowLog, IOrder, workflow_states

class RecurrentManagerTests( base.GetPaidTestCase ):
    """
    """

def test_suite():
    return unittest.TestSuite((
        # Unit tests
        ztc.ZopeDocTestSuite(
                module='getpaid.core.recurrent',
                test_class=RecurrentManagerTests),
        DocFileSuite('../recurrent.txt',
                     setUp=base.coreSetUp,
                     tearDown=placelesssetup.tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))
