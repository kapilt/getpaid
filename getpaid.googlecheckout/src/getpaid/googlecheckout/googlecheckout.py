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
"""
from zope import component
from zope import interface

from gchecky.controller import Controller
from gchecky import model as gmodel

import interfaces

class GController(Controller):
    pass

def gcart_item(entry):
    return gmodel.item_t(
        name = entry.name,
        description = entry.description,
        unit_price = gmodel.price_t(
            value = entry.cost,
            currency = 'USD'
            ),
        quantity = entry.quantity
        )

class GCartAdapter(object):
    """
    """
    def __init__(self, context):
        self.context = context
        self.gcart = gmodel.checkout_shopping_cart_t(
            shopping_cart = gmodel.shopping_cart_t(
                items = [gcart_item(entry) for entry in cart.values()]
                )
            )

    def toxml(self):
        return self.gcart.toxml()
        

class GoogleCheckoutProcessor( object ):
   
    interface.implements( interfaces.IGoogleCheckoutProcessor )

    options_interface = interfaces.IGoogleCheckoutOptions

    def __init__( self, context ):
        self.context = context
        self._controller = None

    def getController( self ):
        if self._controller is None:
            options = interfaces.IGoogleCheckoutOptions( self.context )
            self._controller = GController(options.merchant_id,
                                           options.merchant_key,
                                           options.server_url == 'Sandbox')
        return self._controller

    controller = property(getController)

    def cart_post_button( self, cart ):
        prepared = self.controller.prepare_order(GCartAdapter(cart))
        return prepared.html

    def authorize( self, order, payment ):
        pass
