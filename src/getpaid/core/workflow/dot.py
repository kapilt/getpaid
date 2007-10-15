

import order
import item
import shipment

import os

fh = open( os.path.join( os.path.dirname( order.__file__), 'order-finance.dot' ), 'w' )
fh.write( order.FinanceWorkflow().toDot() )
fh.close()

fh = open( os.path.join( os.path.dirname( order.__file__), 'order-fulfillment.dot'), 'w' )
fh.write( order.FulfillmentWorkflow().toDot() )
fh.close()

fh = open( os.path.join( os.path.dirname( order.__file__), 'item.dot'  ), 'w' )
fh.write( item.ItemWorkflow().toDot() )
fh.close()

fh = open( os.path.join( os.path.dirname( order.__file__), 'shipment.dot'  ), 'w' )
fh.write( shipment.ShipmentWorkflow().toDot() )
fh.close()

