"""
$Id: $
"""

from Products.Five.browser import BrowserView
from zc.table import column, table
from getpaid.report import report
from getpaid.report.i18n import _

#getpaid.report is too prone to find errors caused by the data on the sql db
#not being consistent with the data.fs so instead of lambda, we need to do
# methods with a more complex error control.

def description(item,f):
    resolved_item = item.resolve()
    if resolved_item:
        resolved_item = resolved_item.Title()
    return resolved_item or "Not Available"

class BackorderReport( BrowserView ):

    report_name = _(u"Backordered Products")
    
    columns = [
        column.GetterColumn( title=_(u"Product Code"), getter=lambda i,f:i.product_code ),
        column.GetterColumn( title=_(u"Description"), getter=description ),
        column.GetterColumn( title=_(u"Total Backordered"), getter=lambda i,f:abs(i.stock_reserve) ),
        ]

    def listing( self ):
        entries = report.backorder_products( supplier_id=None )
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
        

    
