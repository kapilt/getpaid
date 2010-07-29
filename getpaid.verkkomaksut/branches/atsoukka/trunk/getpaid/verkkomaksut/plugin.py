"""
Payment Processor Plugin manager
"""

__version__ = "$Revision$"
# $Id$
# $URL$

from zope import component, interface
from getpaid.core.interfaces import IPluginManager, IPaymentProcessor

from getpaid.verkkomaksut import NAME, TITLE, DESCRIPTION
from getpaid.verkkomaksut import interfaces
from getpaid.verkkomaksut import verkkomaksut


class VerkkomaksutPluginManager( object ):
    """ A simple plugin manager, which  manages plugins as local persistent object """
    interface.implements( IPluginManager )

    name = NAME
    title = TITLE
    description = DESCRIPTION

    def __init__( self, context ):
        self.context = context

    def install( self ):
        """ Create and register payment processor as local persistent utility """
        sm = self.context.getSiteManager()
        util = sm.queryUtility( IPaymentProcessor, name=self.name)
        if util is None:
            payment_processor = verkkomaksut.VerkkomaksutProcessor()
            sm.registerUtility(component=payment_processor, provided=IPaymentProcessor,
                               name=self.name, info=self.description )
        
    def uninstall( self ):
        """ Delete and unregister payment processor local persistent utility """
        sm = self.context.getSiteManager()
        util = sm.queryUtility( IPaymentProcessor, name=self.name )
        if util is not None:
            sm.unregisterUtility(util, IPaymentProcessor, name=self.name )
            del util # Requires successful transaction to be effective

    def status( self ):
        """ Return payment processor utility registration status """
        sm = self.context.getSiteManager()
        return sm.queryUtility( IPaymentProcessor, name=self.name ) is not None

def storeInstalled( object, event ):
    """ Install at IStore Installation (e.g. when PloneGetPaid is installed) """
    return VerkkomaksutPluginManager( object ).install()
