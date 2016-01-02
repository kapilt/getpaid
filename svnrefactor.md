#Proposal to change the svn tree structure of getpaid

# Introduction #

This is a compilation of the emails exchanged between Matt Halstead and Kapil. I (lucielejard) have added some comments too.

The current svn tree structure of getpaid needs changing to help compartmentalize the packages properly.
The structure would look like the packages used in plone (see http://svn.plone.org/svn/plone/ - e.g. http://svn.plone.org/svn/plone/plone.app.content/)

Ideally all the packages currently located in
http://getpaid.googlecode.com/svn/trunk/PACKAGENAME
should be moved to
http://getpaid.googlecode.com/svn/PACKAGENAME/trunk

This would mean we can begin making individual releases of these packages to pypi and follow a more obvious method for people branching and tagging them. It will mean an update to the buildout for development, but not a difficult task.

Once this is done, we can use Tarek's release machinery (see post http://tarekziade.wordpress.com/2008/06/08/eggs-releasing-procedure-and-continuous-integration/)
to make releases of the individual packages to PyPi (it will create the necessary branch and tag for the package in svn and play the setup.cfg game automatically).

Once this is done, we can put together a production buildout example, and perhaps get to packaging PloneGetPaid product as an egg as well.

# Details #

## Potential Problems ##

1)
Problem: There will potentially be major consequences for people who are tracking trunk and not a fixed revision of getpaid and are doing this through their own buildout configurations.

Answer: Very few are running off of trunk for environments other than development; even so, we will need to update documentation (DevGettingStarted, plone.org and also in the PloneGetPaid/docs), the buildouts, and make sure we let everyone know. Also, once we are done moving everything, put a README to say where the code has moved and tell people what to do.

2)
Problem: One problem is that google code has always felt like it was "one project per google code account", which is why it starts off with a svn/trunk layout. We would effectively be saying there are now multiple projects within the same space and possible an array of licenses (though that could be normalized).

Answer: The original structure was chosen because it is much easier to branch and tag the set of packages. If individual packages are being released and pushed out, then switching the structure makes sense. It's easy enough to do, you're not forced into google code's /trunk /branches /tags structure, you can move other things to the the top level and delete the top level structures.

Given that we have buildout, we can probably do the change without causing too much pain for existing checkouts (if we keep the existing layout for buildouts.. )... or not and document and notify. personally i'd prefer if svn up didn't barf because we moved the buildout and invalidated every extant checkout.

3)
Problem:
Regarding the repo, we do need to formalize the contributor policy. Apparently there was some confusion around the license (GetPaid is ZPL, not GPL) and it would be best to keep things consistent imho in the repo. Though if we do get extensive enough that we need a "collective" and "core", then that would allow people to do as they please.

Answer: the getpaid code is BSD (not ZPL, although the two are very similiar ), and i think that all code in the getpaid repository should be the same. It's not meant to be the collective bumper car free for all. If there are add ons that people want to contribute under different licenses, they can host a repo in the collective (or wherever they want) and release it to pypi for distribution. So all the licenses need to be checked too.

4)
Problem: Are you thinking every commit should generate a development egg release on any packages touched? or timed snapshots? I'm not sure moving to development eggs would benefit development. Timed tarball releases of all packages would seem useful though.

Answer:
-1 to dev eggs on pypi .. if you using dev code, use svn. Eggs are much easier to release if its actually warranted.
Dev eggs will be in src and dev products will be in products => normal buildout way
We will only release eggs (and put them on pypi) when there is something to release.

## How to Contribute ##

