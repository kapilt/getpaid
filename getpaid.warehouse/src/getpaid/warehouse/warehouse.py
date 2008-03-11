
from persistent import Persistent

from zope import interface
from zope.app.container.btree import BTreeContainer
from zope.app.container.contained import Contained

import interfaces

class WarehouseContainer( BTreeContainer ):
    
    interface.implements( interfaces.IWarehouseContainer )
    
class Warehouse( Persistent, Contained ):

    interface.implements( interfaces.IWarehouse )

    name = ""
