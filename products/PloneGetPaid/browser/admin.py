"""
admin setting and preferences

$Id$
"""

import os

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser import BrowserView
from Products.Five.formlib import formbase
from Products.PloneGetPaid import interfaces, pkg_home

from zope import component
from zope.formlib import form

import getpaid.core.interfaces as igetpaid

from Products.PloneGetPaid.i18n import _

from base import BaseView
from widgets import SelectWidgetFactory, CountrySelectionWidget, StateSelectionWidget


class Overview( BrowserView ):
    """ overview of entire system
    """
    def __call__( self ):
        self.settings = interfaces.IGetPaidManagementOptions( self.context )
        return super( Overview, self).__call__()
    
    def getVersion( self ):
        fh = open( os.path.join( pkg_home, 'version.txt') )
        version_string = fh.read()
        fh.close()
        return version_string

class BaseSettingsForm( formbase.EditForm, BaseView ):

    options = None
    template = ZopeTwoPageTemplateFile("templates/settings-page.pt")
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request
        self.setupLocale( request )
        self.setupEnvironment( request )    

    def update( self ):
        try:
            interface = iter( self.form_fields ).next().field.interface
        except StopIteration:
            interface = None
        if interface is not None:
            self.adapters = { interface : interfaces.IGetPaidManagementOptions( self.context ) } 
        super( BaseSettingsForm, self).update()
        
class Identification( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementIdentificationOptions)
    form_fields['contact_country'].custom_widget = CountrySelectionWidget
    form_fields['contact_state'].custom_widget = StateSelectionWidget
    form_name = _(u'Site Profile')

class ContentTypes( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields( interfaces.IGetPaidManagementContentTypes )
    form_fields = form_fields.omit('premium_types')
    #form_fields = form_fields.omit('shippable_types')
    form_name = _(u'Content Types')
    
    form_fields['buyable_types'].custom_widget = SelectWidgetFactory
    #form_fields['premium_types'].custom_widget = SelectWidgetFactory
    form_fields['donate_types'].custom_widget = SelectWidgetFactory
    form_fields['shippable_types'].custom_widget = SelectWidgetFactory

class ShippingMethods( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementShippingMethods)
    form_fields['shipping_methods'].custom_widget = SelectWidgetFactory
    form_name = _(u'Shipping Methods')

class ShippingSettings( BaseSettingsForm ):
    """
    get paid management interface, slightly different because our form fields
    are dynamically set based on the store's setting for a shipping method.
    """
    
    form_fields = form.Fields(interfaces.IGetPaidManagementShippingMethods)
    form_name = _(u'Shipping Methods')
    
    def __call__( self ):
        self.setupServices()
        return super( ShippingSettings, self).__call__()
    
    # this is going to need to change to acommodate viewlets.  ugh.  ::Liam
    def setupServices( self ):
        manage_options = interfaces.IGetPaidManagementShippingMethods( self.context )
        service_names = manage_options.shipping_methods
        self.form_fields = form.Fields()
        self.status = _(u"Shipping settings are getting revamped at the moment...")
        return

class PaymentOptions( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementPaymentOptions)
    form_fields['accepted_credit_cards'].custom_widget = SelectWidgetFactory
    form_name = _(u'Payment Options')

class PaymentProcessor( BaseSettingsForm ):
    """
    get paid management interface, slightly different because our form fields
    are dynamically set based on the store's setting for a payment processor.
    """
    
    form_fields = form.Fields()
    form_name = _(u'Payment Processor Settings')

    def __call__( self ):
        self.setupProcessorOptions()
        return super( PaymentProcessor, self).__call__()
        
    def setupProcessorOptions( self ):
        manage_options = interfaces.IGetPaidManagementOptions( self.context )
        
        processor_name = manage_options.payment_processor
        if not processor_name:
            self.status = _(u"Please Select Payment Processor in Payment Options Settings")
            return

        #NOTE: if a processor name is saved in the configuration but the corresponding payment method package
        # doesn't exist anymore, a corresponding adapter will not be found.
        try:
            processor = component.getAdapter( self.context,
                                              igetpaid.IPaymentProcessor,
                                              processor_name )
        except:
            self.status = _(u"The currently configured Payment Processor cannot be found; please check if the corresponding package is installed correctly.")
            return
        
        self.form_fields = form.Fields( processor.options_interface )
        
# Order Management
class CustomerInformation( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementCustomerInformation)

class PaymentProcessing( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementPaymentProcessing)
        
class WeightUnits( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementWeightUnits)
        
class SessionTimeout( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementSessionTimeout)

class SalesTax( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementSalesTaxOptions)
    form_name = _(u'Sales Tax Configuration')
                
#Currency        
class Currency( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementCurrencyOptions)

#Emails
class Email( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementEmailOptions)
    form_name = _(u'Email Notifications')

#Customize Header/Footer        
class LegalDisclaimers( BaseSettingsForm ):
    """
    get paid management interface
    """
    form_fields = form.Fields(interfaces.IGetPaidManagementLegalDisclaimerOptions)
    form_name = _(u'Legal Disclaimers')
        
        
       

