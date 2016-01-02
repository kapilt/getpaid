A proposal to change how we take orders in PloneGetPaid
# Introduction #
Getpaid currently has an order workflow that does not allow orders to be placed and paid afterwards, does not permit anonymouse users to see their order status and other shortcomings that can be fixed.

# Details #
This is my proposal:
(it's just a copy/paste from the email I just sent to the mailing list; I write it here so that it can be edited and kept current if it has consensus, and also to add a picture that will make it easier to understand it)

the approach currently is that we don't create an order if it's not paid, but we instead create it after the paypal process is over and an IPN comes.
Customer data is also collected on the paypal site.
Some customers are propably going to place an order and for some reasons (computer crash or phone call etc) wait some time before paying it, or lose their browser session.
I really think we should create the order object and destroy the cart before the customer is sent to paypal, collecting data on the getpaid-enabled site as well.
We could then provide the "pay with paypal" button on the order summary page. This would allow orders to be paid after they have been taken.
It would also simplify the solution of a bug with the current implementation; the function order\_id of the view getpaid.paypal.views.PayPalCheckoutButton is:
> 30     def order\_id(self):
> 31         return 'PUT ORDER ID HERE'
and it would be handy to have the actual order id available when we create the button.
BTW, we should also fix the personal details form and separate "first name" from "surname": we can't programmatically split "Full name" when we pass it to paypal.
One more issue: anonymous users can't see their own orders, so they wouldn't be able to pay with the described setup.
We could solve this providing a token in the emails we send after the order is created; the token could be the md5 hash of the date and time of the order.
Would this be secure enough? It would prevent a random person from collecting personal data of users, would it?
I currently use this approach in production and, at least for me, it has worked well; but I'm not sure it's secure enough. Anyway, users like **a lot** not to be forced to remember username/password pairs. This would also allow them to email the link to the order details page to a friend, and he could see only that particular order. This could be useful for gifts if the recipient wants to check the shipping status.

# Diagram #
dotted line represent automatic steps, while solid lines represent user actions.
![http://getpaid.googlecode.com/files/GetPayWorkflow.png](http://getpaid.googlecode.com/files/GetPayWorkflow.png)