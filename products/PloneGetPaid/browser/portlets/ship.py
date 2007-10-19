from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import getpaid.core.interfaces as igetpaid
from Products.PloneGetPaid.i18n import _
from Products.PloneGetPaid.interfaces import IShippableMarker


class IShippablePortlet(IPortletDataProvider):
    pass


class Assignment(base.Assignment):
    implements(IShippablePortlet)

    @property
    def title(self):
        """Title shown in @@manage-portlets.
        """
        return _(u"Shippable")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('../templates/portlet-content-shippable.pt')

    @property
    def available(self):
        return IShippableMarker.providedBy(self.context)


    def isPayable(self):
        """When we are rendered, the context is always payable.

        Or shippable, etcetera.  Otherwise the 'available' method
        would return False already.

        """
        return True

    @property
    def payable(self):
        """Return the payable (shippable) version of the context.

        Maybe do this the same as in content.py
        """
        return igetpaid.IShippableContent(self.context)


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
