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

OK, where are we at... Basically: it works to authorise transactions currently.
Deferred payment, repeating payments, authorisations, etc, are not yet implemented,
but the PXPay interface supports them, so there's no reason they can't be added.

Integration with the standard GetPaid exit-points from the checkout wizard is still
required. In other words, we hook in at the beginning correctly to implement a sane
checkout flow, but at the end, we don't yet hook back in to the GetPaid 'workflow'
to provide notification in the usual places of succes/failure of payment.

Error handling etc is still in flux. Most(?) errors probably get trapped, but choosing a
sensible codepath at the point of failure is still very much up in the air.

Requirements:
1) A developer account with PaymentExpress
2) GetPaid core
3) zc.ssl
4) I think that's about it.
