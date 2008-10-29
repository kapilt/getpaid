##############################################################################
#
# Copyright (c) 2007 YOMA PTY LTD. All Rights Reserved.
#
##############################################################################
"""grid for layouts

$Id$
"""

from zope.interface import implements
from yoma.layout.interfaces import IGrid, ICell

##############################################################################

class _Reserved:
    def __repr__(self):
        return 'reserved'
_reserved = _Reserved()


class Grid(object):
    implements(IGrid)

    width=0
    height=0

    def __init__(self):
        self.cells = {}

    def set(self, row, col, cell):
        # check for cell collision
        for i in range(row, row+cell.height):
            for j in range(col, col+cell.width):
                try:
                    self.get(i, j)
                    raise IndexError('cell taken: row %s, col %s' % (i, j))
                except KeyError:
                    pass
        # write cell and reserve adjacent cells if necessary
        for i in range(row, row+cell.height):
            for j in range(col, col+cell.width):
                if i==row and j==col:
                    self.__set(i, j, cell)
                else:
                    self.__set(i, j, Cell(_reserved))
        self.width = max(self.width, col+cell.width)
        self.height = max(self.height, row+cell.height)

    def __set(self, row, col, ob):
        self.cells.setdefault(row, {})[col] = ob

    def get(self, row, col):
        return self.cells[row][col]

    def iter(self, showall=False):
        for i in sorted(self.cells):
            row = self.cells[i]
            for j in sorted(row):
                cell = row[j]
                if showall or (cell() is not _reserved):
                    yield i, j, cell

    def iterRows(self):
        for i in sorted(self.cells):
            # only return rows which have non-reserved cell(s)
            if len([j for j in self.iterCols(i)]):
                yield i

    def iterCols(self, row):
        for j in sorted(self.cells[row]):
            cell = self.get(row, j)
            if cell() is _reserved:
                continue
            yield j

    def __repr__(self):
        return '%s(width=%s, height=%s)' % (
            self.__class__.__name__, self.width, self.height)

##############################################################################

class Cell(object):
    implements(ICell)

    def __init__(self, value, width=1, height=1):
        self.value = value
        self.width = width
        self.height = height

    def __call__(self):
        return self.value

    def __repr__(self):
        return '%s(%s, width=%s, height=%s)' % (
            self.__class__.__name__,
            repr(self.value),
            self.width,
            self.height)

##############################################################################

