"""

$Id$
"""

from persistent import Persistent

from zope.interface import implements
from zope import component

try:
    from zope.annotation.interfaces import IAttributeAnnotatable
except ImportError:
    # BBB for Zope 2.9
    from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.app.intid.interfaces import IIntIds

from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from getpaid.core import interfaces


class LineItem( Persistent ):
    """
    an item in the cart

    lineitems are not generically attribute annotatable, which typically requires
    zodb persistence, instead to enable storage in other mediums, we use a specific
    limited set of components that use annotations on line items, specifically the
    workflow engine to enable fulfillment workflows on individual items.
    """
    implements( interfaces.ILineItem, IAttributeAnnotatable )

    
    # default attribute values, item_id is required and has no default
    name = ""
    description = ""
    quantity = 0
    cost = 0

    @property
    def fulfillment_state( self ):
        return IWorkflowState( self ).getState()

    @property
    def fulfillment_workflow( self ):
        return IWorkflowInfo( self )

    
class PayableLineItem( LineItem ):
    """
    an item in the cart for a payable
    """
    implements( interfaces.IPayableLineItem )

    # required
    uid = None
    
    def resolve( self ):
        utility = component.getUtility( IIntIds )
        return utility.queryObject( self.uid )
        
        
