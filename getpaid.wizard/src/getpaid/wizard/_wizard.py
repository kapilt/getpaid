from zope import interface, schema, component
try:
    from zope.publisher.browser import IBrowserView
except ImportError:
    #plone2.5 compatibility
    from zope.app.publisher.interfaces.browser import IBrowserView
from zope.formlib import form

from getpaid.core import interfaces as coreinterfaces

import interfaces

class Wizard( object ):

    interface.implements( interfaces.IWizard, IBrowserView  )
    
    def __init__( self, context, request ):
        self.context = context
        self.request = request

        # TODO query portal settings in pgp subclass
        self.controller = interfaces.IWizardController( self )
        self.data_manager = interfaces.IWizardDataManager( self )
        
    def update( self ):
        self.data_manager.update()        
        self.controller.update()
                
    def render( self ):
        current_step = self.controller.getCurrentStep()
        current_step.setExportedVariables(
            self.data_manager.getFormVariables()
            )
        return current_step.render()

    def __call__( self ):
        self.update()
        return self.render()


class DataManager( object ):
    
    interface.implements( interfaces.IWizardDataManager )
    
    def __init__( self, wizard ):
        self.wizard = wizard
        self.controller = wizard.controller
        self._state = {}
        self._adapters = None

    def __setitem__( self, k, v ):
        self._state[k] = v
    
    def __delitem__( self, k ):
        if k in self._state:
            del self._state[ k ]
            
    def get( self, k ):
        return self._state.get( k )
        
    def update( self ):
        """
        """
        self._adapters, self._fields = None, None
        self._extractRequestVariables()
        
    def reset( self ):
        """ certain state operations like resetting the form variables are useful when resetting the form
        under error conditions to reset the step
        """
        # not meaningful in a form request scenario, a redirect will destroy state, but useful for impl
        # that use persistent server state
        self._state = {}
        
    @property
    def form_state( self ):
        return self._state
    
    def getFormVariables( self ):
        return self.form_state
        
    @property
    def adapters( self ):
        """
        adapter objects always have their values recalculated
        from the request form values and validated. we cache
        for the request lifecycle. callers can modify to
        maintain state through the request.
        """
        # process though. its a bit expensive
        if self._adapters:
            return self._adapters
        self._adapters, self._fields = self._extractDataManagers()
        return self._adapters
        
    @property
    def fields( self ):
        if self._fields is not None:
            return self._fields
        self._adapters, self._fields = self._extractDataManagers()
        return self._fields
        
    def _extractDataManagers( self ):
        # we extract object values from the request for 
        # conveinent use by any step.
        data_adapters = {}
        fields = form.Fields()
        for step in self.controller.getTraversedFormSteps():
            if not interfaces.IWizardFormStep.providedBy( step ):
                continue
            data_adapters.update( step.getSchemaAdapters() )
            
            widgets = form.setUpEditWidgets(
                step.form_fields,
                step.prefix,
                step.context,
                step.request,
                adapters = data_adapters,
                ignore_request = False
                )
            fields += step.form_fields 
            data = {}
            form.getWidgetsData( widgets, step.prefix, data )
            
            # extract the form data to the adapters actualize
            # their state.
            self._restoreAdapterValues( data, data_adapters )
        
        return data_adapters, fields
        
    def _restoreAdapterValues( self, data, adapters ):
        for iface, adapter in adapters.items():
            for name, field in schema.getFieldsInOrder( iface ):
                if name in data:
                    field.set( adapter, data[ name ] )

    def _extractRequestVariables( self ):
        """
        extract all form variables in the request, except those belonging
        to the current step.
        """
        step = self.controller.getCurrentStep()
        passed = {}
        ignore = [ ]
        if 'cur_step' in self._state:
            ignore.append( 'cur_step' )
        
        # we don't carry forward actions
        ignore.append( "%s.actions"%(step.prefix) )
        
        for f in step.form_fields:
            ignore.append( "%s.%s"%( step.prefix, f.__name__) )
            
        for k in step.request.form.keys():
            # all multi element widgets need to use the same field prefix
            next = False
            for i in ignore:
                if k.startswith(i):
                    next = True        
                    break
            if next:
                continue
            # grabs from request not form to allow overriding by components
            passed[ k ] = step.request[ k ] 
        self._state.update( passed )
        
