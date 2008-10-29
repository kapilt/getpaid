"""
$Id: $
"""

from Products.PloneGetPaid.browser.base import BaseFormView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from zope import interface, schema
from zope.formlib import form
from zc.table import column, table
from getpaid.report import report
from getpaid.report.i18n import _

class IReportSettings( interface.Interface ):
    start_date = schema.Date( title=_(u"Start Date") )
    end_date = schema.Date( title=_(u"End Date") )    

def orderLink( item, formatter):
    oid = item['order_zid']
    return u'<a href="@@admin-manage-order/%s/@@fulfillment">%s</a>'%( oid, oid )

class FulfillmentReport( BaseFormView ):

    form_description=_(u"Select the dates to view the fulfilled orders. Date Format is YYYY-MM-DD")
    form_fields = form.Fields(  IReportSettings )
    template = ZopeTwoPageTemplateFile('fulfillment.pt')
    
    entries = ()

    columns = [
        column.GetterColumn( title=_(u"Date"), getter=lambda i,f:i['creation_date'].strftime('%m/%d/%y') ),
        column.GetterColumn( title=_(u"Order Number"), getter=orderLink ),
        column.GetterColumn( title=_(u"Line Items"), getter=lambda i,f:i['line_items'] ),
        column.GetterColumn( title=_(u"Packages"), getter=lambda i,f: 1 ),
        column.GetterColumn( title=_(u"Pieces"), getter=lambda i,f: i['pieces'] )
        ]

    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        self.widgets = form.setUpDataWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            ignore_request=ignore_request
            )

    def listing( self ):
        formatter = table.StandaloneFullFormatter(
            self.context,
            self.request,
            self.entries,
            prefix='form',
            visible_column_names = [c.name for c in self.columns],
            columns = self.columns
            )
        formatter.cssClasses['table'] = 'listing'
        return formatter()

    @form.action( _(u"Generate Report"), condition=form.haveInputWidgets )
    def generate_report( self, action, data ):
        self.entries = report.fulfillment_history( data['start_date'], data['end_date'] )
        self.summary = report.fulfillment_summary( data['start_date'], data['end_date'] )
        
                                                   
        
