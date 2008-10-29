# Copyright (c) 2007 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import unittest
from Testing import ZopeTestCase
from zope.testing import doctest
from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase
import getpaid.googlecheckout.tests
import getpaid.googlecheckout.tests.patch
from Products.Five import zcml
from xml.dom.minidom import parseString


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_UDIFF)


class GoogleCheckoutFuncationalTestCase(PloneGetPaidFunctionalTestCase):

    def afterSetUp(self):
        super(GoogleCheckoutFuncationalTestCase, self).afterSetUp()
        zcml.load_config('testing.zcml', package=getpaid.googlecheckout.tests)
        self.portal.portal_quickinstaller.installProduct('PloneGetPaid')
        getpaid.googlecheckout.tests.patch.gchecky()

    def extract_data(self, xml_blob, name):
        xml = parseString(xml_blob)
        return str(xml.getElementsByTagName(name)[0].firstChild.data).strip()


def test_suite():
    return unittest.TestSuite([
        ZopeTestCase.ZopeDocFileSuite(
            'googlecheckout.txt',
            package='getpaid.googlecheckout',
            test_class=GoogleCheckoutFuncationalTestCase,
            optionflags=OPTIONFLAGS,
            ),
        ZopeTestCase.ZopeDocFileSuite(
            'googlecheckout-browser.txt',
            package='getpaid.googlecheckout',
            test_class=GoogleCheckoutFuncationalTestCase,
            optionflags=OPTIONFLAGS,
            ),
        ])
