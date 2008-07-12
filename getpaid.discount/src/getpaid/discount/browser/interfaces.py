from zope import schema
from zope.interface import Interface

class IDiscountable(Interface):
    """
    Marker interface for the Discountable items
    """
    discount_title = schema.TextLine(title=u'Discount Title',
                           required=True)
    
    discount_type = schema.Choice(title=u'Type of Discount',
                                  values=['Dollars Off', 'Percentage off'],
                                  required=True)
    
    discount_value = schema.Float(title=u'Value of the discount',
                                  required=True,)

class IDiscountableMarker(Interface):
    """
    Discount Interface
    """

class IBuyXGetXFreeable(Interface):
    """
    Marker interface for the BuyXGetXFreeable items
    """
    discount_title = schema.TextLine(title=u'Discount Title',
                           required=True)
    
    number_to_buy = schema.Int(title=u'Number of items to buy',
                                  required=True)
    
    number_free = schema.Int(title=u'Number of free items',
                                  required=True)

class IBuyXGetXFreeableMarker(Interface):
    """
    Discount Interface
    """
