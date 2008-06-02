from zope import interface
from getpaid.core import interfaces, options
from interfaces import IPXPayStandardOptions
from zope.app.annotation.interfaces import IAnnotations

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

    def authorize( self, order, payment ):
        pass

    def capture( self, order, amount ):
        pass

    def refund( self, order, amount ):
        pass
