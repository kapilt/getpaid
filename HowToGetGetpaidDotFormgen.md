# Introduction #

I saw (on AugustSprint) that there was a need to create this page (and a page for how to use getpaid.formgen, but one thing at a time!). Because getpaid.formgen is not available as an egg yet (as of January 2009), getting it can be a little challenging. I hope this saves you some time!

# Details #

Because getpaid.formgen is not available as an egg yet, you need to find some way to get the code. You can either
  * checkout getpaid.formgen from this repository anonymously: `svn co http://getpaid.googlecode.com/svn/getpaid.formgen/trunk/src getpaid.formgen` _(untested)_
  * checkout getpaid.formgen from this repository securely (i.e., with Write access) by contacting someone and using: `svn co http://getpaid.googlecode.com/svn/getpaid.formgen/trunk/src getpaid.formgen`

Now, you need to let your instance know about the code.

If you're not using Buildout: _(untested)_
  1. Because getpaid.formgen is not in the magic "Products" namespace, you have to copy or link the files under zope2/lib/python/getpaid/formgen.
  1. `cd `my-site-path`/zope2/lib/python`.
  1. `ls getpaid`. See if there's already a getpaid folder (there probably is).
  1. If there is, `cd getpaid`. Else, `mkdir getpaid; cd getpaid`.
  1. To link: `ln -s `path-to-svn-checkout`/getpaid.formgen/getpaid/formgen ./formgen`. To copy: `cp -R `path-to-svn-checkout`/getpaid.formgen/getpaid/formgen/* ./formgen`.
  1. getpaid.formgen depends on Products.DataGridField. Get it here: http://plone.org/products/datagridfield.

If you're using Buildout:
  1. You can use getpaid.formgen as a development egg by copying or linking the files under src/.
  1. `cd `buildout-path`/src`.
  1. To link: `ln -s `path-to-svn-checkout`/getpaid.formgen ./getpaid.formgen`. To copy _(untested)_: `cp -R `path-to-svn-checkout`/getpaid.formgen ./getpaid.formgen`.
  1. `cd ..` to get to your buildout root again.
  1. edit your buildout.cfg with something like `nano buildout.cfg` and make the following additions:
    * 
```
[buildout]
eggs =
    getpaid.formgen
develop = 
   src/getpaid.formgen

[instance]
zcml =
    getpaid.formgen
```
    * That is, if you don't have a list of eggs in the `[buildout`] part of your buildout.cfg, add it with getpaid.formgen as a value. If you have it, add getpaid.formgen to the list of values. `[instance`] is what my plone.recipe section is called; yours may be different.
  1. `./bin/buildout -vvvv`
    * You can't simply run `./bin/buildout -No` because getpaid.formgen will tell zc.buildout to grab Products.DataGridField for you.

Finally, fire up your instance.

You should see getpaid.formgen listed in mydomain:myport/Control\_Panel/Products/manage\_main and mydomain:myport/mySite/portal\_quickinstaller/manage\_installProductsForm

Install the product.

Also, install DataGridField.