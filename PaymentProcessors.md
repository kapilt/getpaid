Related Information
See the user story for site admins setting up payment processor: http://www.openplans.org/projects/plonecommerce/set-up-payment-processor

Outline:
Current Work | Recurring Billing | Code Assets | API Links | Pay Processors Overview

Current work:

  * 2Checkout will be done (Richard needs this), which is very international
  * Interest in Authorize.net also, which is what Kapil is planning on next processor to implement.
  * Some work in place is with Google Checkout (only usable for US), but this is on hold to have international, in-site processor option

  * TrustCommerce may already be available and be provided soon (they are very open source and have Python coders; NICE API; load-balancing; store user info on their site, not yours, etc.)
  * Let's get 3-4 processors to have a few options, document learnings, etc.

Recurring Billing

Not all processors support recurring payments; we can't do if processor doesn't support it...

Processors that support recurring payments:

  * 2checkout works well, automatically sends out notice
  * Authorize.net supports recurring billing, but for an extra fee (currently $10/m)
  * Paypal (standard and Pro)

Interface should ensure user understands that their pay processor will dictate if they can use that aspect of the product.

Payment Processors Code Assets

Authorize.net:

  * Kapil mentions a python tool for authorize.net processor (http://svn.zope.org/zc.authorizedotnet/)
  * Authorize.net (pure python library) svn://svn.zope.org/repos/main/zc.authorizedotnet - http://svn.zope.org/zc.authorizedotnet/trunk (from Zope Corp)
  * Authorize.net (cmf tool that posts and gets info via api + layer of plonemall integration): https://svn.sixfeetup.com/svn/public/SFUAuthorizeNetPlugin/trunk/

PayFloPro:

  * PayFloPro integration: see PremiumMembership product in collective from Nate

2Checkout:

  * ???((2CheckOut))

Trust Commerce:

  * Trust Commerce cmf tool: https://agendaless.com/Members/tseaver/software/trustcommerce/trustcommerce-1.0/  (from Tres and Chris McDonough) This product provides a ZMI-manageable tool as a facade for the API exported by TrustCommerce's tclink Python library.

PayPal

  * Paypal tool from 6ftup to post the paypal transaction data to Plone site: https://svn.sixfeetup.com/svn/public/PaypalManager/trunk/
  * Note from a friend who recently implemented Paypal on a major ecommerce site: "akamai is a caching server that serves up pages if your down, but they have had less than stellar performance, so we've been having to tweak things here and there because of our old backend." Not sure if this might be something we will have to think about. (Veda)

GoogleCheckout:

  * GoogleCheckout integration worked on by Kapil, in GetPaid product

Protx:

  * Zprotx (http://plone.org/products/zprotx ) is a Python framework to integrate with Protx VSP Form credit card payment service (http://www.protx.com/). It fills the gap because Protx doesn't support Python. It is build as a Zope2 product. It can be used in Plone or other Zope systems.

Other stuff can be found in zwarehouse:

  * Great collection of processors can be used. Find them in the code.


Links to APIs for Developers
For each kind of payment processor, the necessary fields should be determined and integrated into the appropriate interface in GetPaid.
Authorize.net:
Note: Developer documentation: http://developer.authorize.net/

PayFlowPro
Developer documentation: https://www.paypal.com/cgi-bin/webscr?cmd=_payflow-about-gateway-outside

Google Checkout
Developer documentation: http://code.google.com/apis/checkout/

2Checkout
https://support.2co.com/deskpro/faq.php?do=article&articleid=61
https://support.2co.com/deskpro/faq.php?categoryid=25

ZenCart
http://www.zen-cart.com/wiki/index.php/Developers_API_Tutorials

Paypal
Developer documentation: https://www.paypal.com/cgi-bin/webscr?cmd=_payflow-about-gateway-outside

PayPal Integration Guide. See https://www.paypal.com/IntegrationCenter/ic_documentation.html (first two documents especially)

NOVA/viaKLIX
https://www2.viaklix.com/admin/support/default.asp

General Payment Processor Overview

Zwork, who developed plonemallpayment, and Ofer shared the following information:

There are two main types of payment processors:

  1. Standard payment processing:�  the payment processor itself collects information from the shopper and then calls the payment service's backend. Has the advantage that the customer stays in your shop, but it is more work to develop + the merhant's shop must have https + a certificate
> 2. Lighweight redirecting payment processors that redirect the customer to the payment provider's site from which you then get redirected back (e.g. paypal). Processors are easily to develop, and quicker to set up for a shop

Both types of payment processor consist of 3 parts:

  1. The payment setting (a user-editable in our case Archetype object) that stores the payment processors settings like merchant code, transaction code etc
> 2. The processor itself
> 3. The payment information (a persistent object that has the workflow (processing - success - failed - aborted)

There are currently a set of processors in plonemall:

  * paypal, (type 2)
  * qenta (an austrian cc provider, type 2) and
  * authorize.net (type 1), (from 6ftup)
  * and cash on delivery.
  * Purchase Order (see 6ftup)