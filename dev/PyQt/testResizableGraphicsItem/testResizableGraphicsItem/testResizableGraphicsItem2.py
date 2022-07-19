# https://stackoverflow.com/questions/34429632/resize-a-qgraphicsitem-with-the-mouse

import sip
import sys
from enum import IntEnum

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *





class DataFlow(IntEnum):
    Unknown         = -1
    Input           = 0
    Output          = 1
    Internal        = 2 # internal.




# Commonn Settings
g_TitlebarHeight = 25
g_AttribAreaHeight = 25
g_LabelMargin = 10
g_LabelColor = QColor(0, 64, 128)#QColor(255,255,255)
g_WidthMargin = 5
g_HeightMargin = 5
g_BoxRoundRadius = 5




# Label Graphics Settings
g_LabelFont = QFont('Times', 9.0)


# Port Graphics Settings
g_PortDepth = 2
g_PortRadius = 7.5
g_PortFrameWidth = 1.75

g_PortColor = [ QColor(150, 200, 100), QColor(80,90,75) ] 
g_PortFrameColor = QColor(32,32,32)




class Port(QGraphicsItem):

    def __init__(self, name, object_id, portType):
        super(Port, self).__init__()

        # attributes
        #self.__m_ID = object_id
        self.__m_Name = name
        self.__m_Flow = portType

        self.radius = g_PortRadius
        self.diam = self.radius * 2
        self.__m_PortRect = QRectF( -self.diam, -self.diam, self.diam*2, self.diam*2 )

        self.path = QPainterPath()
        self.path.addEllipse( self.__m_PortRect )

        self.__m_Pen = QPen(g_PortFrameColor, g_PortFrameWidth)

        # create label graphics object
        self.__m_Font = g_LabelFont
        self.__m_LabelAlignment = Qt.AlignBottom | (Qt.AlignLeft if self.__m_Flow==DataFlow.Input else Qt.AlignRight)
        self.__m_LabelMargin = g_LabelMargin
        self.__m_LabelRect = QRectF()
        self.__m_BoundingRect = QRectF()

        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.__UpdateBoundingRect()

        ## connected edges
        #self.__m_ConnectedEdges = {}


    #def ConnectEdge( self, edge ):
    #    self.__m_ConnectedEdges[ edge.Name() ] = edge


    #def DisconnectEdge( self, edge ):
    #    name = edge.Name()
    #    if( name in self.__m_ConnectedEdges ):
    #        self.__m_ConnectedEdges[ name ] = None
    #        del self.__m_ConnectedEdges[ name ]


    def SetName( self, name ):
        self.__m_Name = name
        self.__UpdateBoundingRect()


    #def ConnectedEdges( self ):
    #    return self.__m_ConnectedEdges


    def Name( self ):
        return self.parentItem().Name() + '.' + self.__m_Name


    def ParentName( self ):
        return self.parentItem().Name()


    def LocalName( self ):
        return self.__m_Name


    #def ParentID( self ):
    #    return self.__m_ID[0]


    #def ID( self ):
    #    return self.__m_ID[1]


    #def PortID( self ):
    #    return self.__m_ID
        

    def DataFlow( self ):
        return self.__m_Flow


    def IsInputFlow( self ):
        return self.__m_Flow==DataFlow.Input


    def IsOutputFlow( self ):
        return self.__m_Flow==DataFlow.Output


    def __UpdateBoundingRect( self, max_width=1000 ):

        fm = QFontMetricsF( self.__m_Font )
        label_dim = ( min( fm.width(self.__m_Name)+1.0, max_width), fm.height() )


        label_pos = ( self.__m_LabelMargin, -label_dim[1]*0.5 ) if self.__m_Flow==DataFlow.Input else ( -self.__m_LabelMargin - label_dim[0], -label_dim[1]*0.5 )
        self.__m_LabelRect = QRectF( label_pos[0], label_pos[1], label_dim[0], label_dim[1] )

        bb_min = ( min( self.__m_PortRect.left(), self.__m_LabelRect.left() ), min( self.__m_PortRect.top(), self.__m_LabelRect.top() ) )
        bb_max = ( max( self.__m_PortRect.right(), self.__m_LabelRect.right() ), max( self.__m_PortRect.bottom(), self.__m_LabelRect.bottom() ) )
        self.__m_BoundingRect = QRectF( bb_min[0], bb_min[1], bb_max[0]-bb_min[0], bb_max[1]-bb_min[1] )



    #def __UpdateEdgePath( self ):

    #    if( self.__m_Flow==DataFlow.Input ):
    #        for edge in self.__m_ConnectedEdges.values():
    #            edge.SetDestPosition( self.scenePos() )
    #            edge.UpdatePath()
    #    else:
    #        for edge in self.__m_ConnectedEdges.values():
    #            edge.SetSourcePosition( self.scenePos() )
    #            edge.UpdatePath()



    ########################### QGraphicsItem func override ################################

    def itemChange( self, change, value ):

        ## workaround for pyqt bug:
        ## http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        if( change==QGraphicsItem.ItemParentChange ):
            print( '!!!!!')#return sip.cast(value, QGraphicsItem)

        return super(Port, self).itemChange( change, value )


    def boundingRect(self):
        return self.__m_BoundingRect


    def shape(self):
        #if( self.scene().FocusViewID() != self._IGraphicsPortItem__m_RenderLayerID ):# QGraphicsViewごとにアイテムの表示/非表示を視切り替えて正しく動かすのに必要
        #    return QPainterPath()
        return self.path


    def paint(self, painter, option, widget):
        #if( self.scene().IsVisibleFromActiveView(self)==False ):
        #    return
        painter.setClipRect(option.exposedRect)
        painter.setPen(self.__m_Pen)
        painter.setBrush(g_PortColor[self.__m_Flow])
        painter.drawRoundedRect( -self.radius, -self.radius, self.diam, self.diam, self.radius, self.radius )

        #if( option.levelOfDetailFromTransform(painter.worldTransform()) < 0.5):
        #    return 
        painter.setFont( self.__m_Font )
        painter.setPen(g_LabelColor)
        painter.drawText( self.__m_LabelRect, self.__m_LabelAlignment, self.__m_Name )















