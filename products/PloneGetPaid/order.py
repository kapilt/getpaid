
from getpaid.core import interfaces as igp
from zope import interface

import interfaces

def classifyOrder( order, event ):
    """ on order creation, classify order according to its contents """

    shipped = False
    donation = False
    recurrent = False

    for item in order.shopping_cart.values():
        if igp.IPayableLineItem.providedBy( item ):
            payable = item.resolve()
            if payable is None:
                # raise ??
                continue
            if interfaces.IShippableMarker.providedBy( payable ):
                shipped = True
            elif interfaces.IDonatableMarker.providedBy( payable ):
                donation = True
            elif interfaces.IRecurrentPaymentMarker.providedBy( payable ):
                recurrent = True

    if shipped is False:
        interface.directlyProvides( order, igp.IVirtualOrder )
    else:
        interface.directlyProvides( order, igp.IShippableOrder )
    if donation:
        interface.directlyProvides( order, igp.IDonationOrder )
    if recurrent:
        interface.directlyProvides( order, igp.IRecurrentOrder )

