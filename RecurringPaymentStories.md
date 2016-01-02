# Problem #

A single payment is not always sufficient for ecommerce use cases. Many ecommerce applications require ongoing payments - subscriptions to premium content, membership in a site, licenses, etc.

# Proposed Solution #

GetPaid needs to create general interfaces for handling recurring billing in order to enable that functionality general in the system and make it available for integrators and developers to include in their own application. Payment processors that offer recurring billing (for example, authorize.net) could then implement these interfaces.

# Use cases #

  * Many Plone sites cater to non-profit organizations, which are often membership organizations (ie charge yearly dues as a significant source of revenue).
  * Given Plone's strong content management capabilities, site owners can use subscriptions to their site as a revenue source based on their investment in content collections.

# Details #

  * Add a delivery method for content (ie available via "actions" dropdown): "recurring payment"

  * Interface (general framework, implementation is processor-dependent):
    * Set frequency of recurring billing (number of days/months/years)
    * Cost (per frequency)
    * What to do if recurring payment fails (could be initial action, ie grace period, and final action, ie account deletion)
    * Mechanism for user to cancel their subscription

  * This story probably necesitates registered users (ie no anonymous checkout)

  * This story probably means simple use case out of the box, and flexibility via work of integrators (ie hook to workflow changes etc).

  * Extensions of this base case would be to apply the delivery method to member objects (ie make subscription membership) and to premium content groups (see ConfigureMembershipTypes).

# Features #

  * Site admin: make an object "recurring payment"
  * System: notify subscription users when credit card processing was not successful, direct user to area where they can finalize the payment
  * System: regularly checks status of subscribers (to find any with failed recurring payments). Cron job? Can be set to take action when finding failed payment.
  * User: purchase a item/service with recurring billing (with adequate notification in checkout, including possibly agreement process).
  * User: ability to cancel recurring payment

# Further Information #

  * Authorize.net Automated Recurring Billing API: available in XML and SOAP. Go to authorize.net/help and search for "automated recurring billing" to find API documentation and case study.