##############################################################################
#
# Copyright (c) 2008 Darryl Dixon <darryl.dixon@winterhouseconsulting.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the GNU General Public License
# Version 2 (GPL). A copy of the GPL should accompany this distribution.
# 
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

This is a Payment Processor for the PaymentExpress PXPay hosted Payments solution
SEE: http://www.paymentexpress.com/technical_resources/ecommerce_hosted/pxpay.html

We hook into the last checkout and payment step of the checkout so
that the user is redirected to the pxpay web interface to fill out
their credit card details and the redirected back to our site where we
handle success or failure status of the transaction.

Deferred payment, repeating payments, authorisations, etc, are not yet implemented,
but the PXPay interface supports them, so there's no reason they can't be added.

Orders and Finance workflow
---------------------------

An orders persistence and workflow is managed entirely by this payment
processor. Since we hook into the last step of the checkout, we are
responsible for creating the order, storing it in the manager, and
handling the finance workflow.

When a user selects "make payment"

- an order is created and stored in the order manager (i.e. it is now persistent in the zodb)

- finance workflow:  None  -->  REVIEWING

- the order is authorized - which means a payment request is made to
  pxpay.

If pxpay returns saying this is ok and here is the url to redirect to,
then we update the finance workflow: REVIEWING --> CHARGEABLE -->
CHARGING (note: CHARGEABLE --> CHARGING is an automatic transition.

The user is redirected to the pxpay web interface to enter credit card
details. The site then redirects them back to our callback and we
negotiate a response message. This tells us whether the payment was
successful or not.

If the payment was successful, then we update the finance workflow:
CHARGING --> CHARGED

If the payment was unsuccessful, then we update the finance workflow:
CHARGING --> PAYMENT_DECLINED

If there is an error in the communication with pxpay, then we update
the finance workflow: * --> CANCELLED_BY_PROCESSOR with a comment
that this was a communication error. We don't destroy the cart though
so the user can try again.

The error handler for a communications error is a utility so that it
can be overriden easily, for example to redirect the user to another
view.

Requirements
------------

1) A developer account with PaymentExpress
2) GetPaid core
3) zc.ssl
4) elementtree
5) plone (tested on plone 3.1)




Contributors
------------

Darryl Dixon <darryl.dixon@winterhouseconsulting.com>
Matt Halstead <matt@elyt.com>
