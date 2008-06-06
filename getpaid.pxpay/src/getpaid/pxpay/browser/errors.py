from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class PXPAYCommunicationError(BrowserView):

    _template = ViewPageTemplateFile('templates/pxpay-communication-error.pt')

    def __call__(self):
        return self._template()
