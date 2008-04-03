
from sqlalchemy import orm

import domain, schema

orm.mapper( domain.Order, schema.orders )
orm.mapper( domain.BillingAddress, schema.addresses )
#orm.class_mapper( domain.ShippingAddress, schema.addresses )
orm.mapper( domain.LineItem, schema.items )
#orm.class_mapper( domain.ShippableLineItem, schema.items )
orm.mapper( domain.OrderLogEntry, schema.order_log )