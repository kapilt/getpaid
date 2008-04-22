# -*- coding=utf-8 -*-
"""
Recurrent payments utility implementation.

Exported classes:

RecurrentPaymentsManager, a class to store recurrent payable orders.

@author: Juan Pablo Giménez <jpg@rcom.com.ar>
@organization: ifPeople
@organization: Rcom
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

class RecurrentPaymentsManager( Persistent ):
    """
    Class to store recurrent payable orders.

    Public methods:
        store, Stores a recurrent order.
        query, Query recurrent orders.
        get, Gets an order by id.

    """

    implements( interfaces.IRecurrentPaymentsManager )

    def __init__( self ):
        self.storage = OrderStorage()

    def store( self, order ):
        """
        Stores a recurrent order.

        @type order: Order
        @param order: The order.

        Some tests now,
            >>> 1
            1

        """
        self.storage[ order.order_id ] = order

    def query( self, **kw ):
        """
        Query recurrent orders.

        Some tests now,
            >>> 1
            1

        """
        return query.search( **kw )

    def get( self, order_id ):
        """
        Gets an order by id.

        @type order_id: string
        @param order_id: The order id.

        Some tests now,
            >>> 1
            1

        """
        return self.storage.get( order_id )
