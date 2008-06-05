"""

notes on error handling, if we haven't talked to the processor then raise an exception,
else return an error message so higher levels can interpret/record/notify user/etc.

$Id: $
"""

from time import gmtime, strftime

from zope import interface
from zope.component import getUtility, getAdapter
from zope.app.annotation.interfaces import IAnnotations

from zc.authorizedotnet.processing import CcProcessor
from zc.authorizedotnet.subscription import ARBProcessor

from getpaid.core import interfaces

from interfaces import IAuthorizeNetOptions

SUCCESS = 'approved'

# needed for refunds
LAST_FOUR = "getpaid.authorizedotnet.cc_last_four"

APPROVAL_KEY = "getpaid.authorizedotnet.approval_code"

class AuthorizeNetAdapter(object):
    interface.implements( interfaces.IPaymentProcessor )

    options_interface = IAuthorizeNetOptions

    _sites = dict(
        Production = "secure.authorize.net:443",
        Test = "test.authorize.net:443"
        )
    _arb_sites = dict(
        Production = "api.authorize.net:443",
        Test = "apitest.authorize.net:443"
        )

    def __init__(self, context):
        self.context = context

    def authorize(self, order, payment):

        if interfaces.IRecurrentOrder.providedBy(order):
            return self.arb_create(order, payment)

        billing = order.billing_address
        amount = order.getTotalPrice()
        contact = order.contact_information
        order_id = order.getOrderId()
        contact_fields = 'Contact Name: ' + contact.name + ';  Contact Phone: ' + contact.phone_number  + ';  Contact Email: ' + contact.email

        options = dict(
            amount = str(amount),
            card_num = payment.credit_card,
            last_name = payment.name_on_card,
            phone     = payment.phone_number,
            exp_date = payment.cc_expiration.strftime('%m%y'),
            address = billing.bill_first_line,
            city = billing.bill_city,
            state = billing.bill_state,
            zip = billing.bill_postal_code,
            invoice_num = order_id,
            description = contact_fields
            )


        result = self.processor.authorize( **options )

        # result.response may be
        # - approved
        # - error
        # - declined
        # - held for review
        #
        # Other result fields:
        #   result.response_reason
        #   result.approval_code
        #   result.trans_id

        if result.response == SUCCESS:
            annotation = IAnnotations( order )
            annotation[ interfaces.keys.processor_txn_id ] = result.trans_id
            annotation[ LAST_FOUR ] = payment.credit_card[-4:]
            annotation[ APPROVAL_KEY ] = result.approval_code
            return interfaces.keys.results_success

        return result.response_reason

    def capture( self, order, amount ):

        if interfaces.IRecurrentOrder.providedBy(order):
            return self.arb_capture(order, amount)

        annotations = IAnnotations( order )
        trans_id = annotations[ interfaces.keys.processor_txn_id ]
        approval_code = annotations[ APPROVAL_KEY ]

        result = self.processor.captureAuthorized(
            amount = str(amount),
            trans_id = trans_id,
            approval_code = approval_code,
            )

        if result.response == SUCCESS:
            annotation = IAnnotations( order )
            if annotation.get( interfaces.keys.capture_amount ) is None:
                annotation[ interfaces.keys.capture_amount ] = amount
            else:
                annotation[ interfaces.keys.capture_amount ] += amount
            return interfaces.keys.results_success

        return result.response_reason

    def refund( self, order, amount ):

        annotations = IAnnotations( order )
        trans_id = annotations[ interfaces.keys.processor_txn_id ]
        last_four = annotations[ LAST_FOUR ]

        result = self.processor.credit(
            amount = str( amount ),
            trans_id = trans_id,
            card_num = last_four
            )

        if result.response == SUCCESS:
            annotation = IAnnotations( order )
            if annotation.get( interfaces.keys.capture_amount ) is not None:
                annotation[ interfaces.keys.capture_amount ] -= amount
            return interfaces.keys.results_success

        return result.response_reason

    def arb_create(self, order, payment):
        """
        """
        item = order.shopping_cart.values()[0]

        billing = order.billing_address
        amount = order.getTotalPrice()
        contact = order.contact_information
        order_id = order.getOrderId()
        contact_fields = 'Contact Name: ' + contact.name + \
                         ';  Contact Phone: ' + contact.phone_number  + \
                         ';  Contact Email: ' + contact.email

        today = strftime("%Y-%m-%d", gmtime())

        options = dict(
            amount = str(amount),
            card_num = payment.credit_card,
            phone     = payment.phone_number,
            exp_date = payment.cc_expiration.strftime('%Y-%m'),
            address = billing.bill_first_line,
            city = billing.bill_city,
            state = billing.bill_state,
            zip = billing.bill_postal_code,
            invoice_num = order_id,
            description = contact_fields,
            total_occurrences=item.total_occurrences,
            trial_occurrences='0',
            start_date=today,
            length=int(float(item.frecuency)),
            unit='months',
            first_name=payment.name_on_card.rsplit(' ', 1)[0],
            last_name=payment.name_on_card.rsplit(' ', 1)[1],
            )

        result = self.arb_processor.create( **options )

        # result.response may be
        # - approved
        # - error
        # - declined
        # - held for review
        #
        # Other result fields:
        #   result.response_reason
        #   result.approval_code
        #   result.trans_id

        if result.response == SUCCESS:
            annotation = IAnnotations( order )
            annotation[ interfaces.keys.processor_txn_id ] = result.trans_id
            annotation[ LAST_FOUR ] = payment.credit_card[-4:]
            annotation[ APPROVAL_KEY ] = result.response_code
            return interfaces.keys.results_success

        return result.response_reason


    def arb_update(self, order):
        """
        """
        annotation = IAnnotations( order )
        options = dict(
            invoice_num = annotation[ interfaces.keys.processor_txn_id ],
            )
        result = self.arb_processor.update( **options )

        # result.response may be
        # - approved
        # - error
        # - declined
        # - held for review
        #
        # Other result fields:
        #   result.response_reason
        #   result.approval_code
        #   result.trans_id

        if result.response == SUCCESS:
            annotation = IAnnotations( order )
            annotation[ LAST_FOUR ] = payment.credit_card[-4:]
            annotation[ APPROVAL_KEY ] = result.response_code
            return interfaces.keys.results_success

        return result.response_reason

    def arb_cancel(self, order):
        """
        """

    def arb_capture( self, order, amount ):

        annotations = IAnnotations( order )
        trans_id = annotations[ interfaces.keys.processor_txn_id ]
        approval_code = annotations[ APPROVAL_KEY ]

        annotation = IAnnotations( order )
        if annotation.get( interfaces.keys.capture_amount ) is None:
            annotation[ interfaces.keys.capture_amount ] = amount
        else:
            annotation[ interfaces.keys.capture_amount ] += amount
        return interfaces.keys.results_success

    @property
    def processor( self ):
        options = IAuthorizeNetOptions(self.context)
        server = self._sites.get(options.server_url)
        cc = CcProcessor(server=server,
                         login=options.merchant_id,
                         key=options.merchant_key)
        return cc

    @property
    def arb_processor( self ):
        options = IAuthorizeNetOptions(self.context)
        server = self._arb_sites.get(options.server_url)
        arbp = ARBProcessor(server=server,
                            login=options.merchant_id,
                            key=options.merchant_key)
        return arbp
