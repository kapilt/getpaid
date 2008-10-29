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

from zope import schema, interface
from getpaid.core import interfaces

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.flatrateshipping')

class IFlatRateShippingSettings( interfaces.IShippingMethodSettings ):
    """
    Flat Rate Shipping Settings
    """
    
    flatrate_option = schema.Choice(
        title=_(u"Shipping Rate Configuration"),
        description = _(u"Choose either a flat rate for all orders, or calculate shipping as a percentage of total order cost."),
        default="Flat Rate",
        values = ( "Flat Rate", "Percentage" ),
        required=True,
        )
    
    flatrate = schema.Float(
        title=_(u"Flat Shipping Rate"),
        description = _(u"If 'Flat Rate' is selected above, this is the rate applied to all orders."),
        default=5.00,
        required=True,
        )
        
    flatrate_percentage = schema.Float(
        title=_(u"Flat Shipping Percentage"),
        description = _(u"If 'Percentage' is selected above, this is the percentage of the total order to charge for shipping."),
        default=10.0,
        required=True,
        )
        
    flatrate_max = schema.Float(
        title=_(u"Max Handling Charge"),
        description = _(u"If 'Percentage' is selected above, the total shipping charge is never greater than this number."),
        default=20.0,
        required=True,
        )



