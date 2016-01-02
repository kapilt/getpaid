# Configure Membership Types #

## Overview ##
The subscription use case is for the **purchase** of access to a **set of benefits** on a given site for a period of time. This could be an annual membership in an organization, a monthly access to site content, or a newspaper subscription.

Site Admins can access a "Subscription Configuration" screen that allows them to set the prices, descriptions of membership types (as currently set), and also allows for them to set benefits involved with their membership levels. This includes association with a group (for assigning local permissions in the site). There is one new role introduced when using this system "premium member" role, which is applied locally when a group is given access to an area.

## Add Membership Type ##

Under "Add a membership type", the Admin can add enter:

  * Type Name:
  * Description
  * Price,
  * Type of payment (dropdown of: "One-time", "Annual", "Monthly"), ie the price would be charged each period. Indefinite would imply a one-time fee for the membership/subscription. Deferred: Weekly
> > Note: we should include a disclaimer along with this field to let user know which pay processors are supported for recurring charges.

and then that is stored on the page for edit and review. The system would create a new group (or role??) on the fly to represent a given level.  Once the role is created, the interface provides a URL that will enable the site admin to add a link anywhere in the cart that would provide the "add to cart" ability for a given access level.

## Edit Membership Overview Page ##
Instructions: Please add an overview of membership levels, benefits, prices here for your users. Those registering will be directed to this information to choose a level. Use the URL for each given level to provide a way for the user to add that level to their purchase workflow.

Text: (rich text window)

[save](save.md) [cancel](cancel.md)


## Implementation issues ##

We assume that there is a free level of access to a site.

How can users be moved between the levels manually? Answer: admin can move people to different group, and by default the expiration date is the same, but admin can edit expiration date manually on member. manually adding users and putting in groups gives them default _Note: this should be turned into another user story, i think_

How does admin see numbers for a site (ie how many people are in each level of membership)? See view-history-of-payments.

What does implementation look like? PAS Pluggin to annotate members with zope3 schemas. (don't want to depend on membrane/remember). Want to instead use a PAS structure to define member reg and shipping/billing info via separate schemas. As PAS pluggin, is easier to defer storage elsewhere. Task: Write PAS plugin and replace registration form and personalization form. Data stored by default on existing membership tool, but pas can have storage adapter to store it anywhere.

  * Might store last 4 dig of CC # in order to reconcile

## Deferred ##

Deferred: If a subscription is about to expire (i.e. 30 days in advance), the system should automatically generate emails to users to remind them to renew their membership. It should be possible to configure these emails in the site setup area. Additionally, if a user logs into their account and their membership is about to expire, users should be prompted to renew.

Deferrred: Adding in additional fields for the registration process, such as demographics, will need to be handled by a plugin adaptor.

Deferred: For a given membership type, a price could be specified for multiple periods (ie monthly price and annual price with discount over monthly price). Once a membership type is added, it includes a "add pricing option" button which lets the admin add another period+price option for the given level.

Deferred: The screen also allows the ability to associated given site actions with a membership type.
Deferred: This screen also has the ability to set the site to "private", which would require a user to have one of the set membership levels to see any content.