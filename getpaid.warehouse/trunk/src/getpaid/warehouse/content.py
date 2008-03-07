

from getpaid.core import options

import interfaces

options.PersistentOptions.wire( "Inventory", "getpaid.content.buyable", interfaces.IBuyableContent )