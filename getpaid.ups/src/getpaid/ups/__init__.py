"""
"""
from getpaid.core.options import PersistentOptions
import interfaces

UPSRateServiceOptions = PersistentOptions.wire("UPSRateServiceOptions",
                                               "getpaid.ups",
                                               interfaces.IUPSRateServiceOptions )


