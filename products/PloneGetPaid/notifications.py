"""
email notifications for store admins and customers.
"""

from zope import component, interface
from getpaid.core.interfaces import workflow_states
from Products.CMFCore.utils import getToolByName

import interfaces

from DocumentTemplate.DT_HTML import HTML

from interfaces import _
from zope.i18n import translate

customer_new_order_template = '''\
To: ${to_email}
From: "${from_name}" <${from_email}>
Subject: New Order Notification

Thank you for you order.

Total Amount to be Charged : ${total_price}

You can view the status of your order here

${store_url}/@@getpaid-order/${order_id}

Order Contents

${order_contents}

'''

class CustomerOrderNotificationTemplate( object ):

    interface.implements( interfaces.INotificationMailTemplate )

    __call__ = customer_new_order_template

    def __call__( self, **kwargs):
        msg = _(customer_new_order_template, mapping=kwargs)
        return translate(msg)

    def __init__( self, order ):
        self.order = order

merchant_new_order_template = HTML('''\
To: ${to_email}
From: "${from_name}" <${from_email}>
Subject: New Order Notification

A New Order has been created

Total Cost: ${total_price}

To continue processing the order follow this link:
${store_url}/@@admin-manage-order/${order_id}/@@admin

Order Contents

${order_contents}

''')


class MerchantOrderNotificationTemplate( object ):

    interface.implements( interfaces.INotificationMailTemplate )

    __call__ = merchant_new_order_template
                                   
    def __init__( self, order ):
        self.order = order
        
def sendNotification( order, event ):
    """ sends out email notifications to merchants and clients based on settings.

    For now we only send out notifications when an order initially becomes
    chargeable. We may not raise or pass exceptions: the payment has already
    happened and everything else is our, not the customer's fault.
    """
    site = component.getSiteManager()
    try:
        portal = getToolByName(site, 'portal_url').getPortalObject()
    except AttributeError:
        # BBB for Zope 2.9
        portal = site.context
    mailer = getToolByName(portal, 'MailHost')
    
    if event.destination != workflow_states.order.finance.CHARGEABLE:
        return
    
    if not event.source in ( workflow_states.order.finance.REVIEWING,
                             workflow_states.order.finance.PAYMENT_DECLINED ):
        return 
    
    settings = interfaces.IGetPaidManagementOptions( portal )

    store_url = portal.absolute_url()

    order_contents = [u' '.join((cart_item.name, 
                                 u"%0.2f" % (cart_item.cost,),
                                 str(cart_item.quantity),
                               )) for cart_item in order.shopping_cart.values()]
    
    if settings.merchant_email_notification == 'notification' \
       and settings.contact_email:

        template = component.getAdapter(  order, interfaces.INotificationMailTemplate, "merchant-new-order")
        message = template( to_email = settings.contact_email,
                            from_name = settings.store_name,
                            from_email = settings.contact_email,
                            total_price = order.getTotalPrice(),
                            store_url = store_url,
                            order_id = order.order_id,
                            order_contents = order_contents,
                            )
        try:
            mailer.send( str(message) )
        except:
            # Something happened and most probably we weren't able to send the
            # message. That's bad, but we got the money already and really
            # should do the shipment
            # XXX: somebody should be notified about that
            pass


    if settings.customer_email_notification == 'notification' \
       and order.user_id:
        
        member = portal.portal_membership.getMemberById( order.user_id )

        if member.getProperty('email'):
            template = component.getAdapter( order, interfaces.INotificationMailTemplate, "customer-new-order")
            message = template( to_email = member.getProperty('email'),
                                from_name = settings.store_name,
                                from_email = settings.contact_email,
                                total_price = order.getTotalPrice(),
                                store_url = store_url,
                                order_id = order.order_id,
                                order_contents = order_contents,
                                )
            try:
                mailer.send( str(message) )
            except:
                # Something happened and most probably we weren't able to send the
                # message. That's bad, but we got the money already and really
                # should do the shipment
                # XXX: somebody should be notified about that
                pass

    
    


