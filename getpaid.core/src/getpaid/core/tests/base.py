"""Doc test runner
"""

__docformat__ = "reStructuredText"

import doctest
import unittest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import placelesssetup, ztapi

try:
    from zope.annotation import interfaces as annotation_interfaces
    from zope.annotation import attribute
except ImportError:
    # BBB for Zope 2.9
    from zope.app.annotation import interfaces as annotation_interfaces
    from zope.app.annotation import attribute

from hurry.workflow import interfaces

import random, string, datetime

from zope import component

from getpaid.core.interfaces import IOrder, IOrderManager, IOrderWorkflowLog, workflow_states
from getpaid.core import order, cart, item as line_item
from getpaid.core.workflow import store, order as oworkflow
from getpaid.core import payment

from Products.PloneGetPaid.browser.checkout import ContactInfo

class GetPaidTestCase( unittest.TestCase ):
    
    def setUp( self ):
        coreSetUp( )
        super(GetPaidTestCase, self).setUp()

    def tearDown( self ):
        placelesssetup.tearDown()

def createOrders( how_many=10 ):
    manager = component.getUtility( IOrderManager )

    for i in range(1, how_many):
        o = order.Order()
        o.order_id = str(i)

        o.shopping_cart = sc = cart.ShoppingCart()
        
        for i in range(0, 10):
            item = line_item.LineItem()
            item.name = "p%s"%random.choice( string.letters )
            item.quantity = random.randint(1,25)
            item.cost = random.randint(30, 100)
            item.item_id = "i%s"%random.choice( string.letters )
            if item.item_id in sc:
                continue
            sc[item.item_id] = item
            
        o.user_id = "u%s"%random.choice( string.letters )
        o.contact_information = ContactInfo()
        o.contact_information.email = "example@example.com"
        #o.finance_workflow.fireTransition('create')
        #o.fulfillment_workflow.fireTransition('create')
        
        manager.store( o )

        yield o

def coreSetUp( test=None ):
    placelesssetup.setUp()

    ###########################
    # order workflow
    ztapi.provideAdapter( IOrder,
                          interfaces.IWorkflowState,
                          oworkflow.FinanceState,
                          'order.finance')

    ztapi.provideAdapter( IOrder,
                          interfaces.IWorkflowState,
                          oworkflow.FulfillmentState,
                          'order.fulfillment')

    ztapi.provideAdapter( IOrder,
                          interfaces.IWorkflowInfo,
                          oworkflow.FinanceInfo,
                          'order.finance')

    ztapi.provideAdapter( IOrder,
                     interfaces.IWorkflowInfo,
                     oworkflow.FulfillmentInfo,
                    'order.fulfillment')
    
    ztapi.provideAdapter(annotation_interfaces.IAttributeAnnotatable,
                         annotation_interfaces.IAnnotations,
                         attribute.AttributeAnnotations)

    ztapi.provideUtility(interfaces.IWorkflow,
                         oworkflow.FulfillmentWorkflow(),
                        'order.fulfillment')
                        
    ztapi.provideUtility(interfaces.IWorkflow,
                        oworkflow.FinanceWorkflow(),
                        'order.finance')

    ztapi.provideUtility(interfaces.IWorkflowVersions,
                         store.StoreVersions())
    
    ztapi.provideUtility( IOrderManager, order.OrderManager() )

    ztapi.provideAdapter( IOrder, IOrderWorkflowLog, order.OrderWorkflowLog )

    ztapi.subscribe( (IOrder, interfaces.IWorkflowTransitionEvent), 
                       None, 
                       order.recordOrderWorkflow )

    ######################
    # product catalog

