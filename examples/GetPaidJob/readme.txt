-------------------
GetPaid in Practice
-------------------

This an example of using getpaid against an existing third party content type,
that also demonstrates workflow integration, and dynamic pricing.

Content Workflow Integration
----------------------------

Use Case
++++++++

The scenario is that We'd like to have users pay for submitting content to a site.
In this particular example, their submitting a job board posting to a job board.
We don't want that content visible to other users of the site till the content 
has been paid for.

Implementation
++++++++++++++

When the user submits the content, we enable a conditional link on the content's default view, 
to allow them to pay for the content ( in plone 3 this isn't nesc, as a workflow's action url
is respected and we take the user straight to checkout when the content is submitted ).

We hookup a workflow subscriber, which when an order is paid for, checks the order's contents
looking for job posts, and transitions to them to the published state, at which point their
visible to the public.

Custom Pricing
--------------

Use Case
++++++++

Additionally we'd like to have, the price of a job board post be dependent on a price attribute
of the particular job board instance its being created in, and we want members with a particular 
role get a different price then the default price. 

Implementation
++++++++++++++

We use a custom view to add the post to the user's cart, which creates a line item by hand, and
which determines the price based on context. The view then redirects the user to the checkout 
process.

