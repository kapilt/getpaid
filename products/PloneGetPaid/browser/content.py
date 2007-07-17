"""
Content Control

$Id$
"""

import getpaid.core.interfaces as igetpaid
from getpaid.core import options, event

from zope.formlib import form
from zope import component
from zope.event import notify

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from Products.Five.utilities import marker
from Products.PloneGetPaid import interfaces
from base import BaseView, BaseFormView

class PayableFormView( BaseFormView ):

    adapters = None
    interface = None
    marker = None
    form_fields = form.FormFields()
    template = ZopeTwoPageTemplateFile('templates/payable-form.pt')

class PayableForm( PayableFormView, formbase.EditForm ):

    def allowed( self ):
        adapter = component.queryAdapter( self.context, igetpaid.IBuyableContent)
        return not ( adapter is None )
        
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
        
class PayableCreation( PayableForm ): 

    actions = form.Actions()

    def update( self ):
        # create a temporary object so we don't have to modify context until we're ready to activate
        # it.. this creates some odd behavior on remarking though, where the user is always filling
        # in new values even though previously values are present in the underlying contxt annotation.
        self.adapters = { self.interface : options.PropertyBag.makeinstance( self.interface ),
                          igetpaid.IPayable : options.PropertyBag.makeinstance( igetpaid.IPayable ) }
        
        return super( PayableForm, self).update()

    @form.action("Activate", condition=form.haveInputWidgets)
    def activate_payable( self, action, data):
        self.adapters = {}
        marker.mark( self.context, self.marker)
        self.handle_edit_action.success_handler( self, action, data )
        self.adapters[ igetpaid.IPayable ].made_payable_by = getSecurityManager().getUser().getId()
        notify(
            event.PayableCreationEvent( self.context, self.adapters[ igetpaid.IPayable ], self.interface )
            )

##     # formlib has serious issues do something as simple as a cancel button in our version of zope
##     # lame, seriously lame - kapilt
##     @form.action("Cancel")
##     def handle_cancel( self, action, data):
##         marker.erase( self.context, self.marker )
##         self.request.RESPONSE.redirect( self.context.absolute_url() ) 

class PayableDestruction( BrowserView ):
    
    def __call__(self):
        marker.erase( self.context, self.marker )
        self.request.RESPONSE.redirect( self.context.absolute_url() )


class BuyableForm( PayableForm ):
    form_fields = form.Fields( igetpaid.IBuyableContent )
    interface = igetpaid.IBuyableContent
    marker = interfaces.IBuyableMarker
    
class BuyableCreation( BuyableForm, PayableCreation ):
    actions = PayableCreation.actions
    update  = PayableCreation.update
    
class BuyableEdit( BuyableForm ): pass
class BuyableDestruction( PayableDestruction ):
    marker = interfaces.IBuyableMarker    

    
class ShippableForm( PayableForm ):
    """ shippable content operations """
    form_fields = form.Fields( igetpaid.IShippableContent )
    interface = igetpaid.IShippableContent
    marker = interfaces.IShippableMarker
    
class ShippableCreation( ShippableForm, PayableCreation ):
    actions = PayableCreation.actions
    update  = PayableCreation.update
    
class ShippableEdit( ShippableForm ): pass
class ShippableDestruction( PayableDestruction ):
    marker = interfaces.IShippableMarker
    
class PremiumForm( PayableForm ):
    """ premium content operations """
    form_fields = form.Fields( igetpaid.IPremiumContent )
    interface = igetpaid.IPremiumContent
    marker = interfaces.IPremiumMarker

class PremiumCreation( PremiumForm, PayableCreation ):
    actions = PayableCreation.actions
    update  = PayableCreation.update
    
class PremiumEdit( PremiumForm ): pass
class PremiumDestruction( PayableDestruction ):
    marker = interfaces.IPremiumMarker

    
class DonateForm( PayableForm ):
    """ donation operations """
    form_fields = form.Fields( igetpaid.IDonationContent )
    interface = igetpaid.IDonationContent
    marker = interfaces.IDonatableMarker

