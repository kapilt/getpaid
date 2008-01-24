from Product.PloneGetPaid.browser.checkout import BaseCheckoutForm

from getpaid.ups.interfaces import IUPSRateService

class ShippingForm( BaseCheckoutForm ):

    def update( self ):
        self.setupHiddenFormVariables()

        
