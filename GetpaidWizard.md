# GetpaidWizard #

## wizard component ##

> - manage multi step transitions

> - defer to a wizard controller for steps

> - manages content provider components ( viewlets in practice )

> - remove

> - request form step

> def getFormMapping( ):
> - form schema
> - form adapter

# Controller #

controllers should be managed by name in the admin.

> -  we need access to the schemas provided by the chain of steps to
> > validate our inputs, while allowing variation.


> - provides actions for current state's next, previous, via
> > getActions method.


> def getStep( ): pass
> def getTraversedSteps( ): pass


# Data Manager #

> manages the data that is collected through the wizard through
> different states.

> - manages keeping state through the form

