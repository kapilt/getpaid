# Introduction #

Currently there is no handling for taxes. Some users are starting to need this, and it is a complex set of functionalities. This page is notes for refining requirements. We sprinted on this during the NOLA Symposium June 6, 2008 and created a branch called "tax" for the work.

# Background and Issues #

  * http://svn.plone.org/svn/collective/PloneMall/core/PloneMall/trunk/PloneMall/docs/Tax.txt

Tax rules (examples of the complexity in various use cases):
  * in US, customer pays tax if in same state as a brick-n-mortar store
  * in UK, different levels of VAT based on type of good
  * in Brazil, 5 different taxes
  * in US, some states tax shipping, some don't
  * in Indiana, zip code crosses 3 counties, which provides
  * in NYC, city sales tax applies based on price (below certain price, no tax)

# Requirements #

**Basic use case**

The system manages taxes (rates and rules) on items and/or on shipping. Use case includes:
  * Developer sets up different rules of taxation (eggs).
  * Site admin can enable taxes on the store
  * Once taxes enabled on the store admin, can enter in the name and rate for each tax applied for a store, and can designate whether the tax is the default rate and if it applies to shipping costs.
  * For each buyable item, admin picks which tax rate/category applies. If no tax is chosen, then the default tax is applied.
  * Taxes calculated during checkout and recorded on the order (and in total), if they apply to the purchased items.

Future enhancements: Admin has tax table and counties/zips in csv and can upload to the site.

To use taxes, the site admin would have to install the egg(s) for that applies appropriate tax rates (ie the getpaid.tax.usa egg). The product should ship a simple tax module (handles a flat rate for a tax that can be given a name) with GetPaid, but this would be easy to overwrite for custom needs.

**Design criteria**
  * Make it pluggable so other countries/states/regions can make own tax rules
  * Supports multiple taxes to be paid (example: federal, state, municipal)
  * The content/cart objects know what rules apply to them

**Implementation details**
  * Use the existing tax utility (admin screen): make it have a list of taxes (admin can add tax name and rate). Set of rules are coded in by developer. Each tax has optional "applies to shipping" and "default tax rate" check boxes.
  * add iTax interface:
    * 3 methods (one for item, one for shipping, one for total order), has to be callable;
    * Register named utilities for it (ex "VAT"): objects inside utility for rules, like 3 levels of VAT; Another scenario was suggested here by ChrisW (plz verify details!): getName method on iTax (key in dictionary) would allow the 3 levels of VAT to be 3 separate utilities, though would be able to sum to common "VAT" line item on cart total.
    * Future: add convenience utilities to upload csv file
  * iTaxUtility:
    * has one method getTax returns a dictionary of tax amount and tax id name
    * iTaxUtility has control over part of payable tab to be able to insert rendered information for admin to set on content. Admin get a list of taxes (multiselect list) on the payable form. Needs to be coded based on the tax utility you have.

# Issues and Questions #

  * What about auditing or reporting? Make sure that possible to get out / export of tax info for accountant.


# Reference #

An example is the Yahoo! store tax handling.

```
Yahoo! Merchant Solutions Tax Wizard

Select "do not collect tax" if you determine that you do not need to collect tax from buyers. Consult the tax agency for your state (or any state where you may be deemed to have a presence) or a tax accountant to determine if you must collect sales tax.

Select "collect tax at checkout" to set up and collect tax as buyers complete the checkout process. You can select states in which to charge tax and specify a rate. You can also set up additional rates by zip code to cover special city or county tax rates.

Select "collect tax after checkout" if you wish to determine the correct tax rate while processing each order. The key benefits to this method are you do not need to set up applicable tax rates for cities and counties before opening for business, and can determine the correct tax charges for each order as they are processed. Note: Buyers may cancel an order (or worse initiate a chargeback), if their card is charged for a higher amount than displayed at checkout.
```

Here is the test page for the tax calculation from Yahoo!:
![http://www.ncpc.org/resources/enhancement-assets/web/yahoo-shipping-tax-test-page.png](http://www.ncpc.org/resources/enhancement-assets/web/yahoo-shipping-tax-test-page.png)