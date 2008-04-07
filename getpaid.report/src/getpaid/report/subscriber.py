from sqlalchemy.orm import session

import domain, sync

def handleInventoryModified( _inventory, event ):
    """
    when an inventory is modified, we record inventory adjustments to the database
    """
    def _( ):
        pass

    _interact( _ )

def handleInventoryOrderModified( _inventory, event ):
    """
    when an order is fufilled, we record inventory levels to the database
    """
    
    def _( ):
        pass

    _interact( _ )
    
def handleOrderTransition( _order, event ):
    """
    when an order is transition, we record the state changes to the database
    """
    def _( ):
        order = s.query( domain.Order ).filter(
            domain.Order.order_zid = _order.order_id ).first()
        if order is None:
            return
        sync.copyState( _order, order )
    _interact( _ )
        
def handleNewOrder( _order, event ):
    """
    when a new order is created, we serialize it do the database.
    """
    def _():
        order = domain.Order()
        sync.copyOrder( s, _order, order )
        return order
    _interact( _ )

def _interact( func ):
    s = session.Session()
    s.begin()

    try:
        value = func()
    except:
        s.rollback()
        raise
    else:
        if value is not None:
            s.save( value )
        s.commit()
