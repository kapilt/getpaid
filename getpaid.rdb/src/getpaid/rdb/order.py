from zope import interface
from getpaid.core import interfaces

import domain

def createRDBOrder( order ):
    rdb_order = domain.Order()
    return rdb_order
    
class RDBOrderManager( object ):
    
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
        
