"""
$Id: $
"""

from zope import component
from zope.app.intid.interfaces import IIntIds
from sqlalchemy.orm import session
import sqlalchemy as rdb
import domain, schema

def product_history( product ):
    iid = component.getUtility( IIntIds ).queryId( product )
    s = session.Session()
    entries = s.query( domain.InventoryEntry ).select_from(
        schema.inventory.join( schema.products )
        ).filter( domain.Product.content_uid == iid
                  ).order_by( domain.InventoryEntry.date )
    return entries

_fulfillment_report = rdb.sql.text("""
select orders.creation_date,
       orders.order_zid,       
       item_orders.*
  from orders,
      (select order_id,
              count(*) as line_items,
              sum( items.quantity) as pieces
       from items group by order_id) as item_orders
  where orders.order_id = item_orders.order_id
    and orders.creation_date > :start_date
    and orders.creation_date < :end_date
  order by orders.creation_date desc
""")

def fulfillment_history( start_date, end_date ):
    connection = schema.metadata.bind.contextual_connect()
    results = connection.execute( _fulfillment_report,
                                  start_date = start_date,
                                  end_date = end_date )
    return list(results)

_fulfillment_report_summary = rdb.sql.text("""
select count( items ) as line_items,
       sum( quantity ) as pieces
  from items, orders
  where orders.creation_date > :start_date
    and orders.creation_date < :end_date  
""")

def fulfillment_summary( start_date, end_date ):
    connection = schema.metadata.bind.contextual_connect()
    results = connection.execute( _fulfillment_report_summary,
                                 start_date = start_date,
                                 end_date = end_date )
    return list(results)

def backorder_products( supplier_id ):
    s = session.Session()
    return s.query( domain.Product ).filter(
        domain.Product.stock_reserve < 0
        ).all() #.filter(
        #domain.Product.supplier_uid == supplier_id
        #).all()
    
    
    
