from Products.CMFCore.utils import getToolByName
from getpaid.core.options import PersistentOptions
from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility
from getpaid.ogone.interfaces import IOgoneStandardProcessor, IOgoneStandardOptions
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.interface import implements
from zope.component import getUtility
from getpaid.core.interfaces import keys
import interfaces
import urllib
import sha

OgoneStandardOptions = PersistentOptions.wire("OgoneStandardOptions",
                                              "getpaid.ogone",
                                              interfaces.IOgoneStandardOptions)

class OgoneStandardProcessor(object):
    """
    Ogone Standard Processor
    """
    implements(IOgoneStandardProcessor)

    options_interface = IOgoneStandardOptions

    def __init__(self, context):
        self.context = context

    def cart_post_button(self, cart):
        options = IOgoneStandardOptions(self.context)

    def getLanguage(self):
        """
        Ogone requires en_EN or en_US language id
        We are parsing the request to get the right
        """
        languages = IUserPreferredLanguages(self.context.request)
        langs = languages.getPreferredLanguages()
        if langs:
            language = langs[0]
        else:
            plone_props = getToolByName(self.context, 'portal_properties')
            language = plone_props.site_properties.default_language
        language = language.split('-')
        if len(language) == 1:
            language.append(language[0])
        language = language[:2]
        return "_".join(language)

    def createSHASignature(self, order):
        """
        Create the basic SHA signature
        See the Ogone Advanced e-commerce documentation SHA-IN for more informations
        """
        options = IOgoneStandardOptions( self.context )
        shaPassword = options.shain
        shaObject = sha.new()
        shaObject.update("%s%s%s%s%s" % (order.order_id,
                                   int(order.getTotalPrice()*100),
                                   options.currency, options.pspid,
                                   shaPassword))
        hexString = shaObject.hexdigest()
        return hexString.upper()

    def authorize(self, order, payment_information):
        """
        authorize an order, using payment information.
        """
        price = order.getTotalPrice()
        ogone_price = int(price * 100)
        orderId = order.order_id
        options = IOgoneStandardOptions( self.context )
        server_url = options.server_url
        urlArgs = dict(pspid=options.pspid,
                       orderID=orderId,
                       RL='ncol-2.0',
                       currency=options.currency,
                       amount=ogone_price)
        urlArgs['language'] = self.getLanguage()
        if options.cancel_url:
            urlArgs['cancelurl'] = options.cancel_url
        if options.accept_url:
            urlArgs['accepturl'] = options.accept_url
        if options.decline_url:
            urlArgs['declineurl'] = options.decline_url
        if options.error_url:
            urlArgs['exceptionurl'] = options.error_url
        urlArgs['SHASign'] = self.createSHASignature(order)
        arguments = urllib.urlencode(urlArgs)
        url = "%s?%s" % (server_url, arguments)
        order_manager = getUtility(IOrderManager)
        order_manager.store( order )
        order.finance_workflow.fireTransition("authorize")
        getUtility(IShoppingCartUtility).destroy(self.context)
        self.context.request.response.redirect(url)

    def capture(self, order, amount):
        """
        capture amount from order.
        """
        return keys.results_async

    def refund(self, order, amount):
        """
        reset
        """

