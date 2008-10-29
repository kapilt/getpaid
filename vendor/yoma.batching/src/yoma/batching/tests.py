##############################################################################
#
# Copyright (c) 2007 YOMA PTY LTD. All Rights Reserved.
#
##############################################################################
"""yoma.batching tests

$Id$
"""

import unittest
from zope.testing.doctest import DocFileSuite
from zope.component.testing import setUp, tearDown

##############################################################################

def test_suite():
    return DocFileSuite('BATCHING.txt', setUp=setUp, tearDown=tearDown)

##############################################################################

if __name__=="__main__":
    unittest.main(defaultTest='test_suite')
