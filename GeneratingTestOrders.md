### Generating Test Orders ###

In order to make testing our admin screens easier, we've put together a procedure
for generating test order data.

To create this test data, In the ZMI of the plone portal where getpaid is installed,
and an external method with the following values:

```
id : generate_orders
module : PloneGetPaid.gen_order
function : createOrders
```

if you test this function, it will return sayings its created 20 orders.

now if you go to the getpaid admin screens and click on the order management you'll be able
to search, and manipulate orders and their workflow states.


