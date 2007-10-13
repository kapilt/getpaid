from getpaid.core import interfaces
from zope import schema
from upsconstants import UPS_SERVICES

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.ups')

class IUPSRateService( interfaces.IShippingRateService ):
    """
    UPS Rates Service
    """
    
class IUPSRateServiceOptions( interfaces.IShippingRateServiceOptions ):
    """
    UPS Rates Service Options
    """
    server_url = schema.Choice(
        title = _(u"UPS Shipment Processor URL"),
        values = ( "Sandbox", "Production" ),
        description = _(u"Select Sandbox while testing your store, and switch to Production for the real thing."),
        default = "Sandbox",
        required = True,
        )
    
    ups_services = schema.List( title = _(u"UPS Services"),
                                required = True,
                                default = [],
                                description = _(u"The services to offer in your store."),
                                value_type = schema.Choice( title=u"ups_services_choice",
                                                            source=schema.vocabulary.SimpleVocabulary.fromValues( UPS_SERVICES.keys() )
                                                            )
                                )
    
    ups_username = schema.ASCIILine( title = _(u"UPS User Name"),
        required = True,
        description = _(u"The user name you supplied when registering for your UPS access key."))
                                    
    ups_password = schema.Password( title = _(u"UPS Password"),
        required = True,
        description = _(u"The password you supplied when registering for your UPS access key."))
                                    
    ups_access_key = schema.ASCIILine( title = _(u"UPS Access Key"), 
        required = True,
        description = _(u"The access (not developer!) key issued to you by UPS."))
                                            
    # ups_weight_unit = schema.Choice( title = _(u"Unit of weight"),
    #     values = upsconstants.UPS_WEIGHT_UNITS.keys(),
    #     required = True,
    #     description = _(u"Select which unit of weight to use for your products."),
    #     default = 'Pounds',
    #     )
    #     
    # ups_currency_code = schema.Choice( title = _(u"UPS Currency Code"),
    #     values = upsconstants.UPS_CURRENCY_CODES.keys(),
    #     required = True,
    #     description = _(u"The currency that UPS will use when calculating your rates."),
    #     default = 'US Dollars (USD)',
    #     )




                                            
