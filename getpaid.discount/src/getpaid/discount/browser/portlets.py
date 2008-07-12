from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from getpaid.discount.browser.interfaces import IDiscountableMarker
from getpaid.discount.browser.interfaces import IBuyXGetXFreeableMarker
from getpaid.discount.browser.interfaces import IDiscountable
from getpaid.discount.browser.interfaces import IBuyXGetXFreeable

from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.PloneGetPaid.interfaces import PayableMarkerMap
from Products.PloneGetPaid.interfaces import IPayableMarker
from Products.PloneGetPaid.browser.portlets import buy
from Products.PloneGetPaid.browser.portlets import donate
from Products.PloneGetPaid.browser.portlets import premium
from Products.PloneGetPaid.browser.portlets import ship

class BaseDiscountPortlet(object):
    """
    """
    def isDiscountable(self):
        return IDiscountableMarker.providedBy(self.context)
    
    def isBuyXGetXFreeable(self):
        return IBuyXGetXFreeableMarker.providedBy(self.context)
    
    def getPrice(self, item):
        """
        returns the price of the payable item
        """
        for marker, iface in PayableMarkerMap.items():
            if marker.providedBy(item):
                payable = iface(item)
                return payable.price
        return None
     
    def hasNormalDiscount(self, item):
        """
        returns a nice display of the discount on the item
        """
        result = None
        price = self.getPrice(item)
        if IDiscountableMarker.providedBy(item) and price:
            adapter_obj = IDiscountable(item)
            discount_value = adapter_obj.getDiscountValue()
            if discount_value != 0.0:
                discount_type = adapter_obj.getDiscountType()
                if discount_type == 'Dollars Off':
                    result = "$%0.2f ($%0.2f off)" % (price - discount_value, discount_value)
                else:
                    result = "$%0.2f (%0.0f%s off)" % (price - price*discount_value/100, discount_value, '%')
        return result

    def hasBuyXGetXFreeDiscount(self, item):
        """
        returns a nice display of the discount on the item
        """
        result = None
        if IBuyXGetXFreeableMarker.providedBy(item):
            adapter_obj = IBuyXGetXFreeable(item)
            number_to_buy = adapter_obj.getNumberToBuy()
            number_free = adapter_obj.getNumberFree()
            if number_to_buy != 0 and number_free != 0:
                result = "Order %d get %d additional free" % (number_to_buy, number_free)
        return result
    

class DiscountContentPortlet(BrowserView, BaseDiscountPortlet):
    """ Plone 2.5 View methods for the ContentPortlet """
    
    def __init__(self, *args, **kw):
        super(BrowserView, self).__init__(*args, **kw)
        
        
class PGPContentPortlet(BrowserView):
    """ Plone 2.5 override of the View methods for the ContentPortlet """
    payable = None
    def __init__( self, *args, **kw):
        super( BrowserView, self).__init__( *args, **kw)

        found = False
        for marker, iface in PayableMarkerMap.items():
            if marker.providedBy( self.context ):
                found = True
                break

        if found:
            self.payable = iface( self.context )
        
    def isPayable(self):
        return self.payable is not None and \
            not IDiscountableMarker.providedBy(self.context) and \
            not IBuyXGetXFreeableMarker.providedBy(self.context)


class DiscountRenderer(base.Renderer, BaseDiscountPortlet):
    """Plone 3.0 Base rendered useful for discount portlets.
    """

    # Marker interface that this renderer is meant for.
    marker = IPayableMarker
    # Supply a template id in the inheriting class.

    @property
    def available(self):
        """Portlet is available when a marker interface is provided.

        Overwrite this by picking a different interface.
        """
        return self.marker.providedBy(self.context)
        
    @property
    def payable(self):
        """Return the payable (shippable) version of the context.
        """
        iface = PayableMarkerMap.get(self.marker, None)
        if iface is None:
            # Something is badly wrong here.
            return None
        return iface( self.context )


class IDiscountablePortlet(IPortletDataProvider):
    pass


class DiscountableAssignment(base.Assignment):
    implements(IDiscountablePortlet)

    @property
    def title(self):
        """Title shown in @@manage-portlets.
        """
        return u"Discountable"


class DiscountableAddForm(base.NullAddForm):

    def create(self):
        return DiscountableAssignment()


class DiscountableRenderer(DiscountRenderer):
    marker = IDiscountableMarker
    render = ViewPageTemplateFile('templates/portlet_content_discountable.pt')


class IBuyXGetXfreeablePortlet(IPortletDataProvider):
    pass


class BuyXGetXfreeableAssignment(base.Assignment):
    implements(IBuyXGetXfreeablePortlet)

    @property
    def title(self):
        """Title shown in @@manage-portlets.
        """
        return u"BuyXGetXFreeable"


class BuyXGetXfreeableAddForm(base.NullAddForm):

    def create(self):
        return BuyXGetXfreeableAssignment()


class BuyXGetXfreeableRenderer(DiscountRenderer):
    marker = IBuyXGetXFreeableMarker
    render = ViewPageTemplateFile('templates/portlet_content_buyxgetxfreeable.pt')


#Plone 3 renderers for the portlets
class BuyRenderer(buy.Renderer):
    """"""
    
    @property
    def available(self):
        """"""
        return self.marker.providedBy(self.context) and \
            not IDiscountableMarker.providedBy(self.context) and \
            not IBuyXGetXFreeableMarker.providedBy(self.context)

class DonateRenderer(donate.Renderer):
    """"""
    
    @property
    def available(self):
        """"""
        return self.marker.providedBy(self.context) and \
            not IDiscountableMarker.providedBy(self.context) and \
            not IBuyXGetXFreeableMarker.providedBy(self.context)

class PremiumRenderer(premium.Renderer):
    """"""
    
    @property
    def available(self):
        """"""
        return self.marker.providedBy(self.context) and \
            not IDiscountableMarker.providedBy(self.context) and \
            not IBuyXGetXFreeableMarker.providedBy(self.context)

class ShipRenderer(ship.Renderer):
    """"""
    
    @property
    def available(self):
        """"""
        return self.marker.providedBy(self.context) and \
            not IDiscountableMarker.providedBy(self.context) and \
            not IBuyXGetXFreeableMarker.providedBy(self.context)
