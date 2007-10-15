"""

very lightweight catalog implementation

"""


import datetime

from persistent.dict import PersistentDict
from zope.app.container.btree import BTreeContainer
from zope.app.intids.interfaces import IIntIds

from BTrees.IFBTree import weightedIntersection, intersection

class ResultSet:
    """Lazily accessed set of objects."""

    def __init__(self, uids, storage):
        self.uids = uids or []
        self.storage = storage

    def __len__(self):
        return len(self.uids)

    def __iter__(self):
        for uid in self.uids:
            yield self.storage[ str( uid ) ]

class IndexedRecords( BTreeContainer ):

    # define something like this for indexing and querying
    # 
    #index_map = { 'index_name' : ( Factory, query_method )}


    
    def __init__( self ):
        super( IndexedRecords, self).__init__()
        self.indexes = PersistentDict()
        self.setupIndexes()
        
    def setupCatalog( self):
        for index_name, (factory, query) in self.index_map:
            self.indexes[ index_name ] = factory
        
    def query( self, **args ):
        results = self.apply( args )        
        return ResultSet( results, self )

    def apply(self, query):
        results = []
        for index_name, index_query in query.items():
            index = self.indexes[index_name]
            r = index.apply(index_query)
            if r is None:
                continue
            if not r:
                # empty results
                return r
            results.append((len(r), r))

        if not results:
            # no applicable indexes, so catalog was not applicable
            return None

        results.sort() # order from smallest to largest

        _, result = results.pop(0)
        for _, r in results:
            _, result = weightedIntersection(result, r)

        return result
    
    def __setitem__( self, key, object):
        super( IndexedRecords, self ).__setitem__( key, object )
        self.index( key, object )

    def reset_index( self ):
        # reindex all orders
        for index in self.indexes.values():
            index.clear()
        for order in self.values():
            self.index( order )

    def reindex( self, key ):
        self.unindex( key )
        object = self[ key ]
        self.index( key, object )
            
    def index( self, key, object ):
        doc_id = int( key )
        for attr, index in self.indexes.items():
            value = getattr( object, attr, None)
            if callable( value ):
                value = value()
            if value is None:
                continue
            index.index_doc( doc_id, value )

    def unindex( self, key ):
        for index in self.indexes.values():
            index.unindex_doc( int( key ) )
        
    def __delitem__( self, key ):
        super( IndexedRecords, self).__delitem__( key )
        self.unindex( key )

    #################################
    # junk for z2.9 / f 1.4
    def manage_fixupOwnershipAfterAdd(self, *args):
        return

    def manage_setLocalRoles( self, *args ):
        return 

class RecordQuery( object ):
    """
    simple query construction.. it might be problematic for other storages without collapsing
    sort clauses where possible. best to minimize any query combinations in the released product.

    main interface to searching is the search method

    from getpaid.core.order import query
    from datetime import timedelta
    
    # find orders from the last week
    results = query.search( creation_date = timedelta(7) )

    """
    
    indexes =  [ 'finance_state',
                 'fulfillment_state',
                 'user_id',
                 'creation_date' ]
    default_sort = None
    @classmethod
    def search( cls, data=None, **kw ):
        """ take a dictionary of key, value pairs, and based on available queries/indexes
        construct query and return results """
        
        results = None
        if data is None:
            data = kw
        elif data and kw:
            data.update( kw )

        storage = cls.getStorage()
        indexes = [(name, query) for name, (f, query) in storage.index_map.items()]
        
        for term, query_method in indexes:
            term_value = data.get( term )
            if term_value is None:
                continue
            
            term_results = getattr( cls, query_method )( term, term_value )
            if term_results is None: # short circuit .. default and intersection
                return []
            if results is None:
                results = term_results
            else:
                results = cls.merge( results, term_results )

        # actualize to order objects
        results = cls.generate( results )

        if 'no_sort' in kw:
            return results        
        elif not storage.default_sort:
            return results
        return cls.sort( results, *storage.default_sort)
        
    @classmethod
    def generate( cls, results ):
        """ used to actualize results from ifsets to 
        """
        intids = cls.getIntIds()
        return ResultSet( results, intitds )

    @classmethod
    def getIntIds( self ):
        return component.getUtility( IIntIds )

    @staticmethod
    def sort( results, attribute, reverse=False ):
        results = list( results )
        results.sort( lambda x,y: cmp( getattr( x, attribute ), getattr( y, attribute ) ) )
        if reverse:
            results.reverse()
        return results

    @staticmethod
    def merge( *results  ):
        return reduce( intersection, [res for res in results if res is not None] )        
        
    @classmethod
    def date( cls, field_name, delta = None ):
        """ query by creation date, pass in either a delta to be used from the current time
            or a tuple of start date, end date to return orders from.
        """
        if not delta:  # default to one last week ?
            delta = datetime.timedelta(7)
        if isinstance( delta, tuple ):
            value = delta
        else:
            now = datetime.datetime.now()
            value = ( now-delta, now )
        storage = cls.getStorage()
        return storage.apply( { field_name : value } )
        

    @classmethod
    def field( cls, field_name, value ):
        storage = cls.getStorage()
        return storage.apply( { field_name : (value, value) } )
        

    @classmethod
    def getStorage( cls ):
        raise NotImplemented
