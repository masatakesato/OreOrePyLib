import sys, os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# http://stackoverflow.com/questions/26227885/drag-and-drop-rows-within-qtablewidget

#class TableWidgetDragRows(QTableWidget):
#    def __init__(self, *args, **kwargs):
#        QTableWidget.__init__(self, *args, **kwargs)

#        self.setDragEnabled(True)
#        self.setAcceptDrops(True)
#        self.viewport().setAcceptDrops(True)
#        self.setDragDropOverwriteMode(False)
#        self.setDropIndicatorShown(True)

#        self.setSelectionMode(QAbstractItemView.SingleSelection) 
#        self.setSelectionBehavior(QAbstractItemView.SelectRows)
#        self.setDragDropMode(QAbstractItemView.InternalMove)   

#    def dropEvent(self, event):
#        if event.source() == self and (event.dropAction() == Qt.MoveAction or self.dragDropMode() == QAbstractItemView.InternalMove):
#            success, row, col, topIndex = self.dropOn(event)
#            if success:             
#                selRows = self.getSelectedRowsFast()                        

#                top = selRows[0]
#                # print 'top is %d'%top
#                dropRow = row
#                if dropRow == -1:
#                    dropRow = self.rowCount()
#                # print 'dropRow is %d'%dropRow
#                offset = dropRow - top
#                # print 'offset is %d'%offset

#                for i, row in enumerate(selRows):
#                    r = row + offset
#                    if r > self.rowCount() or r < 0:
#                        r = 0
#                    self.insertRow(r)
#                    # print 'inserting row at %d'%r


#                selRows = self.getSelectedRowsFast()
#                # print 'selected rows: %s'%selRows

#                top = selRows[0]
#                # print 'top is %d'%top
#                offset = dropRow - top                
#                # print 'offset is %d'%offset
#                for i, row in enumerate(selRows):
#                    r = row + offset
#                    if r > self.rowCount() or r < 0:
#                        r = 0

#                    for j in range(self.columnCount()):
#                        # print 'source is (%d, %d)'%(row, j)
#                        # print 'item text: %s'%self.item(row,j).text()
#                        source = QTableWidgetItem(self.item(row, j))
#                        # print 'dest is (%d, %d)'%(r,j)
#                        self.setItem(r, j, source)

#                # Why does this NOT need to be here?
#                # for row in reversed(selRows):
#                    # self.removeRow(row)

#                event.accept()

#        else:
#            QTableView.dropEvent(event)                

#    def getSelectedRowsFast(self):
#        selRows = []
#        for item in self.selectedItems():
#            if item.row() not in selRows:
#                selRows.append(item.row())
#        return selRows

#    def droppingOnItself(self, event, index):
#        dropAction = event.dropAction()

#        if self.dragDropMode() == QAbstractItemView.InternalMove:
#            dropAction = Qt.MoveAction

#        if event.source() == self and event.possibleActions() & Qt.MoveAction and dropAction == Qt.MoveAction:
#            selectedIndexes = self.selectedIndexes()
#            child = index
#            while child.isValid() and child != self.rootIndex():
#                if child in selectedIndexes:
#                    return True
#                child = child.parent()

#        return False

#    def dropOn(self, event):
#        if event.isAccepted():
#            return False, None, None, None

#        index = QModelIndex()
#        row = -1
#        col = -1

#        if self.viewport().rect().contains(event.pos()):
#            index = self.indexAt(event.pos())
#            if not index.isValid() or not self.visualRect(index).contains(event.pos()):
#                index = self.rootIndex()

#        if self.model().supportedDropActions() & event.dropAction():
#            if index != self.rootIndex():
#                dropIndicatorPosition = self.position(event.pos(), self.visualRect(index), index)

#                if dropIndicatorPosition == QAbstractItemView.AboveItem:
#                    row = index.row()
#                    col = index.column()
#                    # index = index.parent()
#                elif dropIndicatorPosition == QAbstractItemView.BelowItem:
#                    row = index.row() + 1
#                    col = index.column()
#                    # index = index.parent()
#                else:
#                    row = index.row()
#                    col = index.column()

