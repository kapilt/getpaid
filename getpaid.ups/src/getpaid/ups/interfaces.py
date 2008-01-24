"""
$Id: $
"""

from zope import schema, interface
from constants import *

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.ups')
#
class IUPSRateService( interface.Interface ):
    """
    UPS Rates Service
    """
    
    def getRates( order ):
        """
        """
    
class IOriginRouter( interface.Interface ):
    
    def getOrigin( ):
        """
        determine the origin shipping point for an order..
        
        return the contact and address info for origin
        
        TODO: support multiple origins for an order if someone can justify ;-)
        """

class IShippingMethodRate( interface.Interface ):
    """
     Service Code: UPS Next Day Air
     Shipment unit of measurement: LBS
     Shipment weight: 3.0
     Currency Code: USD
     Total Charge: 58.97
     Days to Delivery: 1
     Delivery Time: 10:30 A.M.
    """
    
    service_code = schema.ASCIILine( description=_(u"UPS Service Code (2 Letter)"))
    service = schema.TextLine( description=_(u"UPS Service Name"))
    
    currency = schema.ASCII( description=_(u"Currency Denomination Code"))
    cost = schema.Float( description=_(u"Cost of Delivery"))
    
    # really shouldn't show these, as they ignore store processing time
    days_to_delivery = schema.Int( description=_(u"Estimated Days to Deliver") )
    delivery_time = schema.TextLine( description=_(u"Estimated Delivery Time") ) 


class IUPSSettings( interface.Interface ):
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
    
    services = schema.List( title = _(u"UPS Services"),
                            required = True,
                            default = [],
                            description = _(u"The services to offer in your store."),
                            value_type = schema.Choice( title=u"ups_services_choice",
                                                        source=schema.vocabulary.SimpleVocabulary.fromValues( UPS_SERVICES.keys() )
                                                        )
                            )
    
    username = schema.ASCIILine( title = _(u"UPS User Name"),
        required = True,
        description = _(u"The user name you supplied when registering for your UPS access key."))
                                    
    password = schema.Password( title = _(u"UPS Password"),
        required = True,
        description = _(u"The password you supplied when registering for your UPS access key."))
                                    
    access_key = schema.ASCIILine( title = _(u"UPS Access Key"), 
        required = True,
        description = _(u"The access (not developer!) key issued to you by UPS."))
                                            
    # weight_unit = schema.Choice( title = _(u"Unit of weight"),
    #     values = upsconstants.UPS_WEIGHT_UNITS.keys(),
    #     required = True,
    #     description = _(u"Select which unit of weight to use for your products."),
    #     default = 'Pounds',
    #     )
    #     
    # currency_code = schema.Choice( title = _(u"UPS Currency Code"),
    #     values = upsconstants.UPS_CURRENCY_CODES.keys(),
    #     required = True,
    #     description = _(u"The currency that UPS will use when calculating your rates."),
    #     default = 'US Dollars (USD)',
    #     )




                                            
