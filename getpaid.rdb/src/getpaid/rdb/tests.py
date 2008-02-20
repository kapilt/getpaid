

from zope.app.testing import placelesssetup, ztapi
from zope.testing.doctestunit import DocFileSuite

from zope import component 
from getpaid.core.tests import base

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('readme.txt',
                     setUp=base.coreSetUp,
                     tearDown=placelesssetup.tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),    
        ))      