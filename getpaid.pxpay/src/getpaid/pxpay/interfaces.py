from getpaid.core import interfaces
from zope import schema
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

    PxPaySiteCurrency = schema.Choice(
        title = _(u"Site Currency"),
        vocabulary = "getpaid.pxpay.currencies",
       )

