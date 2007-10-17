"""
$Id$
"""

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
    import sys
    sys.modules['zope.annotation'] = zope.app.annotation
    sys.modules['zope.annotation.interfaces'] = zope.app.annotation.interfaces
