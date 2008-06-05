import logging

from zope import interface
from zope.component import getUtility
from zope.app.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from getpaid.core import interfaces, options

from getpaid.pxpay.interfaces import IPXPayStandardOptions, \
     IPXPayWebInterfaceGateway
from getpaid.pxpay import parser

log = logging.getLogger('getpaid.pxpay')

PXPayStandardOptions = options.PersistentOptions.wire(
    "PXPayStandardOptions",
    "getpaid.pxpay",
    IPXPayStandardOptions
    )

class PXPayPaymentAdapter( object ):

    interface.implements( interfaces.IPaymentProcessor )

    options_interface = IPXPayStandardOptions

    def __init__( self, context ):
        self.context = context
        self.settings = IPXPayStandardOptions( self.context )
        self.pxpay_gateway = IPXPayWebInterfaceGateway(self.settings)
        self.site_root = getToolByName(context, 'portal_url').getPortalObject()
        self.site_url = self.site_root.absolute_url()

    def authorize( self, order, payment, request=None ):
        # async processors need to store the order so that it is
        # retrievable when the callback is initiated from the external
        # site we redirect to.

        return_url = '/'.join((self.site_url,
                              '@@pxpayprocessresponse'))
        initial_request = parser.InitialRequest()
        initial_request.pxpay_user_id = self.settings.PxPayUserId
        initial_request.pxpay_key = self.settings.PxPayKey
        initial_request.amount_input = order.getTotalPrice()
        initial_request.currency_input = self.settings.PxPaySiteCurrency
        initial_request.merchant_reference = self.settings.MerchantReference
        initial_request.transaction_type = "Purchase"
        initial_request.transaction_id = order.order_id
        initial_request.url_failure = return_url
        initial_request.url_success = return_url

        state_valid, errors = initial_request.state_validate()
        if not state_valid:
            raise PXPayException(errors)
        data = self.pxpay_gateway.send_message(initial_request)
        response_message = parser.InitialResponse(data)
        if not response_message.is_valid_response:
            raise PXPayInvalidMessageException
        log.info("Recieved: %s" % response_message)
        payment_url = response_message.request_url
        order.finance_workflow.fireTransition("authorize")
        request.response.redirect(payment_url)

    def capture( self, order, amount ):
        return  interfaces.keys.results_async

    def refund( self, order, amount ):
        pass

