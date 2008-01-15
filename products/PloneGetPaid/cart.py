"""
Session Based Cart Implementation

$Id$
"""
from zope.component import getUtility
from zope.interface import implements

from getpaid.core.cart import ShoppingCart
from getpaid.core.interfaces import IShoppingCartUtility
from Products.CMFCore.utils import getToolByName
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from AccessControl import getSecurityManager

class ShoppingCartUtility(Persistent):

    implements(IShoppingCartUtility)

    def __init__(self):
        self._sessions = OOBTree()


    def get(self, context, create=False):
        """ Get the persistent cart. It does not persist for anonymous users.
        """
        uid = getSecurityManager().getUser().getId()

        if not uid:
            session_manager = getToolByName( context, 'session_data_manager')
            if not session_manager.hasSessionData() and not create:
                return None

            session = session_manager.getSessionData()
            if not session.has_key('getpaid.cart'):
                if create:
                    session['getpaid.cart'] = cart = ShoppingCart()
                else:
                    return None
            return session['getpaid.cart']

        cart = self._sessions.get(uid)
        if cart or not create:
            return cart

        cart = ShoppingCart()
        cart.member_id = uid
        self._sessions[uid] = cart
        return cart


    def destroy(self, context):
        """ Destroy the cart.
        """
        uid = getSecurityManager().getUser().getId()

        if not uid:
            # delete the current shopping cart
            session_manager = getToolByName( context, 'session_data_manager')
            if not session_manager.hasSessionData(): #nothing to destroy
                return None
            session = session_manager.getSessionData()
            if not session.has_key('getpaid.cart'):
                return
            del session['getpaid.cart']

        if self._sessions.has_key(uid):
           del self._sessions[uid]


    def manage_fixupOwnershipAfterAdd(self):
        pass
