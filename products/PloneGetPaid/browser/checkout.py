"""

cart-review checkout

$Id$
"""

"""
random notes

get order
 
 - create order [ entry points ]
 - dispatch on workflow state

Order Workflow
  
  - created
     - system invariant - make sure we don't create multiple orders from the same cart, need to create cart_id, retrieve order by user_id, cart_id
     - automatic ready
  
  - ready
     - user submit
  
  - pending
     - automatic declined
     - automatic accepted
  
  - declined
     - user submit pending
  
  - accepted
     - admin submit processed
  
  - processed
  
  - re
  
  - status

allow linear progression

carry hidden to force transition to required, allow linear links to be used though

"""

import sys
from cPickle import loads, dumps


from zope.dottedname import resolve
from zope.event import notify
from zope.formlib import form
from zope import schema, interface
from zope.interface.interfaces import IInterface
from zope.app.event.objectevent import ObjectCreatedEvent
from zope.app.renderer.plaintext import PlainTextToHTMLRenderer

from zope import component

from zc.table import table, column

from getpaid.core import interfaces, options, payment
from getpaid.core.order import Order

from AccessControl import getSecurityManager
from ZTUtils import make_hidden_input

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.formlib import formbase
from Products.CMFCore.utils import getToolByName

from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions

from Products.PloneGetPaid.i18n import _

from base import BaseView
import cart as cart_core
from widgets import CountrySelectionWidget, StateSelectionWidget, CCExpirationDateWidget

def null_condition( *args ):
    return ()

class BaseCheckoutForm( formbase.EditForm, BaseView ):
    
    template = None # must be overridden
    hidden_form_vars = None
    _next_url = None
    wizard = None
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )
    
    def hidden_inputs( self ):
        if not self.hidden_form_vars: return ''
        return make_hidden_input( **self.hidden_form_vars )
    
    hidden_inputs = property( hidden_inputs )
    
    def setupHiddenFormVariables( self ):
        """ 
        export all values for all request form variables, excepting our own ourselves.
        for ourselves, its expected that a step will render widgets to pickup request values (default)        
        """
        # widgets don't nesc. have one to one mapping, greedily pass through
        # all the previous form data in the request.. skip actions. and only
        # pass through values which this step isn't collecting itself (issue 88)
        passed = {}
        ignore = []
        for f in self.form_fields:
            ignore.append( "%s.%s"%(self.prefix, f.__name__) )
        
        for k, v in self.request.form.items():
            # we need to do a second loop, if we want to allow custom multi part widgets (credit card date for example)
            # so we can ignore the entire input for the widget, probably a nicer way.
            next = False
            for i in ignore:
                if k.startswith(i):
                    next = True        
                    break
            if next:
                continue                
            passed[ k ] = v
        self.hidden_form_vars.update( passed )
    
    def invariantErrors( self ):
        errors = []
        for error in self.errors:
            if isinstance( error, interface.Invalid ):
                errors.append( error )
        return errors
    
    def getAdapters( self ):
        return self.adapters.values()
    
    def getFieldsByAdapter( self, adapter ):
        return [ff for ff in self.form_fields if ff.field.interface == adapter.schema]
    
    def getWidgetsByAdapter( self, adapter ):
        return [w for w in self.widgets if w.context.interface == adapter.schema ]
    
    def getWidgetsByIName( self, name ):
        # XXX only call through unrestricted code..
        iface  = resolve.resolve( name )
        assert IInterface.providedBy( iface )
        return self.getWidgetsByInterface( iface )
    
    def getWidgetsByInterface( self, interface ):
        return [w for w in self.widgets if w.context.interface == interface ]
    
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
    
    def hasPreviousStep( self, *args ):
        step = self.hidden_form_vars.get('cur_step', self.wizard.start_step )
        c, n, p = self.wizard.getSteps( step )
        return p != None

    def hasNextStep( self, *args ):
        step = self.hidden_form_vars.get('cur_step', self.wizard.start_step )
        c, n, p = self.wizard.getSteps( step )
        return n != None
                
    def render( self ):
        if self._next_url:
            self.request.RESPONSE.redirect( self._next_url )
            return ""
        return super( BaseCheckoutForm, self).render()

##############################
# Some Property Bags - transient adapters

class BillingInfo( options.PropertyBag ):
    title = "Billing Information"

    def __init__(self, context):
        # need a context to be able to get the current available credit
        # cards.
        self.context = context

class ShipAddressInfo( options.PropertyBag ):
    title = "Shipping Information"

class BillAddressInfo( options.PropertyBag ):
    title = "Payment Information"

class ContactInfo( options.PropertyBag ):
    title = "Contact Information"    

