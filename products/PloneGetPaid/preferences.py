"""

Annotation Property Storage and Site Configuration Settings

$Id$
"""

from getpaid.core.options import PersistentOptions, PersistentBag
from zope import component
import interfaces

def ConfigurationPreferences( site ):

    settings = component.getUtility( interfaces.IGetPaidManagementOptions )
    # store access to the site, because our vocabularies get the setting as context
    # and want to access portal tools to construct various vocabs
    settings._v_site = site
    return settings

# previously we stored settings as annotations on the site, we've migrated this to
# its own utility, so we don't have to carry context to access the store settings.
# we have it here so we can do a migration. 
OldConfigurationPreferences = PersistentOptions.wire("OldConfigurationPreferences",
                                                     "getpaid.configuration",
                                                     interfaces.IGetPaidManagementOptions )

_StoreSettings = PersistentBag.makeclass( interfaces.IGetPaidManagementOptions )

class StoreSettings( _StoreSettings ):

    _v_site = None
    
    @property
    def context( self ):
        return self._v_site
    
    def manage_fixOwnershipAfterAdd( self ): pass

