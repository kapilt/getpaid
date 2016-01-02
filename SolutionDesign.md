New Stuff

  * ((Components Mindmap))
  * ((Nate Premium Membership Product))



Goals

Goal 1: Provide a general framework for Plone developers and users to easily incorporate payment processing into their site.

Goal 2: Have this framework incorporated into core Plone bundle
Requirements

[R1](https://code.google.com/p/getpaid/source/detail?r=1): Secure, secure, secure,...follow BestPracticesInSecurity at all times.

[R2](https://code.google.com/p/getpaid/source/detail?r=2): Easy to use for site administrators and payees

[R3](https://code.google.com/p/getpaid/source/detail?r=3): Good documentation available
Design Description

  * We want an out of the box solution that targets the common needs of non profits organizations, which primarily means donations, both one time and reoccuring, basic financial account management, and an easy way of linking payment processing to existing content and content types. so no cart management, catalog, or inventory management needed for the core use cases, ie. its not traditional ecommerce, in the sense of shipping products to consumers. It's a facilitator for organizations to collect money online, and optionally to provide online/offline services or content to users.
  * The idea is to have core infrastructure for processing and user interfaces, and then other tools can sit on top of that. In order to do so, need to
> > have all the info people need to do so. Need hooks for these things that are to be extensable or explanation of creating/using adapters with the
> > framework.
  * From a code perspective, what's needed are an interface and utility for payment processors, with pluggable implementations, and out useable of the box defaults for those. Storage of orders, linked to users, an easy way of linking to content, and publishing events for order/payment lifecycles so that we can have decoupled integration of business logic customization.
  * A point of reference for the payment framework product is the ContentLicensing product. Essentially, after installing the payment product, any content type or individual object in the site can become part of a payment process. The site administrator can set defaults for the site (ie all "book" ATCT become payable), and then all these objects will have appropriate fields for price, etc.
  * The administrative screen will have an area to configure how payments are handled (ie merchant acct, gateway), with a set of default options available. The admin UI is a view on the control panel. We want to use viewlets so other applications can plug in to use the templates for the processors.
  * The payment framework can be leveraged by third-party products in Plone that have payment needs.

Technologies

  * Use zope 3 technologies, and an architecture with interfaces for payment. This way there would be payment-utility delegating the actual work to a layer for each payment-method. This would make it easy for developers writing a new plugin for paying stuff,Â  since the programmer would only have to worry about satisfying the interface, not writing forms and reinveinting payment stuff. (from Geir BÃŠkholt)
  * Potentially use Content Flavors to apply the "payable" information to any existing content object or type of content. Assign behaviors to the flavors. Add a management interface. (from Kapil Thangavelu). Consider also work done by Nate on Plone4ArtistsCalendar product.
  * Content integration: originally looked at ContentFlavors (integate to archetype), but will be simpler to use zope3 schemas and annotations and
> > have a separate page for content (Plone4Audio marker interface approach. Controller view (no UI), generates condition that is checked by the action tool, and based on that, adds entry on actions menu for piece of content (make shippable, purchasable, premium content). View is via Five. Annotate the content directly with info about pricing, shipping wt, etc.
  * When action is triggered, the marker interface applies something to Â the view (CMFOnFive - allows content actions to be pulled in from views or something); content grows additional tabs if marked as purch/ship/etc.