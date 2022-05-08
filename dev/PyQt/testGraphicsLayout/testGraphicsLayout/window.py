from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from layoutitem import LayoutItem



class Window(QGraphicsWidget):

    def __init__( self, parent=None ):
        super(Window, self).__init__(parent)#, Qt.Window)

        windowLayout = QGraphicsLinearLayout(Qt.Vertical)
        linear = QGraphicsLinearLayout(windowLayout)
        item = LayoutItem()
        linear.addItem(item)
        linear.setStretchFactor(item, 1)

        #item2 = LayoutItem()
        #linear.addItem(item2)
        #linear.setStretchFactor(item2, 3)
        windowLayout.addItem(linear)

        #grid = QGraphicsGridLayout(windowLayout)
        #item = LayoutItem()
        #grid.addItem(item, 0, 0, 4, 1)
        #item = LayoutItem()
        #item.setMaximumHeight(item.minimumHeight())
        #grid.addItem(item, 0, 1, 2, 1, Qt.AlignVCenter)
        #item = LayoutItem()
        #item.setMaximumHeight(item.minimumHeight())
        #grid.addItem(item, 2, 1, 2, 1, Qt.AlignVCenter)
        #item = LayoutItem()
        #grid.addItem(item, 0, 2)
        #item = LayoutItem()
        #grid.addItem(item, 1, 2)
        #item = LayoutItem()
        #grid.addItem(item, 2, 2)
        #item = LayoutItem()
        #grid.addItem(item, 3, 2)
        #windowLayout.addItem(grid)

        self.setLayout(windowLayout)
        self.setWindowTitle( "Basic Graphics Layouts Example" )
