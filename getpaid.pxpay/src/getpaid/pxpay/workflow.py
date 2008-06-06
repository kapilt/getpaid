from zope.interface import implements
from hurry.workflow import workflow
from hurry.workflow import interfaces as iworkflow

from getpaid.core.workflow.order import create_finance_workflow
from getpaid.core.interfaces import workflow_states
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid')

class FinanceWorkflow( workflow.Workflow ):
    implements( iworkflow.IWorkflow )
    def __init__( self ):
        fs = workflow_states.order.finance
        transitions = create_finance_workflow()
        transitions.append(workflow.Transition(
            transition_id = 'processor-charging-cancelled',
            title = _(u'Processor Cancel from Charging'),
            source = fs.CHARGING,
            destination = fs.CANCELLED_BY_PROCESSOR,
            trigger = iworkflow.SYSTEM, ))
        super( FinanceWorkflow, self).__init__( transitions )


FinanceWorkflowAdapter, _, _ = workflow.ParallelWorkflow(
    workflow.AdaptedWorkflow( FinanceWorkflow() ),
    workflow_states.order.finance.name,
    )