You need to send you pypi login id to Kapil and he will add you to the maintainers on the getpaid eggs already uploaded (getpaid.core/getpaid.report, see http://pypi.python.org/pypi?%3Aaction=search&term=getpaid&submit=search).

The vendors packages are in the getpaid repo, and have a whole set of issues associated with them relating to using via eggs:
  * hurry.workflow i've basically forked due to lack of upstream response on patches/tests for parallel/adapted workflows and 2.9 compatiblity, its distributed as ore.workflow and works with the existing annotations of hurry.workflow.
  * zc.table relies on zc.resourcelibrary, both of these were basically non functional without some minor mods.
  * zc.resourcelibrary is basically deadweight, its not usable in z2. however recent versions will pull in a lot of zope3 eggs that will break a plone instance.

## Implementation Proposition ##

I (lucielejard) will work on the following (unless someone disagree):

### Friday 8/8 ###
  * create the new structure on my computer:
    * create a tmp folder
    * put all the sources needed in it, for example:
      * create tmp/getpaid.discount/branches and tmp/getpaid.discount/tags
      * no need to create the trunk yet since we will copy over later
  * once the structure is ready, import it: svn import tmp http://getpaid.googlecode.com/svn/
  * move everything that needs to be moved from http://getpaid.googlecode.com/svn/trunk/PACKAGENAME to http://getpaid.googlecode.com/svn/PACKAGENAME/trunk, for example:
    * mv http://getpaid.googlecode.com/svn/trunk/getpaid.discount/ http://getpaid.googlecode.com/svn/getpaid.discount/trunk
  * update the EXTERNALS files and buildout config files that need to


### Friday 8/15 ###

Goal: create a new release tag (0.7): http://plone.org/products/getpaid/releases/0.7.0

  * change the version of the product PloneGetPaid and the egg getpaid.core to be 0.7.0
  * use paster template to create a new recipe:
    * create pypi sources for the eggs that are in getpaid-buildout/src (for the eggs that need it)
    * make sure to set up the categories correctly
  * Other important things:
    * Ricardo's "unfix"/rollback was to undo this change, which broke the checkout in .6.1: http://code.google.com/p/getpaid/source/detail?r=1482 .So in .7, we need to remove "site" from the parameters passed, that's it.
    * make sure that there is good documentation for the buildout.cfg for new releases. i.e need to mention to add googlecheckout-overrides.zcml to instances part if you want google checkout
    * eggify getpaid-buildout/develop-products/PloneGetPaid (getmeteored)
    * We also should give some extra love to the way we do, for instance, externals => there are at least 2 or 3 externals that have to be changed when doing a branch or a tag (perrito666)
    * http://code.google.com/p/getpaid/issues/detail?id=204 => create a 0.6.2 tag with the fix, when 0.7 release done (backport fixes)



## Notes ##

### preparing for buildout ###

Perhaps reviewing grok's method is useful.

a grok project's setup.py dependencies are:

```
      install_requires=['setuptools',
                        'grok',
                        'z3c.testsetup',
                        # Add extra requirements here
                        ],

```

the grok egg itself depends on all the individual packages that make up the grok framework. These are unversioned ... see http://svn.zope.org/grok/trunk/setup.py?rev=89307&view=auto

in a grok projects buildout.cfg you pin versions by referring to an external versions reference for the particular release you are interested in:

see http://grok.zope.org/releaseinfo/readme.html for reasoning
see http://grok.zope.org/releaseinfo/grok-0.13.cfg for an example.

you can override individual packages in your project by redefining the egg and it's version in your own versions part.


This avoids the need for specific recipes for getpaid, but does require everything to be have an egg.

Note from Lucie: using a recipe would be easier for people to use getpaid. It doesn't seem to me that grok is the good solution in this case, when you can have a recipe that will do everything at once.

Note from Matt: which ever way this is done, the important part is that there is a method for overriding egg versions within your buildout.  plone.recipe.plone provides an explicit method for this which is picked up by the recipe - (see http://dev.plone.org/plone/browser/dist/plone.recipe.plone/trunk/plone/recipe/plone/recipe.py#L62). The grok method just uses buildout and no extra recipe-fu. Perhaps the 'extends' method grok uses could be wrapped into a recipe through the buildout api, and local overrides could then be added via a local versions section - which is ideally where you want to be thinking about version pinning or overrides.

### releasing eggs to pypi ###

see http://tarekziade.wordpress.com/2008/06/08/eggs-releasing-procedure-and-continuous-integration/

collective.releaser is worth considering - obviously a change in the svn tree structure of getpaid would be necessary for this

Note from Lucie: I wrote to Tarek to figure out why does a branch is created when releasing using his product, and he said it's because it changes the setup.cfg file before it is tagged. I asked him if he can make his product not create a branch by default, or at least, give us the option to not use a branch. I hope to have an answer soon.

### pypi categories ###

Note from Michael: Would be useful to have some consistency with the pypi categories. And to establish a new category specifically for getpaid. Perhaps "Framework :: GetPaid". This would make it easier to either find or exclude GetPaid work.

Some suggested categories:
  * Framework :: Plone
  * Framework :: Zope3
  * Intended Audience :: Developers
  * License :: OSI Approved :: Zope Public License
  * Operating System :: OS Independent
  * Programming Language :: Python
  * Topic :: Office/Business :: Financial
  * Topic :: Software Development :: Libraries

There seems to be nothing on ecommerce directly unfortunately :(