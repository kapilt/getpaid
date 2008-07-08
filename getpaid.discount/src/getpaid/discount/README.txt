Tested with Plone 2.5.5, Plone 3.0.6 and PloneGetPaid 0.6.0.

Steps to install:
 * uncomment the getpaid.discount egg into buildout.cfg
 * run bin/buildout
 * start your instance
 * go to portal_setup and run the steps for the profile getpaid.discount

After that, on each payable product, you will have an available action to make the product "discountable" or "buy x get y free".

Once you make a product discountable, you will have a new tab "Discountable" available to you, for you to edit/update your discount.
