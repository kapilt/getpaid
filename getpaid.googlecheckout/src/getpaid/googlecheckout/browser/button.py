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

from getpaid.googlecheckout.interfaces import IGoogleCheckoutOptions

SANDBOX_URL = 'http://sandbox.google.com/checkout/buttons/checkout.gif?merchant_id=%s&w=160&h=43&style=white&variant=text&loc=%s'
PRODUCTION_URL = 'http://checkout.google.com/buttons/checkout.gif?merchant_id=%s&w=160&h=43&style=white&variant=text&loc=%s'


def checkout_button_url(portal):
    options = IGoogleCheckoutOptions(portal)
    if options.server_url == 'Production':
        url = PRODUCTION_URL
    else:
        url = SANDBOX_URL
    if options.currency == 'GBP':
        loc = 'en_GB'
    else:
        loc = 'en_US'
    return url % (options.merchant_id, loc)
