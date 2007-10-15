"""
$Id$
"""

from zope.interface import implements
from zope.app.event.objectevent import ObjectEvent
from zope.event import notify

import interfaces

class PayableCreationEvent( ObjectEvent ):

    implements( interfaces.IPayableCreationEvent )
    
    def __init__( self, object, payable, payable_interface ):
        super( PayableCreationEvent, self).__init__( object )
        self.payable = payable
        self.payable_interface = payable_interface

class BeforeCheckoutEvent( ObjectEvent ):
    
    def __init__( self, context, order, request):
        super( BeforeCheckoutEvent, self).__init__( order )
        self.request = request
        self.context = context

# we need to move the payable markers into getpaid
# def objectCreation( object, event ):
#     
#     if interfaces.IPayable.providedBy( object ):
#         notify( PayableCreationEvent( object, object, interfaces.IPayable ) )

        
        
    
    
    
    