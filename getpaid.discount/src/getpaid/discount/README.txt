Tested with:
 * Plone 3.0.6
 * PloneGetPaid 0.6.0
 * Not fully working with Plone 2.5.5, see the note at the bottom

Steps to install:
 * uncomment the getpaid.discount egg into buildout.cfg
 * if you use Plone3.0, uncomment the zcml slugs for the getpaid.discount egg into buildout.cfg.
 * run bin/buildout
 * start your instance
 * go to portal_setup and run the steps for the profile getpaid.discount

Action:
After running the steps, on each payable product, you will have an available action to make the product "discountable" or "buy x get y free".

Tab:
Once you make a product discountable, you will have a new tab "Discountable" available to you, for you to edit/update your discount.

Portlets:
When you make a product discountable, it will automatically show the Discounted Product portlet instead of the default PGP one.

Viewlets:
When there are some discounted items in your cart, a viewlet with the list of discounts will show up automatically on the cart listing.

Note: when you use Plone2.5, you can't uncomment the zcml slugs for the getpaid.discount egg into buildout.cfg because it creates an error when you start your instance. I haven't found a fix for that yet. The consequences are that the portlet for the Discounted Product details won't show up. You can probably put the overriding into your own product, and use what I've put into the overrides.zcml as a model.

Developped by Six Feet Up. Contact: lucie AT sixfeetup DOT com, or lucielejard on irc.