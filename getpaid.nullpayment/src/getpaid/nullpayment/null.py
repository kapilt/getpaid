"""
$Id$
"""

from zope import interface
from getpaid.core import interfaces, options
from interfaces import INullPaymentOptions
from zope.app.annotation.interfaces import IAnnotations

NullPaymentOptions = options.PersistentOptions.wire(
    "NullPaymentOptions",
    "getpaid.nullpayment",
    INullPaymentOptions
    )

LAST_FOUR = "getpaid.null.cc_last_four"

class NullPaymentAdapter( object ):

    interface.implements( interfaces.IPaymentProcessor )

    options_interface = INullPaymentOptions

    def __init__( self, context ):
        self.context = context
        self.settings = INullPaymentOptions( self.context )
        
    def authorize( self, order, payment ):
        if self.settings.allow_authorization == u'allow_authorization':
            annotation = IAnnotations( order )
            annotation[ LAST_FOUR ] = payment.credit_card[-4:]
            return interfaces.keys.results_success
        return "Authorization Failed"

    def capture( self, order, amount ):
        if self.settings.allow_capture == u'allow_capture':
            return interfaces.keys.results_success
        return "Capture Failed"

    def refund( self, order, amount ):
        if self.settings.allow_refunds == u'allow_refund':
            return interfaces.keys.results_success
        return "Refund Failed"
