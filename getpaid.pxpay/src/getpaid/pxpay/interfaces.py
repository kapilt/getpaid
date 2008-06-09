from zope.interface import Interface
from zope import schema

from getpaid.core import interfaces

from getpaid.pxpay import _

class IPXPayStandardOptions(interfaces.IPaymentProcessorOptions):
    """
    PXPay Standard Options
    """
    PxPayServerType = schema.Choice(title = _(u"PXPay Website Payments Server"),
                                    vocabulary = "getpaid.pxpay.server_urls")

    PxPayUserId = schema.ASCIILine(
        title = _(u"PXPay UserId"),
        description = _(u"Enter your PXPay account UserId"),
        required = True,
       )

    PxPayKey = schema.ASCIILine(
        title = _(u"PXPay Key"),
        description = _(u"Enter the 64 character key that you were supplied for your PXPay account"),
        required = True,
      )

    MerchantReference = schema.ASCIILine(
        title = _(u"Merchant Reference"),
        description = _(u"Enter the 64 character merchant reference. This is free text to appear on transaction reports."),
        required = False,
      )

    PxPaySiteCurrency = schema.Choice(
        title = _(u"Site Currency"),
        vocabulary = "getpaid.pxpay.currencies",
       )


class IPXPayWebInterfaceGateway( Interface ):
    """
    A utility for connecting to and sending XML messages to the DPS
    pxpay web interface gateway.
    """

    def send_message(message, timeout):
        """
        Send a PXPay XML message to the pxpay web interface
        """

    def send_message_offline_testmode(message):
        """
        An offline mode that returns a canned test response to a
        send_message.
        """

class IPXPayInvalidMessageError( Interface ):
    """Utility to provide a hanlder for pxpay message errors,
    """

class IPXPayNetworkError( Interface ):
    """Utility to provide a handler for pxpay network errors.
    """


class IPXPayPaymentProcessor( interfaces.IPaymentProcessor ):
    """
    PXPay payment processor
    """
