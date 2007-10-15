"""

workflow event driven payment processor integration and property bags needed for
an order.
"""

from getpaid.core import interfaces, options 
from zope import component, interface

class ShippingAddress( options.PersistentBag ):
    
    interface.implements( interfaces.IShippingAddress )
    schema = interfaces.IShippingAddress
    
class BillingAddress( options.PersistentBag ):

    interface.implements( interfaces.IBillingAddress )
    schema = interfaces.IBillingAddress
    
class ContactInformation( options.PersistentBag ):
    
    interface.implements( interfaces.IUserContactInformation )
    schema = interfaces.IUserContactInformation
    
def fireAutomaticTransitions( order, event ):    
    """ fire automatic transitions for a new state """ 
    order.finance_workflow.fireAutomatic()


def processorWorkflowSubscriber( order, event ):
    """
    fire off transition from charging to charged or declined based on
    payment processor interaction.
    """

    # check for a payment processor associated with the 
    # there is a default notion here that the workflows for finance / fulfillment can't share state names
    # 
    if order.finance_state == event.destination:
        adapter = component.queryMultiAdapter( (order, order.finance_workflow.workflow() ),
                                               interfaces.IWorkflowPaymentProcessorIntegration )
                                               
    elif order.fulfillment_state == event.destination:
        adapter = component.queryMultiAdapter( (order, order.fulfillment_workflow.workflow() ),
                                               interfaces.IWorkflowPaymentProcessorIntegration )
    else:
        return
                                              
    if adapter is None:
        return

    return adapter( event )

class DefaultFinanceProcessorIntegration( object ):
    
    interface.implements( interfaces.IWorkflowPaymentProcessorIntegration )
    
    def __init__( self, order, workflow):
        self.order = order
        self.workflow = workflow
        
    def __call__( self, event ):
        if event.destination != interfaces.workflow_states.order.finance.CHARGING:
            return

        # ick.. get a hold of the store
        # this is a little gross, we need some access to context, so we fetch line items
        # till we find something that resolves to an object, and try to get the store from that
        # 
        context = component.queryUtility( interfaces.IStore )
        if context is None:
            from Products.CMFCore.utils import getToolByName
            ob = None
            for i in self.order.shopping_cart.values():
                if interfaces.IPayableLineItem.providedBy( i ):
                    ob = i.resolve()
            if ob is None:
                raise AttributeError("can't get store, TODO - please switch processors settings to utility adapters")
            context = getToolByName( ob, 'portal_url').getPortalObject()

        processor = component.getAdapter( context,
                                          interfaces.IPaymentProcessor,
                                          self.order.processor_id )

        result = processor.capture( self.order, self.order.getTotalPrice() )
    
        if result == interfaces.keys.results_async:
            return
        elif result == interfaces.keys.results_success:
            self.order.finance_workflow.fireTransition('charge-charging')
        else:
            self.order.finance_workflow.fireTransition('decline-charging', comment=result)
