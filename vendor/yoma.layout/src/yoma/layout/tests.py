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
from zope import component
from zope.formlib import namedtemplate
from zope.formlib.interfaces import IForm
from zope.formlib.tests import formSetUp
from zope.app.testing import setup

##############################################################################

@component.adapter(IForm)
@namedtemplate.NamedTemplateImplementation
def TestTemplate(self):
    return self.form_layout.render(self)


def setUp(test):
    formSetUp(test)
    component.provideAdapter(TestTemplate, name='layout')
    setup.setUpAnnotations()
    setup.setUpDependable()
    setup.setUpTraversal()
    setup.setUpSiteManagerLookup()
    site = setup.rootFolder()
    setup.createSiteManager(site, setsite=True)
    test.globs['site'] = site


def tearDown(self):
    setup.placefulTearDown()


def test_suite():
    return unittest.TestSuite((
        DocFileSuite('GRID.txt'),
        DocFileSuite('LAYOUT.txt'),
        DocFileSuite('MIXIN.txt', setUp=setUp, tearDown=tearDown),
        ))

##############################################################################

if __name__=="__main__":
    unittest.main(defaultTest='test_suite')
