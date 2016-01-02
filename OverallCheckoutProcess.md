![http://getpaid.googlecode.com/files/sitepaymentworkflow.jpg](http://getpaid.googlecode.com/files/sitepaymentworkflow.jpg)

## Overall Workflow ##

Unauthenticated, Add to cart: Add to Cart--> Sign In --> Your Details<sup>1</sup> --> Back to Item View (with link on page to "checkout")

Checkout: Checkout/Buy Now/Donate --> (Sign In --> Your Details<sup>1</sup> -->) Review Cart --> Finalize Payment --> Confirmation

Authenticated versions: same, but without the "sign in" step

<sup>1</sup>Your Details: this is designed to collect information for the site manager to have access to. It is by default just the necessary information about an order (ie billing address), but should be extensible by developers/integrators to include demographic information collection, newsletter signup, etc.


## Assumptions ##

Objects marked as buyable can be added to the shopping cart.

When a user is on an aggregated page of content (eg. a category page), it is possible to click on an Add to Cart button. This means that the aggregate page must be flagged as buyable. Clicking on the button will take the user to the Review Cart view.

If a user is on a product page, it is possible to click on a Buy Now button. Clicking on the button will redirect the user to the Checkout page.