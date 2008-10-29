from Products.Five import BrowserView
from getpaid.core.interfaces import IOrderManager
from getpaid.ogone.interfaces import IOgoneStandardOptions
from zope.component import getUtility

class OgoneCheck(BrowserView):
    """
    A class which check
    """

    def __call__(self):
        """
        This takes the order Id and returns
        the XML to Ogone
        """
        orderId = self.request.orderID
        options = IOgoneStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        ogonePrice = int(order.getTotalPrice() * 100)
        return '<orderid="%s" amount="%s" currency="%s">' % (order.getOrderId(),
                                                             ogonePrice,
                                                             currency)
