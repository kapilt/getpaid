
from Products.Five.formlib import formbase    
from Products.PloneGetPaid.browser.base import BaseFormView
from zope.formlib import form
from getpaid.warehouse import interfaces

class ContentInventory( BaseFormView, formbase.EditForm ):
    
    form_fields = form.Fields( interfaces.IProductInventory )
    form_name = "Product Inventory"
    
