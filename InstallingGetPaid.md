# Introduction #

The recommended approach to installing GetPaid varies depending on whether you are using Plone 3 or Plone 4.

# Plone 4 #

To install GetPaid in Plone 4.0 or 4.1, you need to add Products.PloneGetPaid as an egg for your instance, and make sure that the appropriate versions are pinned.  Add the following to your buildout.

```
[buildout]
versions = versions
find-links =
    http://getpaid.googlecode.com/files/hurry.workflow-0.9.2-getpaid.zip
    http://getpaid.googlecode.com/files/ore.viewlet-0.2.3-getpaid.zip
    http://getpaid.googlecode.com/files/yoma.batching-0.2.2-getpaid.zip

[versions]
five.intid = 0.5.2
getpaid.authorizedotnet = 0.5.0
getpaid.core = 0.9.2
getpaid.discount = 0.11
getpaid.formgen = 0.5
getpaid.nullpayment = 0.5.0
getpaid.wizard = 0.4
hurry.workflow = 0.9.2-getpaid
M2Crypto = 0.20.2
ore.viewlet = 0.2.3-getpaid
Products.PloneGetPaid = 0.10.4
yoma.batching = 0.2.2-getpaid
zc.authorizedotnet = 1.3.1
zc.creditcard = 1.0
zc.resourcelibrary = 1.3.1
zc.ssl = 1.2
zc.table = 0.8.0
# (add other getpaid add-ons here, as long as they've been tested on Plone 4)

# The following pin is needed on Plone 4.0, but should not be used with Plone 4.1.  Uncomment it on Plone 4.0
# zope.browserresource = 3.9.0


[instance]
...
eggs =
    ...
    Products.PloneGetPaid
#    (list other getpaid add-ons here)
```

(This list will be updated to reflect the most recent stable releases of the various packages.)

The extra 'find-links' are required so that buildout/easy\_install can find some special GetPaid-specific versions of a few packages that are not available from PyPI.

If you like, you can keep the versions list in a separate file called versions.cfg, and include it like this:

```
[buildout]
extends = versions.cfg
versions = versions
```

You may also use this approach in Plone 3 instead of the recommended recipe, if you use five.intid 0.4.4-1 and a fake egg for zope.browserresource.


# Plone 3 #

For Plone 3, we recommend using the getpaid.recipe.release buildout recipe.  If you don't have a buildout-based Plone installation, use one of the Plone installers from http://plone.org/products/plone to get one.  Then make sure the following bits are included in your buildout configuration.

```
[buildout]
parts = 
    ...
    getpaid

[getpaid]
recipe = getpaid.recipe.release==2.1
addpackages =
    getpaid.authorizedotnet

[instance]
...
eggs =
    ...
    ${getpaid:eggs}
```

(Some of these parts may already be in your buildout configuration.)

Run buildout, restart Zope/Plone, and you should be able to install PloneGetPaid via the Add/Remove Products panel in Site Setup.

Note: The getpaid.recipe.release recipe has not yet been updated to include some of the recent releases of the packages that make up getpaid, so it's a bit out of date.

We recommend pinning the recipe to a particular version, as shown, to make sure that you don't accidentally upgrade when a new release of the recipe comes out.

The 'addpackages' setting is optional, and may include a list of add-on packages to install. Supported add-ons include: getpaid.authorizedotnet, getpaid.clickandbuy, getpaid.formgen, getpaid.googlecheckout, getpaid.ogone, getpaid.payflowpro, getpaid.paymentech, getpaid.paypal, getpaid.pxpay, getpaid.flatrateshipping, getpaid.ups, getpaid.discount, getpaid.report, getpaid.warehouse, getpaid.SalesforcePloneFormGenAdapter, getpaid.SalesforceOrderRecorder.

You may also specify an optional 'eggs' setting, which is a list of getpaid dependencies that should be installed as eggs, rather than by fetching tarballs as the recipe normally does.  This is necessary if you want to pin one of the dependencies to a different version than what is specified in the recipe.  The following dependencies are included by default: ore.viewlet, getpaid.core, Products.PloneGetPaid, getpaid.wizard, getpaid.nullpayment, five.intid, hurry.workflow, simplejson, yoma.batching, zc.resourcelibrary, and zc.table.  five.intid is the most common package you will need to do this for, as some other add-ons (such as Dexterity) require a newer version of five.intid than what is installed by the getpaid recipe.

# Developing GetPaid #

If you want to work on making improvements to GetPaid or its add-ons, we recommend following the instructions at DevGettingStarted