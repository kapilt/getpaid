GetPaid Authorize.Net Payment Processor
=======================================


Store Specific Processor Setting Tests
--------------------------------------

Creating an Order
=================

	>>> from getpaid.core.order import Order
	>>> order = Order()

An order consists of line items. line items can come from a variety of
sources, content space payables, gift certificates, ie. anything we
potentially want to purchase:

	>>> from getpaid.core.item import LineItem
	>>> item = LineItem()

Let's set some attributes expected on line items. The only system invariant
here is that item_id should be unique when referring to purchasing the same
item:

	>>> item.item_id = "event-devtalk-2007-1"
	>>> item.name = "Event Registration"
	>>> item.cost = 25.00
	>>> item.quantity = 5
	>>> item.description = "Development Talk"

Line Items are stored in a line item container, such as a shopping cart
of shipment:

	>>> from getpaid.core.cart import ShoppingCart
	>>> cart = ShoppingCart()
	>>> cart[ item.item_id ] = item

we can ask the cart how many items it has:

	>>> cart.size()
	5

Let's attach our cart to the order:

	>>> order.shopping_cart = cart

and now we can ask the order, its total price:

	>>> order.getSubTotalPrice()
	Decimal("125.0")

We need some additional information for an order to successfully process it:

	>>> from getpaid.core import payment
	>>> bill_address = payment.BillingAddress()
	>>> bill_address.bill_first_line = '1418 W Street NW'
	>>> bill_address.bill_city = 'Washington'
	>>> bill_address.bill_state = "DC"
	>>> bill_address.bill_country = "US"
	>>> bill_address.bill_postal_code = '20009'
	>>>
	>>>
	>>> contact_info = payment.ContactInformation()
	>>> contact_info.name = 'Juan Pablo Gimenez'
	>>> contact_info.phone_number = '+54-341-555-5555'
	>>> contact_info.email = 'jpg@nospam.org'

	>>> order.contact_information = contact_info
	>>> order.billing_address = bill_address

If we don't need to ship anything to the user, then we can forgo
setting a shipping address.

	>>> order.fulfillment_workflow.fireTransition('create')
	>>> order.fulfillment_workflow.fireTransition('process-order')
	>>> state = order.fulfillment_state
	>>> print state
	PROCESSING

First let's create a store class to work with:

	>>> from getpaid.core import interfaces
	>>> from zope.app.annotation import IAttributeAnnotatable
	>>> from zope.interface import implements
	>>> class Store:
	...	implements( interfaces.IStore, IAttributeAnnotatable )
	>>> store = Store()

And configure our payment processor:

	>>> from zope import component
	>>> from getpaid.core import interfaces, options, payment
	>>> processor = component.getAdapter( store, interfaces.IPaymentProcessor, "Authorize.Net" )
	>>> # processor.authorize( order, payment )

	>>> # interfaces.I
	>>

Now let's create an order to process:

	>>> from getpaid.core import order, item, cart
	>>> order1 = order.Order()
	>>> my_cart = cart.ShoppingCart()
	>>> my_cart['abc'] = abc = item.LineItem()
	>>> abc.cost = 22.20; abc.name = 'abc'; abc.quantity = 3
	>>> # str(order1.getTotalPrice()) '22.20'

Authorizing an Order
--------------------

Now we can run it through a processor:

	>>> from zope import component
	>>> from getpaid.core import interfaces, options, payment
	>>> # processor = component.getAdapter( self.context, interfaces.IPaymentProcessor, processor_name )
	>>> # processor = IPaymentProcessor( store )
	>>> # processor.authorize( order ) == interfaces.keys.results_sucess

Capturing/Charing an Order
--------------------------

Refunding an Order
------------------


Voiding an Order
----------------


Recurring Payment Order
-----------------------

Now let's create a recurrent order to process:

	>>> from getpaid.core import order, item, cart
	>>> order2 = order.Order()
