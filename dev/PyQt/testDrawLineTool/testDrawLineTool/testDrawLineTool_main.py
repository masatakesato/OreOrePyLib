from oreorepylib.utils import environment

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



style = """
QGraphicsView
{
    background-color: rgb(127,127,127);
}

QGraphicsView:focus
{
    background-color: rgb(200,200,200);
    border: 2px solid rgb(127,0,0);
}
"""


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.view = View(self)
        self.view.setStyleSheet( style )
        self.button = QPushButton('Clear View', self)
        self.button.clicked.connect(self.handleClearView)
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)

    def handleClearView(self):
        self.view.scene().clear()



class OreOreScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(OreOreScene,self).__init__(parent)
        self.line = None


    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != Qt.LeftButton):
            return

        self.line = QGraphicsLineItem(QLineF(mouseEvent.scenePos(), mouseEvent.scenePos()))
        #self.line.setPen(QPen(self.myLineColor, 2))
        self.addItem(self.line)

        super(OreOreScene, self).mousePressEvent(mouseEvent)


    def mouseMoveEvent(self, mouseEvent):

        if( self.line ):
            newLine = QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)

        else:
            super(OreOreScene, self).mouseMoveEvent(mouseEvent)


    def mouseReleaseEvent(self, mouseEvent):

        #if self.line:
        #    startItems = self.items(self.line.line().p1())

        #    if len(startItems) and startItems[0] == self.line:
        #        startItems.pop(0)
        #    endItems = self.items(self.line.line().p2())
        #    if len(endItems) and endItems[0] == self.line:
        #        endItems.pop(0)

        #    self.removeItem(self.line)
        #    self.line = None

        #    if len(startItems) and len(endItems) and \
        #            isinstance(startItems[0], DiagramItem) and \
        #            isinstance(endItems[0], DiagramItem) and \
        #            startItems[0] != endItems[0]:
        #        startItem = startItems[0]
        #        endItem = endItems[0]
                
        if( self.line and  self.line.line().length() < 1.0e-5 ):
            self.removeItem( self.line )
        self.line = None
        super(OreOreScene, self).mouseReleaseEvent(mouseEvent)



class View(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        self.setScene(OreOreScene(self)) #QGraphicsScene(self))
        self.setSceneRect(QRectF(self.viewport().rect()))

    #def mousePressEvent(self, event):
    #    self._start = event.pos()

    #    super(QGraphicsView, self).mousePressEvent(event)


    #def mouseReleaseEvent(self, event):

    #    start = QPointF(self.mapToScene(self._start))
    #    end = QPointF(self.mapToScene(event.pos()))
    #    self.scene().addItem(
    #        QGraphicsLineItem(QLineF(start, end)))
    #    for point in (start, end):
    #        text = self.scene().addSimpleText(
    #            '(%d, %d)' % (point.x(), point.y()))
    #        text.setBrush(Qt.red)
    #        text.setPos(point)

    #    super(QGraphicsView, self).mouseReleaseEvent(event)




if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())







#class DiagramScene(QGraphicsScene):
#    InsertItem, InsertLine, InsertText, MoveItem  = range(4)

#    itemInserted = pyqtSignal(DiagramItem)

#    textInserted = pyqtSignal(QGraphicsTextItem)

#    itemSelected = pyqtSignal(QGraphicsItem)

#    def __init__(self, itemMenu, parent=None):
#        super(DiagramScene, self).__init__(parent)

#        self.myItemMenu = itemMenu
#        self.myMode = self.MoveItem
#        self.myItemType = DiagramItem.Step
#        self.line = None
#        self.textItem = None
#        self.myItemColor = Qt.white
#        self.myTextColor = Qt.black
#        self.myLineColor = Qt.black
#        self.myFont = QFont()

#    def setLineColor(self, color):
#        self.myLineColor = color
#        if self.isItemChange(Arrow):
#            item = self.selectedItems()[0]
#            item.setColor(self.myLineColor)
#            self.update()

