"""
$Id: $



these views are directly ontop of the warehouse utility and its data, 
and for the sake of z2/plone.. manage context as needed via form 
variables. 

"""

import os

from getpaid.warehouse import interfaces, warehouse
from getpaid.warehouse.interfaces import _


from zope import component
from zope.formlib import form

from zc.table import column
from ore.viewlet.container import ContainerViewlet
from zExceptions import Redirect
from Products.Five.viewlet import manager
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PloneGetPaid.browser import base
from Products.PloneGetPaid.browser.widgets import CountrySelectionWidget, StateSelectionWidget
from Products.CMFPlone.utils import safe_unicode

from getpaid.core.payment import Address

class Container( BrowserView ):
    """ admin view on warehouse utility """
    

def warehouseURL( item, formatter ):
    return '<a href="@@pgp-view-warehouse?wid=%s">%s</a>'  % (item.__name__, safe_unicode(item.name))

    
class Listing( ContainerViewlet ):
    """ viewlet for managing contents """
    
    actions = ContainerViewlet.actions.copy()
    template = ViewPageTemplateFile('listing.pt')
    
    columns = [
        column.SelectionColumn( lambda item: item.name, name="selection"),
        column.GetterColumn( title=_(u"Name"), getter=warehouseURL )
       ]

    selection_column = columns[0]
        
    def getContainerContext( self ):
        return component.getUtility( interfaces.IWarehouseContainer )
    
    @form.action( _(u"Add") )
    def handle_add( self, action, data):
        self.request.response.redirect('@@pgp-add-warehouse')
        return
        
_prefix = os.path.dirname( base.__file__ )

manager_template = os.path.join( _prefix, "templates", "viewlet-manager.pt")
admin_template = os.path.join( _prefix, "templates", 'settings-page.pt')

ContainerVM = manager.ViewletManager(
                "ContainerVM", 
                interfaces.IWarehouseContainerVM,
                manager_template,
                )

class Add( base.BaseFormView ):
    """ add a warehouse """
    
    template = ViewPageTemplateFile( admin_template )
    
    form_fields = form.Fields( interfaces.IWarehouse )
    form_fields = form_fields.select('name') + form.Fields( interfaces.IAddress )

    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        self.widgets = form.setUpDataWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            ignore_request=ignore_request
            )

    @form.action( _(u"Add Warehouse"), condition=form.haveInputWidgets )
    def handle_add_warehouse( self, action, data ):
        adapters = { interfaces.IWarehouse : warehouse.Warehouse(),
                     interfaces.IAddress   : Address() }
                     
        form.applyChanges( self.context, self.form_fields, data, adapters )
        
        container = component.getUtility( interfaces.IWarehouseContainer )
        w = adapters[ interfaces.IWarehouse ]
        w.location = adapters[ interfaces.IAddress ]
        container[ w.name ] = w
        self.request.response.redirect('@@pgp-view-warehouse?wid=%s'% w.name )

class Edit( base.BaseFormView ):
    """ edit a warehouse """
    
    template = ViewPageTemplateFile( admin_template )
    
    form_fields = form.Fields( interfaces.IWarehouse )
    form_fields['name'].for_display = True
    
    form_fields = form.Fields( form_fields['name'], form.Fields( interfaces.IAddress ) )
    form_fields['state'].custom_widget = StateSelectionWidget
    form_fields['country'].custom_widget = CountrySelectionWidget    
    
    form_name = _(u'Warehouse Information')
                
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, 
            ignore_request=ignore_request
            )
            
    def update( self ):
        self.form_fields['name'].for_display = True
        wid = self.request.get('wid', None)
        container = component.getUtility( interfaces.IWarehouseContainer )
        if not wid or not wid in container:
            raise Redirect('@@pgp-warehouse-admin')
        w = container[ wid ]
        self.adapters = { interfaces.IWarehouse : w,
                          interfaces.IAddress   : w.location }
        self.hidden_form_vars = {'wid':wid}                          
        super( Edit, self).update()

class View( base.BaseFormView ):
    """ view a warehouse """
    
    template = ViewPageTemplateFile( admin_template )
    form_fields = form.Fields( interfaces.IWarehouse )
    form_fields = form.Fields( form_fields.select('name') + form.Fields( interfaces.IAddress ) )
        
    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters or {}
        self.widgets = form.setUpEditWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            adapters=self.adapters, for_display=True,
            ignore_request=ignore_request
            )

    def update( self ):
        wid = self.request.get('wid', None)
        container = component.getUtility( interfaces.IWarehouseContainer )
        if not wid or not wid in container:
            self.request.response.redirect('@@pgp-warehouse-admin')
        w = container[ wid ]
        self.adapters = { interfaces.IWarehouse : w,
                          interfaces.IAddress   : w.location }
        self.hidden_form_vars = {'wid':wid}
        super( View, self).update()
        self.form_name = \
                u'Warehouse Information (<a href="@@pgp-edit-warehouse?wid=%s">Edit</a>)'%wid

    def isOrdered( self ):
        return False