class DonateCreation( DonateForm, PayableCreation ):
    actions = PayableCreation.actions
    update  = PayableCreation.update
    
class DonateEdit( DonateForm ): pass
class DonateDestruction( PayableDestruction ):
    marker = interfaces.IDonatableMarker    


class ContentControl( BrowserView ):
    """ conditions for presenting various actions
    """

    __allow_access_to_unprotected_subobjects__ = 1
    __slots__ = ( 'context', 'request', 'options' )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request

        portal = getToolByName( self.context, 'portal_url').getPortalObject()
        options = interfaces.IGetPaidManagementOptions( portal )
        self.options = options

    def isPayable( self ):
        """  does the context implement the IPayable interface
        """
        return interfaces.IPayableMarker.providedBy( self.context )

    isPayable.__roles__ = None

    def isBuyable( self ):
        """  
        """
        return interfaces.IBuyableMarker.providedBy( self.context )

    isBuyable.__roles__ = None

    def isPremium( self ):
        """ 
        """
        return interfaces.IPremiumMarker.providedBy( self.context )

    isPremium.__roles__ = None

    def isShippable( self ):
        """ 
        """
        return interfaces.IShippableMarker.providedBy( self.context )
        
    isShippable.__roles__ = None

    def isDonatable( self ):
        """ 
        """
        return interfaces.IDonatableMarker.providedBy( self.context )
        
    isDonatable.__roles__ = None
        
    def _allowChangePayable( self, types ):
        """ 
        """
        return self.context.portal_type in types
    
    def allowMakeBuyable( self ):
        """  
        """
        return self._allowChangePayable(self.options.buyable_types) \
               and not self.isBuyable() and not self.request.URL0.endswith('@@activate-buyable')

    allowMakeBuyable.__roles__ = None
    
    def allowMakeNotBuyable( self ):
        """  
        """
        return self._allowChangePayable(self.options.buyable_types) \
               and self.isBuyable()
    
    allowMakeNotBuyable.__roles__ = None

    def allowMakeShippable( self ):
        """  
        """
        return self._allowChangePayable(self.options.shippable_types) \
               and not self.isPayable() and not self.request.URL0.endswith('@@activate-shippable')
    
    allowMakeShippable.__roles__ = None
    
    def allowMakeNotShippable( self ):
        """  
        """
        return self._allowChangePayable(self.options.shippable_types) \
               and self.isShippable()
    allowMakeNotShippable.__roles__ = None

    def allowMakePremiumContent( self ):
        """  
        """
        return self._allowChangePayable(self.options.premium_types) \
               and not self.isPayable() and not self.request.URL0.endswith('@@activate-premium-content')
    
    allowMakePremiumContent.__roles__ = None
    
    def allowMakeNotPremiumContent( self ):
        """  
        """
        return self._allowChangePayable(self.options.premium_types) \
               and self.isPremium()
    
    allowMakeNotPremiumContent.__roles__ = None
    
    def allowMakeDonatable( self ):
        """  
        """
        return self._allowChangePayable(self.options.donate_types) \
               and not self.isPayable() and not self.request.URL0.endswith('@@activate-donate')
    
    allowMakeDonatable.__roles__ = None
    
    def allowMakeNotDonatable( self ):
        """  
        """
        return self._allowChangePayable(self.options.donate_types) \
               and self.isDonatable()
    allowMakeNotDonatable.__roles__ = None

    def showManageCart( self ):
        utility = component.getUtility( igetpaid.IShoppingCartUtility )
        return utility.get( self.context ) is not None
    showManageCart.__roles__ = None

class ContentPortlet( BrowserView ):
    """ View methods for the ContentPortlet """

    payable = None
    def __init__( self, *args, **kw):
        super( BrowserView, self).__init__( *args, **kw)

        found = False
        for marker, iface in interfaces.PayableMarkerMap.items():
            if marker.providedBy( self.context ):
                found = True
                break

        if found:
            self.payable = iface( self.context )

    def isPayable(self):
        return self.payable is not None
        
