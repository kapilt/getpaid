A lot of documentation has been ported to plone.org/products/getpaid/documentation . Where that has happened, I am removing the links here. Please use this as a place to outline what is needed and work on drafting it.

## General Questions ##

  * How does a session-based cart work?
  * What happens when a user places an order on my site (offline vs online order completion)?

## Using the Product ##

  * How do I set up a payment processor in GetPaid? [Answer](SetUpPaymentProcessorDoc.md)
  * How do I add a donation to the site? [Answer](AddDonationDoc.md)
  * How do I add a product to the site?
  * What is the difference between adding a donation to a site versus making something buyable?
  * How do I manage my orders?
  * How do I make a content object payable? Not payable? [Answer](MakeObjectPayableDoc.md)

## Customization and Extension ##

  * How should I make customizations to the product? [Answer](CustomizationsBestPracticesDoc.md)
  * How do I build an extension of the product?
  * How do I make my custom content type integrate with the product (so I can make it buyable)? [Answer](CustomContentTypeDevelopmentDoc.md)
  * How do I make a donation appear in a portlet vs within the page content?
  * How do I make an "Add to Cart" button appear in the body of the content on my site?
  * How do I change the "Add to Cart" text or make it a button?

> _Not implemented yet_
  * How do I configure my currency?
  * How do I set up my shipping information?
  * How do I create a category and add products to the category?

## Payment Processor Questions ##

  * When will payment processor <my favorite processor> be supported?
  * How do I integrate payment processor <my processor>?
  * Authorize.net:
    * How do I get a test or dev account? [Submit request form](http://developer.authorize.net/support/)
    * Are there test credit card numbers I can use? [See authnet doc](http://developer.authorize.net/faqs/#7429)
    * How do I get an authorize.net account?
    * How do I get my merchant ID and transaction key? [See authnet doc](http://developer.authorize.net/faqs/#7423)
    * How do I set up my gateway to accept international credit cards? [Answer](AcceptInternationalCardsDoc.md)

## Developer Concerns ##

  * What unit tests are available?
  * How do I write an adapter for a new payment processor?

