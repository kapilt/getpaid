"""

Annotation Property Storage and Site Configuration Settings

$Id$
"""

from getpaid.core.options import PersistentOptions

import interfaces

ConfigurationPreferences = PersistentOptions.wire("ConfigurationPreferences",
                                                  "getpaid.configuration",
                                                  interfaces.IGetPaidManagementOptions )
