##############################################################################
#
# Copyright (c) 2006-2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
zope transaction manager integration for sqlalchemy

$Id: manager.py 299 2008-05-23 20:31:48Z kapilt $
"""

from zope import interface

import transaction
import transaction.interfaces

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession


class SessionDataManager( object ):
    """
    a data manager facade for sqlalchemy sessions participating in
    zope transactions.    
    """
    
    interface.implements( transaction.interfaces.IDataManager )

    def __init__(self, session):
        self.session = session
        self.joined = False

    def _check( self ):
        return bool( self.session.new or self.session.deleted or self.session.dirty )
    
    def abort(self, transaction):
        self.session.joined = False
        if self.session.transaction:
            self.session.transaction.rollback()
        self.session.clear()
        
    def commit(self, transaction):
        if not self.session.transaction:
            self.session.begin()
        if self.session.autoflush:
            return
        self.session.flush()

    def tpc_vote(self, transaction):
        self.session.joined = False        
        self.session.transaction.commit()
        self.session.clear()
        
    def tpc_abort(self, transaction):
        self.session.joined = False                
        self.session.transaction.rollback()
        self.session.clear()
        
    def sortKey(self):
        return "100-alchemist"
    
    def null( self, *args, **kw): pass

    tpc_finish = tpc_begin = null

    def register( self ):
        txn = transaction.get()
        txn.join( self )


class TransactionScoped( ScopedSession ):
    def __call__( self, **kwargs ):
        session = super( TransactionScoped, self).__call__( **kwargs )
        if not session.joined:
            data_manager = SessionDataManager( session )
            data_manager.register()
            session.joined = True
        if not session.transaction:
            session.begin()
        return session

def _zope_session( session_factory ):
    # session factory
    class ZopeSession( session_factory ):
        joined = False
        def __init__( self, **kwargs ):
            super( ZopeSession, self).__init__( **kwargs )
    return ZopeSession

Session = TransactionScoped( _zope_session( sessionmaker( autoflush=True,
                                                          transactional=True ) ) )
        
        
