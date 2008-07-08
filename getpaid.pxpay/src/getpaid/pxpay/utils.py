from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from getpaid.pxpay.interfaces import ICheckoutContext

class CheckoutContext(object):
    """
    Pretty benign implementation here. It's just a convenient abstraction.
    """
    implements(ICheckoutContext)

    def __init__(self, context):
        self.site_root = getToolByName(context, 'portal_url').getPortalObject()

    @property
    def root_object(self):
        return self.site_root

    @property
    def root_url(self):
        return self.root_object.absolute_url()

    @property
    def store(self):
        """
        the store object
        """
        return self.site_root