class GraphicsRectItem(QGraphicsRectItem):

    #handleTopLeft = 1
    #handleTopMiddle = 2
    #handleTopRight = 3
    #handleMiddleLeft = 4
    handleMiddleRight = 5
    #handleBottomLeft = 6
    #handleBottomMiddle = 7
    #handleBottomRight = 8

    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        #handleTopLeft: Qt.SizeFDiagCursor,
        #handleTopMiddle: Qt.SizeVerCursor,
        #handleTopRight: Qt.SizeBDiagCursor,
        #handleMiddleLeft: Qt.SizeHorCursor,
        handleMiddleRight: Qt.SizeHorCursor,
        #handleBottomLeft: Qt.SizeBDiagCursor,
        #handleBottomMiddle: Qt.SizeVerCursor,
        #handleBottomRight: Qt.SizeFDiagCursor,
    }


    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()


    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        
        for k, v, in self.handles.items():

            print( v.left(), v.right(), point.x() )

            if v.contains(point):
                return k
        return None


    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        print( 'hoverEnterEvent()...' )
        return super().hoverEnterEvent(QGraphicsSceneHoverEvent)


    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        print( 'hoverMoveEvent()...' )
        handle = self.handleAt(moveEvent.pos())
        cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
        self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)


    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        print( 'hoverLeaveEvent()...' )
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)


    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)


    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        print( 'mouseMoveEvent()...' )
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)


    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()


    def boundingRect( self ):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)


    def updateHandlesPos( self ):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()

        #self.handles[self.handleTopLeft] = QRectF( b.left(), b.top(), s, s )
        #self.handles[self.handleTopRight] = QRectF( b.right() - s, b.top(), s, s )
        #self.handles[self.handleBottomRight] = QRectF( b.right() - s, b.bottom() - s, s, s )
        #self.handles[self.handleBottomLeft] = QRectF( b.left(), b.bottom() - s, s, s )

        #self.handles[self.handleTopMiddle] = QRectF( b.left()+s, b.top(), b.width()-2*s, s ) #QRectF(b.center().x() - s / 2, b.top(), s, s)
        self.handles[self.handleMiddleRight] = QRectF( b.right()-12, b.top()+s, 8, b.height()-2*s ) #QRectF(b.right() - s, b.center().y() - s / 2, s, s)
        #self.handles[self.handleBottomMiddle] = QRectF( b.left()+s, b.bottom()-s, b.width()-2*s, s )#QRectF(b.center().x() - s / 2, b.bottom() - s, s, s)
        #self.handles[self.handleMiddleLeft] = QRectF( b.left(), b.top()+s, s, b.height()-2*s ) #QRectF(b.left(), b.center().y() - s / 2, s, s)
        

    def interactiveResize( self, mousePos ):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        #if self.handleSelected == self.handleTopLeft:

        #    fromX = self.mousePressRect.left()
        #    fromY = self.mousePressRect.top()
        #    toX = fromX + mousePos.x() - self.mousePressPos.x()
        #    toY = fromY + mousePos.y() - self.mousePressPos.y()
        #    diff.setX(toX - fromX)
        #    diff.setY(toY - fromY)
        #    boundingRect.setLeft(toX)
        #    boundingRect.setTop(toY)
        #    rect.setLeft(boundingRect.left() + offset)
        #    rect.setTop(boundingRect.top() + offset)
        #    self.setRect(rect)

        #elif self.handleSelected == self.handleTopMiddle:

        #    fromY = self.mousePressRect.top()
        #    toY = fromY + mousePos.y() - self.mousePressPos.y()
        #    diff.setY(toY - fromY)
        #    boundingRect.setTop(toY)
        #    rect.setTop(boundingRect.top() + offset)
        #    self.setRect(rect)

        #elif self.handleSelected == self.handleTopRight:

        #    fromX = self.mousePressRect.right()
        #    fromY = self.mousePressRect.top()
        #    toX = fromX + mousePos.x() - self.mousePressPos.x()
        #    toY = fromY + mousePos.y() - self.mousePressPos.y()
        #    diff.setX(toX - fromX)
        #    diff.setY(toY - fromY)
        #    boundingRect.setRight(toX)
        #    boundingRect.setTop(toY)
        #    rect.setRight(boundingRect.right() - offset)
        #    rect.setTop(boundingRect.top() + offset)
        #    self.setRect(rect)

        #elif self.handleSelected == self.handleMiddleLeft:

        #    fromX = self.mousePressRect.left()
        #    toX = fromX + mousePos.x() - self.mousePressPos.x()
        #    diff.setX(toX - fromX)
        #    boundingRect.setLeft(toX)
        #    rect.setLeft(boundingRect.left() + offset)
        #    self.setRect(rect)

        if self.handleSelected == self.handleMiddleRight:

            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right() - offset)
            self.setRect(rect)

        #elif self.handleSelected == self.handleBottomLeft:

        #    fromX = self.mousePressRect.left()
        #    fromY = self.mousePressRect.bottom()
        #    toX = fromX + mousePos.x() - self.mousePressPos.x()
        #    toY = fromY + mousePos.y() - self.mousePressPos.y()
        #    diff.setX(toX - fromX)
        #    diff.setY(toY - fromY)
        #    boundingRect.setLeft(toX)
        #    boundingRect.setBottom(toY)
        #    rect.setLeft(boundingRect.left() + offset)
        #    rect.setBottom(boundingRect.bottom() - offset)
        #    self.setRect(rect)

        #elif self.handleSelected == self.handleBottomMiddle:

        #    fromY = self.mousePressRect.bottom()
        #    toY = fromY + mousePos.y() - self.mousePressPos.y()
        #    diff.setY(toY - fromY)
        #    boundingRect.setBottom(toY)
        #    rect.setBottom(boundingRect.bottom() - offset)
        #    self.setRect(rect)

        #elif self.handleSelected == self.handleBottomRight:

        #    fromX = self.mousePressRect.right()
        #    fromY = self.mousePressRect.bottom()
        #    toX = fromX + mousePos.x() - self.mousePressPos.x()
        #    toY = fromY + mousePos.y() - self.mousePressPos.y()
        #    diff.setX(toX - fromX)
        #    diff.setY(toY - fromY)
        #    boundingRect.setRight(toX)
        #    boundingRect.setBottom(toY)
        #    rect.setRight(boundingRect.right() - offset)
        #    rect.setBottom(boundingRect.bottom() - offset)
        #    self.setRect(rect)

        self.updateHandlesPos()

        self.__UpdatePortPosition()


    def shape( self ):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        #if self.isSelected():
        #    for shape in self.handles.values():
        #        path.addEllipse(shape)
        return path


    def paint( self, painter, option, widget=None ):
        """
        Paint the node in the graphic view.
        """
        painter.setBrush(QBrush(QColor(255, 0, 0, 100)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawRect(rect)


    def AddPort( self, port ):

        port.setParentItem(self)

        # create port object
        if( port.DataFlow()==DataFlow.Input ):
            #idx = 0
            #posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)
            port.setPos( 0, 25 )
            

        elif( port.DataFlow()==DataFlow.Output ):
            
            #idx = 0
            #posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)
            port.setPos( self.boundingRect().width()-self.handleSize, 25 )
            


    def __UpdatePortPosition( self ):

        b = self.boundingRect()
        max_width = max( b.width() * 0.5 - self.handleSize - g_LabelMargin, 0 )

        for port in self.childItems():
            if( port.DataFlow()==DataFlow.Input ):
                #idx = 0
                #posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)
                port.setPos( b.left() + self.handleSize/2, 25 )
                port._Port__UpdateBoundingRect( max_width )

            elif( port.DataFlow()==DataFlow.Output ):
            
                #idx = 0
                #posy = g_TitlebarHeight + g_AttribAreaHeight * (idx + 0.5)
                port.setPos( b.right()-self.handleSize/2, 25 )
                port._Port__UpdateBoundingRect( max_width )





if __name__ == '__main__':

    app = QApplication( sys.argv )

    view = QGraphicsView()
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 680, 459)
    view.setScene(scene)


    item = GraphicsRectItem(0, 0, 300, 150)
    scene.addItem(item)

    port1 = Port('88888888888888888888888888888888888888888888888888888888-----------', None, DataFlow.Input )
    port2 = Port('Output-----------', None, DataFlow.Output )
    #text = QGraphicsTextItem('88888888888888888888888888888888888888888888888888888888-----------')# サイズ変更したいときはboundingRect()メソッドをオーバーライド
    
    item.AddPort(port1)
    item.AddPort(port2)
    
    view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
    view.show()

    sys.exit(app.exec_())
