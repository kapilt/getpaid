"""
$Id: $
"""

from zope import component, interface
from getpaid.core.interfaces import IPluginManager
from getpaid.warehouse import interfaces 
from getpaid.warehouse import warehouse

class WarehousePlugin( object ):

    interface.implements( IPluginManager )
    
    title = "Warehouse/Inventory Management"
    description = ""
    
    def __init__(self, context ):
        self.context = context
        
    def install( self ):
        sm = self.context.getSiteManager()
        
        utility = sm.queryUtility( interfaces.IWarehouseContainer )
        
        if utility is not None:
            return

        warehouses = warehouse.WarehouseContainer()
         
        try:
            sm.registerUtility(component=warehouses, provided=interfaces.IWarehouseContainer )
        except TypeError:
            # BBB for Zope 2.9
            sm.registerUtility(interface=interfaces.IWarehouseContainer, utility=warehouses)
        
    def uninstall( self ):
        pass
        
    def status( self ):
        return component.queryUtility( interfaces.WarehouseContainer ) is not None
        
def storeInstalled( object, event ):
    return WarehousePlugin( object ).install()