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
order utility implementation
"""
import decimal, datetime, random

from persistent import Persistent
from persistent.list import PersistentList
from persistent.dict import PersistentDict

from BTrees.IFBTree import weightedIntersection, intersection

from zope import component
from zope.interface import implements
from zope.index.field import FieldIndex
from zope.i18nmessageid import MessageFactory
from zope.index.keyword  import KeywordIndex
from zope.schema.fieldproperty import FieldProperty

from zope.app.container.btree import BTreeContainer
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo

try:
    from zope.annotation.interfaces import IAttributeAnnotatable
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    # BBB for Zope 2.9
    from zope.app.annotation.interfaces import IAttributeAnnotatable
    from zope.app.annotation.interfaces import IAnnotations

from getpaid.core import interfaces, cart

_ = MessageFactory('getpaid')

try:
    from AccessControl import getSecurityManager
except ImportError:
    getSecurityManager = None

class workflow_state( object ):
    
    def __init__(self, workflow_name ):
        self.workflow_name = workflow_name
        self.__doc__ = "workflow state %s"%workflow_name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self         
        return component.getAdapter( obj, IWorkflowState, self.workflow_name).getState()            

    def __set__(self, obj, value):
        return component.getAdapter( obj, IWorkflowState, self.workflow_name).setState( value )

    def __delete__(self, obj):
        raise AttributeError, "can't delete attribute"


class Order( Persistent, cart.CartItemTotals ):

    implements( interfaces.IOrder, interfaces.ILineContainerTotals, IAttributeAnnotatable )

    _order_id = None
    shipping_address = None
    billing_address = None
    shopping_cart = None
    processor_order_id = None
    user_id = None
    creation_date = None

    def __init__( self ):
        self.creation_date = datetime.datetime.now()

    def getOrderId( self ):
        return self._order_id

    def setOrderId( self, order_id):
        if self._order_id is not None:
            raise SyntaxError(_(u"Order Id already set"))
        if not order_id:
            raise TypeError(_(u"Invalid Order Id"))
        self._order_id = order_id

    order_id = property( getOrderId, setOrderId )

    finance_state = workflow_state( "order.finance")

    fulfillment_state = workflow_state( "order.fulfillment")


    def __len__( self ):
        return len(self.shopping_cart)

    @property
    def finance_workflow( self ):
        return component.getAdapter( self, IWorkflowInfo, "order.finance")

    @property
    def fulfillment_workflow( self ):
        return component.getAdapter( self, IWorkflowInfo, "order.fulfillment")

##     # ILineContainerTotals implementation
##     def getTotalPrice( self ):
##         if not self.shopping_cart:
##             return 0

##         total = 0
##         total += self.getSubTotalPrice()
##         total += self.getShippingCost()
##         total += self.getTaxCost()
        
##         return float( str( total ) )            

##     def getSubTotalPrice( self ):
##         if not self.shopping_cart:
##             return 0
##         total = 0
##         for item in self.shopping_cart.values():
##             d = decimal.Decimal ( str(item.cost ) ) * item.quantity
##             total += d        
##         return total
        
##     def getShippingCost( self ):
##         shipping_method = component.getUtility( interfaces.IShippingMethod )
##         return shipping_method.getCost( self )

##     def getTaxCost( self ):
##         tax_utility = component.getUtility( interfaces.ITaxUtility )
##         return tax_utility.getCost( self )


class OrderManager( Persistent ):

    implements( interfaces.IOrderManager )
    
    def __init__( self ):
        self.storage = OrderStorage()

    def store( self, order ):
        self.storage[ order.order_id ] = order
    
    def query( self, **kw ):
        return query.search( **kw )

    def get( self, order_id ):
        return self.storage.get( order_id )

    def newOrderId( self ):
        """
        Return an order id that has some kind of guarantee that it
        hasn't been used for an order before.
        """
        while 1:
            order_id = str( random.randint( 2**10, 2**30 ) )
            if self.get( order_id ) is None:
                break
        return order_id


    #################################
    # junk for z2.9 / f 1.4
    def manage_fixupOwnershipAfterAdd(self, *args):
        return

    def manage_setLocalRoles( self, *args ):
        return 


class OrderQuery( object ):
    """
    simple query construction.. it might be problematic for other storages without collapsing
    sort clauses where possible. best to minimize any query combinations in the released product.

    main interface to searching is the search method

    from getpaid.core.order import query
    from datetime import timedelta
    
    # find orders from the last week
    results = query.search( creation_date = timedelta(7) )

    """

    @staticmethod
    def search( data=None, **kw ):
        """ take a dictionary of key, value pairs, and based on available queries/indexes
        construct query and return results """
        
        results = None
        if data is None:
            data = kw
        elif data and kw:
            data.update( kw )
            
        for term in [ 'finance_state',
                      'fulfillment_state',
                      'user_id',
                      'creation_date' ]:
            term_value = data.get( term )
            if term_value is None:
                continue
            
            term_results = getattr( query, term )( term_value )
            if term_results is None: # short circuit .. default and intersection
                return []
            if results is None:
                results = term_results
            else:
                results = query.merge( results, term_results )

        # actualize to order objects
        results = query.generate( results )

        if 'no_sort' in kw:
            return results
        
        # reverse sort on creation date
        return query.sort( results, 'creation_date', reverse=True )
    
    @staticmethod
    def generate( results ):
        """ used to actualize results from ifsets to 
        """
        manager = component.getUtility( interfaces.IOrderManager )
        return ResultSet( results, manager.storage )

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
    
    @staticmethod
    def latest( delta = None ):
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
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( { 'creation_date': value } )

    creation_date = latest
    
    @staticmethod
    def finance_state( value ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( { 'finance_state':( value, value ) } )
    
    @staticmethod
    def fulfillment_state( value ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( {'fulfillment_state':( value, value ) } )        

    @staticmethod
    def products( *products ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( {'products':products } )
    
    @staticmethod
    def user_id( value ):
        manager = component.getUtility( interfaces.IOrderManager )
        return manager.storage.apply( {'user_id':( value, value ) } )                

query = OrderQuery

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

class OrderStorage( BTreeContainer ):

    def __init__( self ):
        super( OrderStorage, self).__init__()
        self.indexes = PersistentDict( {
            'products' : KeywordIndex(),
            'user_id'  : FieldIndex(),
            'processor_order_id' : FieldIndex(),
            'finance_state'   : FieldIndex(),
            'fulfillment_state' : FieldIndex(),
            'creation_date' : FieldIndex() 
            } )
        
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
        super( OrderStorage, self ).__setitem__( key, object )
        self.index( object )

    def reset_index( self ):
        # reindex all orders
        for index in self.indexes.values():
            index.clear()
        for order in self.values():
            self.index( order )

    def reindex( self, object ):
        self.unindex( object.order_id )
        self.index( object )
            
    def index( self, object ):
        doc_id = int( object.order_id )
        for attr, index in self.indexes.items():
            value = getattr( object, attr, None)
            if callable( value ):
                value = value()
            if value is None:
                continue
            index.index_doc( doc_id, value )

    def unindex( self, order_id ):
        for index in self.indexes.values():
            index.unindex_doc( int( order_id ) )
        
    def __delitem__( self, key ):
        super( OrderStorage, self).__delitem__( key )
        doc_id = int( key )
        self.unindex( doc_id )

class OrderWorkflowRecord( Persistent ):

    I = interfaces.IOrderWorkflowEntry
    FP = FieldProperty

    implements( interfaces.IOrderWorkflowEntry )

    changed_by = FP( I['changed_by'] )
    change_date = FP( I['change_date'] )
    comment = FP( I['comment'] )
    new_state = FP( I['new_state'] )
    previous_state = FP( I['previous_state'] )
    change_kind = FP(I['change_kind'])
    
    def __init__( self, **kw ):
        names = interfaces.IOrderWorkflowEntry.names()
        for k,v in kw.items():
            if k in names:
                self.__dict__[ k ] = v

class OrderWorkflowLog( object ):

    implements( interfaces.IOrderWorkflowLog )

    _store = None
    _key = "getpaid.order.auditlog"

    def __init__( self, context ):
        self.context = context

    def add( self, record ):
        self._storage().append( record )

    def _storage( self ):
        if self._store:
            return self._store

        annotation = IAnnotations( self.context )
        if annotation.has_key( self._key ):
            self._store = annotation[ self._key ]
        else:
            annotation[ self._key ] = self._store = PersistentList()
        return self._store

    def __iter__( self ):
        for record in self._storage():
            yield record


def recordOrderWorkflow( order, event ):

    data = {}

    if getSecurityManager is not None:
        data['changed_by'] = getSecurityManager().getUser().getId()

    data['change_date'] = datetime.datetime.now()
    data['new_state'] = event.destination
    data['previous_state'] = event.source
    data['transition'] = event.transition.title
    data['comment'] = event.comment

    # figure out which workflow it is to denote change kind
    if order.finance_state == event.destination:
        data['change_kind'] = _(u'Finance')
    else:
        data['change_kind'] = _(u'Fulfillment')
        
    audit_log = interfaces.IOrderWorkflowLog( event.object )
    audit_log.add( OrderWorkflowRecord( **data ) )


 
