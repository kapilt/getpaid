# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
product catalog
"""


from zope.index.field import FieldIndex
from zope.index.keyword  import KeywordIndex
from zope.app.intids.interfaces import IIntIds
from zope import component, interface
from persistent import Persistent

from getpaid.core import interfaces, catalog, options

def productModified( product, event ):
    products = component.getUtility( interfaces.IProductCatalog )
    products.reindex( product.uid, product )
    
def productDeleted( product, event ):
    products = component.getUtility( interfaces.IProductCatalog )
    products.unindex( product.uid, product )
    products[ product.uid ] = 'deleted'
    
class ProductBag( Persistent, options.PropertyBag): pass

ProductBag.initclass( interfaces.IPayable )

class ProductQuery( catalog.RecordQuery ):

    @classmethod
    def getStorage( cls ):
        catalog = component.getUtility( interfaces.IProductCatalog )
        return catalog

class ProductCatalog( catalog.IndexedRecords ):
    
    interface.implements( interfaces.IProductCatalog )
    
    index_map = dict(
         product_id = (FieldIndex, 'field'),
         categories = (KeywordIndex, 'key'),
         featured = (FieldIndex, 'field'),
         price = (FieldIndex, 'field'),
         deleted = (FieldIndex, 'field')
         )
         
    def __getitem__( self, key ):
        intids = component.getUtility( IIntIds )
        return intids.queryObject( int(key) ) or self[ key ]
        
    def values( self ):
        intids = component.getUtility( IIntIds )
        for k in self.keys():
            ob = intids.queryObject( int( k ) )
            if ob:
                yield ob
            else:
                yield self[ k ]
            
    def __setitem__( self, key, payable ):
        bag = ProductBag.frominstance( payable )
        super( ProductCatalog, self).__setitem__( key, bag )
