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


coci_actions = [

       ( dict(  id = 'getpaid_make_buyable',
                name = 'Make Buyable',
                action = 'string:$object_url/@@activate-buyable',
                category ='object_buttons',
                permission = "Modify portal content",
                condition = "python:path('object/@@getpaid_control').allowMakeBuyable()",
                visible = True ),
         "user.gif" ),

       ( dict(  id = 'getpaid_make_shippable',
                 name = 'Make Shippable Product',
                 action = 'string:$object_url/@@activate-shippable',
                 category ='object_buttons',
                 permission = "Modify portal content",
                 condition = "python:path('object/@@getpaid_control').allowMakeShippable()",
                 visible = True ),
          "user.gif" ),

##       ( dict(  id = 'getpaid_make_premium',
##                 name = 'Make Premium Members Only',
##                 action = 'string:$object_url/@@activate-premium-content',
##                 category ='object_buttons',
##                 permission = "Modify portal content",
##                 condition = "python:path('object/@@getpaid_control').allowMakePremiumContent()",
##                 visible = True ),
##          "user.gif" ),

     ( dict(  id = 'getpaid_make_donatable',
              name = 'Make this a Donation',
              action = 'string:$object_url/@@activate-donate',
              category ='object_buttons',
              permission = "Modify portal content",
              condition = "python:path('object/@@getpaid_control').allowMakeDonatable()",
              visible = True ),
       "user.gif" ),


       ( dict(  id = 'getpaid_make_not_buyable',
                name = 'Make Not Buyable',
                action = 'string:$object_url/@@deactivate-buyable',
                category ='object_buttons',
                permission = "Modify portal content",
                condition = "python:path('object/@@getpaid_control').allowMakeNotBuyable()",
                visible = True ),
         "user.gif" ),

      ( dict(  id = 'getpaid_make_not_shippable',
                name = 'Make Not Shippable Product',
                action = 'string:$object_url/@@deactivate-shippable',
                category ='object_buttons',
                permission = "Modify portal content",
                condition = "python:path('object/@@getpaid_control').allowMakeNotShippable()",
                visible = True ),
         "user.gif" ),

      ( dict(  id = 'getpaid_make_not_premium',
                name = 'Make Not Premium Members Only',
                action = 'string:$object_url/@@deactivate-premium-content',
                category ='object_buttons',
                permission = "Modify portal content",
                condition = "python:path('object/@@getpaid_control').allowMakeNotPremiumContent()",
                visible = True ),
         "user.gif" ),

     ( dict(  id = 'getpaid_make_not_donatable',
              name = 'Make this not a Donation',
              action = 'string:$object_url/@@deactivate-donate',
              category ='object_buttons',
              permission = "Modify portal content",
              condition = "python:path('object/@@getpaid_control').allowMakeNotDonatable()",
              visible = True ),
       "user.gif" ),

      ( dict(  id = 'getpaid_manage_cart',
                name = 'Manage Cart',
                action = 'string:$object_url/@@getpaid-cart',
                category ='user',
                permission = "View",
                condition = "python:path('object/@@getpaid_control').showManageCart()",
                visible = True ),
         None ),

     ( dict(  id = 'getpaid_order_history',
               name = 'Order History',
               action = 'string:$portal_url/@@getpaid-order-history',
               category ='user',
               permission = "View",
               condition = "python:path('object/@@getpaid_control').showOrderHistory()",
               visible = True ),
        None ),


        ]

def setup_actions( self ):
    actions = getToolByName( self, 'portal_actions')
    action_icons = getToolByName( self, 'portal_actionicons')
    
    for action, image in coci_actions:
        actions.addAction( **action )

        if not image:
            continue
        
        if action_icons.queryActionIcon( action['category'], action['id'], None) is None:
            action_icons.addActionIcon( action['category'],
                                        action['id'],
                                        image,
                                        action['name'] )

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

def install_control_panel( self ):

    manage_ui= getToolByName( self, 'portal_controlpanel')

    manage_ui.addAction(
        id = "getpaid",
        name = "GetPaid",
        action = "string:${portal_url}/@@manage-getpaid-overview",
        appId = "PloneGetPaid",
        imageUrl = "++resource++getpaid.png",
        description = "Management Access to Commerce Backend",
        category = "Products",
        permission=cmf_perms.ManagePortal
        
        )

def uninstall_control_panel( self ):
    manage_ui= getToolByName( self, 'portal_controlpanel')
    manage_ui.unregisterApplication( "PloneGetPaid" )

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

    # Run all import steps for ItalianSkin
    portal = getToolByName(self, 'portal_url').getPortalObject()
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-Products.PloneGetPaid:default')
    setup_tool.runAllImportSteps()
    setup_tool.setImportContext('profile-CMFPlone:plone')
    
    print >> out, "Installing Control Panel"
    install_control_panel( self  )

    print >> out, "Installing Cart Portlet"
    install_cart_portlet( self )

    print >> out, "Installing Content Widget Portlet"
    install_contentwidget_portlet( self )

    print >> out, "Installing Actions"
    setup_actions( self )

    print >> out, "Installing Local Site"
    setup_site( self )

    print >> out, "Installing Store Marker Interface"
    setup_store( self )
    
    print >> out, "Installing Order Local Utility"
    setup_order_manager( self )

    print >> out, "Installing IntId Utility"
    add_intids( self )
    
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
