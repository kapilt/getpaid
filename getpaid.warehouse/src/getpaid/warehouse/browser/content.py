"""
$Id: $
"""

from Products.Five.formlib import formbase    
from Products.PloneGetPaid.browser.content import PayableFormView

from zope.formlib import form
from zope.event import notify
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

        _modified = False
        if inventory.stock != data.get('stock', inventory.stock):
            # if we're adding to the current stock on hand we should
            # also increment the amount that can be ordered (includes unfufilled
            # orders ). we use reset store stock to the stock minus the
            # current delta between stock/storestock
            delta = inventory.stock - inventory.store_stock
            inventory.store_stock = data.get('stock') - delta

            # notify on change in stock levels 
            _modified = True            
            stock_delta = data.get('stock') - inventory.stock
            
        retvalue = super(ContentInventory, self).handle_edit_action.success_handler( self, action, data )

        if _modified:
            notify(
                interfaces.InventoryModified( inventory, self.context, stock_delta )
                )
            
        return retvalue
            
