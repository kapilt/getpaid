"""
$Id: $
"""

from zope.formlib import form
from zope import component
from getpaid.salesforce import  interfaces
from getpaid.core.options import PersistentOptions

from Products.PloneGetPaid.browser.admin import BaseSettingsForm

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.salesforce')

class SalesforceScreen( BaseSettingsForm ):
    """
    Salesforce management interface
    """
    form_fields = form.Fields(interfaces.ISalesforceOptions)
    form_name = _(u'Salesforce')


def SalesforceConfigurationPreferences( site ):

    settings = component.queryUtility(interfaces.ISalesforceOptions, site)
    if settings is None: # we have an unmigrated site.. fallback gracefully
        return OldConfigurationPreferences( site )

    # store access to the site, because our vocabularies get the setting as context
    # and want to access portal tools to construct various vocabs
    settings._v_site = site
    return settings

# previously we stored settings as annotations on the site, we've migrated this to
# its own utility, so we don't have to carry context to access the store settings.
# we have it here so we can do a migration.
OldConfigurationPreferences = PersistentOptions.wire("OldConfigurationPreferences",
                                                     "getpaid.salesforce",
                                                     interfaces.ISalesforceOptions )

