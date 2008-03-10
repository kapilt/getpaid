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
