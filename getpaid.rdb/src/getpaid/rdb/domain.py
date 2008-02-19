from zope import interface
from getpaid.core import interfaces
from ore.alchemist import Session

import schema

class Order( object ):
    interface.implements( interfaces.IOrder )

class Address( object ):
    pass
    
class BillingAddress( Address ):
    interface.implements( interfaces.IBillingAddress )
    
class ShippingAddress( Address ):
    interface.implements( interfaces.IShippingAddress )
    
class LineItem( object ):
    interface.implements( interfaces.ILineItem )
    
class ShippableLineItem( object ):
    interfaces.implements( interfaces.IShippableLineItem )
    
class OrderLogEntry( object ):
    interface.implements( interfaces.IOrderWorkflowEntry )

class OrderLog( object ):
    interface.implements( interfaces.IOrderWorkflowLog )
        
    def __init__( self, context ):
        self.context = context
        
    def __iter__( self ):
        return iter( 
            session.query( OrderLogEntry ).filter( 
                    schema.order_log.c.order_id == self.context.order_id,
                    ).order_by( schema.order_log.c.creation_date ).all()
                    )
        
    def last( self ):
        session = Session()
        return session.query( OrderLogEntry ).filter( 
                schema.order_log.c.order_id == self.context.order_id,
                ).order_by( schema.order_log.c.creation_date ).one()
            
