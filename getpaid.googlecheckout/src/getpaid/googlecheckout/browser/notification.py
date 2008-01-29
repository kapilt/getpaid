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

from Products.Five.browser import BrowserView
from getpaid.core.interfaces import IPaymentProcessor
from getpaid.core.interfaces import IShoppingCartUtility
from zope.component import getAdapter
from zope.component import getUtility
from zExceptions import Unauthorized
from getpaid.googlecheckout.interfaces import IGoogleCheckoutOptions


class Notification(BrowserView):

    def validate_authorization(self):
        auth = self.request._authUserPW()
        if auth is None:
            raise Unauthorized
        else:
            name, password = auth
            options = IGoogleCheckoutOptions(self.context)
            if name != options.merchant_id or password != options.merchant_key:
                raise Unauthorized

    def __call__(self):
        self.validate_authorization()
        self.request.stdin.seek(0)
        xml = self.request.stdin.read()
        processor = getAdapter(self.context, IPaymentProcessor,
                               'Google Checkout')
        return processor.notify(xml)

