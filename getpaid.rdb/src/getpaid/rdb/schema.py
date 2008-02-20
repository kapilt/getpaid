
import sqlalchemy as rdb

metadata = rdb.MetaData()

order_ids = rdb.Sequence('order_id_seq', metadata=metadata)

orders = rdb.Table( 
  "orders",
  metadata,
  rdb.Column("order_rid",rdb.Integer(), order_ids, primary_key=True ),
  rdb.Column("billing_id", rdb.Integer,  rdb.ForeignKey('addresses.address_id'), nullable=False ),
  rdb.Column("ship_id", rdb.Integer, rdb.ForeignKey('addresses.address_id'), nullable=False ), 
  rdb.Column("customer_id", rdb.Integer, rdb.ForeignKey('customers.customer_id'), nullable=False ),
  rdb.Column("creation_date", rdb.DateTime(timezone=True) ),
  rdb.Column("finance_status", rdb.Unicode(20) ),
  rdb.Column("fulfillment_status", rdb.Unicode(20) )
  )
  
order_log = rdb.Table(
  "order_log",
  metadata,
  rdb.Column("log_id", rdb.Integer, primary_key=True),
  rdb.Column("order_id", rdb.Integer, rdb.ForeignKey('orders.order_id'), nullable=False ),
  rdb.Column("changed_by", rdb.Unicode(20) ),
  rdb.Column("change_date", rdb.DateTime( timezone=True) ),
  rdb.Column("chage_kind", rdb.Unicode(30) ),
  rdb.Column("comment", rdb.Unicode(90) ),  
  rdb.Column("new_state", rdb.String(20) ),
  rdb.Column("previous_state", rdb.String(20) ),  
  rdb.Column("transition", rdb.String(20) )
  )

items = rdb.Table( 
  "items",
  metadata,
  rdb.Column("item_id", rdb.Integer, primary_key=True ),
  rdb.Column("product_id", rdb.Integer, rdb.ForeignKey('products.product_id'), nullable=False  ),
  rdb.Column("product_code", rdb.Unicode(30), nullable=False), 
  rdb.Column("name", rdb.Unicode(30), nullable=False),
  rdb.Column("description", rdb.Unicode(100), nullable=False), 
  rdb.Column("cost", rdb.Float(precision=2), nullable=False ),
  rdb.Column("quantity", rdb.Integer, nullable=False)
  )
  
products = rdb.Table( 
  "products",
  metadata,
  rdb.Column("product_id", rdb.Integer, primary_key=True ),
  rdb.Column("product_code", rdb.Unicode(30), nullable=False ),
  rdb.Column("content_uid", rdb.Integer, nullable=False ),  # five.intid reference
  rdb.Column("type", rdb.String(30), nullable=False ),
  rdb.Column("price", rdb.Float(precision=2), nullable=False )
)

customers = rdb.Table( 
  "customers",
  metadata,
  rdb.Column('customer_id', rdb.Integer, primary_key=True),
  rdb.Column('name', rdb.Unicode(80), nullable=True),
  rdb.Column('phone_number', rdb.Unicode(15) ),
  rdb.Column('email', rdb.Unicode(30) ),
  rdb.Column('marketing_preference', rdb.Boolean, default=False ),
  rdb.Column('email_html_format', rdb.Unicode(5) )
  )
    
addresses = rdb.Table( 
  "addresses",
  metadata,
  rdb.Column("address_id", rdb.Integer, primary_key=True ),
  rdb.Column("first_line", rdb.Unicode(60), nullable=False ),
  rdb.Column("second_line", rdb.Unicode(60), nullable=False ),
  rdb.Column("city", rdb.Unicode(60), nullable=False ),
  rdb.Column("state", rdb.Unicode(6), nullable=False ),
  rdb.Column("country", rdb.Unicode(4), nullable=False ),
  rdb.Column("postal_code", rdb.Unicode(10) ),
  )
  
def main( ):
    db = rdb.create_engine('sqlite://')
    metadata.bind = db
    metadata.create_all()
    
if __name__ == '__main__':
    main()