ContactInfo.initclass( interfaces.IUserContactInformation )
BillingInfo.initclass( interfaces.IUserPaymentInformation )
ShipAddressInfo.initclass( interfaces.IShippingAddress )
BillAddressInfo.initclass( interfaces.IBillingAddress )

class ImmutableBag( object ):
    
    def initfrom( self, other, iface ):
        for field_name, field in schema.getFieldsInOrder( iface ):
            setattr( self, field_name, field.get( other ) )
        return self


class OrderIdManagerMixin( object ):
    def getOrderId( self ):
        """ get the current order id out of the request,
            or generate a new one if it's not there yet."""
        order_id = self.request.get('order_id', None)
        if order_id is None and 'cur_step' not in self.request:
            # you're at the first step. Ok, have a new Id then            
            order_manager = component.getUtility( interfaces.IOrderManager )
            order_id = order_manager.newOrderId()
        return order_id

WIZARD_NEXT_STEP = object()
WIZARD_PREVIOUS_STEP = object()

class CheckoutWizard( OrderIdManagerMixin, BrowserView ):
    """
    a bidirectional checkout wizard.
    
    steps should export all form variables not from themselves as hidden inputs, to 
    allow for prepopulated forms from previous inputs on that step. 
    
    steps are specified in order and by view name. a step view must minimally have a
    an update/render cycle ala content_provider or formlib views.
    
    forms are processed as normal, we depend on a _next_url attribute being present
    and set to the either a url or one of the marker values for next or previous steps.
    
    the form must specify handlers for next / previous / finished steps.
    
    steps can't override call methods, as such logic won't be processed, since we call
    update / render methods directly.
    """
    steps = ['checkout-address-info', 'checkout-review-pay']


    @property
    def start_step( self ):
        return self.steps[0]
    
    def checkShoppingCart(self):
        cart = component.getUtility(interfaces.IShoppingCartUtility).get( self.context )
        if cart is None or not len(cart):
            self.request.response.redirect('@@empty-cart')
            return False
        return True
    
    def checkAuthenticated( self ):
        membership = getToolByName( self.context, 'portal_membership')
        if membership.isAnonymousUser():
            portal = getToolByName( self.context, 'portal_url').getPortalObject()
            if IGetPaidManagementOptions( portal ).allow_anonymous_checkout:
                return True
            self.request.response.redirect('login_form?came_from=@@getpaid-checkout-wizard')
            return False
        return True
        
    def __call__( self ):
        
        if not self.checkShoppingCart():
            return
        if not self.checkAuthenticated():
            return

        current_step, next_step, previous_step = self.getSteps()
        
        current = self.context.restrictedTraverse('@@%s'%current_step)
        current.wizard = self
        current.hidden_form_vars = dict( cur_step = current_step,
                                         order_id = self.getOrderId() )
        current.update()
        
        if current._next_url == WIZARD_NEXT_STEP:
            assert next_step, "No Next Step Or Redirect"
            current = self.context.restrictedTraverse('@@%s'%next_step )
            current.hidden_form_vars = dict( cur_step = next_step,
                                             order_id = self.getOrderId() )
        elif current._next_url == WIZARD_PREVIOUS_STEP:
            assert previous_step, "No Previous Step Or Redirect"            
            current = self.context.restrictedTraverse('@@%s'%previous_step)
            current.hidden_form_vars = dict( cur_step = previous_step,
                                             order_id = self.getOrderId() )
        else:
            # finish processing current step
            return current.render()

        # new current view
        current.wizard = self
        return current()
    
    def getSteps( self, cur_step=None ):
        """ return the current, next, and previous steps. """
        if cur_step is None:
            cur_step = self.request.get('cur_step', self.steps[0] )
            
        assert cur_step in self.steps
        
        step_idx = self.steps.index( cur_step )
        # check last step
        if len(self.steps) -1 == step_idx:
            next_step = None
        else:
            next_step = self.steps[ step_idx + 1 ]
            
        # check first step
        if step_idx == 0:
            previous_step = None
        else:
            previous_step = step_idx-1
            
        return cur_step, next_step, previous_step

