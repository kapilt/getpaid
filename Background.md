Plone Ecommerce and Payment Process Current State

In a word: sad. There is no "state of the art", but instead a few points of light in a vacuum. However, momentum is building and we will be changing that! The following page is designed to give a greater background on commerce in Plone. These notes were first started based on the "Plone e-commerce BOF" at Plone Conference 2006.

## User scenarios to be addressed: ##

STORE: Beyond having a simple single item payment processing, site owners with many objects need to be able to handle store functions. They need to be able to let users browse shopping areas, collect items in a cart, assign relevant taxes and shipping charges, collect and manage billing information, and handle payment processing and reporting.

NGO: Non-profit use of Plone has exploded over the last few years. All non-profits have a common need - raising money. Non-profits need to be able to use the web site to handle donation processing, as well as gathering information about donors and providing them information they need (ie in case of tax deductible donation in US, a letter for IRS). Jon Stahl has written up some detail on this in the ((Wish List)).

PREMIUM CONTENT REPOSITORIES: Users need to be able to purchase subscriptions to access premium content, i.e. articles. This scenario follows a similar process as purchasing a tangible good, except that it sets special permissions for subscribed users to allow them to access the premium content.

EVENTS: Plone manages information great, including event information. But people who run events have to be able to handle registrations. Registration is about information collection, connecting that to payment processing, and having a real-time record that can be used to manage registration (ie see how many people are registered at any given time, who has paid, etc).  (Deferred)

## Attempting Plone Solutions ##

