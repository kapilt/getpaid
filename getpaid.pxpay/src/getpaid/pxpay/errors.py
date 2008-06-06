from zope.interface import implements
from zope.component import getUtility
from hurry.workflow.interfaces import IWorkflowState

from getpaid.core.interfaces import IOrderManager
from getpaid.core.interfaces import workflow_states

from getpaid.pxpay.interfaces import IPXPayCommunicationError
from getpaid.pxpay.exceptions import PXPayInvalidMessageException

fs = workflow_states.order.finance

class PXPayCommunicationError( object ):

    implements(IPXPayCommunicationError)

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

        raise PXPayInvalidMessageException(" ".join((msg,
                                                     message.generateXML())))


class PXPayCommunicationErrorRedirect( object ):
    """
    alternative implementation to redirect to an error view
    """
    implements(IPXPayCommunicationError)

    def __call__(self, context, request, order, message):
        url = '/'.join((context.absolute_url(),
                        '@@pxpay-communication-error'))
        request.response.redirect(url)
