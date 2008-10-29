import random, sys

from persistent import Persistent
from zope import interface 
from zope.event import notify
from zope.security.management import getInteraction, NoInteraction
from zope.security.interfaces import Unauthorized
from zope.security.checker import CheckerPublic

from zope.app import zapi
try:
    from zope.annotation.interfaces import IAnnotations
except:
    from zope.app.annotation.interfaces import IAnnotations
    
from zope.app.container.contained import Contained

try:
    from zope.lifecycleevent import ObjectModifiedEvent
except ImportError:
    from zope.app.event.objectevent import ObjectModifiedEvent

try:    
    from zope.component.interfaces import ObjectEvent
except ImportError:
    from zope.app.event.objectevent import ObjectEvent

from zope import component
from hurry.workflow import interfaces
from hurry.workflow.interfaces import MANUAL, AUTOMATIC, SYSTEM
from hurry.workflow.interfaces import\
     IWorkflow, IWorkflowState, IWorkflowInfo, IWorkflowVersions, \
     IAdaptedWorkflow
from hurry.workflow.interfaces import\
     InvalidTransitionError, ConditionFailedError

def NullCondition(wf, context):
    return True

def NullAction(wf, context):
    pass

# XXX this is needed to make the tests pass in the absence of
# interactions..
def nullCheckPermission(permission, principal_id):
    return True

class Transition(object):

    def __init__(self, transition_id, title, source, destination,
                 condition=NullCondition,
                 action=NullAction,
                 trigger=MANUAL,
                 permission=CheckerPublic,
                 order=0,
                 **user_data):
        self.transition_id = transition_id
        self.title = title
        self.source = source
        self.destination = destination
        self.condition = condition
        self.action = action
        self.trigger = trigger
        self.permission = permission
        self.order = order
        self.user_data = user_data
        
    def __cmp__(self, other):
        return cmp(self.order, other.order)
    
class Workflow(Persistent, Contained):
    interface.implements(IWorkflow)
    
    def __init__(self, transitions):
        self.refresh(transitions)

    def _register(self, transition):
        transitions = self._sources.setdefault(transition.source, {})
        transitions[transition.transition_id] = transition
        self._id_transitions[transition.transition_id] = transition

    def refresh(self, transitions):
        self._sources = {}
        self._id_transitions = {}
        for transition in transitions:
            self._register(transition)
        self._p_changed = True
        
    def getTransitions(self, source):
        try:
            return self._sources[source].values()
        except KeyError:
            return []
        
    def getTransition(self, source, transition_id):
        transition = self._id_transitions[transition_id]
        if transition.source != source:
            raise InvalidTransitionError
        return transition

    def getTransitionById(self, transition_id):
        return self._id_transitions[transition_id]

    def dot(self):
        """
        Return the 'GraphViz Dot Language' representation of the workflow
        """
        states = [None]
        visited = set()
        num_transitions = 0
        out = ["digraph g {",
               "None [shape=doublecircle]"]
        while states:
            state = states.pop()
            for transition in self.getTransitions(state):
                num_transitions += 1
                dest = transition.destination
                if dest not in visited:
                    states.append(dest)
                    visited.add(dest)
                out.append('t%d [shape=none, label="%s"]' % (num_transitions,
                                                             transition.title))
                out.append('"%s" -> t%d -> "%s"' % (state, num_transitions, dest))
        out.append("}")

        return "\n".join(out)
        
class WorkflowState(object):
    
    interface.implements(IWorkflowState)

    workflow_state_key = "hurry.workflow.state"
    workflow_id_key  = "hurry.workflow.id"
    
    def __init__(self, context):
        # XXX okay, I'm tired of it not being able to set annotations, so
        # we'll do this. Ugh.
        from zope.security.proxy import removeSecurityProxy
        self.context = removeSecurityProxy(context)

    def initialize(self):
        wf_versions = zapi.getUtility(IWorkflowVersions)
        self.setId(wf_versions.createVersionId())
        
    def setState(self, state):
        if state != self.getState():
            IAnnotations(self.context)[ self.workflow_state_key ] = state
            
    def setId(self, id):
        # XXX catalog should be informed (or should it?)
        IAnnotations(self.context)[ self.workflow_id_key ] = id
        
    def getState(self):
        try:
            return IAnnotations(self.context)[ self.workflow_state_key ]
        except KeyError:
            return None

    def getId(self):
        try:
            return IAnnotations(self.context)[ self.workflow_id_key ]
        except KeyError:
            return None
            