#    def setTextColor(self, color):
#        self.myTextColor = color
#        if self.isItemChange(DiagramTextItem):
#            item = self.selectedItems()[0]
#            item.setDefaultTextColor(self.myTextColor)

#    def setItemColor(self, color):
#        self.myItemColor = color
#        if self.isItemChange(DiagramItem):
#            item = self.selectedItems()[0]
#            item.setBrush(self.myItemColor)

#    def setFont(self, font):
#        self.myFont = font
#        if self.isItemChange(DiagramTextItem):
#            item = self.selectedItems()[0]
#            item.setFont(self.myFont)

#    def setMode(self, mode):
#        self.myMode = mode

#    def setItemType(self, type):
#        self.myItemType = type

#    def editorLostFocus(self, item):
#        cursor = item.textCursor()
#        cursor.clearSelection()
#        item.setTextCursor(cursor)

#        if item.toPlainText():
#            self.removeItem(item)
#            item.deleteLater()

#    def mousePressEvent(self, mouseEvent):
#        if (mouseEvent.button() != Qt.LeftButton):
#            return

#        if self.myMode == self.InsertItem:
#            item = DiagramItem(self.myItemType, self.myItemMenu)
#            item.setBrush(self.myItemColor)
#            self.addItem(item)
#            item.setPos(mouseEvent.scenePos())
#            self.itemInserted.emit(item)
#        elif self.myMode == self.InsertLine:
#            self.line = QGraphicsLineItem(QLineF(mouseEvent.scenePos(),
#                    mouseEvent.scenePos()))
#            self.line.setPen(QPen(self.myLineColor, 2))
#            self.addItem(self.line)
#        elif self.myMode == self.InsertText:
#            textItem = DiagramTextItem()
#            textItem.setFont(self.myFont)
#            textItem.setTextInteractionFlags(Qt.TextEditorInteraction)
#            textItem.setZValue(1000.0)
#            textItem.lostFocus.connect(self.editorLostFocus)
#            textItem.selectedChange.connect(self.itemSelected)
#            self.addItem(textItem)
#            textItem.setDefaultTextColor(self.myTextColor)
#            textItem.setPos(mouseEvent.scenePos())
#            self.textInserted.emit(textItem)

#        super(DiagramScene, self).mousePressEvent(mouseEvent)

#    def mouseMoveEvent(self, mouseEvent):
#        if self.myMode == self.InsertLine and self.line:
#            newLine = QLineF(self.line.line().p1(), mouseEvent.scenePos())
#            self.line.setLine(newLine)
#        elif self.myMode == self.MoveItem:
#            super(DiagramScene, self).mouseMoveEvent(mouseEvent)

#    def mouseReleaseEvent(self, mouseEvent):
#        if self.line and self.myMode == self.InsertLine:
#            startItems = self.items(self.line.line().p1())
#            if len(startItems) and startItems[0] == self.line:
#                startItems.pop(0)
#            endItems = self.items(self.line.line().p2())
#            if len(endItems) and endItems[0] == self.line:
#                endItems.pop(0)

#            self.removeItem(self.line)
#            self.line = None

#            if len(startItems) and len(endItems) and \
#                    isinstance(startItems[0], DiagramItem) and \
#                    isinstance(endItems[0], DiagramItem) and \
#                    startItems[0] != endItems[0]:
#                startItem = startItems[0]
#                endItem = endItems[0]
#                arrow = Arrow(startItem, endItem)
#                arrow.setColor(self.myLineColor)
#                startItem.addArrow(arrow)
#                endItem.addArrow(arrow)
#                arrow.setZValue(-1000.0)
#                self.addItem(arrow)
#                arrow.updatePosition()

#        self.line = None
#        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)

#    def isItemChange(self, type):
#        for item in self.selectedItems():
#            if isinstance(item, type):
#                return True
#        return False
