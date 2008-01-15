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

- Includes integration with Google Analytics.


Todo
====

- Need to fix the buildout experience. Currently there is no download
  for PyXML (needed by gchecky) and there are few wrinkles with the
  install of ghcecky.

- Still need to override the cart portlet to use the Google Checkout
  buttons.

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

Configure the Google Checkout processor in GetPaid with the your
Merchant ID and Merchant Key for the sandbox. You'll find these in
"Settings" -> "Integration" of the `Google Checkout Manager`_.

If you want to use this with along with Google Analytics then copy the
following snippet to your Plone site by editing "Site Setup" -> "Site
Settings" -> "JavaScript for web statistics support"::

    <script src="http://www.google-analytics.com/ga.js" type="text/javascript"></script>
    <script src="http://checkout.google.com/files/digital/ga_post.js" type="text/javascript"></script>
    <script type="text/javascript">
    <!--
      var pageTracker = _gat._getTracker("UA-XXXXXXX-X");
      pageTracker._initData();
      pageTracker._trackPageview();
      var checkout_forms = cssQuery('form.googlecheckout');
      for (var i=0; i < checkout_forms.length; i++) {
        checkout_forms[i].onsubmit = function(e) {
          setUrchinInputCode(pageTracker);
        };
      };
    //-->
    </script>

You will need to replace ``UA-XXXXXXX-X`` with your own Google
Analytics account number.


.. _Google Checkout:
   http://code.google.com/apis/checkout/developer/index.html

.. _Getting Started with Google Checkout:
   http://code.google.com/apis/checkout/developer/index.html#integration_overview

.. _Google Checkout Manager:
   http://sandbox.google.com/checkout/sell
