"""
$Id$
"""

import hmac, sha, base64

from zope.interface import implements
from zope import component
from zope.documenttemplate import HTML as Template
from zope.app.annotation.interfaces import IAnnotations
from getpaid.core.options import PersistentOptions

import interfaces

checkout_xml = Template("""\
<?xml version="1.0" encoding="UTF-8"?>
<checkout-shopping-cart xmlns="http://checkout.google.com/schema/2">
  <shopping-cart>
    <items>
      <dtml-in items>
      <item>
        <item-name><dtml-var "item.name"></item-name>
        <item-description><dtml-var "item.description"></item-description>
        <unit-price currency="USD"><dtml-var "item.cost"></unit-price>
        <quantity><dtml-var "item.quantity"></quantity>
      </item>
      </dtml-in>
    </items>
  </shopping-cart>
  <checkout-flow-support>
    <merchant-checkout-flow-support>
    </merchant-checkout-flow-support>
  </checkout-flow-support>
</checkout-shopping-cart>
""")

GoogleCheckoutOptions = PersistentOptions.wire("GoogleCheckoutOptions",
                                               "getpaid.googlecheckout",
                                               interfaces.IGoogleCheckoutOptions )

class GoogleCheckoutProcessor( object ):
   
    implements( interfaces.IGoogleCheckoutProcessor )

    options_interface = interfaces.IGoogleCheckoutOptions

    def __init__( self, context ):
        self.context = context

    def setup( self, cart ):
        options = interfaces.IGoogleCheckoutOptions( self.context )
        xml_order = checkout_xml( items=cart.values() )
        signature = hmac.new( options.merchant_key, xml_order, digestmod=sha ).digest()
        
        self.encoded_signature = base64.encodestring( signature )
        self.encoded_order = base64.encodestring( xml_order )
        self.post_url = ""



                 

        
        

