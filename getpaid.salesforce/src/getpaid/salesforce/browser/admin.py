"""
$Id: $
"""

from zope.formlib import form
import interfaces

from Products.PloneGetPaid.browser.admin import BaseSettingsForm

class SalesforceScreen( BaseSettingsForm ):
    """
    Salesforce management interface
    """
    form_fields = form.Fields(interfaces.ISalesforceSettings)
    form_name = _(u'Salesforce')


