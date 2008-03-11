"""
$Id: $
"""

from Products.Five.formlib import formbase    
from Products.PloneGetPaid.browser.content import PayableFormView

from zope.formlib import form
from getpaid.warehouse import interfaces
from getpaid.warehouse.interfaces import _

class ContentInventory( PayableFormView, formbase.EditForm ):
    
    form_fields = form.Fields( interfaces.IProductInventory )
    form_fields['store_stock'].for_display = True
    
    form_name = "Product Inventory"
    allowed = True
    
    @form.action(_("Apply"), condition=form.haveInputWidgets)
    def handle_edit_action(self, action, data):
        inventory = self.adapters[ interfaces.IProductInventory ]
        if inventory.stock != data.get('stock', inventory.stock):
            delta = inventory.stock - inventory.store_stock
            inventory.store_stock = data.get('stock') - delta
        return super(ContentInventory, self).handle_edit_action.success_handler( self, action, data )
