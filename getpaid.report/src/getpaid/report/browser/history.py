"""
$Id: $
"""

from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from zc.table import column, table

from getpaid.report import report
from getpaid.report.i18n import _

def orderLink( item, formatter):
    if item.order_id is None:
        return item.action
    oid = item.order.order_zid
    resolved_product = item.product.resolve()
    if resolved_product is None:
        return u"Not Available"
    portal_absolute_url = getToolByName(item.product.resolve(),'portal_url').getPortalObject().absolute_url()
    return u'<a href="%s/@@admin-manage-order/%s/@@fulfillment">%s</a>'%(portal_absolute_url, oid, oid)

class ProductHistoryReport( BrowserView ):

    columns = [
        column.GetterColumn( title=_(u"Date"), getter=lambda i,f:i.date.strftime('%m/%d/%y') ),
        column.GetterColumn( title=_(u"Order Number"), getter=orderLink ),
        column.GetterColumn( title=_(u"Quantity"), getter=lambda i,f:i.quantity ),
        column.GetterColumn( title=_(u"On Hand"), getter=lambda i,f: i.stock ),        
        ]
    
    def listing( self ):
        entries = report.product_history( self.context )
        formatter = table.StandaloneFullFormatter(
            self.context,
            self.request,
            entries,
            prefix='form',
            visible_column_names = [c.name for c in self.columns],
            columns = self.columns
            )

        formatter.cssClasses['table'] = 'listing'
        return formatter()
    

            
        
    
