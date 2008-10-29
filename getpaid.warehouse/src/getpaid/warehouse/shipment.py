"""
$Id: $
"""

from zope.app.container.ordered import OrderedContainer
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from datetime import datetime
from persistent import Persistent

from getpaid.core import interfaces

class OrderShipments( OrderedContainer ):

    implements( interfaces.IShipmentContainer )

class Shipment( OrderedContainer ):

    implements( interfaces.IShipment )

    tracking_code = FieldProperty( interfaces.IShipment['tracking_code'] )
    service_code = FieldProperty( interfaces.IShipment['service_code'] )
    service_name = FieldProperty( interfaces.IShipment['service'] )
    shipping_cost = FieldProperty( interfaces.IShipment['shipping_cost'] )

    creation_date = FieldProperty( interfaces.IShipment['creation_date'] )

    def __init__( self ):
        self.creation_date = datetime.now()
        super( Shipment, self).__init__()
    
    


    
