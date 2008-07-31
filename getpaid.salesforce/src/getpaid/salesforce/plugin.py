"""
$Id: $
"""
from StringIO import StringIO
from zope import component, interface
from getpaid.core.interfaces import IPluginManager
from getpaid.salesforce import interfaces
from getpaid.salesforce import salesforce

class SalesforcePlugin( object ):

    interface.implements( IPluginManager )

    title = "GetPaid Salesforce Adapter"
    description = "Provides data uploading to salesforce on checkout. Requires a Salesforce account."

    def __init__(self, context ):
        self.context = context

    def install( self ):
        sm = self.context.getSiteManager()

        utility = sm.queryUtility( interfaces.ISalesforceAdapter )

        if utility is not None:
            return

        print "Installing SALESFORCE"
        salesforce_adapter = salesforce.SalesforceAdapter()

        try:
            sm.registerUtility(component=salesforce_adapter, provided=interfaces.ISalesforceAdapter )
        except TypeError:
            # BBB for Zope 2.9
            sm.registerUtility(interface=interfaces.ISalesforceAdapter, utility=salesforce_adapter)

    def uninstall( self ):
        pass

    def status( self ):
        return component.queryUtility( interfaces.SalesfoceAdapter ) is not None

def storeInstalled( object, event ):
    return SalesforcePlugin( object ).install()
