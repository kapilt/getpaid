from zope import interface
from getpaid.core import interfaces
from ore.alchemist import Session, container
from hurry.workflow.interfaces import IWorkflowState
import domain

def createRDBOrder( order ):
    rdb_order = domain.Order()
    return rdb_order
    
class WorkflowAttributeState( object ):
    
    interface.implements( IWorkflowState )
    
    _attribute = "_status"
    
    def __init__( self, context ):
        self.context = context
        
    def setState( self, state):
        setattr( self.context, self._attribute, state )
        
    def setId( self, id):
        return
        
    def getState( self ):
        return getattr( self.context, self._attribute )
        
    def getId( self ):
        return self.context.order_id
    
class FinanceState( object ):
    _attribute = "_finance_status"

class FulfillmentState( object ):
    _attribute = "_fufillment_status"
    
class ShoppingCart( container.PartialContainer ):
    
    def __setitem__( self, key, item ):
        super( ShoppingCart, self).__setitem__( key, item )        
        rid = self.__parent__.order_rid
        item.order_id = rid

class OrderManager( object ):
    
    interface.implements( interfaces.IOrderManager )
    
    def query( self, **query ):
        session = Session()
        return session.query( domain.Order ).all()
        
    def __contains__( self, oid ):
        session = Session()
        return session.query( domain.Order ).exists( order_id=oid )        

    def get( self, oid ):
        session = Session()
        return session.query( domain.Order ).get( oid )
        
    def store( self, order ):
        rdb_order = createRDBOrder( order )
        session = Session()
        session.save( rdb_order )

    def isValid( self, oid ):
        try:
            int(oid)
            return True
        except TypeError, ValueError:
            return False
        
    def newOrderId( self ):
        return domain.order_ids.execute()
        
    #################################
    # junk for z2.9 / f 1.4
    def manage_fixupOwnershipAfterAdd(self, *args):
        return

    def manage_setLocalRoles( self, *args ):
        return 
        