Some attempts at making payment processing and commerce possible in Plone have taken place. Most of these are either buggy, not maintained, or not very useful. But better than nothing! A quick synopsis:

  * PayPal: Probably the most commonly used tool for payment processing and simple stores in Plone. Unfortunately most of the products haven't kept up with the evolution of Plone. Products for this include: SimpleCartItem (stable, Plone 2.1, 2.5) PlonePayPal (stable, Plone 2.0) CMFPaypalHelper (stable, Plone 2.0). A newer product, released 1/07, called LetsPay is another paypal product (in beta state).
    1. Plone Mall: No stable release; After a long time with no releases (since 6/2005), there was a Feb 2007 release (1.1 Alpha) to bring PloneMall into 2.5 technologies! Read ((Kapil's Thoughts On PloneMall)). Apparently there was a sprint to make it Plone 2.1-compatible earlier as well. Most recent annecdotal evidence is that it is now obsolete given framework changes in Plone, though haven't had any reports as to what that means for the recent release. See product page (note: the plonemall.com web site is not maintained or official! Use the product page on plone.org linked here). This product represented the merging of several early attempts at plone ecommerce, including PloneShop and other now-defunct projects. It was intended as a framework, not an out-of-the-box store product, and leverages UML to generate code.�
    1. Spawn of PloneMall: There's been some discussion on the collective-commerce list: http://sourceforge.net/mailarchive/forum.php?forum=collective-commerce  On that list, Sam Stainsby also indicated that he is about to release a non-PloneMall ecommerce framework that he developed for a client, having rejected PloneMall as a starting point.�  This may represent an interesting new starting point.

  * Shopping Cart: Inventory Builder Cart is an addon product to a catalog product that allows you to create carts. No stable release. See product page.


http://plone.org/products/simplecartitem
http://zope.org/Members/bowerymarc/PlonePayPal
http://plone.org/products/cmfpaypalhelper
http://plone.org/products/letspay
http://plone.org/products/plonemall
http://sourceforge.net/mailarchive/forum.php?thread_id=31628908&forum_id=33456

## Other Ways to Make Money with Plone ##

Though direct payment integration is difficult, other opportunities exist for making money in Plone.

  * Amazon Store: Anyone can become an Amazon Associate and thus earn money through the affiliate marketing program. ATAmazon is a Plone product (for 2.1) that integrates metadata from Amazon.com for books displayed on your site.
  * Ad referrals (Google AdSense, Yahoo!, etc): Google Adwords have become prevalent around the internet, and given the revenue sharing model through AdSense, represent a way site owners can earn money from traffic on the site. Other search engines and advertisers do it too...
  * Banner ads: You can add a portlet to manage banner ads that are either from within your site or coming in from an external service (a la adwords or other). Existing products to help you manage banner ads on your site include: KBannerAd (for Plone 2.1, allows you to set weights and numbers of clicks for images or Flash ads); PromoEngine (for Plone 2.1, alpha state, allows you to manage text, images, and links of ads in different areas of site.�  "There has been a lot of work on the trunk (new release soon) of this product that allows flash ads and kupu based ads for more flexibility" - claytron); PloneBannerManager (Plone 2.0, mysql backend, allowed for tracking, weights, images and text ads)
  * Other affiliate programs: Netflix, GreenHome , etc (add as you see important)


http://affiliate-program.amazon.com/gp/associates/join
http://plone.org/products/atamazon
https://www.google.com/adsense/?sourceid=aso&subid=ww-en_US-et-awhome&medium=link&hl=en_US
http://plone.org/products/kbannerad
http://plone.org/products/promoengine
http://www.contentmanagementsoftware.info/plone/PloneBannerManager
http://www.netflix.com/Affiliates?nfse=Y
http://www.greenhome.com/about/affiliates/

Opportunities from current products or features that could also be used include

  * Event registration: Several attempts to include event registration exist. Jon Stahl also outlines how these could integrate payment processing in the WishList
  * Job Listings: There is a beta product for creating a Job Board on a Plone site. Also, there are third-party products like JobThread that can be integrated.

http://www.jobthread.com/

## Non-Plone, but Related, Examples ##

  * Zope: Bizar shop is a hosted zope-based ecommerce shop. Looks like decent marketing info (video of features). Any chance we can get pieces of that for processing? I think we can also check out the video to get ideas for our interfaces.
  * Django: Satchmo is a django-based open source ecommerce shop system. Maybe we can get payment processor libraries??? See trac page also.

http://www.bizarshop.com.au/products/bizar_shop_specs.html
http://www.bizarsoftware.com.au/resource_centre/tour.html
http://www.satchmoproject.com/
http://satchmo.python-hosting.com/wiki

## How People Really Did It ##

Some people get around the problem by re-evaluating its priority. For example, use a form that collects and encrypts data that is sent to a staff member securely for processing (ie non-real-time).

Most people who have to implement Plone with payment/donation processing do it with PayPal.

Most people who have to implement Plone with an ecommerce/store/shopping cart do it by adding another software alongside of Plone. For example:

  * Snow Leopard Trust Plone Site and the visually-integrated ZenCart commerce system by OneNW
  * Plone Solutions made a Paynet (Norway) integrated Plone product
  * Integrating actual PayPal API: SpankyFromBRC (Tom Kapanka) and Sean McCormick worked on developing pyPayPal, a set of modules that both communicated with PayPal's SOAP-based API, and de/serialized these communiques into Python objects.�  They also worked on PlonePayPal, the Plone side of this process to expose the pyPayPal objects to the Archetypes layer of Plone. One of the key features of both of these projects was the idea that generation of each of the pieces should be programmatic.�  The PayPal API, expressed as SOAP-based WDSL files provided all of the necessary descriptors to build the python objects for the transaction, and the python objects' requirements determine what an Archetype schema to satisfy this should look like.�  The goal was "one click" generation of the entire chain of critical pieces for the complete round trip of the entire PayPal "Website Pro Payments" system.�  This work was not satisfactorily completed due to problems with the Python/SOAP processor (ZSI), issues with PayPal's WDSL formats, and lack of funding.
  * Integrating Paypal API: Fundable.org is a Plone-based site with Paypal integrated, though not sure how it is done (probably custom API integration).
  * Bizar Shop: A zope product created by an Australian company that features a full ecommerce store with impressive functionality. Code not made available or mentioned on the site.
  * (insert other examples)

http://www.snowleopard.org/
http://www.snowleopard.org/shop/
http://fundable.org/
http://www.bizarsoftware.com.au/

Systems integrated include OSCommerce, ZenCart, J2EE solutions, as well as zwarehouse and Joomla's VirtueMart.