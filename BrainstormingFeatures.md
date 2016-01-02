# Introduction #

Please add the features, with as much detail to clearly depict what you are seeking (if you want to flesh out lots of details, please just add a new wiki page and link it here). Please also put your name / company name beside features you need.


# Feature Requests #

Feature details (Interested people/orgs):

**New features**
  * TaxHandling
    * who: 6ftup, ChrisW, Jason Lantz

  * PloneFormGenAdapter
    * who: ifPeople, Trees for Life, One/Northwest, Daniel Holth, SteveM
    * to make single page checkout and flexible info gathering

  * Invoices
    * who: Suno Ano
    * automatically create Invoices (preferably .pdf) and sending them via email to customers once they bought something, payed for membership, etc. There is a first mailing list thread about this [here](http://thread.gmane.org/gmane.comp.web.zope.plone.getpaid.devel/1039).


  * PayToSubmitContent
    * who: perrito, javimansilla

  * Salesforce.com Integration
    * who: One/Northwest, ifPeople, Trees for Life
    * for loading info into SF from GetPaid checkout (related to PFG integration),

  * Conference/event registration
    * who: NCPC
    * including limited seating and wait list

  * Customizable/personalizable products
    * who: NCPC
    * e.g. the GREEN shirt with JOE embroidered on the front --- what role would GetPaid play in this?

  * modifying/flagging user profiles
    * who: NCPC
    * e.g. this user gets a gold start for being a Champion donor

  * Membership Dues
    * who: Suno Ano, NCPC
    * wiki: ConfigureMembershipTypes, RecurringPaymentStories
    * recurring payments, granting special site access for payment (we think of members in a non-Plone way and have Members Only sections for different programs).

  * Support for product variants
    * who: 6fup
    * which item A do you need: the red one or the blue one?

  * Common pricing policy settings
    * who: 6ftup, TOT
    * Support for Distributors special discount code (or a retail vs wholesale pricing).
    * Support for bundle discounts (product A + product B = discount)

  * Payment options
    * who:
    * payment by PO number (order generated without actual credit card)

**Feature Enhancements**
  * Enhance reports on sales data (NCPC)
  * Repeat orders / enhanced order templates (NCPC)
  * Marketing email list (e.g., building a customer list for targeted mailings) (NCPC)
  * UPS shipping label generation through the web (TOT)

**Best Practices and Product management**
  * Package GetPaid eggs
  * Document customization philosophies and approaches (what are implications if you change things in checkout, for example). (Matt Halstead)
  * There has been a lot of work gone in to allow checkout forms to be customisable in a way that automatically stores gathered data onto an order. Other processes need to respect this by requesting schemas/interfaces and not assuming them, and in some instance requesting adapters - e.g. don't ask for "order.contact\_information" ask for an "IContactInfo" adapter. (Matt Halstead)