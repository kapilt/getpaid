"""

Session Based Cart Implementation

$Id$
"""

from zope.interface import implements

from getpaid.core.cart import ShoppingCart
from getpaid.core.interfaces import IShoppingCartUtility
from Products.CMFCore.utils import getToolByName

class ShoppingCartUtility( object ):
    
    implements( IShoppingCartUtility )

    def get( self, context, create=False ):
        session_manager = getToolByName( context, 'session_data_manager')
        if not session_manager.hasSessionData() and not create:
            return None
            
        session = session_manager.getSessionData()
        if not session.has_key('getpaid.cart'):
            if create:
                session['getpaid.cart'] = cart = ShoppingCart()
                member_tool =  getToolByName( context, 'portal_membership')
                member = member_tool.getAuthenticatedMember()
                cart.member_id = member and member.getId() or "Anonymous"
            else:
                return None
        return session['getpaid.cart']
        
    def destroy( self, context ):
        # delete the current shopping cart
        session_manager = getToolByName( context, 'session_data_manager')
        if not session_manager.hasSessionData(): #nothing to destroy
            return None
        session = session_manager.getSessionData()
        if not session.has_key('getpaid.cart'):
            return
        del session['getpaid.cart']

        
        

        

        
