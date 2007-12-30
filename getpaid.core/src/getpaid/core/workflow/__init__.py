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

from hurry.workflow import workflow, interfaces
from cStringIO import StringIO

def toDot( self ):
    """
    export workflow as dot
    """
    io = StringIO()
    states = set()
    end_states = set()
    print >> io, "digraph workflow {"

    for state, transitions in self._sources.items():
        states.add( state )

        for tid, t in transitions.items():
            option = []
            states.add(  t.destination )
            if t.destination not in self._sources:
                end_states.add( t.destination )
            if t.trigger is interfaces.AUTOMATIC:
                option.append( 'color=green' )
            elif t.trigger is interfaces.SYSTEM:
                if not t.condition in (None, workflow.NullCondition):
                    option.append( 'color=yellow' )
                else:
                    option.append('color=blue')
            elif not t.condition in ( None, workflow.NullCondition):
                option.append( 'color=red' )
                 
            print >> io, '  %s -> %s [label="%s", %s];'%(t.source, t.destination, t.transition_id, ', '.join( option ) )
            
    for state in states:
        if state in end_states:
            print >> io, " %s [color=red];"%state
        else:
            print >> io, "  %s [shape=box ]; "%state
    print >> io, " }"

    return io.getvalue()


workflow.Workflow.toDot = toDot