class CheckoutAddress( BaseCheckoutForm ):
    """
    browser view for collecting credit card information and submitting it to
    a processor.
    """
    
    form_fields = form.Fields( interfaces.IBillingAddress,
                               interfaces.IShippingAddress,
                               interfaces.IUserContactInformation )
    
    form_fields['ship_country'].custom_widget = CountrySelectionWidget
    form_fields['bill_country'].custom_widget = CountrySelectionWidget
    form_fields['ship_state'].custom_widget = StateSelectionWidget
    form_fields['bill_state'].custom_widget = StateSelectionWidget
    
    template = ZopeTwoPageTemplateFile("templates/checkout-address.pt")

    _next_url = None
    
    def setupDataAdapters( self ):
        self.adapters = {}        
        user = getSecurityManager().getUser()   
        contact_info = component.queryAdapter( user, interfaces.IUserContactInformation )
        if contact_info is None:
            contact_info = ContactInfo()
            
        billing_address = component.queryAdapter( user, interfaces.IBillingAddress)
        if billing_address is None:
            billing_address = BillAddressInfo()
        
        shipping_address = component.queryAdapter( user, interfaces.IShippingAddress )
        if shipping_address is None:
            shipping_address = ShipAddressInfo()
            
        self.adapters[ interfaces.IUserContactInformation ] = contact_info
        self.adapters[ interfaces.IShippingAddress ] = shipping_address
        self.adapters[ interfaces.IBillingAddress ] = billing_address
        return
    
    def update( self ):
        self.setupDataAdapters()
        self.setupHiddenFormVariables()        
        super( CheckoutAddress, self).update()
    
    @form.action(_(u"Cancel"), name="cancel", validator=null_condition)
    def handle_cancel( self, action, data):
        return self.request.response.redirect( self.context.portal_url.getPortalObject().absolute_url() )
        
    @form.action(_(u"Continue"), name="continue", condition='hasNextStep')
    def handle_continue( self, action, data ):
        self._next_url = WIZARD_NEXT_STEP

class CheckoutReviewAndPay( OrderIdManagerMixin, BaseCheckoutForm ):
    
    form_fields = form.Fields( interfaces.IUserPaymentInformation )
    passed_fields = form.Fields( interfaces.IBillingAddress ) + \
                    form.Fields( interfaces.IShippingAddress ) + \
                    form.Fields( interfaces.IUserContactInformation )
    form_fields['cc_expiration'].custom_widget = CCExpirationDateWidget

    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")
    
    columns = [
        column.GetterColumn( title=_(u"Quantity"), getter=cart_core.LineItemColumn("quantity") ),
        column.GetterColumn( title=_(u"Name"), getter=cart_core.lineItemURL ),
        column.GetterColumn( title=_(u"Price"), getter=cart_core.lineItemPrice ),
        column.GetterColumn( title=_(u"Total"), getter=cart_core.lineItemTotal ),
       ]
    
    
    def setupDataAdapters( self ):
        self.adapters = {}
        self.adapters[ interfaces.IUserContactInformation ] = ContactInfo()        
        self.adapters[ interfaces.IBillingAddress ] = BillAddressInfo()
        self.adapters[ interfaces.IShippingAddress ] = ShipAddressInfo()
        self.adapters[ interfaces.IUserPaymentInformation ] = BillingInfo(self.context)

        # extract data that was passed through in the request, using edit widgets
        # for marshalling value extraction. we'll basically throw an error here
        # if the values aren't found, but that shouldn't happen in normal operation
        data = {}
        widgets = form.setUpEditWidgets( self.passed_fields, self.prefix, self.context,
                                         self.request, adapters=self.adapters,
                                         ignore_request=False )
        form.getWidgetsData( widgets, self.prefix, data )
        
        
        # save the data to the adapters, we're not an edit form so we won't automatically
        # be storing to them, and we don't want to use the values as object attributes
        self.extractData( data )
    
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}
        
        # edit widgets for payment info
        self.widgets = form.setUpEditWidgets(
            self.form_fields.select( *schema.getFieldNames( interfaces.IUserPaymentInformation)),
            self.prefix, self.context, self.request,
            adapters=self.adapters, ignore_request=ignore_request
            )
        
        # display widgets for bill/ship address
        self.widgets += form.setUpEditWidgets(
            self.passed_fields,  self.prefix, self.context, self.request,
            adapters=self.adapters, for_display=True, ignore_request=ignore_request
            )
    
    def renderCart( self ):
        cart = component.getUtility( interfaces.IShoppingCartUtility ).get( self.context )
        if not cart:
            return _(u"N/A")

        # create an order so that tax/shipping utilities have full order information
        # to determine costs (ie. billing/shipping address ).
        order = self.createOrder()
        formatter = cart_core.CartFormatter( order,
                                             self.request,
                                             cart.values(),
                                             prefix=self.prefix,
                                             visible_column_names = [c.name for c in self.columns],
                                             #sort_on = ( ('name', False)
                                             columns = self.columns )
        
        formatter.cssClasses['table'] = 'listing'
        return formatter()

    
    def update( self ):
        self.setupDataAdapters()
        self.setupHiddenFormVariables()
        super( CheckoutReviewAndPay, self).update()
    
    # custom validator.. make sure we have all relevant data
    #def validatePayment( self, action, data ):
    #    pass
    
    @form.action(_(u"Cancel"), name="cancel", validator=null_condition)
    def handle_cancel( self, action, data):
        return self.request.response.redirect( self.context.portal_url.getPortalObject().absolute_url() )
        
    @form.action(_(u"Back"), name="back", condition='hasPreviousStep')
    def handle_back( self, action, data):
        self._next_url = WIZARD_PREVIOUS_STEP                
        
    @form.action(_(u"Make Payment"), name="make-payment", condition=form.haveInputWidgets )
    def makePayment( self, action, data ):
        """ create an order, and submit to the processor
        for async processors we never even got here.???
        """
        manage_options = IGetPaidManagementOptions( self.context )
        processor_name = manage_options.payment_processor
        
        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )
        
        processor = component.getAdapter( self.context,
                                          interfaces.IPaymentProcessor,
                                          processor_name )
        self.extractData( data )
        
        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )
        
        # extract data to our adapters
        
        result = processor.authorize( order, self.adapters[ interfaces.IUserPaymentInformation ] )
        if result is interfaces.keys.results_async:
            # shouldn't ever happen, on async processors we're already directed to the third party
            # site on the final checkout step, all interaction with a processor are based on processor
            # adapter specific callback views.
            pass
        elif result is interfaces.keys.results_success:
            order_manager = component.getUtility( interfaces.IOrderManager )
            order_manager.store( order )
            order.finance_workflow.fireTransition("authorize")
            # kill the cart after we create the order
            component.getUtility( interfaces.IShoppingCartUtility ).destroy( self.context )
        else:
            order.finance_workflow.fireTransition('reviewing-declined')
            self.status = result
            self.form_reset = False
        
        self._next_url = self.getNextURL( order )
    
    def extractData( self, data ):
        for iface, adapter in self.adapters.items():
            for name, field in schema.getFieldsInOrder( iface ):
                if name in data:
                    field.set( adapter, data[ name ] )
    
    def createOrder( self ):
        order_manager = component.getUtility( interfaces.IOrderManager )
        order = Order()
        
        shopping_cart = component.getUtility( interfaces.IShoppingCartUtility ).get( self.context )
        
        # shopping cart is attached to the session, but we want to switch the storage to the persistent
        # zodb, we pickle to get a clean copy to store.
        
        order.shopping_cart = loads( dumps( shopping_cart ) )
        order.shipping_address = payment.ShippingAddress.frominstance( self.adapters[ interfaces.IShippingAddress ] )
        order.billing_address = payment.BillingAddress.frominstance( self.adapters[ interfaces.IBillingAddress ] )
        order.contact_information = payment.ContactInformation.frominstance( self.adapters[ interfaces.IUserContactInformation ] )

        order.order_id = self.getOrderId()
        order.user_id = getSecurityManager().getUser().getId()
        notify( ObjectCreatedEvent( order ) )
        
        return order
    
    def getNextURL( self, order ):
        state = order.finance_state
        f_states = interfaces.workflow_states.order.finance
        base_url = self.context.absolute_url()

