# Introduction #

Need to be able to allow users to purchase subscriptions to content. Content can be accessed for certain periods of time. Somehow the Payment Processors need to be able to interface back to Plone to tell administrators that users are ready to be billed again when their subscription expires.

Also need to define how the subscriptions will work in terms of workflow issues -- assigning rights to groups. If a user purchases a subscription of type X, they would get assigned to a group with rights X. We need to expose the workflow for this to make it easily customizeable for administrators.