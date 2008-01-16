from persistent.dict import PersistentDict

from zope import component
from zope import interface
from zope.formlib import form
from zope.schema import fieldproperty
from zope.interface import implements
from zope.app.annotation.interfaces import IAnnotations

from Products.Five.formlib import formbase
from Products.Five.browser import pagetemplatefile
from Products.Five.utilities import marker
from Products.Five.browser import BrowserView

from getpaid.discount.browser.interfaces import IDiscountable
from getpaid.discount.browser.interfaces import IBuyXGetXFreeable
from getpaid.discount.browser.interfaces import IDiscountableMarker
from getpaid.discount.browser.interfaces import IBuyXGetXFreeableMarker

from Products.PloneGetPaid.interfaces import IPayableMarker

class DiscountForm(formbase.EditForm):
    """
    """
    form_fields = form.FormFields(IDiscountable)
    marker = IDiscountableMarker
    actions = form.Actions()
    interface = IDiscountable
    
    def allowed( self ):
        adapter = component.queryAdapter( self.context, IPayableMarker)
        return not (adapter is None)

class DiscountEdit(DiscountForm):
    """
    """
    @form.action("Update", condition=form.haveInputWidgets)
    def update_discountable( self, action, data):
        self.handle_edit_action.success_handler( self, action, data )
        message = 'Changes saved.'
        self.request.response.redirect( '%s/view?portal_status_message=%s' % (self.context.absolute_url(), message) )

class DiscountCreation(DiscountForm):
    """
    """
    
    @form.action("Activate", condition=form.haveInputWidgets)
    def activate_discountable( self, action, data):
        #we set up the type as IDiscountable
        interface.alsoProvides(self.context, self.marker)
        self.handle_edit_action.success_handler( self, action, data )
        message = 'Changes saved.'
        self.request.response.redirect( '%s/view?portal_status_message=%s' % (self.context.absolute_url(), message) )

class DiscountDestruction(BrowserView):
    marker = IDiscountableMarker
    
    def __call__(self):
        marker.erase( self.context, self.marker )
        self.request.response.redirect( '%s/view' % self.context.absolute_url() )

class BuyXGetXFreeEdit(DiscountEdit):
    """
    """
    interface = IBuyXGetXFreeable
    form_fields = form.FormFields(IBuyXGetXFreeable)
    marker = IBuyXGetXFreeableMarker

class BuyXGetXFreeCreation(DiscountCreation):
    """
    """
    interface = IBuyXGetXFreeable
    form_fields = form.FormFields(IBuyXGetXFreeable)
    marker = IBuyXGetXFreeableMarker

class BuyXGetXFreeDestruction(DiscountDestruction):
    marker = IBuyXGetXFreeableMarker

class DiscountAdapter(object):
    """
    """
    implements(IDiscountable)
    
    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)
        discount_title = self.annotations.get('discount_title', None)
        if discount_title is None:
            self.annotations['discount_title'] = ''
        discount_type = self.annotations.get('discount_type', None)
        if discount_type is None:
            self.annotations['discount_type'] = 'Dollars Off'
        discount_value = self.annotations.get('discount_value', None)
        if discount_value is None:
            self.annotations['discount_value'] = 0.0
    
    def getDiscountTitle(self):
        return self.annotations['discount_title']

    def setDiscountTitle(self, data):
        self.annotations['discount_title'] = data

    def getDiscountType(self):
        return self.annotations['discount_type']

    def setDiscountType(self, data):
        self.annotations['discount_type'] = data
    
    def getDiscountValue(self):
        return self.annotations['discount_value']

    def setDiscountValue(self, data):
        self.annotations['discount_value'] = data
    
    discount_title = property(fget=getDiscountTitle, fset=setDiscountTitle)
    discount_type = property(fget=getDiscountType, fset=setDiscountType)
    discount_value = property(fget=getDiscountValue, fset=setDiscountValue)

class BuyXGetXFreeAdapter(object):
    """
    """
    implements(IBuyXGetXFreeable)
    
    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)
        discount_title = self.annotations.get('discount_title', None)
        if discount_title is None:
            self.annotations['discount_title'] = ''
        number_to_buy = self.annotations.get('number_to_buy', None)
        if number_to_buy is None:
            self.annotations['number_to_buy'] = 0
        number_free = self.annotations.get('number_free', None)
        if number_free is None:
            self.annotations['number_free'] = 0
    
    def getDiscountTitle(self):
        return self.annotations['discount_title']

    def setDiscountTitle(self, data):
        self.annotations['discount_title'] = data

    def getNumberToBuy(self):
        return self.annotations['number_to_buy']

    def setNumberToBuy(self, data):
        self.annotations['number_to_buy'] = data
    
    def getNumberFree(self):
        return self.annotations['number_free']

    def setNumberFree(self, data):
        self.annotations['number_free'] = data
    
    discount_title = property(fget=getDiscountTitle, fset=setDiscountTitle)
    number_to_buy = property(fget=getNumberToBuy, fset=setNumberToBuy)
    number_free = property(fget=getNumberFree, fset=setNumberFree)
