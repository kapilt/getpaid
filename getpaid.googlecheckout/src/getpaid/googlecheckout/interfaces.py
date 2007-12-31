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
$Id: interfaces.py 10 2007-05-10 15:34:29Z kapilt $
"""

from getpaid.core import interfaces
from zope import schema

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.googlecheckout')

class IGoogleCheckoutProcessor( interfaces.IPaymentProcessor ):
    """
    Google Checkout Processor
    """

class IGoogleCheckoutOptions( interfaces.IPaymentProcessorOptions ):
    """
    Google Checkout Options
    """
    server_url = schema.Choice(
        title = _(u"Google Checkout Server URL"),
        values = ( "Sandbox", "Production" ),
        )

    merchant_id = schema.ASCIILine( title = _(u"Merchant Id"))
    merchant_key = schema.ASCIILine( title = _(u"Merchant Key"))
