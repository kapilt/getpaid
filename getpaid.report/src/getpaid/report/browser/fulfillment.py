"""
$Id: $
"""

from PloneGetPaid.browser.base import BaseFormView

from zope import interface, schema
from zope.formlib import form

class IReportSettings( interface.Interface ):

    start_date = schema.Date( title=_(u"Start Date") )
    end_date = schema.Date( title=_(u"Start Date") )    

_fulfillment_report = """
select orders.creation_date,
       orders.order_zid,       
       item_orders.*
  from orders,
      (select order_id,
              count(*) as line_items,
              sum( items.quantity) as pieces
       from items group by order_id) as item_orders
  where orders.order_id = item_orders.order_id;
    and orders.creation_date > :start_date
    and orders.creation_date < :end_date
"""

_fulfillment_report_summary = """
select count( items ) as line_items,
       sum( quantity ) as pieces
  from items, orders
  where orders.creation_date > :start_date
    and orders.creation_date < :end_date  
"""
class FulfillmentReport( BaseFormView ):

    form_fields = form.Fields(  IReportSettings )

    def listing( self ):
        pass

    @form.action( _(u"Generate Report"), condition=form.haveInputWidgets )
    def generate_report( self, action, data ):
        pass
        
