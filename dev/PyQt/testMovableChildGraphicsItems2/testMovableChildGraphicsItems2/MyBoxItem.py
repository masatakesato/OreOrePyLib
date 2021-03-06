import math
import random
import sys
import sip


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



def Distance( p1, p2 ):
    return math.sqrt( math.pow(p1.x()-p2.x(), 2.0) + math.pow(p1.y()-p2.y(), 2.0) )


def DistanceSqrd( p1, p2 ):
    return math.pow(p1.x()-p2.x(), 2.0) + math.pow(p1.y()-p2.y(), 2.0)


def DistanceManhattan( p1, p2 ):
    return math.fabs(p1.x()-p2.x()) + math.fabs(p1.y()-p2.y())




class MyBox(QGraphicsItem):

    def __init__(self, x, y, w,h, label="", parent=None):
        super(MyBox, self).__init__(parent=parent)

        self.__m_Rect = QRectF(x, y, w, h)
        self.__m_Brush = QBrush( QColor( random.randint(128,255), random.randint(128,255), random.randint(128,255) ) )

        self.setFlag( QGraphicsItem.ItemIsSelectable )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )

        self.__m_Label = label
        self.__m_SlotIndex = -1


    def __del__(self):
        print('MyBox::__del__')


    def SetColor( self, color ):
        self.__m_Brush.setColor(color)


    def SetSlotIndex( self, index ):
        self.__m_SlotIndex = index


    def SlotIndex( self ):
        return self.__m_SlotIndex


    #def mousePressEvent( self, event ):
    #    print( 'MyBox::mousePressEvent')
    #    return super(MyBox, self).mousePressEvent(event)


    #def mouseMoveEvent( self, event ):
    #    print( 'MyBox::mouseMoveEvent')
    #    super(MyBox, self).mouseMoveEvent(event)


    #def mouseReleaseEvent( self, event ):
    #    print( 'MyBox::mouseReleaseEvent')        
    #    return super(MyBox, self).mouseReleaseEvent(event)


    def itemChange( self, change, value ):

        # workaround for pyqt bug: http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        if( change==QGraphicsItem.ItemParentChange and isinstance(value, QGraphicsItem) ): 
            return sip.cast(value, QGraphicsItem)
        
        return super(MyBox, self).itemChange( change, value )




    def boundingRect(self):
        return self.__m_Rect


    def paint( self, painter, option, widget = None ):

        #painter = QPainter()

        painter.setBrush( self.__m_Brush )
        painter.drawRect( self.__m_Rect )

        painter.drawText( 0, 15, self.__m_Label+": "+str( self.__m_SlotIndex) )


        #return super().paint(QPainter, QStyleOptionGraphicsItem, widget)


