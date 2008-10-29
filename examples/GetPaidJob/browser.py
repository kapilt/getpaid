"""
"""

from zope import interface, component
from zope.app.intid.interfaces import IIntIds
from getpaid.core import interfaces, item

from Products.PloneGetPaid.interfaces import IPayableMarker
from Products.Five.utilities.marker import mark
from Products.CMFCore.utils import getToolByName

class JobPostCheckout(object):
    """fill a cart with the job post and redirect to checkout"""
        
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def __call__( self ):
        utility = component.getUtility( interfaces.IShoppingCartUtility )
        cart = utility.get(self.context, create=True)
        
        portal_url = getToolByName( self.context, 'portal_url').getPortalObject().absolute_url()
        
        # don't add a job post multiple times..
        if len(cart):
           return self.request.response.redirect('%s/@@getpaid-checkout-wizard'%portal_url)
          
        # get the price for the posting
        price = self.getPostingPrice()
        
        # add the posting to the cart
        self.createLineItem( cart, price )
        
        # send to checkout
        return self.request.response.redirect('%s/@@getpaid-checkout-wizard'%portal_url)    
        
    def getPostingPrice(self):
        """docstring for getPostingPrice"""
        cost = self.context.aq_inner.getPostingFee()
        return cost
            
    def createLineItem( self, cart, price ):
        # we didn't explicitly make the job post payable, but if we want to add it to a cart,
        # we need to make it resolvable from the line item back to the posting, to do this
        # we need to add register it with the intids utility. 
        intids = component.getUtility( IIntIds )
        iid = intids.queryId( self.context )
        if iid is None:
            iid = intids.register( self.context )

        nitem = item.PayableLineItem()
        nitem.item_id = self.context.UID() # archetypes uid
        nitem.uid = iid

        # copy over information regarding the item
        nitem.name = self.context.Title()
        nitem.description = self.context.Description()
        nitem.cost = price
        nitem.quantity = 1
        nitem.product_code = nitem.item_id
        
        # add to cart
        cart[ nitem.item_id ] = nitem
        cart.last_item = nitem.item_id        
            
                
        
        
        
