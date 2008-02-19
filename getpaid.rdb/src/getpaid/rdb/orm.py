
from sqlalchemy import orm

import domain, schema

orm.class_mapper( domain.Order, schema.orders )
orm.class_mapper( domain.BillingAddress, schema.addresses )
#orm.class_mapper( domain.ShippingAddress, schema.addresses )
orm.class_mapper( domain.LineItem, schema.items )
#orm.class_mapper( domain.ShippableLineItem, schema.items )
orm.class_mapper( domain.OrderLogEntry, schema.order_log )