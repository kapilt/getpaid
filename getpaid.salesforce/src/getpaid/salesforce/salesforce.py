"""
$Id:
"""

from urllib2 import Request, urlopen, URLError
import logging
import elementtree.ElementTree as etree

from zope import interface, schema, component
from zope.app.container.contained import Contained
from persistent import Persistent

from getpaid.core.interfaces import IShippableLineItem, IStoreSettings, IShippingMethodRate, IOriginRouter

import interfaces

log = logging.getLogger("getpaid.salesforce")

class SalesforceAdapter( Persistent, Contained ):

    interface.implements(interfaces.ISalesforceAdapter)

    def __init__(self):
        super(SalesforceAdapter,self).__init__()

    def successAdapterAction(self, order):
        """
        On a successful checkout, perform the following
        """
        pass

    def failureAdapterAction(self, order):
        """
        On a fail on transaction perform the following
        """
        pass
    
    

