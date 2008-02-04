"""
migrate store settings from annotations to persistent utility
"""

from Products.PloneGetPaid.Extensions.install import setup_settings
from Products.PloneGetPaid import preferences, interfaces

from zope import component, schema

def evolve( portal ):

    setup_settings( portal )
    
    settings = component.getUtility( interfaces.IGetPaidManagementOptions )
    old_settings = preferences.OldConfigurationPreferences( portal )

    for field in schema.getFields( interfaces.IGetPaidManagementOptions ).values():
        field.set( settings, field.query( old_settings  ) )
        

    
    

    
