

from zope.app.testing import placelesssetup, ztapi
from zope.testing.doctestunit import DocFileSuite

import unittest
import doctest

from getpaid.core.workflow import order as oworkflow
from getpaid.core.interfaces import IOrderManager

from getpaid.rdb.interfaces import IRDBOrder
from getpaid.rdb.order import FinanceState, FulfillmentState, OrderManager
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo, IWorkflow

def coreSetUp( test=None ):
    placelesssetup.setUp()

    ###########################
    # order workflow
    ztapi.provideAdapter( IRDBOrder,
                          IWorkflowState,
                          FinanceState,
                          'order.finance')

    ztapi.provideAdapter( IRDBOrder,
                          IWorkflowState,
                          FulfillmentState,
                          'order.fulfillment')

    ztapi.provideAdapter( IRDBOrder,
                          IWorkflowInfo,
                          oworkflow.FinanceInfo,
                          'order.finance')

    ztapi.provideAdapter( IRDBOrder,
                          IWorkflowInfo,
                          oworkflow.FulfillmentInfo,
                          'order.fulfillment')

    ztapi.provideUtility( IWorkflow,
                          oworkflow.FulfillmentWorkflow(),
                          'order.fulfillment')
                        
    ztapi.provideUtility( IWorkflow,
                          oworkflow.FinanceWorkflow(),
                         'order.finance')

#    ztapi.provideUtility(interfaces.IWorkflowVersions,
#                         store.StoreVersions())
    
    ztapi.provideUtility( IOrderManager, OrderManager()  )

   # 
   # # ztapi.provideAdapter( IOrder, IOrderWorkflowLog, order.OrderWorkflowLog )
   # 
   #  ztapi.subscribe( (IOrder, interfaces.IWorkflowTransitionEvent), 
   #                     None, 
   #                     order.recordOrderWorkflow )

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('readme.txt',
                     setUp=coreSetUp,
                     tearDown=placelesssetup.tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),    
        DocFileSuite('order.txt',
                     setUp=coreSetUp,
                     tearDown=placelesssetup.tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),    
        ))      
