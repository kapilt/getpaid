"""
$Id: $
"""

import unittest
 
from getpaid.report import subscriber, domain, schema
from getpaid.warehouse.interfaces import InventoryModified, InventoryOrderModified

from zope.app.intid.interfaces import IIntIds
from zope.app.testing import placelesssetup, ztapi
from getpaid.core.tests import base, generator

from sqlalchemy.orm import session

import sqlalchemy as rdb

def setUpReport( ):
    ztapi.provideUtility( IIntIds, generator.ProductIntId() )

class ReportTests(unittest.TestCase):
    
    def setUp(self):
        base.coreSetUp()
        setUpReport()
        schema.metadata.bind = rdb.create_engine( 'sqlite://')
        schema.metadata.create_all()

        # Set up some preconditions
        self.products = generator.ProductGenerator()
        self.orders   = generator.OrderGenerator()
        
        for i in range( 20 ):
            self.products.new()
            
    def tearDown(self):
        # Clean up after each test
        generator.ProductGenerator._products = {}
        self.order = None
        self.products = None
        placelesssetup.tearDown()
        schema.metadata.bind = None
        
    def test_orderSerialization(self):
        order = self.orders()
        subscriber.handleNewOrder( order, None )
        s = session.Session()
        _order = s.query( domain.Order ).filter(
            domain.Order.order_zid == order.order_id ).first()
        self.assertNotEqual( _order, None )
        self.assertEqual( len( order.shopping_cart ), len( _order.items ) )

    def test_inventoryModified( self ):
        product = self.products.new()
        inventory = generator.Mock()
        inventory.stock = 10
        inventory.store_stock = 7        
        
        
        event = InventoryModified(
            inventory,
            product,
            10
            )

        _entry = subscriber.handleInventoryModified( inventory, event )

        self.assertEqual( _entry.action, u"added")
        self.assertEqual( _entry.stock, 10 )
        self.assertEqual( _entry.quantity, 10 )
        self.assertEqual( _entry.product.content_uid, product.uid )
        
    def test_inventoryOrderModified( self ):

        order = self.orders()
        item = order.shopping_cart.values()[0]
        product = item.resolve()
        inventory = generator.Mock()
        inventory.stock = 10
        inventory.store_stock = 7        
        
        event = InventoryOrderModified(
            inventory,
            product,
            order,
            item.quantity 
            )

        # serialize the order
        _order = subscriber.handleNewOrder( order, None )

        # serialize the inventory modified event
        _entry = subscriber.handleInventoryOrderFulfilled( inventory, event )

        # verify serialization
        self.assertEqual( _order.order_id, _entry.order_id )
        self.assertTrue( isinstance(_entry.product_id, int ) )
        self.assertEqual( _entry.stock, inventory.stock )
        self.assertEqual( _entry.quantity, -item.quantity )
        
        
    def test_orderTransition( self ):
        order = self.orders()
        subscriber.handleNewOrder( order, None )        
        order.finance_workflow.fireTransition('create')
        order.fulfillment_workflow.fireTransition('create')
        subscriber.handleOrderTransition( order, None )

        s = session.Session()
        _order = s.query( domain.Order ).filter(
            domain.Order.order_zid == order.order_id ).first()
        self.assertNotEqual( _order, None )

        self.assertEqual( _order.finance_status, order.finance_state )
        self.assertEqual( _order.fulfillment_status, order.fulfillment_state )


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ReportTests))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

