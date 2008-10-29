##############################################################################
#
# Copyright (c) 2007 YOMA PTY LTD. All Rights Reserved.
#
##############################################################################
"""layout add-on for zope.formlib

$Id$
"""

from StringIO import StringIO

from zope.interface import implements
from zope.app import pagetemplate

from yoma.layout.grid import Grid, Cell
from yoma.layout.interfaces import ILayout

##############################################################################

_marker=object()

class GridLayout(object):
    implements(ILayout)

    def __init__(self, labelpos=None, formatter=None):
        self.grid = Grid()

    def addLayout(self, layout, row, col, rowspan=1, colspan=1):
        self.grid.set(row, col, LayoutCell(layout, colspan, rowspan))
        return self

    def addText(self, text, row, col, rowspan=1, colspan=1):
        self.grid.set(row, col, TextCell(text, colspan, rowspan))
        return self

    def addAction(self, name, row, col, rowspan=1, colspan=1, label=_marker):
        self.grid.set(row, col, ActionCell(name, label, colspan, rowspan))
        return self

    def addWidget(self,
        name, row, col, rowspan=1, colspan=1, label=_marker, hint=_marker,
        ):
        widgetcell = WidgetCell(name, label, hint, rowspan, colspan)
        if label is None:
            # hide label - swallow up the label column
            widgetcell.width += 1
            self.grid.set(row, col, widgetcell)
        else:
            self.grid.set(row, col, LabelCell(widgetcell))
            self.grid.set(row, col+1, widgetcell)
        return self

    def render(self, form):
        formatter = TableFormatter(self.grid, form)
        return formatter()

##############################################################################

class VertLayout(GridLayout):

    def __init__(self, *args, **kw):
        super(VertLayout, self).__init__(*args, **kw)
        self._row = 0

    def addLayout(self, layout):
        row = self._row
        self._row += 1
        return super(VertLayout, self).addLayout(layout, row, 0, colspan=2)

    def addText(self, text):
        row = self._row
        self._row += 1
        return super(VertLayout, self).addText(text, row, 0, colspan=2)

    def addAction(self, name, label=_marker):
        row = self._row
        self._row += 1
        return super(VertLayout, self).addAction(name, row, 0, colspan=2,
                                                 label=label)

    def addWidget(self, name, label=_marker, hint=_marker):
        row = self._row
        self._row += 1
        return super(VertLayout, self).addWidget(name, row, 0, label=label,
                                                 hint=hint)

    def add(self, *items):
        for item in items:
            if ILayout.providedBy(item):
                self.addLayout(item)
            else:
                if item.startswith('action.'):
                    self.addAction(item[7:])
                else:
                    self.addWidget(item)
        return self
            
##############################################################################

class HorzLayout(GridLayout):

    def __init__(self, *args, **kw):
        super(HorzLayout, self).__init__(*args, **kw)
        self._col = 0

    def addLayout(self, layout):
        col = self._col
        self._col += 1
        return super(HorzLayout, self).addLayout(layout, 0, col)

    def addText(self, text):
        col = self._col
        self._col += 1
        return super(HorzLayout, self).addText(text, 0, col)

    def addAction(self, name, label=_marker):
        col = self._col
        self._col += 1
        return super(HorzLayout, self).addAction(name, 0, col, label=label)

    def addWidget(self, name, label=_marker, hint=_marker):
        col = self._col
        self._col += 2
        return super(HorzLayout, self).addWidget(name, 0, col, label=label,
                                                 hint=hint)

    def add(self, *items):
        for item in items:
            if ILayout.providedBy(item):
                self.addLayout(item)
            else:
                if item.startswith('action.'):
                    self.addAction(item[7:])
                else:
                    self.addWidget(item)
        return self
            
##############################################################################

class LayoutCell(Cell):

    def render(self, form):
        layout = self()
        return layout.render(form)


class TextCell(Cell):

    def render(self, form):
        return self()


class WidgetCell(Cell):

    def __init__(self, name, label, hint, width=1, height=1): 
        super(WidgetCell, self).__init__((name, label, hint), width, height)

    def render(self, form):
        name, label, hint = self()
        widget = form.widgets[name]
        if hint is _marker:
            hint = widget.hint
        s = widget()
        if hint:
            s += u'\n<div>%s</div>' % hint
        return s


class LabelCell(Cell):

    def render(self, form):
        widgetcell = self()
        name, label, hint = widgetcell()
        widget = form.widgets[name]
        if label is _marker:
            label = widget.label
        return label


class ActionCell(Cell):

    def __init__(self, name, label, width=1, height=1): 
        super(ActionCell, self).__init__((name, label), width, height)

    def render(self, form):
        name, label = self()
        action = form.actions['form.actions.'+name]
        return action.render()

##############################################################################

class TableFormatter(object):

    def __init__(self, grid, form):
        self.grid = grid
        self.form = form

    def renderCell(self, cell):
        attr = u''
        if cell.width > 1:
            attr += (u' colspan="%s"' % cell.width)
        if cell.height > 1:
            attr += (u' rowspan="%s"' % cell.height)
        print>>self.out, u'<td%s>%s</td>' % (attr, cell.render(self.form))

    def __call__(self):
        self.out = StringIO()
        grid = self.grid
        form = self.form
        out = self.out
        print>>out
        print>>out, u'<table>'
        for row in grid.iterRows():
            print>>out, '<tr>'
            for col in grid.iterCols(row):
                cell = grid.get(row, col)
                self.renderCell(cell)
            print>>out, '</tr>'
        print>>out, u'</table>'
        return out.getvalue()

##############################################################################

class LabelRenderer(object):

    template = pagetemplate.ViewPageTemplateFile('label.pt')

    def __init__(self, context, request, label):
        self.context = context
        self.request = request
        self.label = label

    def render(self):
        return self.template()

##############################################################################

class WidgetRenderer(object):

    template = pagetemplate.ViewPageTemplateFile('widget.pt')

    def __init__(self, context, request, widget):
        self.context = context
        self.request = request
        self.widget = widget

    def render(self):
        return self.template()

##############################################################################

#XXX todo - change to component look up

_default_label_renderer = LabelRenderer
_default_widget_renderer = WidgetRenderer

def getDefaultLabelRenderer():
    return _default_label_renderer

def setDefaultLabelRenderer(renderer):
    global _default_label_renderer
    _default_label_renderer = renderer

def getDefaultWidgetRenderer():
    global _default_widget_renderer
    return _default_widget_renderer

def setDefaultWidgetRenderer(renderer):
    _default_widget_renderer = renderer

def resetDefaultRenderers():
    global _default_label_renderer
    global _default_widget_renderer
    _default_label_renderer = LabelRenderer
    _default_widget_renderer = WidgetRenderer

##############################################################################

