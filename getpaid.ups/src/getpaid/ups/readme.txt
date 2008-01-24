getpaid ups
-----------

This modules provides an integration package for

Usage
-----

First we need to create an instance of a UPS rating utility and configure 
it with our UPS Account Information.

   >>> from getpaid.ups.rates import UPSRateService
   >>> ups = UPSRateService()
   >>> ups.username = UPS_USERNAME
   >>> ups.password = UPS_PASSWORD
   >>> ups.access_key = UPS_ACCESS_KEY

Origin Information
==================

We also need to configure our store to setup a default origin location for
packages to originate from. for brevity, we've done configured the store 
settings in the test setup with a san francisco address.

Creating an Order to Ship
=========================

Let's create an order with some items we'd like to have shipped.

  >>> from getpaid.core import order, item, cart
  >>> myorder = order.Order()
  >>> myorder.shopping_cart = mycart =cart.ShoppingCart()
  >>> mycart
  
Destination Information
=======================

We need some additional information for an order to successfully process it:

  >>> from getpaid.core import payment


  
and of course a place to ship to
  
  >>> ship_address = payment.ShippingAddress()
  >>> ship_address.ship_first_line = '1418 W Street NW'
  >>> ship_address.ship_city = 'Washington'
  >>> ship_address.ship_state = "DC"
  >>> ship_address.ship_country = "US"
  >>> ship_address.ship_postal_code = '20009'  
  >>> myorder.shipping_address = ship_address

Getting Shipping Options
========================

Now we can query UPS to find out the various services, delivery windows, and
 prices that UPS can offer for transit.

  >>> methods = ups.getRates( myorder )
  >>> 
  


