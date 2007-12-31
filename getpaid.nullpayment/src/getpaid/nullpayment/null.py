# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

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
