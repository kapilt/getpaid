##############################################################################
#
# Copyright (c) 2007 YOMA PTY LTD. All Rights Reserved.
#
##############################################################################
"""Batching support for zc.table

$Id$
"""

import sys
from StringIO import StringIO

from zope.app.traversing.browser import AbsoluteURL
from zope.i18nmessageid import MessageFactory

_=MessageFactory('yoma')

##############################################################################

class Paginator(object):

    def __init__(self, bstart, bsize, nitems, margin=None):
        bstart, bsize = sanitise(bstart, bsize, nitems)
        margin = margin or sys.maxint
        self.pre = range(0, bstart, bsize)
        self.post = range(bstart+bsize, nitems, bsize)
        self._cut(margin)
        self._enum(bstart, bsize)
        self._next(bsize, nitems, margin)
        self._prev(bsize, nitems, margin)

    def _cut(self, margin):
        lmarg = min(margin, len(self.pre))
        rmarg = min(margin, len(self.post))
        lmarg, rmarg = (lmarg+margin-rmarg), (rmarg+margin-lmarg)
        self.pre = self.pre[-lmarg:]
        self.post = self.post[:rmarg]

    def _enum(self, bstart, bsize):
        icur = (bstart+bsize)/bsize
        offset = icur-len(self.pre)
        self.pre = [(i+offset, bs) for i, bs in enumerate(self.pre)]
        offset = 1+icur
        self.post = [(i+offset, bs) for i, bs in enumerate(self.post)]
        self.cur = (icur, bstart)

    def _next(self, bsize, nitems, margin):
        self.next = None
        if len(self.post):
            pageno, bstart = self.post[-1]
            pageno += 1
            bstart += bsize
            if bstart < nitems:
                self.next = pageno, bstart

    def _prev(self, bsize, nitems, margin):
        self.prev = None
        if len(self.pre):
            pageno, bstart = self.pre[0]
            if bstart-bsize > 0:
                pageno = max(1, pageno-margin)
                bstart = max(0, bstart-bsize*margin)
                self.prev = pageno, bstart

##############################################################################


class RenderNav(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def link(self, pageno, bstart):
        from urllib import urlencode
        from urlparse import urlsplit, urlunsplit
        from cgi import parse_qsl

        parts = urlsplit(self.request.getURL())
        query = dict(parse_qsl(self.request.get('QUERY_STRING', parts[3])))
        query['bstart'] = bstart
        parts = parts[0:3] + (urlencode(query),) + parts[4:]
        url = urlunsplit(parts)
        return '<a href="%s">%s</a>' % (url, pageno)

    def renderBegin(self):
        print>>self.out, u'<div class="batch navigation">'

    def renderPrev(self):
        prev = self.paginator.prev
        if prev:
            pageno, bstart = prev
            print>>self.out, self.link(_("Prev"), bstart)

    def renderLeft(self):
        for pageno, bstart in self.paginator.pre:
            print>>self.out, self.link(pageno, bstart)

    def renderCurrent(self):
        pageno, bstart = self.paginator.cur
        print>>self.out, u'<span class="current">%s</span>' % pageno

    def renderRight(self):
        for pageno, bstart in self.paginator.post:
            print>>self.out, self.link(pageno, bstart)

    def renderNext(self):
        next = self.paginator.next
        if next:
            pageno, bstart = next
            print>>self.out, self.link(_("Next"), bstart)

    def renderEnd(self):
        print>>self.out, u'</div>'

    def __call__(self, paginator):
        self.out = StringIO()
        self.paginator = paginator
        self.renderBegin()
        self.renderPrev()
        self.renderLeft()
        self.renderCurrent()
        self.renderRight()
        self.renderNext()
        self.renderEnd()
        return self.out.getvalue()

##############################################################################

class BatchingMixin(object):
    """ Mixin for Formatter classes.

    Extracts batching parameters from the request and passes these onto
    the formatter.

    This class should be inherited left most.
    """

    paginator_factory = Paginator
    rendernav_factory = RenderNav

    def __init__(self, context, request, items, visible_column_names=None,
        batch_start=None, batch_size=None, prefix=None, **kw
        ):
        batch_start = toInt(request.get('bstart')) or batch_start
        batch_start, batch_size = sanitise(batch_start, batch_size, len(items))
        super(BatchingMixin, self).__init__(context, request, items,
            visible_column_names, batch_start, batch_size, prefix, **kw)

    def renderNav(self):
        p = self.paginator_factory(self.batch_start, self.batch_size,
                                   len(self.items), margin=4)
        render = self.rendernav_factory(self.context, self.request)
        return render(p)

    def renderExtra(self):
        s = super(BatchingMixin, self).renderExtra()
        return u'\n'.join(filter(None, (s, self.renderNav())))

    def __call__(self):
        s = super(BatchingMixin, self).__call__()
        return u'\n'.join(filter(None, (self.renderNav(), s)))

##############################################################################

def sanitise(bstart, bsize, nitems):
        """ Returns sanitised values for bstart and bsize.
        """
        bsize = bsize or sys.maxint # __zero__ not allowed
        # must be non-negative and rounded to bsize multiple
        bstart = bstart or 0
        if bstart < 0:
            bstart = 0
        bstart = min(bsize*(bstart/bsize), bsize*(nitems/bsize))
        return bstart, bsize

##############################################################################

def toInt(x):
    if x is not None:
        try: return int(x)
        except ValueError: pass

##############################################################################
