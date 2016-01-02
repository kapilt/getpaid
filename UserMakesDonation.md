# Introduction #

This will be addressed in two phases. First phase will be a base implementation using generic forms. Phase two will utilize PloneFormGen to work with an adapter to hook into the shopping cart and payment processor.

## Assumptions ##

Payable items can be shippable, donateable, subscribeable, ie. they can have delivery options. A donateable item MUST also be payable.


## Present Implementation ##

User can add any content object to the site. Once the content object is added, a user can mark it as "make this a donation".

The user will see a form that will contain the following fields:

Product Name
Product Code
Product Description
Price (dropdown with initial defaults)
Free text field for amount
Rich text field
Quantity in basket
Buy Now button
Add to Basket button
Who marked this as donateable (this should be tied to the logged in user, not be a freeform field).

## Future Implementation ##

Will talk to PFG
User donations can appear either inline in a page template or in a portlet.
Will utilize variants.

## Workflow ##

User adds a donateable item to their cart. Press continue to register. It will also be possible to login from this page.

Next, go to review cart step. The user will be given the option to choose a payment processor, modify / update cart / continue shopping / checkout.

Next, go to credit card information page. This page will be dynamic based on payment processor chosen. On page where they enter their cc info show the cart contents.

Pressing "finalize payment" sends payment information to GC or Paypal, etc. (onsite or offsite). For payments made onsite, use https to send out the data.

When the transaction is completed, the user will be returned to plone confirmation page (receipt) or an error will be returned to the Plone interface.

## Storage of credit card information: ##

If there is an error during the transaction, return to the cc page. do not save the credit card data on the roundtrip.

Need to include a disclaimer that advises users not to click the finalize payment button twice to avoid double-charges.