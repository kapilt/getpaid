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
