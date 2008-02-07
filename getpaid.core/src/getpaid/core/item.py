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

$Id$
"""

from persistent import Persistent

from zope.interface import implements
from zope import component

try:
    from zope.annotation.interfaces import IAttributeAnnotatable
except ImportError:
    # BBB for Zope 2.9
    from zope.app.annotation.interfaces import IAttributeAnnotatable
from zope.app.intid.interfaces import IIntIds

from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from getpaid.core import interfaces


class LineItem( Persistent ):
    """
    an item in the cart

    lineitems are not generically attribute annotatable, which typically requires
    zodb persistence, instead to enable storage in other mediums, we use a specific
    limited set of components that use annotations on line items, specifically the
    workflow engine to enable fulfillment workflows on individual items.
    """
    implements( interfaces.ILineItem, IAttributeAnnotatable )

    
    # default attribute values, item_id is required and has no default
    name = ""
    description = ""
    quantity = 0
    cost = 0

    @property
    def fulfillment_state( self ):
        return IWorkflowState( self ).getState()

    @property
    def fulfillment_workflow( self ):
        return IWorkflowInfo( self )

class ShippableLineItem( LineItem ):
    
    implements( interfaces.IShippableLineItem )
    weight = ""
    um_weight = ""
    um_distance = ""
    length = ""
    height = ""
    width = ""

class PayableLineItem( LineItem ):
    """
    an item in the cart for a payable
    """
    implements( interfaces.IPayableLineItem )

    # required
    uid = None
    
    def resolve( self ):
        utility = component.getUtility( IIntIds )
        return utility.queryObject( self.uid )
        
class PayableShippableLineItem( ShippableLineItem, PayableLineItem ):
    """
    a shippable item in a cart for a payable
    """
