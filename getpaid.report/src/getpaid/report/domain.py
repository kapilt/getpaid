
from sqlalchemy import orm

import schema


class Product( object ):
    """ """
    
orm.mapper( Product, schema.products )

class LogEntry( object ):
    """ """
    
orm.mapper( LogEntry, schema.order_log )

class Address( object ):
    """ """    

orm.mapper( Address, schema.addresses )
    
class LineItem( object ):
    """ """

orm.mapper( LineItem, schema.items )


class Order( object ):
    """ """    

orm.mapper(
    Order, schema.orders,
    properties={
      'log':orm.relation( LogEntry, backref='order' ),
      'items':orm.relation( LineItem, backref='order'),
      'shipping_address':orm.relation( Address, primaryjoin=(schema.orders.c.ship_id==schema.addresses.c.address_id)),
      'billing_address':orm.relation( Address, primaryjoin=(schema.orders.c.billing_id==schema.addresses.c.address_id)),      
      }
    )

class Customer( object ):
    """ """

orm.mapper(
    Customer, schema.customers,
    properties = {
       'orders':orm.relation( Order )
    }
    )

    
