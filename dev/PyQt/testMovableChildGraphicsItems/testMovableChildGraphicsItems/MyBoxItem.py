import math
import sys
import sip


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *





#g_SnapRadius = 40


def Distance( p1, p2 ):
    return math.sqrt( math.pow(p1.x()-p2.x(), 2.0) + math.pow(p1.y()-p2.y(), 2.0) )


def DistanceSqrd( p1, p2 ):
    return math.pow(p1.x()-p2.x(), 2.0) + math.pow(p1.y()-p2.y(), 2.0)


def DistanceManhattan( p1, p2 ):
    return math.fabs(p1.x()-p2.x()) + math.fabs(p1.y()-p2.y())




class MyBox(QGraphicsItem):

    def __init__(self, x, y, w,h, parent=None):
        super(MyBox, self).__init__(parent=parent)

        self.__m_Rect = QRectF(x, y, w, h)
        self.__m_Brush = QBrush( QColor( 100, 255, 100 ) )

        self.setFlag( QGraphicsItem.ItemIsSelectable )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )

        self.mouseDragStart = QPointF()
        self.objDragStart = QPointF()
        self.mouseMovement = QPointF()


        self.__m_SlotIndex = -1


    def __del__(self):
        print('MyBox::__del__')


    def SetColor( self, color ):
        self.__m_Brush.setColor(color)


    def SetSlotIndex( self, index ):
        self.__m_SlotIndex = index


    def SlotIndex( self ):
        return self.__m_SlotIndex


    def mousePressEvent( self, event ):
        self.mouseDragStart = event.scenePos()
        self.objDragStart = self.pos()
        return super(MyBox, self).mousePressEvent(event)


    def mouseMoveEvent( self, event ):
        self.mouseMovement = event.scenePos() - self.mouseDragStart

        if( self.parentItem() ):
            print( 'MyBox::mouseMoveEvent')
            pos = self.pos()#self.mapToParent( self.objDragStart + self.mouseMovement )#
            self.parentItem().MoveItem( self )

        super(MyBox, self).mouseMoveEvent(event)


    def mouseReleaseEvent( self, event ):

        if( self.parentItem() ):
            #pos = self.pos()#self.mapToParent( self.objDragStart + self.mouseMovement )
            if( self.parentItem().sceneBoundingRect().contains( event.scenePos() ) ):
                self.parentItem().SnapItem( self )#, pos )
            else:
                self.parentItem().RemoveItem(self)

        #items = self.scene().items()
        #print( items, '---' )
        
        return super(MyBox, self).mouseReleaseEvent(event)


    def itemChange( self, change, value ):

        ## workaround for pyqt bug:
        ## http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        if( change==QGraphicsItem.ItemParentChange and isinstance(value, QGraphicsItem) ): 
            return sip.cast(value, QGraphicsItem)


        # オブジェクト原点がスナップ点に近付いた時だけ、原点位置を固定する.
        #if( change==QGraphicsItem.ItemPositionChange and self.parentItem() ):
        #    if( QApplication.mouseButtons() == Qt.LeftButton ):
        #        pos = self.mapToParent( self.objDragStart + self.mouseMovement )
        #        parentSnappos = QPointF(0,0)# 親空間上のスナップ点
        #        #print( event.scenePos().x(), event.scenePos().y() )
        #        if( Distance(pos, parentSnappos) < g_SnapRadius ):
        #            pos = parentSnappos
        #            return pos
        #        else:
        #            return value
        #else:
        #    return super(MyBox, self).itemChange( change, value )




    ##    #if( change==QGraphicsItem.ItemPositionChange ):# 親boundingRectからはみ出ないようアイテムの位置を修正する            
    ##    #    parent = self.parentItem()
    ##    #    if( parent ):
    ##    #        newPos = value
    ##    #        rect = self.boundingRect()

    ##    #        movablerect = parent.boundingRect().adjusted( 0,0,-rect.width(),-rect.height() )#parent.sceneBoundingRect()

    ##    #        if( movablerect.contains( newPos )==False ):
                    
    ##    #            newPos.setX( min(movablerect.right(), max(newPos.x(), movablerect.left())) )
    ##    #            newPos.setY( min(movablerect.bottom(), max(newPos.y(), movablerect.top())) )
    ##    #            return newPos

        
        return super(MyBox, self).itemChange( change, value )




    def boundingRect(self):
        return self.__m_Rect


    def paint( self, painter, option, widget = None ):

        #painter = QPainter()

        painter.setBrush( self.__m_Brush )
        painter.drawRect( self.__m_Rect )

        painter.drawText( 0, 15, str( self.__m_SlotIndex) )


        #return super().paint(QPainter, QStyleOptionGraphicsItem, widget)


