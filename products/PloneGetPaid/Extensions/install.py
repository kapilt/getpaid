"""
$Id$
"""
from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions as cmf_perms
from Products.PloneGetPaid import _GETPAID_DEPENDENCIES_
from Products.Five.site.localsite import enableLocalSiteHook

from zope.interface import alsoProvides, directlyProvides, directlyProvidedBy
from zope.component.interfaces import ISiteManager
from zope.app.component.hooks import setSite, getSite
from zope.app.component.interfaces import ISite, IPossibleSite
from zope.app.intid.interfaces import IIntIds
from five.intid.site import add_intids
from getpaid.core.interfaces import IOrderManager, IStore
from getpaid.core.order import OrderManager

def setup_site( self ):
    portal = getToolByName( self, 'portal_url').getPortalObject()    
    
    if ISite.providedBy( portal ):
        setSite( portal )
        return
    enableLocalSiteHook( portal )
    setSite( portal )

def setup_store( self ):
    portal = getToolByName( self, 'portal_url').getPortalObject()
    import pdb; pdb
    alsoProvides(portal, IStore)

def teardown_store( self ):
    portal = getToolByName( self, 'portal_url').getPortalObject()
    directlyProvides(portal, directlyProvidedBy(portal) - IStore)
#    marker.erase( portal, IStore )    

def setup_order_manager( self ):
    portal = getToolByName( self, 'portal_url').getPortalObject()
    sm = portal.getSiteManager()
    is_already_registered = [u for u in sm.getUtilitiesFor(IOrderManager)]
    if not len(is_already_registered):
        sm.registerUtility( IOrderManager, OrderManager() )

def setup_intid( self ):
    portal = getToolByName( self, 'portal_url').getPortalObject()
    add_initids( portal ) 

def install_dependencies( self ):
    quickinstaller = self.portal_quickinstaller
    for dependency in _GETPAID_DEPENDENCIES_:
        quickinstaller.installProduct( dependency )    

def install_cart_portlet( self, uninstall=False ):
    slot = 'here/@@portlet-shopping-cart/index/macros/portlet'
    portal = self.portal_url.getPortalObject()
    right_slots = portal.getProperty('right_slots')
    if isinstance( right_slots, str):
        right_slots = right_slots.split('\n')
    else:
        right_slots = list( right_slots )
    if uninstall:
        if slot in right_slots:
            right_slots.remove( slot )
    else:
        if slot not in right_slots:
            right_slots.append( slot )
    portal._updateProperty( 'right_slots', '\n'.join( right_slots ) )    

def install_contentwidget_portlet( self, uninstall=False ):
    slot = 'here/@@portlet-contentwidget'
    portal = self.portal_url.getPortalObject()
    right_slots = portal.getProperty('right_slots')
    if isinstance( right_slots, str):
        right_slots = right_slots.split('\n')
    else:
        right_slots = list( right_slots )
    if uninstall:
        if slot in right_slots:
            right_slots.remove( slot )
    else:
        if slot not in right_slots:
            right_slots.append( slot )
    portal._updateProperty( 'right_slots', '\n'.join( right_slots ) )    

def uninstall_cart_portlet( self ):
    install_cart_portlet( self, True )

def uninstall_contentwidget_portlet( self ):
    install_contentwidget_portlet (self, True )
    
def install( self ):
    out = StringIO()

    # Run all import steps for getPaid
    portal = getToolByName(self, 'portal_url').getPortalObject()
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-Products.PloneGetPaid:default')
    setup_tool.runAllImportSteps()
    setup_tool.setImportContext('profile-CMFPlone:plone')
    
    return out.getvalue()

def uninstall( self ):
    out = StringIO()

    print >> out, "Removing GetPaid"

    print >> out, "Uninstalling Control Panels Actions"
    uninstall_control_panel( self )

    print >> out, "Uninstalling Cart Portlets"
    uninstall_cart_portlet( self )

    print >> out, "Uninstalling Content Portlets"    
    uninstall_contentwidget_portlet( self )

    teardown_store( self )

    return out.getvalue()
