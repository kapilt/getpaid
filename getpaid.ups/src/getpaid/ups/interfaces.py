
from getpaid.core import interfaces
from zope import schema

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
        )
    
    ups_username = schema.ASCIILine( title = _(u"UPS User Name"),
                                    description = _(u"The user name you supplied when registering for your UPS developer key."))
                                    
    ups_password = schema.ASCIILine( title = _(u"UPS Password"),
                                    description = _(u"The password you supplied when registering for your UPS developer key."))
                                    
    ups_developer_key = schema.ASCIILine( title = _(u"UPS Developer Key"), 
                                            description = _(u"The developer key issued to you by UPS."))



                                            
