"""
$Id: $
"""

from zope import schema, interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from getpaid.core.interfaces import ICheckoutAdapter, IPersistentOptions

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.salesforce')

class ISalesforceAdapter( ICheckoutAdapter ):

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

class ISalesforceOptions( interfaces.IPersistentOptions ):
    """
    Options for salesforce adapter
    """
    enable_salesforce_checkout = schema.Bool( title=_(u"Enable data sending to Salesforce on checkout"), default=False)

        


                                            
