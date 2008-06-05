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

Requirements:

1) A developer account with PaymentExpress
2) GetPaid core
3) zc.ssl
4) elementtree
5) plone (tested on plone 3.1)

Contributors
------------

Darryl Dixon <darryl.dixon@winterhouseconsulting.com>
Matt Halstead <matt@elyt.com>