class ControllerBase( object ):
    """
    """
    def __init__( self, wizard ):
        self.wizard = wizard
        self.current_step = None
        
    def hasPreviousStep( self ):
        """
        """
        raise NotImplemented
    
    def hasNextStep( self ):
        """
        """
        raise NotImplemented

    def getStartStepName( self ):
        """
        """
        raise NotImplemented

    def getTraversedFormSteps( self ):
        """
        get all the form steps that have been traversed
        to the current step, to revalidate their input
        into data adapters.
        
        typically this is the path from start point to
        current. full stateful workflows should not
        attempt to get this from the request! as its
        not trusted input, and should try storing
        persistently or in session. 
        """
        raise NotImplemented
    
    def getStep( step_name ):
        raise NotImplemented

    def getNextStepName( self ):
        raise NotImplemented
    
    def reset( self ):
        self.transitionTo( self.getStartStepName() )
        
    def transitionTo( self, step_name ):
        # transition to a new step
        self.current_step = self.getStep( step_name )
        self.current_step.wizard = self.wizard
        # reset any saved request variables as they might be invalid in the new state
        self.wizard.data_manager.reset()
        self.wizard.data_manager['cur_step'] = step_name        
        # extract variables for current state from the request
        self.wizard.data_manager.update()

    def getCurrentStepName( self ):
        cur_step_name = self.wizard.data_manager.get('cur_step') or \
                        self.wizard.request.get('cur_step') or \
                        self.getStartStepName()
        return cur_step_name
    
    def getCurrentStep( self ):
        """
        """
        if self.current_step is not None:
            return self.current_step
        cur_step_name = self.getCurrentStepName()
        self.current_step = self.getStep( cur_step_name )
        self.current_step.wizard = self.wizard
        assert self.current_step is not None
        return self.current_step

    def update( self ):
        """
        """
        step_name = self.getCurrentStepName()
        current_step = self.getCurrentStep()
        current_step.update()
        next_step_name = self.getNextStepName( step_name )
        
        if next_step_name == step_name:
            return
        
        elif next_step_name == interfaces.WIZARD_REDIRECT:
            return

        self.transitionTo( next_step_name )
        self.wizard.data_manager.update()

        self.getCurrentStep().update()
        
    def getActions( self ):
        """
        return an iterable of formlib actions and suggested positions/order
        """
        previous_action = next_action = None
        
        if self.hasPreviousStep():
            previous_action = form.action(u"Back", name="back")
            yield previous_action, 0

        if self.hasNextStep():
            next_action = form.action(u"Continue", name="continue")
            yield next_action, -1

class ViewControllerBase( ControllerBase ):

    def getStep( self, step_name ):
        step = component.getMultiAdapter( 
                    ( self.wizard.context, self.wizard.request ),
                    name=step_name
                    )
        return step
        
class ListViewController( ViewControllerBase ):
    """
    controller which gets steps from a sequence of view names
    """
    steps = []
    
    def hasPreviousStep( self ):
        step_name = self.getCurrentStepName()
        return step_name != self.getStartStepName()
    
    def hasNextStep( self ):
        step_name = self.getCurrentStepName()
        idx = self.steps.index( step_name ) + 1
        return idx < len( self.steps )
    
    def getStartStepName( self ):
        return self.steps[0]
        
    def getNextStepName( self, step_name ):
        step = self.getCurrentStep()
        if step.next_step_name == interfaces.WIZARD_NEXT_STEP:
            idx = self.steps.index( step_name ) + 1
            return self.steps[ idx ]
        elif step.next_step_name == interfaces.WIZARD_PREVIOUS_STEP:
            idx = self.steps.index( step_name ) - 1
            return self.steps[ idx ]
        elif step.next_step_name == interfaces.WIZARD_REDIRECT:
            return step.next_step_name
        return step_name
        
    def getTraversedFormSteps( self ):
        step_name = self.getCurrentStepName()
        idx = self.steps.index( step_name )
        return [ self.getStep( step_name ) for step_name \
                 in self.steps[ : self.steps.index( step_name ) + 1 ] ]

        
