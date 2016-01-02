# Proposals & Requirements for integrating store functionality into GetPaid #

While it's been decided that store functionality will not be included in the 0.3 release of GetPaid, it's become clear that there are plenty of people interested in getting it added in there.  This page will serve as a place to discuss and hopefully come to a consensus about the specification of required features.

# Preliminary Work #

  * Catalog of buyables ([Issue #70](https://code.google.com/p/getpaid/issues/detail?id=#70)): needs to be implemented and upgrade path created, tested leveraging the upgrade framework.

  * Refactor checkout wizard: the wizard needs to be made much more customizable, flexible. Refactoring was originally discussed as related to the NaplesSprint.

  * Make shopping cart persistent: this has been discussed in terms of eliminating problems with five.intid, but also as a way to make more flexible cart storage. We also offer users the convenience of saved information on carts.

  * Save and reuse user address info: Currently a user on the site would have to enter their information every time they checked out. We should (a) associate the address information with the user (save is the right word?) and (b) let them use that information again (ie if they are checking out, their info is pre-populated. An advanced user story here would allow the user to have multiple addresses and be able to choose from them.

  * Advanced order management: Current order management is a bit clunky. For more store features, site admins need to be able to interact with the items in the cart/order for fulfillment (anyone know specs on this?!). Some components:
    * Admin also needs user-friendly way to interact with the workflow states (financial and fulfillment). I have a feeling this last point involves [Issue #29](https://code.google.com/p/getpaid/issues/detail?id=#29).
    * Capturing more of the vital checkout info as suggested in [issue #116](https://code.google.com/p/getpaid/issues/detail?id=#116) .
    * Persisting the order processor id and making that available in search interface, as per [issue #117](https://code.google.com/p/getpaid/issues/detail?id=#117).
    * Report/search screen for querying the items ordered in the site, [issue #120](https://code.google.com/p/getpaid/issues/detail?id=#120)

# Usability / UI #

  * Progress indicator on checkout ([Issue #58](https://code.google.com/p/getpaid/issues/detail?id=#58)): Please add an indicator of where we are in the checkout process. This has to be somewhat flexible given the flexibility being added in checkout refactoring (see above), but should at least ship with something that helps orient the user.

  * Order template: we need to improve the order templates so they show the useful info! Currently (though it is filed in [issue #150](https://code.google.com/p/getpaid/issues/detail?id=#150)), the order for the user and admin doesn't show the address of orderer. This should be formatted appropriately. Also, we should add the print option onto the order, so the user can print the order simply. Additionally, displays of the history on an order should be more human-readable.

  * [Issue #30](https://code.google.com/p/getpaid/issues/detail?id=#30) (though not sure what it is actually referring to...)

  * Update countries list ([Issue #86](https://code.google.com/p/getpaid/issues/detail?id=#86))

  * Setup section UI improvments: [Issue #95](https://code.google.com/p/getpaid/issues/detail?id=#95).

  * AJAX to improve usability! [Issue #32](https://code.google.com/p/getpaid/issues/detail?id=#32). [Issue #20](https://code.google.com/p/getpaid/issues/detail?id=#20)

  * System URL cleanup, [issue #103](https://code.google.com/p/getpaid/issues/detail?id=#103)

  * Inline documentation, [issue #113](https://code.google.com/p/getpaid/issues/detail?id=#113)

  * Checkout review cart gets edit link, #114 . Gets address edit link, [issue #119](https://code.google.com/p/getpaid/issues/detail?id=#119).

  * Billing contact email address captured and posted to pay processor, [issue #121](https://code.google.com/p/getpaid/issues/detail?id=#121)

  * Portlet cleanup, [issue #122](https://code.google.com/p/getpaid/issues/detail?id=#122)

  * Improve system message, [issue #128](https://code.google.com/p/getpaid/issues/detail?id=#128)

  * Deal with multiple delivery type overlap, [issue #131](https://code.google.com/p/getpaid/issues/detail?id=#131)

  * Get better i18n coverage, see [issue #136](https://code.google.com/p/getpaid/issues/detail?id=#136)

  * Dedicated order management area, outside plone setup, see [issue #138](https://code.google.com/p/getpaid/issues/detail?id=#138). Also could be associated with a role or permission, as per [issue #125](https://code.google.com/p/getpaid/issues/detail?id=#125)

  * Cart quantity change improvement, [issue #144](https://code.google.com/p/getpaid/issues/detail?id=#144)

  * Consistent column names and orders, [issue #155](https://code.google.com/p/getpaid/issues/detail?id=#155)

# Core Features #
  * Catalog views.  A store needs to have a nice way to view/browse the items for sale.  I'm not sure what the best way to go about this will be, since the pieces of content on sale can be anything.  But a view/listing for a folder with shippable (or just buyable?) items in it would be nice.  Each item could be added to the cart from this list view, as well as from the page for the item itself, display it's price, and if available, show a thumbnail.

  * Product Categories ([Issue #21](https://code.google.com/p/getpaid/issues/detail?id=#21)): a way of categorizing the buyable items in the site. This should be a criteria that SmartFolders could be used to generate collections with.

  * Product content type? Should we ship our own product content type to make the store story a bit easier to manage?

# Taxes #
This is detailed elsewhere in the wiki, and will need to be implemented.

> _Who is interested in putting work into this? This is a big hairy mess, imho. I don't know how it would be implemented. Surely someone wants it though and can drive it!_ cjj

The way this is done in PayPal is you manually add a sales tax item for each of the locations you need to collect taxes from.  You have the option (check box) to collect taxes on the shipping/handling costs as well.  This makes sense, at least in the US, since internet stores only need to collect tax for states that they have a physical presence in.

We might be able to add this functionality in a reasonably straightforward way with DataGridField - http://plone.org/products/datagridfield.  I was just looking at SimpleCartItem - http://plone.org/products/simplecartitem - which uses DGF to add options (different colors/sizes, etc.) for a store item.  I haven't looked at the code for it, but it seems like the functionality is pretty well aligned with this need.  Unfortunately, it currently currently claims to rely on JavaScript without graceful degradation, so perhaps it's not all that interesting.

# Fulfillment Workflow #
Though perhaps not universal, one common workflow is to have the payment authorized on checkout and then the capture happens when the site admin either fulfills the order or captures the payment manually (_note: by regulation, authorizations are only good for up to 30 days_). How should we support the shipping workflow? Is there a way we can offer through-the-web configurable workflow setups?

See one idea at [Issue #115](https://code.google.com/p/getpaid/issues/detail?id=#115)

# Payment processors #

It would be really nice to be able to integrate with something like Google Checkout ([Issue #5](https://code.google.com/p/getpaid/issues/detail?id=#5)), which supports fulfillment workflow for free.  With PayPal, the free service doesn't support this - you need to pass the customer off to the PayPal site.  GoogleCheckout also integrates nicely with AdWords, which lots of people use to track their online advertising.

# Shipping Services #
It makes tons of sense to integrate with a shipping service to fetch the current shipping rates, as is already detailed elsewhere in the wiki.  A fair amount of work has been done to integrate with UPS.  These can be implemented much the same way the payment processors are implemented - one screen to select the service you want, and then another screen to configure the details for that service.

Each shipping service should also offer store admins the possibility of marking up the prices returned from UPS (or wherever) to account for handling charges.  This system can either be a percentage with a ceiling, or a flat rate (perhaps other configs as well).

Integrating with the shipping label generation for a given service will be important.  For UPS, a desktop app creates shipping labels and assigns a tracking number.  There are reasonable CSV import/export options for this software to get these values in and out of PGP.  This has the added advantage that we can then provide users a quick link to tracking info for their package - in the case of UPS, we'd just link to their tracking service with the tracking number in the URL, I believe.

What is the story for integration at this level for other shipping services?  FedEx?  DHL?  USPS?

# Other Store Features of Interest #

  * Saved order: For sites where users order the same thing frequently, a saved order system

  * InventoryManagement: Site admin would be able to enter the number of an item on hand. When an item is purchased, the number goes down correspondingly (see [issue #100](https://code.google.com/p/getpaid/issues/detail?id=#100)). Advanced version of this story tracks the history of the number on hand, and ties into reporting.

  * Quantity-based price breaks.  Need to be able to specify a percentage discount for orders of quantities in a certain range.  ie, 0-9: 0%, 10-49: 5%, 50-99: 10% etc.

  * Time-based discounts/sales.  Mark an item down a certain percentage or specify a new price, and set a date for the sale to expire at which point the discount is removed automatically.

  * Gift certificates?  I had a customer ask me if we had these, and it struck me that I had no idea how this would work.  It's a nice idea, though!

  * Multiple currencies ([issue #85](https://code.google.com/p/getpaid/issues/detail?id=#85) is placeholder for this...still need better specs)

  * Multiple item add to cart, [issue #123](https://code.google.com/p/getpaid/issues/detail?id=#123). This may also be associated with a desire to give differing pricing based on quantity purchased.