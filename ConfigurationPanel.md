# Introduction #
After installing PloneGetPaid the site admin goes to the GetPaid Settings in the configuration panel. The top of the page includes a portal message: "This product is currently inactive. You need to fill out required settings before you can make content in your site payable."

The site admin can tab through the following screens to set account information for the
system:

  * identification
  * configure
  * currency
  * maintenance mode
  * emails
  * header / footer
  * order management

Refer to these mockups for possible site layout:

[Admin Main Page](http://dev.zwarehouse.org/attachment/wiki/ScreenShots/admin_main_screen.png)

[Admin Products Menu](http://dev.zwarehouse.org/attachment/wiki/ScreenShots/admin_products_menu.png)

[Admin Edit Product](http://dev.zwarehouse.org/attachment/wiki/ScreenShots/admin_edit_product.png)


## Identification ##
  * Store / Organization name
  * Contact name
  * Contact email
  * Company
  * Address
  * Address2
  * City
  * State / Provice
  * Zip / Postal Code
  * Country
  * Phone
  * Fax

## Configure (shippable types, shipping options, payment settings, unit of measurement, session timeout, sales tax) ##

> ### Shippable Types ###

> ### Shipping options ###
    * Require shipping (boolean)
    * Flat rate shipping

> ### Payment Settings ###
    * Select Payment Processor
    * Enter Payment Processor details (merchant ID, license key, etc.)
    * Credit cards supported by the system (Visa, MC, Discover, AMEX)
    * Once the required fields are set, the message changes to state that "This product is now active. You can set content in your site to be "Payable" in the "actions" menu."

> ### Unit of measurement (weight) ###

> ### Session (basket) timeout -- default 60 minutes - possible in this version? ###

> ### Sales tax configuration (this needs discussion) ###
    * Require tax (boolean)
    * State-based (Select a state?)
    * Canadian VAT
    * German VAT
    * Shopper selected
    * Generic VAT (non-European)
    * Default encryption key

## Currency ##

Need to find a resource to figure out how to implement this.

> ### Generic Currency Formatting ###
It would be impossible to catalog (and anticipate) the formatting for all the world's currencies. Select this option to customize all aspects of displaying your currency.

  * Currency symbol
  * Positive currency format
  * Negative currency format
  * Digit grouping symbol
  * Number of digits in group
  * Decimal symbol
  * Number of digits after decimal
  * US currency formatting


## Emails ##
> ### Email preferences ###
    * Do not send merchant email notification of a completed transaction (radio1)
    * Send merchant email notification when a transaction happens (radio1)
    * Send merchant encrypted email notification when a transaction happens (radio1)
    * Do not send customer email notification of a completed transaction (radio2)
    * Send customer email notification of a completed transaction (radio2)
> ### Customer Order Confirmation Email ###
    * email address of the sender
    * cc address
    * subject field
    * name of the sender, i.e. the name of the store
    * thank you text
> ### Merchant Notification Email ###
    * email address of the customer or a freetext email address (i.e. customerservice@)
    * a subject field ("an order has been placed")
    * text field

## Header / Footer ##
  * Rich text box for header.
  * Rich text for footer.
  * Instructions for adding disclaimer text, links to order information and privacy policy.



## Order Management ##
Order Listing is the entry page. Contains tabs for Customer Information, Order Information, Payment Processing, displays a list of all recent orders, sorted by most recent). Click through from an order to the customer's information page.

> ### Customer information page ###
    * Order number (click through to see order details and more detailed info)
    * Username (click through to see order details and more detailed info)
    * Email address
    * First Name
    * Last Name
    * Shipping / Billing Information
    * Shipping address
    * Billing address
    * Order history
    * Amount Paid


> ### Order Information (ship to / bill to information) ###
    * Product Code
    * Product Description
    * Product Variants
    * Quantity
    * Price/ea
    * Line item total
    * Shipping cost
    * Sales tax
    * Total
    * Status (processed, refunded)
    * Update / refund / export to CSV / delete / reset


> ### Payment Processing ###
    * Method (credit card)
    * Name on Card
    * Card Number
    * Expiration Date
    * AVS Code (?)
    * Transaction ID
    * Response Reason Text (approved / rejected)
    * Authorization Code
    * Authorization Date / Time





Deferred items:

  * Discounts (deferred)
  * Membership Types

  * Batched & unbatched orders listing
    * Run report
    * Process orders
      * Batch ID
      * Date
      * Total
      * Method (GC / Auth.net)
    * Delete batch

Maintenance mode
  * Maintenance message
  * Store online (radio button)
  * Store offline at (date / time)
  * No new customer x minutes before store goes offline
  * Warning message
  * Store message