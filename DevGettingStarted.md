# Getting Started #

Setting up a development environment is now easy thanks to our use of
`zc.buildout` ( http://python.org/pypi/zc.buildout )

`zc.buildout` is a framework for creating repeatable installs, and is in
widespread use in the Zope3 and Plone 3 communities. It installs Zope,
Plone, all the getpaid products, the requisite python libraries, and
setups an instance that's usable out of the box for development.

## Ingredients ##

You'll need:

  * 1 Gmail account and a GoogleCode subversion password (you can get the latter at http://code.google.com/hosting/settings)
  * 1 subversion commandline client, `svn`
  * 1 zope-acceptable python interpreter, header files, and libraries.
  * 1 working C toolchain (everything you could have used to compile the above interpreter), such as 'gcc'
  * Libraries: profiler, simplejson and elementtree. For testing authorized.net with buildout, you'll also need libssl-dev and swig **does not work with the latest version of SWIG (1.3.31)**
  * 2 tbsp. fair trade, organic, shade-grown tea, coffee or _yerba mate_.
  * 254MiB of diskspace

## To Get Started ##

Checkout the getpaid.buildout infrastructure. The code for both Plone 3.0 and 4.0 buildouts can be obtained together, so only one place to check out from. Make sure you check it out to a location outside of any existing Zope instances.

```
svn co https://getpaid.googlecode.com/svn/getpaid.buildout/trunk getpaid.buildout
```

Make sure you use https and not http, as you will have authentication problems later if you do.

**Note: The anonymous buildout is no longer supported.**

For using authorize.net payment processor, uncomment zc.authorizedotnet and getpaid.authorizenet at the bottom of sources.cfg

Run the buildout bootstrap script using a python interpreter that Zope likes (use Python 2.4 for Plone 3, or Python 2.6 for Plone 4):

```
cd getpaid.buildout
python2.4 bootstrap.py -c 335.cfg
```

This creates a few directories used by buildout. Then you run a command depending on which version of Plone you want:

For Plone 3 run:
```
bin/buildout -vc 335.cfg
```

For Plone 4 run:
```
bin/buildout -vc 4.0b3.cfg
```


The -v isn't necessary, but may make you feel better in the knowledge that
a lot is going on.

_Note:  Do NOT attempt to run a buildout of one instance in a buildout directory that you had a different version in already.  Start with a clean buildout directory and choose either the 3.x or 4.x buildout config for that buildout (do not run a 4.x buildout in the directory that you had a 3.x buildout.)_

You can copy the cfg and alter the Plone version it's pinned to, if you'd prefer to attempt a different, possibly more recent Plone version.

Brew your caffeinated beverage of choice: this will take a long time and use up to 200Mb of disk space. It will:

  * Create the 'parts' directory
  * Create a directory var where your Data.fs will live.
  * Install Zope 2 and create a Zope 2 instance.
  * Install Plone and dependencies into the Zope 2 instance
  * Setup the GetPaid Product/Package suite for Plone

If you've done this once, see "Updating the buildout" below.

To start Zope 2, you can now do:

```
bin/instance fg
```

By default, the ZMI administration username/password is admin/admin. If the ZMI hangs, check your console: PDBDebugMode is installed by default, so you get a debugger prompt whenever there would have been a traceback.

## Installing the product ##

Create a Plone site within your zope instance. Go to site setup. Install the GetPaid product. It is not necessary to install the other products listed.

## Debugging and testing ##

If you wish to have an interactive python prompt that has all the packages
Zope is aware of, e.g. for testing purposes, you can run:

```
bin/instance debug
```

## Updating the buildout ##

Just do a

```
svn up
```

from your getpaid.buildout folder to update the buildout.

Then run the buildout again. **Be sure to run the command corresponding to the same version of Plone you built originally, otherwise this will break your build.**

**For Plone 3**
```
./bin/buildout -vc 335.cfg
```

**For Plone 4**
```
./bin/buildout -vc 4.0b3.cfg
```

That's it!




## Troubleshooting ##

### hurry.workflow errors ###

You need to re-run the build-out to get the latest .cfg file.  Try:

```
~/getpaid.buildout/bin/buildout -v -N
```

### M2Crypto errors and Authorize.net ###

Authorize.net requires some new crypto libraries.  We removed this from buildout.cfg so that dependencies aren't needed at this point for a general audience.

[future](future.md) Steps to install:

**On OSX: It looks like we need to install SWIG via DarwinPorts: sudo apt-get install swig**

**M2Crytpo had some additional dependencies that still need to be worked out for the buildout...**

### GoogleCode profile page doesn't show the SVN password ###

It seems that it only works for Google accounts that have subscribed to Gmail.

### Errors during checkout ###

The initial checkout takes a long time, connects to a multitude of servers, and in general has several interesting ways it can fail. If it does, just enter the `getpaid-buildout` directory and do an `svn up`:

```
cd getpaid-buildout
svn up
```

the svn fu will continue where it left off.

### No such file or directory while doing execfile ###

We really meant it about using the commandline `svn` client; if you use a GUI client, make sure it correctly supports svn:externals. For example, `rapidsvn` prior to 0.9.4 does **not**. Do a `svn up`; make certain all externals are pulled in.

### The instance hangs! ###

Installation of the PloneGetPaid product may appear to hang. There's an installed product called PDBDebugMode that brings up a Python Debugger prompt whenever there's an error (which is why it looks like it's freezing).
When you're running in debug mode, you'll see a prompt appear in your
terminal window. Just hit 'r' (sometimes several times) to continue. If in doubt, stop your Zope instance and restart it.

### AccessControl/cAccessControl ###
```
internal error occured due to a bug in either zc.buildout or in a recipe being used:
AccessControl/cAccessControl.c:2312: error: ‘PROBLEM’ undeclared (first use in this function)
```

Seems to be caused by using the wrong version of Python. You can correct this by providing the full path to Python2.4 when running bootstrap.py

```
/path/to/python24/python bootstrap.py
```

You may need to install PIL to make it run:

http://www.pythonware.com/products/pil/

### AttributeError: ore.member ###

If you got that error trying to install PloneGetPaid on your plone site, please restart the zope instance and try again. Now ore.member should exist and you should have no problems for finishing the PloneGetPaid installation.