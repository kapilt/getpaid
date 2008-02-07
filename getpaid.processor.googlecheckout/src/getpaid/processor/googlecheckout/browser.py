"""
$Id$
"""

from zope.app.publisher.browser import BrowserView

class GoogleCheckoutLink( BrowserView ):

    def __call__( self ):
        self.context.setup( self.request )
        
        return """\
        <form method="POST" action="%s">
          <input type="hidden" name="cart" value="%s">
          <input type="hidden" name="signature" value="%s">
          <input type="image" name="Google Checkout" alt="Fast checkout through Google"
                 src="http://sandbox.google.com/checkout/buttons/checkout.gif?merchant_id=1234567890&w=180&h=46&style=white&variant=text&loc=en_US"  height="46" width="180">
        </form>"""%( self.context.post_url,
                     self.context.encoded_order,
                     self.context.encoded_signature )


class GoogleCheckoutOptions( BrowserView ):
    """ Google Checkout Option Configuration
    """
    
        
