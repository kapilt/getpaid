
from getpaid.core import options
from getpaid.core import interfaces as icore
from zope.event import notify

import interfaces, shipment

Inventory = options.PersistentOptions.wire( 
                "Inventory", 
                "getpaid.content.inventory",
                interfaces.IProductInventory 
                )

def handleNewOrder( order, event ):
    """
    keep track of the amount product we have on hand *MINUS* our 
    outstanding orders. ie. what product do we have to sell, 
    including our unfufilled orders.
    
    what constitutes a new order, an order which is the chargeable 
    finance state.

    attaches shipments to a new shippable order
    """
    
    if event.destination != icore.workflow_states.order.finance.CHARGEABLE:
        return

    if not event.source in ( icore.workflow_states.order.finance.REVIEWING, ):
        return 

    if icore.IShippableOrder.providedBy( order ):
        order.shipments = shipment.OrderShipments()
            
    for item in order.shopping_cart.values():
        if not ( icore.IShippableLineItem.providedBy( item ) 
                 and icore.IPayableLineItem.providedBy( item ) ):
            continue

        payable = item.resolve()
        if payable is None:
            continue
        
        inventory = interfaces.IProductInventory( payable )
        inventory.store_stock -= item.quantity
        
        if inventory.store_stock < 0 and (inventory.store_stock + item.quantity) >= 0:
            notify( interfaces.InventoryBackordered( inventory, payable ) )

        notify(
            interfaces.InventoryAvailabilityModified( inventory, payable, order, item.quantity )
            )

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

        notify(
            interfaces.InventoryOrderFulfilled( inventory, payable, order, item.quantity )
            )
            
        