#            if not self.droppingOnItself(event, index):
#                # print 'row is %d'%row
#                # print 'col is %d'%col
#                return True, row, col, index

#        return False, None, None, None

#    def position(self, pos, rect, index):
#        r = QAbstractItemView.OnViewport
#        margin = 2
#        if pos.y() - rect.top() < margin:
#            r = QAbstractItemView.AboveItem
#        elif rect.bottom() - pos.y() < margin:
#            r = QAbstractItemView.BelowItem 
#        elif rect.contains(pos, True):
#            r = QAbstractItemView.OnItem

#        if r == QAbstractItemView.OnItem and not (self.model().flags(index) & Qt.ItemIsDropEnabled):
#            r = QAbstractItemView.AboveItem if pos.y() < rect.center().y() else QAbstractItemView.BelowItem

#        return r


#class Window(QWidget):
#    def __init__(self):
#        super(Window, self).__init__()

#        layout = QHBoxLayout()
#        self.setLayout(layout) 

#        self.table_widget = TableWidgetDragRows()
#        layout.addWidget(self.table_widget) 

#        # setup table widget
#        self.table_widget.setColumnCount(2)
#        self.table_widget.setHorizontalHeaderLabels(['Colour', 'Model'])

#        items = [('Red', 'Toyota'), ('Blue', 'RV'), ('Green', 'Beetle')]
#        for i, (colour, model) in enumerate(items):
#            c = QTableWidgetItem(colour)
#            m = QTableWidgetItem(model)

#            self.table_widget.insertRow(self.table_widget.rowCount())
#            self.table_widget.setItem(i, 0, c)
#            self.table_widget.setItem(i, 1, m)

#        self.show()


#app = QApplication(sys.argv)
#window = Window()
#sys.exit(app.exec_())




# http://stackoverflow.com/questions/34533878/drag-and-dropping-rows-between-two-separate-qtablewidgets

class TableWidgetDragRows(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropOverwriteMode(False)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.last_drop_row = None

    # Override this method to get the correct row index for insertion
    def dropMimeData(self, row, col, mimeData, action):
        self.last_drop_row = row
        return True


    def dropEvent(self, event):
        # The QTableWidget from which selected rows will be moved
        sender = event.source()

        # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
        super().dropEvent(event)
        # Now we know where to insert selected row(s)
        dropRow = self.last_drop_row

        selectedRows = sender.getselectedRowsFast()

        # Allocate space for transfer
        for _ in selectedRows:
            self.insertRow(dropRow)

        # if sender == receiver (self), after creating new empty rows selected rows might change their locations
        sel_rows_offsets = [0 if self != sender or srow < dropRow else len(selectedRows) for srow in selectedRows]
        selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]

        # copy content of selected rows into empty ones
        for i, srow in enumerate(selectedRows):
            for j in range(self.columnCount()):
                item = sender.item(srow, j)
                if item:
                    source = QTableWidgetItem(item)
                    self.setItem(dropRow + i, j, source)

        # delete selected rows
        for srow in reversed(selectedRows):
            sender.removeRow(srow)

        event.accept()


    def getselectedRowsFast(self):
        selectedRows = []
        for item in self.selectedItems():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
        selectedRows.sort()
        return selectedRows


class Window(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.table_widgets = []
        for _ in range(3):
            tw = TableWidgetDragRows()
            tw.setColumnCount(2)
            tw.setHorizontalHeaderLabels(['Colour', 'Model'])

            self.table_widgets.append(tw)
            layout.addWidget(tw)

        filled_widget = self.table_widgets[0]
        items = [('Red', 'Toyota'), ('Blue', 'RV'), ('Green', 'Beetle')]
        for i, (colour, model) in enumerate(items):
            c = QTableWidgetItem(colour)
            m = QTableWidgetItem(model)

            filled_widget.insertRow(filled_widget.rowCount())
            filled_widget.setItem(i, 0, c)
            filled_widget.setItem(i, 1, m)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())