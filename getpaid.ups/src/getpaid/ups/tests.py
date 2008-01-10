"""
$Id: $

"""
import unittest, doctest
from zope import interface
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import placelesssetup, ztapi
from getpaid.ups import rates, interfaces
from getpaid.core.interfaces import IStoreSettings, IOrder


class MockStoreSettings( object ):
    interface.implements( IStoreSettings )
    store_name = "Rabbit Furs"
    contact_company = "Furs, LLC"
    contact_name = "Mr. Wolf"
    contact_phone = "903-213-1012"
    contact_address = "1126 Alabama St"
    contact_address2 = ""
    contact_email = "mrwolf@example.com"
    contact_city = "San Francisco"
    contact_postalcode = "94117"
    contact_country = "US"
                             
def setUp( test ):
    placelesssetup.setUp()

    ztapi.provideAdapter( IOrder, interfaces.IOriginRouter, rates.OriginRouter )
    ztapi.provideUtility( IStoreSettings, MockStoreSettings() )

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('readme.txt',
                     setUp=setUp,
                     tearDown=placelesssetup.tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),    
        ))



