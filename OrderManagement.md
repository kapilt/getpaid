# Introduction #

This will be tied to the specific payment processor that is used, and should also tie into a common management interface if possible.


# Details #
Site views will include:
**Edit an order**Archive / Batch an order
**Refund an Order**Process an Order.


# Admin View History of Payments #

The Admin can view a History screen, that presents the transactions from the site in a table. The table includes:

  * date
  * username (linked to the user transaction history screen, ie same screen the individual user sees in their history)
  * "paid for" (see below)
  * amount paid (for successful transactions)
  * id of the transaction that corresponds with the order in the merchant account interface

The page shows all the transactions on the site, with the most recent at the top. The history is paged in groups of 20.

Question:

  * Do we show a link to the object that was paid for? ie the particular donation form, membership level, product id, shopping cart details, etc. Seems like this should be a field set by the particular addon product, and be flexible, so what do we need here?


Options from the screen:

  * Sort table by the fields
  * Export table to CSV
  * Future: Export to popular accounting packages: You can specify a date range for your orders and export them as a single file that can then be imported into accounting packages such as MYOB and Quicken/Quickbooks.