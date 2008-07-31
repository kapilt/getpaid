"""
$Id: $
"""

from zope.formlib import form
from getpaid.salesforce import  interfaces

from Products.PloneGetPaid.browser.admin import BaseSettingsForm

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.salesforce')

class SalesforceScreen( BaseSettingsForm ):
    """
    Salesforce management interface
    """
    form_fields = form.Fields(interfaces.ISalesforceOptions)
    form_name = _(u'Salesforce')

    def update( self ):
        try:
            interface = iter( self.form_fields ).next().field.interface
        except StopIteration:
            interface = None
        #if interface is not None:
        #    self.adapters = { interface : interfaces.IGetPaidManagementOptions( self.context ) }
        super(SalesforceScreen , self).update()


