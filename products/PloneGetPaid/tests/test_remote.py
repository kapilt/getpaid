"""PloneGetPaid functional doctests.  This module collects all *.txt
files in the tests directory and runs them. (stolen from Plone)
"""

import os, sys

import glob
import doctest
import unittest
from Globals import package_home
from Testing.ZopeTestCase import FunctionalDocFileSuite

from Products.PloneGetPaid.config import GLOBALS

# Load products
from Products.PloneGetPaid.tests.base import PloneGetPaidFunctionalTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def authdotnetSetUp(test):
    login = os.environ.get('AUTHORIZE_DOT_NET_LOGIN')
    key = os.environ.get('AUTHORIZE_DOT_NET_TRANSACTION_KEY')

    if login is None or key is None:
        raise RuntimeError('all of AUTHORIZE_DOT_NET_LOGIN,'
                           ' AUTHORIZE_DOT_NET_TRANSACTION_KEY must be'
                           ' provided in order to run the zc.authorizedotnet'
                           ' tests against the Authorize.Net test server.')

    test.globs['LOGIN'] = login
    test.globs['KEY'] = key

def test_suite():

    arb = FunctionalDocFileSuite(
            'remote/test_functional_recurrent_items_checkout.txt',
            globs = dict(
                SERVER_NAME='apitest.authorize.net',
                ),
            optionflags = OPTIONFLAGS,
            setUp = authdotnetSetUp,
            package='Products.PloneGetPaid.tests',
            test_class=PloneGetPaidFunctionalTestCase
            )
    arb.level = 5

    return unittest.TestSuite([arb,])