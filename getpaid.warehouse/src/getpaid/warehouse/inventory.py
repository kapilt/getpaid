
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
    
    what constitutes a new order, an order which is the chargeable 
    finance state.
    """
    
    if event.destination != icore.workflow_states.order.finance.CHARGEABLE:
        return

    if not event.source in ( icore.workflow_states.order.finance.REVIEWING, ):
        return 
            
    for item in order.shopping_cart.values():
        if not ( icore.IShippableLineItem.providedBy( item ) 
                 and icore.IPayableLineItem.providedBy( item ) ):
            continue

        payable = item.resolve()
        if payable is None:
            continue
        inventory = interfaces.IProductInventory( payable )
        inventory.store_stock -= item.quantity

def handleFufilledOrder( order, event ):
    """
    when we fufill an order we decrement, our on hand stock, to come 
    inline with our fufillment of this order.
    """            
    if not event.destination in ( 
        icore.workflow_states.order.fulfillment.DELIVERED,
        icore.workflow_states.order.fulfillment.WILL_NOT_DELIVER ):
        return
            
    for item in order.shopping_cart.values():
        if not ( icore.IShippableLineItem.providedBy( item ) 
                 and icore.IPayableLineItem.providedBy( item ) ):
            continue
            
        payable = item.resolve() 
        if payable is None:
            continue
            
        inventory = interfaces.IProductInventory( payable )
        inventory.stock -= item.quantity
        
