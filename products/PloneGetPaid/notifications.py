"""
email notifications for store admins and customers.
"""

from zope import component, interface
from getpaid.core.interfaces import workflow_states

import interfaces

from DocumentTemplate.DT_HTML import HTML


customer_new_order_template = HTML('''\
To: <dtml-var to_email>
From: "<dtml-var "store_settings.store_name">" <<dtml-var from_email>>
Subject: New Order Notification

Thank you for you order.

Total Amount to be Charged : <dtml-var "order.getTotalPrice()">

You can view the status of your order here

<dtml-var store_url>/@@getpaid-order/<dtml-var "order.order_id">

Order Contents

<dtml-in "order.shopping_cart.values()">
 <dtml-with sequence-item>
   <dtml-var "resolve().Title()"> <dtml-var cost> <dtml-var quantity>
  </dtml-with>
</dtml-in>

''')

class CustomerOrderNotificationTemplate( object ):

    interface.implements( interfaces.INotificationMailTemplate )

    __call__ = customer_new_order_template

    def __init__( self, order ):
        self.order = order

merchant_new_order_template = HTML('''\
To: <dtml-var to_email>
From: "<dtml-var "store_settings.store_name">" <<dtml-var from_email>>
Subject: New Order Notification

A New Order has been created

Total Cost: <dtml-var "order.getTotalPrice()">

To continue processing the order this order follow this link.
<dtml-var store_url>/@@admin-manage-order/<dtml-var "order.order_id">/@@admin

Order Contents

<dtml-in "order.shopping_cart.values()">
 <dtml-with sequence-item>
   <dtml-var "resolve().Title()"> <dtml-var cost> <dtml-var quantity>
  </dtml-with>
</dtml-in>

''')


class MerchantOrderNotificationTemplate( object ):

    interface.implements( interfaces.INotificationMailTemplate )

    __call__ = merchant_new_order_template
                                   
    def __init__( self, order ):
        self.order = order
        
def sendNotification( order, event ):
    """ sends out email notifications to merchants and clients based on settings.

    for now we only send out notifications when an order initially becomes chargeable
    """
    site = component.getSiteManager()
    portal = site.context
    mailer = portal.MailHost
    
    if event.destination != workflow_states.order.finance.CHARGEABLE:
        return
    
    if not event.source in ( workflow_states.order.finance.REVIEWING,
                             workflow_states.order.finance.PAYMENT_DECLINED ):
        return 
    
    settings = interfaces.IGetPaidManagementOptions( portal )

    store_url = portal.absolute_url()
    
    if settings.merchant_email_notification == 'notification' \
       and settings.contact_email:

        template = component.getAdapter( interfaces.INotificationMailTemplate, order, "merchant-new-order")
        message = template( to_email = settings.contact_email,
                            from_email = settings.contact_email,
                            store_settings = settings,
                            store_url = store_url,
                            order = order )
        
        mailer.send( str(message) )

    if settings.customer_email_notification == 'notification' \
       and order.user_id:
        
        member = portal.portal_membership.getMemberById( order.user_id )

        if member.getProperty('email'):
            template = component.getAdapter( interfaces.INotificationMailTemplate, order, "customer-new-order")
            message = template( to_email = member.getProperty('email'),
                                from_email = settings.contact_email,
                                store_settings = settings,
                                store_url = store_url,
                                order = order )
            mailer.send( str(message) )

    
    


