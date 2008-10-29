"""

order<->post workflow handler.

responds to events on an order signaling the order has been paid for (charged) 
and posts changes back to the workflow of any job posts in the order. 

our postcondition for this handler is that the content should be published
we do this by calling out to the publish transition.

one invariant we should be careful about, if the order is already published, then its 
possible it was either already paid for and ordered twice. we really want a business rule
to fire on the orders so we can adjust items accordingly.
 

we don't model changes or transitions states, here, the checkout controller can do so if nesc.
 
"""

from Products.CMFCore.utils import getToolByName

from getpaid.core.interfaces import workflow_states

import interfaces

def handlePaymentReceived( order, event ):

    #
    if event.destination != workflow_states.order.finance.CHARGED:
        return
        
    for item in order.shopping_cart.values():
        ob = item.resolve()
        if interfaces.IJobPost.providedBy( ob ):
            workflow = getToolByName( ob, 'portal_workflow')
            state = workflow.getInfoFor( ob, 'review_state' )            
            if state == 'published':
                return
            workflow.doActionFor( ob, 'publish')
    
