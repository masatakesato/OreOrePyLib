from enum import IntEnum

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


#from DoublyLinkedList import DLNode



class CurveMode(IntEnum):
    Impulse = 0
    Linear = 1
    Cubic = 2
    


class CurveItem(QGraphicsPathItem):

    def __init__( self, start, end, mode=CurveMode.Cubic ):
        super(CurveItem, self).__init__()

        self.__m_Start = start
        self.__m_End = end
        self.__m_CurveMode = mode


    def Release( self ):
        self.setParentItem( None )
        self.__m_Start = None
        self.__m_End = None


    def SetAnchors( self, start, end ):
        self.__m_Start = start
        self.__m_End = end
        self.UpdatePath()

    def SetStartAnchor( self, anchor ):
        self.__m_Start = anchor
        self.UpdatePath()


    def SetEndAnchor( self, anchor ):
        self.__m_End = anchor
        self.UpdatePath()


    def StartAnchor( self ):
        return self.__m_Start

    def EndAnchor( self ):
        return self.__m_End


    def SetCurveMode( self, mode ):
        self.__m_CurveMode = mode
        self.UpdatePath()


    def UpdatePath( self ):

        # print( 'CurveItem::UpdatePath()...')

        path = QPainterPath()
        path.moveTo( self.__m_Start.scenePos() )
        if( self.__m_CurveMode==CurveMode.Linear ):
            path.lineTo( self.__m_End.scenePos() )

        elif( self.__m_CurveMode==CurveMode.Cubic):
            start = self.__m_Start.scenePos()
            end = self.__m_End.scenePos()
            c1_pos = self.__m_Start.childItems()[1].scenePos()
            c2_pos = self.__m_End.childItems()[0].scenePos()
            c1 = QPointF( max(start.x(), min(c1_pos.x(), end.x())), c1_pos.y() )
            c2 = QPointF( max(start.x(), min(c2_pos.x(), end.x())), c2_pos.y() )
            path.cubicTo( c1, c2, end )
            #path.cubicTo( c1_pos, c2_pos, end )
            #path.cubicTo( self.__m_C1.scenePos(), self.__m_C2.scenePos(), self.__m_End.scenePos() )

        else:
            path.lineTo( QPointF(self.__m_End.scenePos().x(),self.__m_Start.scenePos().y()) )
            path.lineTo( self.__m_End.scenePos() )

        self.setPath(path)

        #print( self.path().slopeAtPercent( 0.5 ) )



class LineSegmentItem(QGraphicsLineItem):

    def __init__( self, start, end, parent=None ):
        super(LineSegmentItem, self).__init__( parent=parent )

        self.__m_Start = start
        self.__m_End = end


    def Release( self ):
        self.setParentItem( None )
        self.__m_Start = None
        self.__m_End = None


    def UpdatePath( self ):
        # print( 'LineSegmentItem::UpdatePath()...')
        line =QLineF( self.__m_Start.scenePos(), self.__m_End.scenePos() )
        self.setLine( QLineF( self.mapFromScene(self.__m_Start.scenePos()), self.mapFromScene(self.__m_End.scenePos()) ) )


