# Introduction #

After a product has been added and made "shippable", the site admin can "manage inventory" from the actions menu on the item. This adds an additional tab (besides the "payable" called "inventory") and loads this tab for the user. This tab provides a "Location" section and a "Stock" section. In the location section, fields are grouped that allow the site admin to specify "Pick and Pull Bin", "Pallet", and "Warehouse". The first two are fields that allow user to input letter/number/symbol information. The Warehouse would be specified in the GetPaid setup area and then be available via a dropdown on this tab.

## Variations and Notes ##

A variation on this may be needed for the general "buyable", where "manage inventory" would be available but would only show the "stock" information (and not the location/warehouse info).

Note that this only allows for a stock to be in one warehouse. If stock is split across multiple warehouses, we need another story (ie "add warehouse" and then specify the stock/location in that warehouse). Orders would then have to be associated to a warehouse (ie choose warehouse closest to shipping address via default and then give admin ability to change where it comes from).

Further information to be developed about the process of changing quantity, backorder functioning.