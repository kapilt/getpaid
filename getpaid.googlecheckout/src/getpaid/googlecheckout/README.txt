Introduction
============

`Google Checkout`_ integration with GetPaid.


Status
======

Attempt to get minimal integration with Google Checkout using the
Checkout API.

- The GetPaid checkout wizard is completely replaced with Google
  Checkout.

- The GetPaid order manager is not integrated with Google Checkout.
  Google Checkout includes its own order management functionality.
  Although Google Checkout does have a rich enough API that these two
  could be integrated with each other.

- The contents of the shopping cart are emptied just before
  redirecting the browser to Google Checkout. This is done by making
  use of "Option B - Submit a Server-to-Server Checkout API Request".
  (It would be better to empty the shopping cart only once the sale
  has been completed. This could be integrated using Google Checkout
  Notification API.)

- Makes use of zcml overrides to integrate with GetPaid. This is a
  sign that GetPaid is not yet sufficiently plugable to support this
  kind of processor.


Todo
====

- Need to override the cart display and cart portlet to use the google
  checkout buttons.

- Update locales.


Demo
====

Use getpaid.buildout to create your own demo of this integration.
Uncomment the various googlecheckout variable substitutions throughout
buildout.cfg::

    ${googlecheckout:develop}
    ${googlecheckout:eggs}
    ${googlecheckout:zcml}

Create a merchant account in the Google Checkout Sandbox service. See
step 1 of `Getting Startted with Google Checkout`_.

Configure the Google Checkout processor in GetPaid with the given
Merchant ID and Merchant Key.


.. _Google Checkout:
   http://code.google.com/apis/checkout/developer/index.html

.. _Getting Started with Google Checkout:
   http://code.google.com/apis/checkout/developer/index.html#integration_overview
