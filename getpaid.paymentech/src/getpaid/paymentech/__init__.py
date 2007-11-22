"""
$Id: $
"""

import interfaces
from getpaid.core.options import PersistentOptions


PaymentechOptions = PersistentOptions.wire(
                           "PaymentechOptions",
                           "getpaid.paymentech",
                           interfaces.IPaymentechOptions)
