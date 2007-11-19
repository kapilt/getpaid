from Products.Five import BrowserView
from getpaid.core.interfaces import IOrderManager
from getpaid.ogone.interfaces import IOgoneStandardOptions
from zope.component import getUtility
import sha

class ValidatePaymentParameters(object):
    def createShaOutSignature(self):
        """
        Create the sha out signature based on the parameter in the request
        and the sha out password defined in the payment processor parameters
        """
        options = IOgoneStandardOptions( self.context )
        shaPassword = options.shaout
        orderID = self.request.get('orderID')
        currency = self.request.get('currency')
        amount = self.request.get('amount')
        pm = self.request.get('PM')
        acceptance = self.request.get('ACCEPTANCE')
        status = self.request.get('STATUS')
        cardno = self.request.get('CARDNO')
        payid = self.request.get('PAYID')
        ncerror = self.request.get('NCERROR')
        brand = self.request.get('BRAND')
        shaObject = sha.new()
        shaObject.update('%s%s%s%s%s%s%s%s%s%s%s' % (orderID, currency,
                                                     amount, pm, acceptance,
                                                     status, cardno, payid,
                                                     ncerror, brand,
                                                     shaPassword))
        hexString = shaObject.hexdigest()
        return hexString.upper()

    def validate(self):
        """
        Validate the SHA OUT signature
        """
        requestShaOut = self.request.get('SHASIGN')
        if not requestShaOut:
            return False
        return self.createShaOutSignature() == requestShaOut

class OgonePostProcessAccepted(BrowserView, ValidatePaymentParameters):
    """
    The Ogone payment has been accepted
    """

    def __call__(self):
        """
        We update the order information and returns the template
        """
        if not self.validate():
            raise 'Incorrect SHA OUT Signature'
        orderId = self.request.orderID
        options = IOgoneStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        order.finance_workflow.fireTransition("charge-chargeable")
        order.finance_workflow.fireTransition("charge-charging")
        return 1

class OgonePostProcessCancelled(BrowserView, ValidatePaymentParameters):
    """
    The Ogone payment has been cancelled
    """

    def __call__(self):
        """
        We update the order information and returns the template
        """
        if not self.validate():
            raise 'Incorrect SHA OUT Signature'
        orderId = self.request.orderID
        options = IOgoneStandardOptions(self.context)
        currency = options.currency
        orderManager = getUtility(IOrderManager)
        order = orderManager.get(orderId)
        order.finance_workflow.fireTransition("cancel-chargeable")
        return 1