class WorkflowInfo(object):

    interface.implements(IWorkflowInfo)

    def __init__(self, context):
        self.context = context

    def info( self, context = None ):
        if context is None:
            return IWorkflowInfo( self.context )
        return IWorkflowInfo( context )

    def state( self, context = None ):
        if context is None:
            return IWorkflowState( self.context )
        return IWorkflowState( context )
    
    def workflow( self ):
        return zapi.queryAdapter(self.context, IWorkflow) or zapi.getUtility(IWorkflow)
    
    def fireTransition(self, transition_id, comment=None, side_effect=None,
                       check_security=True):
        state = self.state()
        wf = self.workflow()
        # this raises InvalidTransitionError if id is invalid for current state
        transition = wf.getTransition(state.getState(), transition_id)
        # check whether we may execute this workflow transition
        try:
            interaction = getInteraction()
        except NoInteraction:
            checkPermission = nullCheckPermission
        else:
            if check_security:
                checkPermission = interaction.checkPermission
            else:
                checkPermission = nullCheckPermission
        if not checkPermission(
            transition.permission, self.context):
            raise Unauthorized(self.context,
                               'transition: %s' % transition_id, 
                               transition.permission)
        # now make sure transition can still work in this context
        if not transition.condition(self, self.context):
            raise ConditionFailedError
        # perform action, return any result as new version
        result = transition.action(self, self.context)
        if result is not None:
            if transition.source is None:
                self.state(result).initialize()
            # stamp it with version
            state = self.state( result )
            state.setId( self.state().getId() )

            # execute any side effect:
            if side_effect is not None:
                side_effect(result)
            event = WorkflowVersionTransitionEvent(result, self.context,
                                                   transition.source,
                                                   transition.destination,
                                                   transition, comment)
        else:
            if transition.source is None:
                self.state().initialize()
            # execute any side effect
            if side_effect is not None:
                side_effect(self.context)
            event = WorkflowTransitionEvent(self.context,
                                            transition.source,
                                            transition.destination,
                                            transition, comment)
        # change state of context or new object
        state.setState(transition.destination)
        notify(event)
        # send modified event for original or new object
        if result is None:
            notify(ObjectModifiedEvent(self.context))
        else:
            notify(ObjectModifiedEvent(result))
        return result

    def fireTransitionToward(self, state, comment=None, side_effect=None,
                             check_security=True):
        transition_ids = self.getFireableTransitionIdsToward(state)
        if not transition_ids:
            raise interfaces.NoTransitionAvailableError
        if len(transition_ids) != 1:
            raise interfaces.AmbiguousTransitionError
        return self.fireTransition(transition_ids[0],
                                   comment, side_effect, check_security)
        
    def fireTransitionForVersions(self, state, transition_id):
        id = self.state().getId()
        wf_versions = zapi.getUtility(IWorkflowVersions)
        for version in wf_versions.getVersions(state, id):
            if version is self.context:
                continue
            self.info( version ).fireTransition(transition_id)

    def fireAutomatic(self):
        for transition_id in self.getAutomaticTransitionIds():
            try:
                self.fireTransition(transition_id)
            except ConditionFailedError:
                # if condition failed, that's fine, then we weren't
                # ready to fire yet
                pass
            else:
                # if we actually managed to fire a transition,
                # we're done with this one now.
                return
            
    def hasVersion(self, state):
        wf_versions = zapi.getUtility(IWorkflowVersions)
        id = self.state().getId()
        return wf_versions.hasVersion(state, id)
    
    def getManualTransitionIds(self):
        try:
            checkPermission = getInteraction().checkPermission
        except NoInteraction:
            checkPermission = nullCheckPermission
        return [transition.transition_id for transition in
                sorted(self._getTransitions(MANUAL)) if
                transition.condition(self, self.context) and
                checkPermission(transition.permission, self.context)]

    def getSystemTransitionIds(self):
        # ignore permission checks
        return [transition.transition_id for transition in
                sorted(self._getTransitions(SYSTEM)) if
                transition.condition(self, self.context)]

    def getFireableTransitionIds(self):
        return self.getManualTransitionIds() + self.getSystemTransitionIds()
    
    def getFireableTransitionIdsToward(self, state):
        wf = self.workflow()
        result = []
        for transition_id in self.getFireableTransitionIds():
            transition = wf.getTransitionById(transition_id)
            if transition.destination == state:
                result.append(transition_id)
        return result
    
    def getAutomaticTransitionIds(self):
        return [transition.transition_id for transition in
                self._getTransitions(AUTOMATIC)]

    def hasAutomaticTransitions(self):
        # XXX could be faster
        return bool(self.getAutomaticTransitionIds())

    def _getTransitions(self, trigger):
        # retrieve all possible transitions from workflow
        wf = self.workflow()
        transitions = wf.getTransitions( self.state().getState() )
        # now filter these transitions to retrieve all possible
        # transitions in this context, and return their ids
        return [transition for transition in transitions if
                transition.trigger == trigger]