## we display errors inline on the checkout form, so don't redirect
##         if state in ( f_states.CANCELLED,
##                       f_states.CANCELLED_BY_PROCESSOR,
##                       f_states.PAYMENT_DECLINED ):
##             return base_url + '/@@checkout-error'
        
        if state in ( f_states.CHARGEABLE,
                      f_states.CHARGING,
                      f_states.REVIEWING,
                      f_states.CHARGED ):
            return base_url + '/@@getpaid-thank-you?order_id=%s&finance_state=%s' %(order.order_id,state)

class CheckoutConfirmed( BrowserView ):
    """ thank you screen after success
    """

class CartEmpty( BrowserView ):
    """ cart is empty, can't checkout """

class DisclaimerView(BrowserView):
    """ Shows the disclaimer text from the getpaid settings.
    """
    
    @property
    def disclaimer(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        settings = IGetPaidManagementOptions(portal)
        disclaimer = None
        if settings.disclaimer:
            renderer = PlainTextToHTMLRenderer(settings.disclaimer, self.request)
            disclaimer = renderer.render().strip()
        return disclaimer

class PrivacyPolicyView(BrowserView):
    """ Shows the privacy policy text from the getpaid settings.
    """
    
    @property
    def privacy_policy(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        settings = IGetPaidManagementOptions(portal)
        privacy = None
        if settings.privacy_policy:
            renderer = PlainTextToHTMLRenderer(settings.privacy_policy, self.request)
            privacy = renderer.render().strip()
        return privacy
