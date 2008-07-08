from Products.Five.browser import BrowserView

from getpaid.discount.browser.interfaces import IDiscountableMarker
from getpaid.discount.browser.interfaces import IBuyXGetXFreeableMarker

from Products.PloneGetPaid.interfaces import IPayableMarker

class ContentControl(BrowserView):
    """ conditions for presenting various actions
    """
    __allow_access_to_unprotected_subobjects__ = 1
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def isPossibleDiscountable(self):
        """  does the context implement the IPayableMarker interface
        """
        return IPayableMarker.providedBy(self.context) and \
            not IDiscountableMarker.providedBy(self.context) and \
            not IBuyXGetXFreeableMarker.providedBy(self.context)
    
    isPossibleDiscountable.__roles__ = None
    
    def isPossibleBuyXGetXfreeable(self):
        """  does the context implement the IPayableMarker interface
        """
        return IPayableMarker.providedBy(self.context) and \
             not IBuyXGetXFreeableMarker.providedBy(self.context) and \
             not IDiscountableMarker.providedBy(self.context)
    
    isPossibleBuyXGetXfreeable.__roles__ = None
    
    def isDiscountable( self ):
        """  does the context implement the IDiscountableMarker interface
        """
        return IDiscountableMarker.providedBy(self.context)
    
    isDiscountable.__roles__ = None
    
    def isBuyXGetXfreeable(self):
        """does the context implement the IBuyXGetXFreeableMarker interface
        """
        return IBuyXGetXFreeableMarker.providedBy(self.context)

    isBuyXGetXfreeable.__roles__ = None
