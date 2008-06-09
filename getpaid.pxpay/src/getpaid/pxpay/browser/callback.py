"""
The pxpay payment processor involves call backs to the site which
result in an update on the status of an order during and after a
payment transaction.
"""
import logging
from Acquisition import aq_inner
from zope.component import getUtility

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from getpaid.core.interfaces import IOrderManager, IShoppingCartUtility, \
     workflow_states, IOrder

from getpaid.pxpay import parser
from getpaid.pxpay.interfaces import IPXPayStandardOptions, \
     IPXPayWebInterfaceGateway, IPXPayInvalidMessageError, \
     IPXPayNetworkError
from getpaid.pxpay.exceptions import PXPayException, PXPayNetworkException, \
     PXPayInvalidMessageException
from getpaid.pxpay.config import RETURNED_TEST_CARD_NUMBER, TEST_SERVER_TYPE


log = logging.getLogger('getpaid.pxpay')

class ProcessResponse(BrowserView):
    """
    pxppay calls back on the url given in the initial request for
    payment. This url should be set to this view. This view is
    responsible for generating a ProcessResponse packet and sending
    this to pxpay to get confirmation details for the payment. see
    http://www.dps.co.nz/technical_resources/ecommerce_hosted/pxpay.html#ProcessResponse
    """

    def __init__(self, context, request):
        super(ProcessResponse, self).__init__(context, request)
        context = aq_inner(self.context)
        self.site_root = getToolByName(context, 'portal_url').getPortalObject()
        self.processor_options = IPXPayStandardOptions(self.site_root)
        self.pxpay_gateway = IPXPayWebInterfaceGateway(self.processor_options)

    def __call__(self):
        context = aq_inner(self.context)
        order_id = None
        if IOrder.providedBy(context):
            order_id = context.order_id
        encrypted_response = self.request.form.get('result', None)
        if not encrypted_response:
            raise PXPayException("There should be a result attribute in the form data for this view")
        process_response_message = parser.ReturnRequest()
        process_response_message.pxpay_user_id = self.processor_options.PxPayUserId
        process_response_message.pxpay_key = self.processor_options.PxPayKey
        process_response_message.response = encrypted_response

        state_valid, errors = process_response_message.state_validate()
        if not state_valid:
            raise PXPayException(errors)

        try:
            data = self.pxpay_gateway.send_message(process_response_message)
            log.info("About to send: %s" % process_response_message)
        except PXPayNetworkException:
            getUtility(IPXPayNetworkError)(self.context, self.request,
                                           order_id=order.order_id)
            return
        response_message = parser.ReturnResponse(data)
        log.info("Recieved: %s" % response_message)

        if not response_message.is_valid_response:
            getUtility(IPXPayInvalidMessageError)(self.context, self.request,
                                                  order_id=order_id,
                                                  message=response_message)
            return

        order_id = response_message.transaction_id
        order_manager = getUtility( IOrderManager )
        order = order_manager.get(order_id)
        if order is None:
            raise PXPayException("Order id " + order_id + " not found")
        if self.determine_success(response_message):
            order.finance_workflow.fireTransition('charge-charging')
            self.destroy_cart()
        else:
            order.finance_workflow.fireTransition('decline-charging')
        next_url = self.get_next_url(order)
        self.request.response.redirect(next_url)

    def determine_success(self, response_message):
        """
        Wrap up some logic to reconcile DPS transaction success in terms
        of whether we are in Test mode or not - fraud protection
        """
        if response_message.transaction_successful:
            # Apparently all successful.
            # One last check. This protects us from one type of fraud, which the
            # the PXPay interface effectively exposes us to, otherwise...
            if response_message.transaction_card_number == RETURNED_TEST_CARD_NUMBER:
                # Someone has used the Test CC number...
                if self.processor_options.PxPayServerType != TEST_SERVER_TYPE:
                    # ...and has attempted to defraud us.
                    log.info("FRAUD attempt - use of Test CC number in non-test environment: '%s'" % response_message)
                    return False
            # Otherwise all is normal and the transaction was successful 
            return True
        else:
            return False

    def destroy_cart(self):
        """
        time to destroy the cart
        """
        getUtility( IShoppingCartUtility ).destroy( self.context )


    def get_next_url(self, order):
        state = order.finance_state
        f_states = workflow_states.order.finance
        base_url = '/'.join((self.site_root.absolute_url(),
                             '@@getpaid-order',
                             order.order_id))
        if not 'http://' in base_url:
            base_url = base_url.replace("https://", "http://")

        if state in (f_states.CANCELLED,
                     f_states.CANCELLED_BY_PROCESSOR,
                     f_states.PAYMENT_DECLINED):
            return base_url + '/@@getpaid-cancelled-declined'

        if state in (f_states.CHARGEABLE,
                     f_states.CHARGING,
                     f_states.REVIEWING,
                     f_states.CHARGED):
            return base_url + '/@@getpaid-thank-you?order_id=%s&finance_state=%s' %(order.order_id, state)
