
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from zope import interface, schema

from getpaid.core import interfaces
from zope.app.container.sample import SampleContainer
from zope.app.container.constraints import contains
from zope.app.container.interfaces import IContainer

class IAddressBookUtility( interface.Interface ):
    """
    only available for authenticated users.
    """

    def get( uid ):
        """
        """
        
    def destroy( uid ):
        """
        """
        
class IAddressBook( IContainer ):
    
    contains( interfaces.IAbstractAddress )
    
class INamedAddress( interface.Interface ):
    
    schema.TextLine(title=u"Name")
    
def AddressBook( SampleContainer ):
    
    interface.implements( interfaces.IAddressBook )

class AddressBookUtility( Persistent ):

    interface.implements( IAddressBookUtility )
    
    def __init__( self ):
        self._addresses = OOBTree()

    def get( self, uid, create=True ):
        if not self._addresses.has_key( uid ):
            if not create:
                return
            self._addresses[ uid ] = book = AddressBook()
            book.__name__ = uid
        return self._addresses[ uid ]
        
    def destroy( self, uid ):
        if not self._addresses.has_key( uid ):
            return
        del self._addresses[ uid ]
        
    def manage_fixOwnershipAfterAdd( self ): pass
    
