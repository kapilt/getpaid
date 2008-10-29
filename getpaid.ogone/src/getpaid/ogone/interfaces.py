from getpaid.core import interfaces
from zope import schema
from getpaid.ogone import _

class IOgoneStandardOptions(interfaces.IPaymentProcessorOptions ):
    """
    Ogone Standard Options
    """
    server_url = schema.Choice(title = _(u"Ogone Website Payments Server"),
                               vocabulary = "getpaid.ogone.server_urls")

    pspid = schema.ASCIILine(
        description = _(u"Enter here your ogone pspid"),
        required = True,
        title = _(u"Ogone Id"))

    currency = schema.Choice(
        title = _(u"Currency"),
        vocabulary = "getpaid.ogone.currencies")

    shain = schema.Password(
        title = _(u"SHA IN String"),
        required = True,
        description = _(u"The SHA-1 password string you entered in section 3.2 of the Ogone technical information page"))

    shaout = schema.Password(
        title = _(u"SHA OUT String"),
        required = True,
        description = _(u"The SHA-1 password string you entered in section 4.3 of the Ogone technical information page"))


    accept_url = schema.URI(
        title = _("Accept URL"),
        required = False,
        description = _(u"The url of the page that display the success of the payment"),)

    cancel_url = schema.URI(
        title = _("Cancel URL"),
        required = False,
        description = _(u"The url of the page which is displayed when the payment is cancelled"),)

    decline_url = schema.URI(
        title = _("Decline URL"),
        required = False,
        description = _(u"The url of the page which is displayed when the payment is refused by the band card company"),)

    error_url = schema.URI(
        title = _("Error URL"),
        required = False,
        description = _(u"The url of the page which is displayed when there is an error in the payment transation"),)

class IOgoneStandardProcessor( interfaces.IPaymentProcessor ):
    """
    Ogone Standard Processor
    """

