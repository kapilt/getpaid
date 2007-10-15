"""Integration test for notification sending
"""

import unittest
from Testing.ZopeTestCase import ZopeDocTestSuite
from utils import optionflags

from base import PloneGetPaidTestCase

class TestNotification(PloneGetPaidTestCase):

    def mySetup():
        """
        First some mockup:

        >>> from zope import component, interface

        >>> from Products.PloneGetPaid import interfaces
        >>> from Products.PloneGetPaid import notifications
        
        >>> membership = self.portal.portal_membership
        >>> membership.addMember('testmanager', 'secret',
        ...                     ['Member', 'Manager'], [])

        >>> component.provideAdapter( notifications.CustomerOrderNotificationTemplate, 
        ...                          (interface.Interface, ),
        ...                           interfaces.INotificationMailTemplate,
        ...                          'customer-new-order')
        >>> component.provideAdapter( notifications.MerchantOrderNotificationTemplate, 
        ...                          (interface.Interface, ),
        ...                           interfaces.INotificationMailTemplate,
        ...                          'merchant-new-order')

        >>> settings = interfaces.IGetPaidManagementOptions( self.portal)
        >>> settings.merchant_email_notification = 'notification'
        >>> settings.contact_email = 'merchant@foo.bar'
        """
        

    def sendNotification():
        """
        >>> from zope import interface
        >>> class Mock(object):
        ...     interface.implements(interface.Interface)
        ...     def __init__(self, *args, **kwargs):
        ...         for k, v in kwargs.items(): setattr(self, k, v)

        >>> order = Mock( user_id='testmanager',
        ...               getTotalPrice=lambda: 10,
        ...               order_id=1)

        >>> from getpaid.core.interfaces import workflow_states
        >>> finance = workflow_states.order.finance
        >>> event = Mock( source=finance.REVIEWING,
        ...               destination=finance.CHARGEABLE,
        ...               object=self.portal
        ...               )
        >>> from Products.PloneGetPaid.notifications import sendNotification
        >>> sendNotification( order, event)
        """

def test_suite():
    return unittest.TestSuite((
            ZopeDocTestSuite(test_class=TestNotification,
                             optionflags=optionflags),
        ))
