##############################################################################
#
# Copyright (c) 2007 YOMA PTY LTD. All Rights Reserved.
#
##############################################################################
"""LayoutMixin for formlib

$Id$
"""

from zope.formlib import namedtemplate
from zope.formlib.interfaces import IPageForm
from zope.app.pagetemplate import ViewPageTemplateFile


class LayoutMixin(object):
    """ Mixin for formlib classes to provide widget placement control

    This class should be inherited left most.
    """

    form_layout=None
    form_method='POST'
    template = namedtemplate.NamedTemplate('layout')

    # look at override the base class render method to do
    # something sensible with widgets accidentally left
    # out of a form_layout


layout_page_template = namedtemplate.NamedTemplateImplementation(
    ViewPageTemplateFile('layoutform.pt'), IPageForm)

##############################################################################
