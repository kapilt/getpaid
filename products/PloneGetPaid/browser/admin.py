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
    
    # check for one of the 3 possible shipping configurations and act accordingly
    # the most interesting one is for 3rd party rate calculators, in which we create a form with
    # the options interfaces for all of them that are available
    # there's probably a nicer way to format it, but I think this is ok for now. ::Liam
    def setupServices( self ):
        manage_options = interfaces.IGetPaidManagementShippingMethods( self.context )
        service_name = manage_options.shipping_method
        if not service_name or service_name == "None":
            self.status = _(u"Shipping is disabled - select an option from the main menu.")
            return
        elif service_name == "Flat Rate Shipping":
            self.form_name = _(u'Flat Rate Shipping Settings')
            try:
                ship_method = component.getAdapter( self.context, igetpaid.IShippingMethod, service_name )
            except:
                self.status = _(u"The currenly configured Shipping Method cannot be found; please check if the corresponding package is installed correctly.")
                return
            self.form_fields = form.Fields( ship_method.options_interface )
            return
        elif service_name == "3rd Party Shipping Rate Calculators":
            self.form_name = _(u'3rd Party Shipping Calculator Settings')
            try:
                ship_methods = list(component.getAdapters((self.context,), igetpaid.IShippingRateService))
            except:
                self.status = _(u"Couldn't get 3rd party calculators - make sure the packages are properly installed.")
                return
            if len(ship_methods) < 1:
                self.status = _(u"There are no 3rd party shipping calculators installed.")
                return
            else:
                self.form_fields = form.Fields( ) # empty the fields first, since we already have the base one in there
                for item in ship_methods:
                    name, ship_method = item
                    self.form_fields += form.Fields( ship_method.options_interface )
                return
        else:
            self.status = _(u"Unrecognized shipping option.")
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
        
        
       

