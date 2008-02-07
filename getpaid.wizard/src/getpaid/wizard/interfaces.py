from zope import interface, schema
from zope.contentprovider.interfaces import IContentProvider

WIZARD_REDIRECT = object() # breaking out of the wizard
WIZARD_NEXT_STEP = object()
WIZARD_PREVIOUS_STEP = object()
        
    
class IWizardController( interface.Interface ):
    """ an object which decides which steps 
    """
    def update( ):
        """
        process current step and identify next step
        """

    def hasNextStep( ):
        """
        is there a next step
        """
        
    def hasPreviousStep( ):
        """
        is there a previous step
        """

    def getCurrentStep( ):
        """
        get the current step, step should conform to IContentProvider interface
        """
    
    def getStep( step_name ):
        """
        get a step by name, step should conform to IContentProvider interface
        """

    def transitionTo( step_name ):
        """
        transition wizard to the given next step name
        """
        
    def getTraversedFormSteps( ):
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

class IWizardDataManager( interface.Interface ):
    
    adapters = interface.Attribute("mapping of schema to data adapter")
    form_state = interface.Attribute("mapping of form key to form value")
    
    def getFormVariables( ):
        """ return the form variables corresponding to the current wizard state"""
        
class IWizard( IContentProvider ):
    """
    """
    controller = schema.Object( IWizardController )
    data = schema.Object( IWizardDataManager )        
        
        
class IWizardStep( IContentProvider ):
    """ a step in a wizard
    """
    wizard = schema.Object( IWizard )
    
    next_step_name = schema.ASCIILine(
        title=u"Next Step Name",
        description=u"""After update this is set to the next step to use in a wizard,
                        typical values, include interfaces.WIZARD_PREVIOUS_STEP, or WIZARD_NEXT_STEP"""
        )
        
    def setExportedFormVariables(  mapping ):
        """
        additional form variables in key, value form
        """
        
class IWizardFormStep( IWizardStep ):

    form_fields = interface.Attribute("form.Fields instance")
    
    def getSchemaAdapters( ):
        """ return the schema adapters for the form """
