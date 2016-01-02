Framework User Wishlist

Jon Stahl's summary of NGO online donation needs

Online donations is a relatively simple subset of "full fledge" ecommerce functionality, with a few small twists.  The lack of a good, simple-yet-reasonably-featured solution is a key roadblock to increasing NGO-sector use of Plone.
The basics

  * Create an online donation form: ideally using a simple grahpical UI such as PloneFormGen, the user should be able to create a basic donation forms.  The form should be pre-populated with the minimum fields required to process a credit card transaction (name, address, card info), but the user should be free to add, remove and re-arrange fields.
  * When the form is submitted, the payment-related fields should be submitted to a payment gateway, and any errors fed back to the user for correction.
  * If there are no errors, all fields EXCEPT credit card data should be written into appropriate storage in the Plone site for later download.  (Ideally, this component would be pluggable so that successful donations could be stored in an outside CRM system with a strong web services API such as Salesforce.com.)

Things peculiar to online donations

There are a few concepts that don't really exist in ecommerce land that are important to the online donation process.  Here's a quick sketch:

  * Essential: Form needs to support defined payment levels and open-ended donation amounts in a single form.  e.g. $10, $25, $50, $100, $500 or you choose how much.
  * Very important: recurring (monthly) donations.

Payment Gateways

An online donation solution probably needs a somewhat pluggable payment gateway subsystem (ala PloneMall). I would suggest that reasonable US-centric gateways to support could include: PayPal Website Payments Pro; Authorize.net.  Not sure about international requirements, maybe mine the ZenCart universe for ideas.


Jon Stahl's Summary of Basic Event Registration Payment

Event registration can quickly scale to be a large and complicated problem.  IMHO, Plone should seek to do a good job for simple use-cases, but (at least initially) avoid attempting to become a full-fledged event registration platform (e.g. something suitable for running a major, multi-track conference with lots of sub-registrations and options.)

What is most needed in the NGO sector is the ability to:

  * Define a simple, calendarable event (via Plone's existing calendar/event tools)
  * Link that event to a registration page (the way that SignupSheet does now)
  * Have that registration page include credit-card capture fields.


Much like the online donation form described above, the event registration needs to be able to:

  * Contain arbitrary custom fields and blocks of HTML.
  * Pass credit card data to a payment gateway, and receive + display any errors
  * Write successful transaction data into a local storage and/or a pluggable pipeline for passing to an external CRM system