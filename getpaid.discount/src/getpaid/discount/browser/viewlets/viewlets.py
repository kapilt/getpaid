from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.layout.viewlets.common import ViewletBase

from getpaid.core.interfaces import IShoppingCartUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from getpaid.discount.browser.interfaces import IDiscountableMarker
from getpaid.discount.browser.interfaces import IDiscountable
from getpaid.discount.browser.interfaces import IBuyXGetXFreeable
from getpaid.discount.browser.interfaces import IBuyXGetXFreeableMarker

class DiscountListingViewlet(ViewletBase):
    render = ViewPageTemplateFile('discount_listing.pt')
    
    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal_url = self.portal_state.portal_url()
        self.cart = getUtility(IShoppingCartUtility).get(self.context) or {}
    
    def getDiscounts(self):
        """
        for all the items in the cart
        we look if they have a discount
        and if so, we bring back a list of dictionaries
        """
        results = []
        if self.cart:
            for payable_line in self.cart.values():
                ref_obj = payable_line.resolve()
                payable_quantity = payable_line.quantity
                if ref_obj and IDiscountableMarker.providedBy(ref_obj):
                    adapter_obj = IDiscountable(ref_obj)
                    discount_value = adapter_obj.getDiscountValue()
                    if discount_value != 0.0:
                        discount_title = adapter_obj.getDiscountTitle()
                        discount_type = adapter_obj.getDiscountType()
                        if discount_type != 'Dollars Off':
                            description = '%0.0f' % discount_value + "% off"
                        else:
                            description = 'Total of $%0.0f off' % (discount_value * payable_quantity)
                        res = {'title': "%s on %s" % (discount_title, ref_obj.Title()), 
                               'description': description
                              }
                        results.append(res)
                elif IBuyXGetXFreeableMarker.providedBy(ref_obj):
                    adapter_obj = IBuyXGetXFreeable(ref_obj)
                    number_to_buy = adapter_obj.getNumberToBuy()
                    number_free = adapter_obj.getNumberFree()
                    if number_to_buy != 0 and number_free != 0:
                        discount_title = adapter_obj.getDiscountTitle()
                        number_res = int(payable_quantity / number_to_buy * number_free)
                        description = str(number_res) + " free additional item(s)"
                        res = {'title': "%s on %s" % (discount_title, ref_obj.Title()), 
                           'description': description
                          }
                    results.append(res)
                        
        return results