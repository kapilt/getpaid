
from sqlalchemy import orm

import schema

class Product( object ):
    """ """
    
class LogEntry( object ):
    """ """

class Address( object ):
    """ """    
    
class LineItem( object ):
    """ """

class Order( object ):
    """ """    

class Customer( object ):
    """ """

orm.mapper( Product, schema.products )    
orm.mapper( LogEntry, schema.order_log )
orm.mapper( Address, schema.addresses )
orm.mapper( LineItem, schema.items,
            properties={'product':orm.relation( Product ) } )

orm.mapper(
    Order, schema.orders,
    properties={
      'log':orm.relation( LogEntry, backref='order' ),
      'items':orm.relation( LineItem, backref='order'),
      'shipping_address':orm.relation( Address, primaryjoin=(schema.orders.c.ship_id==schema.addresses.c.address_id)),
      'billing_address':orm.relation( Address, primaryjoin=(schema.orders.c.billing_id==schema.addresses.c.address_id)),
      }
    )

orm.mapper(
    Customer, schema.customers,
    properties = {
       'orders':orm.relation( Order, backref='contact_information' )
    }
    )

    
