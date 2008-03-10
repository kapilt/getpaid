"""

order line item fulfillment, we defer full implementation of shippable fulfillment workflows

transition : create

   destination - new

transition : deliver-virtual

   source - new
   condition : not shippable
   state - delivered
   trigger : system

transition : ship

   source - new
   destination - processing

transition : cancel

   source - new
   state - cancelled

transition : cancel - processing

   source - processing
   state - cancelled
   condition - shipment not authorized
    
transition :  shipment-authorized

   source - processing
   state - shipppable

transition : process return

   source - shipped
   state - return in progress
   condition - returnable
   option - restocking fee   
   generate - rma number

   -- returns are there own shipments with workflow ?

transition : received return
  source : return in progress
  condition :
  option : ? 


transition : refund-delievered

   condition : virtual delivery | or refundable
   source : delivered
   state : refund-processing

transition : refund-processed

   state : refunded
   source : refund-processing
   

$Id$
"""

from zope.interface import implements
from zope import component

from hurry.workflow import interfaces as iworkflow
from hurry.workflow import workflow

from getpaid.core.interfaces import workflow_states, IShippableContent

import getpaid.core.workflow

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid')

def VirtualDeliverable( wf, context ):
    return not component.queryAdapter( IShippableContent, context ) is None

def create_item_workflow( ):

    its = workflow_states.item

    transitions = []
    add = transitions.append
    
    add( workflow.Transition(
        transition_id = 'create',
        title='Create',
        source = None,
        destination = its.NEW
        ) )

    add( workflow.Transition(
        transition_id = 'deliver-virtual',
        title=_(u'Electronic Delivery'),
        condition = VirtualDeliverable,
        trigger = iworkflow.SYSTEM,
        source = its.NEW,
        destination = its.DELIVER_VIRTUAL
        ) )    

    add( workflow.Transition(
        transition_id = 'cancel',
        title=_(u'Cancel'),
        source = its.NEW,
        destination = its.CANCELLED
        ) )    


    add( workflow.Transition(
        transition_id = 'refund',
        title=_(u'Refund'),
        source = its.DELIVER_VIRTUAL,
        destination = its.REFUNDING
        ) )

    add( workflow.Transition(
        transition_id = 'refund-processed',
        title=_(u'Refund Processed'),
        source = its.REFUNDING,
        trigger = iworkflow.SYSTEM,
        destination = its.REFUNDED
        ) )


    add( workflow.Transition(
        transition_id = 'ship',
        title=_(u'Ship'),
        source = its.NEW,
        trigger = iworkflow.SYSTEM,
        destination = its.SHIPPED
        ) )
    
    return transitions

class ItemWorkflow( workflow.Workflow ):

    def __init__( self ):
        super( ItemWorkflow, self).__init__( create_item_workflow())

ItemWorkflowAdapter = workflow.AdaptedWorkflow( ItemWorkflow() )

if __name__ == '__main__':
    wf = ItemWorkflow()
    print wf.toDot()


    
