"""
$Id$
"""

from getpaid.core import interfaces
from zope import schema

class IGoogleCheckoutProcessor( interfaces.IPaymentProcessor ):
    """
    Google Checkout Processor
    """

class IGoogleCheckoutOptions( interfaces.IPaymentProcessorOptions ):
    """
    Google Checkout Options
    """
    server_url = schema.Choice( title = u"Google Checkout Server URL",
                                values = ( "https://sandbox.google.com/checkout/cws/v2/Merchant/%s/checkout",
                                           "https://checkout.google.com/cws/v2/Merchant/%s/checkout" ) )

    merchant_id = schema.TextLine( title = u"Merchant Id")
    merchant_key = schema.ASCII( title = u"Merchant Key")