class AdaptedWorkflowBase( object ):
    pass
    
def AdaptedWorkflow( workflow ):
    """
    wraps a IWorkflow utility into an adapter for use as an adapted workflow
    """

    assert IWorkflow.providedBy( workflow )
    
    class AdaptedWorkflow( AdaptedWorkflowBase ):

        def __init__( self, context):
            self.context = context
            self.workflow = workflow

            for m in IWorkflow.names():
                setattr( self, m, getattr( workflow, m ) ) 

    interface.classImplements( AdaptedWorkflow, IWorkflow )
    interface.directlyProvides( AdaptedWorkflow,
                                interface.directlyProvidedBy( AdaptedWorkflow ) + IAdaptedWorkflow )
    return AdaptedWorkflow

def ParallelWorkflow( workflow, wf_name, register_for=None):
    """
    wraps an IWorkflow and constructs IWorkflowState and IWorkflowInfo
    adapters, if register_for is specified registers them with the component
    architecture. else registration needs to be done by hand for the given
    name for all three.

    workflow is assumed to be a utility unless it implements IAdaptedWorkflow
    """

    assert IWorkflow.providedBy( workflow )
    
    class _ParallelWorkflowState( WorkflowState ):
        workflow_state_key = "%s.state"%(wf_name)
        workflow_id_key = "%s.id"%(wf_name)

    class _ParallelWorkflowInfo( ParallelWorkflowInfo ):
        name = wf_name
        
    if not register_for:
        return [ workflow, _ParallelWorkflowState, _ParallelWorkflowInfo ]

    # when you have a few these, zcml registration can be tedious, try to optionally
    # automate some of the pain, even if only for the global site manager
    
    if IAdaptedWorkflow.providedBy( workflow ):
        component.provideAdapter( workflow, (register_for,), IWorkflow, wf_name )
    else:
        component.provideUtility( workflow, IWorkflow, wf_name )

    component.provideAdapter( _ParallelWorkflowInfo,
                              (register_for, ),
                              IWorkflowInfo,
                              wf_name )
    
    component.provideAdapter( _ParallelWorkflowState,
                              (register_for, ),
                              IWorkflowState,
                              wf_name )

    return [ workflow, _ParallelWorkflowState, _ParallelWorkflowInfo ]

class ParallelWorkflowInfo( WorkflowInfo ):

    name = "hurry"
    
    def info( self, context = None ):
        if context is None:
            return zapi.getAdapter( self.context, IWorkflowInfo, self.name )
        return zapi.getAdapter( context, IWorkflowInfo, self.name )        

    def state( self, context = None ):
        if context is None:
            return zapi.getAdapter( self.context, IWorkflowState, self.name )
        return zapi.getAdapter( context, IWorkflowState, self.name )
    
    def workflow( self ):
        return zapi.queryAdapter( self.context, IWorkflow, self.name ) \
               or zapi.getUtility(IWorkflow, self.name )

        
                    
class WorkflowVersions(object):
    interface.implements(IWorkflowVersions)

    def getVersions(self, state, id):
        raise NotImplementedError

    def getVersionsWithAutomaticTransitions(self):
        raise NotImplementedError

    def createVersionId(self):
        while True:
            id = random.randrange(sys.maxint)
            if not self.hasVersionId(id):
                return id
        assert False, "Shouldn't ever reach here"

    def hasVersion(self, state, id):
        raise NotImplementedError

    def hasVersionId(self, id):
        raise NotImplementedError

    def fireAutomatic(self):
        for version in self.getVersionsWithAutomaticTransitions():
            IWorkflowInfo(version).fireAutomatic()

class WorkflowTransitionEvent(ObjectEvent):
    interface.implements(interfaces.IWorkflowTransitionEvent)

    def __init__(self, object, source, destination, transition, comment):
        super(WorkflowTransitionEvent, self).__init__(object)
        self.source = source
        self.destination = destination
        self.transition = transition
        self.comment = comment

class WorkflowVersionTransitionEvent(WorkflowTransitionEvent):
    interface.implements(interfaces.IWorkflowVersionTransitionEvent)

    def __init__(self, object, old_object, source, destination,
                 transition, comment):
        super(WorkflowVersionTransitionEvent, self).__init__(
            object, source, destination, transition, comment)
        self.old_object = old_object
