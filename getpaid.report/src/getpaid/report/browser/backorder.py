"""
$Id: $
"""

from Products.Five.browser import BrowserView
from zc.table import column, table
from getpaid.report import report
from getpaid.report.i18n import _


class BackorderReport( BrowserView ):

    report_name = _(u"Backordered Products")
    
    columns = [
        column.GetterColumn( title=_(u"Product Code"), getter=lambda i,f:i.date.strftime('%m/%d/%y') ),
        column.GetterColumn( title=_(u"Description"), getter=lambda i,f:'' ),
        column.GetterColumn( title=_(u"Total Backordered"), getter=lambda i,f:i.quantity ),
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
        

    
