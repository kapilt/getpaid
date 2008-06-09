from zope.interface import implements
from zope.component import getUtility
from hurry.workflow.interfaces import IWorkflowState

from Products.CMFCore.utils import getToolByName

from getpaid.core.interfaces import IOrderManager
from getpaid.core.interfaces import workflow_states

from getpaid.pxpay.interfaces import IPXPayInvalidMessageError, \
     IPXPayNetworkError
from getpaid.pxpay.exceptions import PXPayInvalidMessageException, \
     PXPayNetworkException

fs = workflow_states.order.finance


def redirect_url(context, order_id):
    site_root = getToolByName(context, 'portal_url').getPortalObject()
    site_url = site_root.absolute_url()
    return_url = '/'.join((site_url,
                           '@@getpaid-order',
                           order_id,
                           '@@pxpay-communication-error'))
    return return_url


class PXPayInvalidMessageError(object):

    implements(IPXPayInvalidMessageError)

    redirect = True

    def __call__(self, context, request, order_id, message):
        msg = "invalid message recieved from pxpay "
        if order_id:
            msg += "order " + order_id
            order_manager = getUtility( IOrderManager )
            order = order_manager.get(order_id)
            state = order.finance_workflow.state().getState()
            if state == fs.REVIEWING:
                order.finance_workflow.fireTransition('processor-cancelled',
                                                      comment="payment gateway failed")
            if state == fs.CHARGING:
                order.finance_workflow.fireTransition('processor-charging-cancelled',
                                                      comment="payment gateway failed")
        if not self.redirect:
            raise PXPayInvalidMessageException("Invalid pxpay message for order " + \
                                               order_id)
        url = redirect_url(context, order_id)
        request.response.redirect(url)


class PXPayNetworkError(object):

    implements(IPXPayNetworkError)

    redirect = True

    def __call__(self, context, request, order_id):
        msg = "invalid message recieved from pxpay "
        if order_id:
            msg += "order " + order_id
            order_manager = getUtility( IOrderManager )
            order = order_manager.get(order_id)
            state = order.finance_workflow.state().getState()
            if state == fs.REVIEWING:
                order.finance_workflow.fireTransition('processor-cancelled',
                                                      comment="payment gateway failed")
            if state == fs.CHARGING:
                order.finance_workflow.fireTransition('processor-charging-cancelled',
                                                      comment="payment gateway failed")

        if not self.redirect:
            raise PXPayNetworkException("PXPay network error occured for order " + \
                                        order_id)
        url = redirect_url(context, order_id)
        request.response.redirect(url)

