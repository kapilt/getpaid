# Configure Pricing #
## On the Object Level ##

For any content object in a site, a Payment option can be attached. The site admin simply views the object, and then clicks "action"--> "Make Payable". That adds schema elements to the object for setting the  price on the object.

Deferred: Schema also adds a rich text box for a teaser description on a purchasable object (We don't have zope3 widget editors for rich text that are available in plone (since zcresourcelibrary not available in zope2)...integator can override the view to directly include rich text widget to include relevant javascript or we can create the widget)


## On the Site-Wide Level ##
Deferred.

Steve thinks is most complex aspect and needs own engine. Should be pluggable...Means creating own tool and interface to do this. PLUGGALBE ADAPTERS will be possible for shippable/premium/etc; Will be able to accomplish via IManagePrice, for example - can just write a method to override or build an entire pricing tool to replace that.

Per Kapil, we can fairly easily have pluggable implementations across the board with adapters. When we apply marker, we can have adapter there that people can override so people can using pricing options to figure out what price should be. Base implementation will have price info only; something else would need to edit that with adapter.

Re mass editing of prices: remember does something useful...can index all the interfaces for an object, so we can query out what are all
things we can buy. Could also be used to generate catalog pages.

However, not doing product catalog as part of base functionality - plug-in any such tools later