
from hurry.workflow import workflow

class StoreVersions( workflow.WorkflowVersions ):

    def hasVersionId( self, id): return False

