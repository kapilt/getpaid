__docformat__ = "reStructuredText"

import doctest
import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import placelesssetup, ztapi
from zope.app.annotation import interfaces as annotation_interfaces
from zope.app.annotation import attribute
from getpaid.core.interfaces import IStore, IPaymentProcessor
from getpaid.ogone.interfaces import IOgoneStandardOptions
from getpaid.ogone.ogone import OgoneStandardProcessor, OgoneStandardOptions

def processorSetUp(test):
    placelesssetup.setUp()
    ztapi.provideAdapter(IStore, IPaymentProcessor, OgoneStandardProcessor,
                         name='Ogone Payments')
    ztapi.provideAdapter(IStore, IOgoneStandardOptions, OgoneStandardOptions)
    ztapi.provideAdapter(annotation_interfaces.IAttributeAnnotatable,
                         annotation_interfaces.IAnnotations,
                         attribute.AttributeAnnotations)


def test_suite():
    return unittest.TestSuite((
        DocFileSuite('ogone.txt',
                     setUp=processorSetUp,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
