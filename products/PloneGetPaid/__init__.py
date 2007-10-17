"""
$Id$
"""

from config import PLONE3
# CMFonFive has been integrated in CMFCore since version 2.0, so in
# Plone 3.0 we do not depend on it anymore.
if PLONE3:
    _GETPAID_DEPENDENCIES_ = [ ]
else:
    _GETPAID_DEPENDENCIES_ = [ 'CMFonFive' ]

import os, sys
from Globals import package_home

import _patch

pkg_home = package_home( globals() )
lib_path = os.path.join( pkg_home, 'lib' )
if os.path.exists( lib_path ):
    sys.path.append( lib_path )


# These imports of zope.annotation are needed needed to get
# annotations to work on Zope 2.9 and 2.10 at the same time.  They are
# needed in this __init__.py so they are always available as
# zope.annotation in configure.zcml.
# See http://comments.gmane.org/gmane.comp.web.zope.general/58334

try:
    import zope.annotation
    import zope.annotation.interfaces
except ImportError:
    # BBB for Zope 2.9
    import zope.app.annotation
    import zope.app.annotation.interfaces
    sys.modules['zope.annotation'] = zope.app.annotation
    sys.modules['zope.annotation.interfaces'] = zope.app.annotation.interfaces
