# Introduction #

GetPaid is a Plone eCommerce framework. GetPaid's architecture favors on-site entry of credit card information. Due to regulatory changes, it is now a common use case to outsource entry of credit card information. This is a proposal to redesign the GetPaid shopping cart and payment processor architecture to better support this, implement the redesign, and rewrite as many extant payment processor modules as is possible within the Google Summer of Code for 2009. This rework is necessary to GetPaid on road to 1.0.


# Details #

## Team ##
  * Derek Richardson (student)
  * Brandon Rhodes (mentor)
  * (add your name here if you'd like to help)

## Deliverables ##

  * PloneGetPaid Version 0.8.0 Alpha with refactored checkout wizard
  * Documentation on upgrading, customization of wizard best practices, and writing a payment processor for the new wizard

## Process ##

  * Start brainstorming desired architecture
  * Get input from GetPaid community
  * Create a branch for the work.
  * Write tests.
  * Refactor the wizard.
  * Watch all tests pass
  * Fork an upgrade process
  * Fork a documentation process
  * Write more tests
  * Refactor payment processors
  * Watch all tests pass
  * Fork another documentation process
  * Merge branch
  * Release!

## Use Cases ##

  * As a site owner, I want to set a payment processor that has my customers enter all their info and credit card information directly on the payment processor's website.
  * As a site owner, I want to capture customer info on my site and then have customer enter credit card info on payment processor's website.
  * As a site owner, I configure how my payment processor should work (all onsite, all offsite, mixed)

_Backlog/Deferred_
  * As a developer, I want to add a field to the checkout wizard
  * As a site owner, I want to configure my payment processor settings to use on-site or off-site entry of credit card information

## Notes about Needs ##

As a site admin, you can configure onsite or offsite payment processors. If you use a payment processor that handles everything within the site, you create a cart, go through the checkout process (enter information, review order + credit card information, confirmation page). However, if you are using an offsite payment processor, the integration is rather clunky because you have to override what GetPaid provides to get the checkout process to move offsite. This can happen at multiple places, depending on preference and the processor being used:
  * Move offsite as soon as someone clicks "Checkout" (from the cart page or cart portlet)
  * Move offsite after the first information collection page in checkout wizard (ie before the review and credit card information).

We understand that to mean that GetPaid needs more pluggable points for the checkout process to make this more flexible and inclusive of different payment processors used and preferences of site owners. The current refactoring aims to enable:
  * Completely onsite (current default)
  * Completely offsite: whole checkout (but GetPaid site knows about order, finance and workflow states based on happenings offsite)
  * Some on-site, some offsite: Gather general user info onsite and then send offsite for credit card entry/authorization and back to site for order confirmation. Getpaid can send cart line item info, cart total value, and user general info (name, address) to processor.


## Architecture ##

_Derek outlining potential solutions_

## Reference ##

  * Payment processor override necessity: http://code.google.com/p/getpaid/issues/detail?id=167
  * Outdated, but close, workflow: http://code.google.com/p/getpaid/wiki/WorkflowGraphviz
  * Notes on GSoC project: http://code.google.com/p/getpaid/wiki/CheckoutRefactoring
  * Payment processors list: https://www.plonegetpaid.com/features
  * Interfaces: http://code.google.com/p/getpaid/source/browse/getpaid.core/trunk/src/getpaid/core/interfaces.py


# History of Notes/Discussions #

## Notes by Brandon Rhodes (from email to Google Group) ##

Derek dropped by this morning and politely pointed out that my goal this
week ought not to have been to just enjoy reading GetPaid code, but to
make specific notes about the technical aspects of his GSOC application.
So I have just looked through the code again to make the following
notes, which are certainly not a design, but might help give the
application the technical heft that it needs.

The getpaid/googlecheckout/README.txt file has two complaints in it that
sound like the source of this GSOC application.  The second one listed
is probably the more minor, so let's tackle that one first:

- Makes use of zcml overrides to integrate with GetPaid. This is a
> sign that GetPaid is not yet sufficiently plugable to support this
> kind of processor.

These overrides are in "override.zcml" files, three of them, in the code
base, which contain the two following substantive overrides:

> <browser:viewlet
> > name="cart-actions"
> > manager="Products.PloneGetPaid.interfaces.IGetPaidCartViewletManager"
> > class=".cart.Actions"
> > permission="zope2.View"
> > weight="20"
> > />


> <plone:portlet
> > name="getpaid.cart"
> > interface="Products.PloneGetPaid.browser.portlets.cart.ICartPortlet"
> > assignment="Products.PloneGetPaid.browser.portlets.cart.Assignment"
> > renderer=".cart.Renderer"
> > addview="Products.PloneGetPaid.browser.portlets.cart.AddForm"
> > />

What's the issue here?  The issue is that, given the way it's currently
designed, you can only have **one** checkout wizard known to the system at
a time.  In other words, you **select** which checkout process you want by
only having **registered** the one you want.

Obviously, this is tawdry.  What we want is to be able to have as many
wizards **registered** at a time as we want, then have some other utility
that **selects** which one should be used.  That way, instead of having to
ZCML-activate something like Google Checkout, you would go to the
checkout wizard selector and select the one you wanted out of the
perhaps very many that were available.

Okay, second issue: the .txt file says:

- The GetPaid order manager is not integrated with Google Checkout.

> Google Checkout includes its own order management functionality.
> Although Google Checkout does have a rich enough API that these two
> could be integrated with each other. And there is already working
> integration with the Google Checkout Notification API.

The details of this are a bit more fuzzy to me, but I think that "order
management" means "keeping up with which things are boxed, which are
shipped, and which have been returned" and so forth.  The idea here
seems to be that, if you use Google Checkout and want to use its order
management functionality, then you have to use Google's site to do so,
because GetPaid can't read back from Google's records about the order's
state to tell you where each order is in the shipping process.

This area is much more of a mystery to me; would integration be done
on-the-fly (pulling from a Google API as you browsed orders in the
GetPaid management backend), or would Google somehow call back to or
alert the Plone site so that content items were paced through a series
of state changes as the order was fulfilled?  I can't tell at this point
exactly what was imagined.

Okay!  That's some bare technical detail; and it almost sounds like
Chris's concern is mostly for the first item, which if true would be
felicitous since that's the issue that's technically the most obvious to
me.

I have a third agenda: I'd like to make it easier to decouple ZODB
storage from the application logic.  Looking over the code, it looks
like whoever wrote this made the content objects inherit from Persistent
and then went ahead and wrote many basic methods right there on the
storage objects.  If this were factored off, then GetPaid could be used
on top of TurboGears objects or Django objects instead by simply marking
them with an interface saying "this is an order object! use it!" or
whatever.