"""

notes on error handling, if we haven't talked to the processor then raise an exception,
else return an error message so higher levels can interpret/record/notify user/etc.

$Id: $
"""

from zope import interface

from getpaid.core import interfaces

from interfaces import IPaymentechOptions


class PaymentechAdapter(object):
    interface.implements(interfaces.IPaymentProcessor)

    options_interface = IPaymentechOptions

    def __init__(self, context):
        self.context = context

    def authorize(self, order, payment):
        pass

    def capture(self, order, amount):
        pass
    
    def refund( self, order, amount ):
        pass
