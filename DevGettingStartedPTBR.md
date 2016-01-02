# Iniciando #

Iniciar um ambiente de desenvolvimento e facil gracas ao uso do `zc.buildout` ( http://python.org/pypi/zc.buildout )

`zc.buildout` e um framework para a criacao de instalacoes repetidas e usado largamente nas comunidades Zope3 e Plone3. Ele instala o Zope, Plone e todos os produtos do getpaid, as bibliotecas requeridas do python e inicia uma instancia para ser utilizada out of the box para o desenvolvimento.

## Ingredientes ##

Voce vai precisar:

  * 1 conta no Gmail account e um GoogleCode subversion password (voce pode pegar o seu em http://code.google.com/hosting/settings)
  * 1 cliente de subversion de linha de comando, `svn`
  * 1 interpretador python aceitado no zope, seus headers e bibliotecas.
  * 1 compilador C funcionando (Tudo que voce precisa para compilar)
  * for testing authorized.net with buildout, you'll also need libssl-dev and swig
  * 2 tbsp. fair trade, organic, shade-grown tea, coffee or _yerba mate_.
  * 254MiB of diskspace

## To Get Started ##

Checkout the getpaid.buildout infrastructure. Make sure you check it out to a location outside of any existing Zope instances.

```
svn co https://getpaid.googlecode.com/svn/trunk/getpaid.buildout
```

For using authorize.net payment processor, uncomment zc.authorizeddotnetet and getpaid.authorizenet in buildout.cfg

Run the buildout bootstrap script using a python interpreter that Zope likes (for example, `python2.4`):

```
cd getpaid.buildout
python2.4 bootstrap.py
```

This creates a few directories used by buildout. Then run:

```
bin/buildout -v
```

The -v isn't necessary, but may make you feel better in the knowledge that
a lot is going on.

Brew your caffeinated beverage of choice: this will take a long time and use up to 200Mb of disk space. It will:

  * Create the 'parts' directory
  * Create a directory var where your Data.fs will live.
  * Download a Zope 2 tarball into parts/zope2.
  * Build Zope 2, using 'setup.py build\_ext -i'
  * Build a Zope 2 instance in parts/instance
  * Install Plone 2.5's products into the Zope 2 instance
  * Setup the GetPaid Product/Package suite for Plone
  * Remove the Zope egg files

If you've done this once, see "Updating the buildout" below.

To start Zope 2, you can now do:

```
bin/instance fg
```

By default, the ZMI adminisration username/password is admin/admin. If the ZMI hangs, check your console: PDBDebugMode is installed by default, so you get a debugger prompt whenever there would have been a traceback.

## Installing the product ##

Create a Plone site within your zope instance. Go to site setup. Install the GetPaid product. It is not necessary to install the other products listed.

## Debugging and testing ##

If you wish to have an interactive python prompt that has all the packages
Zope is aware of, e.g. for testing purposes, you can run:

```
bin/zopepy
```

## Updating the buildout ##

Just do a

```
svn up
```

from your getpaid.buildout folder to update the buildout. Then run the buildout again:

```
./bin/buildout -N
```

Once this is done, reinstall the GetPaid product.




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