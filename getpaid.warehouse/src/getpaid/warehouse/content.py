

from getpaid.core import options
from getpaid.core import interfaces as icore

import interfaces

Inventory = options.PersistentOptions.wire( 
                "Inventory", 
                "getpaid.content.inventory",
                interfaces.IProductInventory 
                )


def handleNewOrder( order, event ):
    """
    keep track of the amount product we have on hand *MINUS* our 
    outstanding orders. ie. what product do we have to sell, if
    include unfufilled orders.
    
    what constitutes a new order, an order which 
    """
    for item in order.shopping_cart.values():
        if not ( icore.IShippableLineItem.providedBy( item ) 
                 and icore.IPayableLineItem.providedBy( item ) ):
            continue
            
        inventory = interfaces.IProductInventory( item.resolve() )
        inventory.store_stock -= item.quantity
            
def handleFufilledOrder( order, event ):
    """
    when we fufill an order we increment
    """            
    
    for item in order.shopping_cart.values():
        if not ( icore.IShippableLineItem.providedBy( item ) 
                 and icore.IPayableLineItem.providedBy( item ) ):
            continue
            
        payable = item.resolve() 
        if payable is None:
            return
            
        inventory = interfaces.IProductInventory( payable )
        inventory.store_stock += item.quantity        
        