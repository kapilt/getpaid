# Specific Workflow #

Payment / Donation screen with fields for adding an amount and pressing submit/add to cart/etc.

If not "Buy Now" (or "quick" checkout), return to the item you added to your cart and display the "cart" icon/text in the interface; else take them to the Review Cart page (where can also enter discount code, if applicable).

The user browsing the site and finishing a purchase (ie donation, shopping cart checkout etc) is then routed through a series of screens to finish. The screens proceed with the current step highlighted in a "Progress Bar" in the top of the page.


## Sign In ##

  * Screen that has login box to either log in or register (with a radio button between them so the user can specify "already a member" or "I am a new member". The page includes a link to "Forgot my password". See Amazon.com checkout process page


## Billing Information ##

Please provide the following information ("Billing Information" indicated now in the status bar).

  * Name (as appears on credit card), prefilled with user's name
  * Billing Address (prepopulated if account already exists)
  * Demographics (deferred)
  * (optional) Shipping Address (only shows if activated in product config screen, and with checkbox that uses member info/billing address for shipping address, prepopulated if account already exists)
  * Form of payment: Dropdown of options configured in GetPaid (http://www.openplans.org/projects/plonecommerce/attach-payment-option-to-content-type). Since now only one payment option permitted in site, will show that option.
  * Disclaimer: note about security etc (set in Configure Payment Disclaimer Text )
  * note: we don't collect the credit card info, but site user off to the pay processor for that (except in case of Authorize.net...), so I removed those fields here.


## Review Cart ##

Screen that summarizes the billing information and the item(s) to be ordered, their prices, and the total to be billed. Allows user to edit cart, enter a discount code, continue shopping, or finalize payment.

See for screenshot:

![http://dev.zwarehouse.org/attachment/wiki/ScreenShots/shopping_cart_status.png](http://dev.zwarehouse.org/attachment/wiki/ScreenShots/shopping_cart_status.png)

## Finalize Payment ##

  * Proceed to checkout form with billing information and credit card fields. Billing fields will be filled in by default with the user's account information.
  *  If the user is not forced to leave the site by the Payment Processor, the payment will continue within the Plone workflow.
  * Proceed to payment.  If the Payment Processor forces you to leave the site, users will be taken to the processor then redirected back to the home page (seems like should end on a more appropriate page, for example site-based success page with confirmation number).
  * If an error is received, the user will be redirected back to the Checkout form.


## Confirmation ##

  * Redirected page will be either a receipt or a thank you page.


Integrate this stuff:

Payment / Donation screen with fields for adding an amount and pressing submit.

If logged in, proceed to Review Cart.

Proceed to Checkout from Payment Processor (AuthNet, etc.).

Proceed to checkout form with billing information and credit card fields. Billing fields will be filled in by default with the user's account information.

Proceed to payment.  If the Payment Processor forces you to leave the site, users will be taken to the processor then redirected back to the home page.

Redirected page will be either a receipt or a thank you page.

If an error is received, the user will be redirected back to the Checkout form.

 If the user is not forced to leave the site by the Payment Processor, the payment will continue within the Plone workflow.