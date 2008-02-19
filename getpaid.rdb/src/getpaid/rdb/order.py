from zope import interface
from getpaid.core import interfaces

import domain

def createRDBOrder( order ):
    rdb_order = domain.Order()
    return rdb_order
    
class RDBOrderManager( object ):
    
    interface.implements( interfaces.IOrderManager )
    
    def store( self, order ):
        rdb_order = createRDBOrder( order )
        session = Session()
        session.save( rdb_order )
        
