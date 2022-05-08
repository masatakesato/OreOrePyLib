import math
import sys
import sip
import traceback


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from MyBoxItem import MyBox

# TODO: Blankの代わりにTempMyBoxみたいのを登録する


g_SlotHeight = 30.0



def clamp( val, min_val, max_val ):
    return min( max(val,min_val), max_val )



def Distance( p1, p2 ):
    return math.sqrt( math.pow(p1.x()-p2.x(), 2.0) + math.pow(p1.y()-p2.y(), 2.0) )


def DistanceSqrd( p1, p2 ):
    return math.pow(p1.x()-p2.x(), 2.0) + math.pow(p1.y()-p2.y(), 2.0)


def DistanceManhattan( p1, p2 ):
    return math.fabs(p1.x()-p2.x()) + math.fabs(p1.y()-p2.y())



class GroupFrame(QGraphicsItem):

    def __init__(self, x, y, w,h, parent=None):
        super(GroupFrame, self).__init__(parent=parent)

        self.__m_Rect = QRectF(x, y, w, h)
        self.__m_Brush = QBrush( QColor( 100, 255, 100 ) )

        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )
        #self.setAcceptHoverEvents(True)


        self.__m_PortSlots = []

        self.__m_BlankIndex = -1
        #self.__m_Blank = MyBox( 0, 0, 10, g_SlotHeight )
        #self.AddItem( self.__m_Blank )

        self.__m_Shape = QPainterPath()


    def SetColor( self, color ):
        self.__m_Brush.setColor(color)


    # Add Item
    def AddItem( self, item ):

        if( item in self.__m_PortSlots ):
            return

        #print( 'before:', item.pos().x(), item.pos().y() )
        groupspacepos = self.mapFromParent(item.pos())
        item.setParentItem( self )
        #print( 'after:', pos2.x(), pos2.y() )
        item.setPos(groupspacepos )

        slot_idx, snap_pos = self.GetSnapPoint( groupspacepos )
        item.setPos(snap_pos )

        if( self.__m_BlankIndex==slot_idx ):
            self.__m_PortSlots[slot_idx] = item
        else:
            self.__m_PortSlots.insert(slot_idx, item)
        item.SetSlotIndex( slot_idx )
        self.__m_BlankIndex = -1

        for i in range(slot_idx+1, len(self.__m_PortSlots)):
            self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
            self.__m_PortSlots[i].SetSlotIndex(i)

        self.prepareGeometryChange()

        self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * len(self.__m_PortSlots) )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( self.__m_Rect )


    # AppendItem
    def AppendItem( self, item ):

        if( item in self.__m_PortSlots ):
            return

        item.setParentItem( self )
        self.__m_PortSlots.append(item)

        slot_idx = len(self.__m_PortSlots) - 1
        item.setPos( self.__CalcSlotPosition( slot_idx ) )
        item.SetSlotIndex(slot_idx)

        self.prepareGeometryChange()

        self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * len(self.__m_PortSlots) )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( self.__m_Rect )


    def RemoveItem( self, item ):
        try:
            print('GroupFrame::RemoveItem...')
            idx = self.__m_PortSlots.index(item)
            self.__m_PortSlots.remove(item)
            item.setParentItem( self.parentItem() )
            
            itempos = self.mapToParent( item.pos() )
            item.setPos( itempos)


            for i in range(idx, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

            self.prepareGeometryChange()

            self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * len(self.__m_PortSlots) )
            self.__m_Shape = QPainterPath()
            self.__m_Shape.addRect( self.__m_Rect )

        except:
            traceback.print_exc()


    def RemoveItemByIndex( self, idx ):
        try:
            item = self.__m_PortSlots.pop(idx)
            item.setParentItem( self.parentItem() )

            for i in range(idx, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

            self.prepareGeometryChange()

            self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * len(self.__m_PortSlots) )
            self.__m_Shape = QPainterPath()
            self.__m_Shape.addRect( self.__m_Rect )

            return item

        except:
            traceback.print_exc()
            return None




# TODO: GroupFrameのboundingbox外側でスロットをドラッグした場合は、他スロットの位置補正は中止したい
# TODO: 指定アイテムだけをスナップする処理と、他のアイテムの位置修正処理を分離する
# 指定アイテムのスナップ処理→

    def MoveItem( self, item ):
        
        pos = item.pos()
        if( self.sceneBoundingRect().intersects(item.sceneBoundingRect())==False ):
            return False

        src_idx = item.SlotIndex()#self.__m_PortSlots.index(item)
        dest_idx, snap_pos = self.GetSnapPoint(pos)
        
        if( src_idx != dest_idx ):
            #print('changing self.__m_PortSlots element order')
            self.__m_PortSlots.insert(dest_idx, self.__m_PortSlots.pop(src_idx))
            item.SetSlotIndex( dest_idx )
        
        # 他の要素の位置を更新する
        idx_min, idx_max = (src_idx, dest_idx) if src_idx<=dest_idx else (dest_idx+1, src_idx+1)
        #print( src_idx, dest_idx )

        for idx in range(idx_min, idx_max):
            #print( 'updating pos at', idx )
            self.__m_PortSlots[idx].setPos( self.__CalcSlotPosition(idx) )
            self.__m_PortSlots[idx].SetSlotIndex( idx )

        return True


    def SnapItem( self, item ):#, pos ):
        dest_idx, snap_pos = self.GetSnapPoint( item.pos() )#pos)
        item.setPos( snap_pos )
            


    def AddBlank( self, scenePos ):

        src_idx = self.__m_BlankIndex
        dest_idx = self.__CalcSlotIndex( self.mapFromScene( scenePos ) )

        if( src_idx==dest_idx ):
            return

        print('GroupFrame::MoveBlank', dest_idx)
        if( self.__m_BlankIndex !=-1 ):  del self.__m_PortSlots[self.__m_BlankIndex]
        self.__m_PortSlots.insert( dest_idx, None )
        self.__m_BlankIndex = dest_idx


        # 他の要素の位置を更新する
        idx_min, idx_max = 0, 0

        if( src_idx ==-1 ):
            idx_min, idx_max = dest_idx+1, len(self.__m_PortSlots)

            self.prepareGeometryChange()
            self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * len(self.__m_PortSlots) )
            self.__m_Shape = QPainterPath()
            self.__m_Shape.addRect( self.__m_Rect )
        else:
            idx_min, idx_max = (src_idx, dest_idx) if src_idx<=dest_idx else (dest_idx+1, src_idx+1)
        #print( src_idx, dest_idx )

        for idx in range(idx_min, idx_max):
            #print( 'updating pos at', idx )
            self.__m_PortSlots[idx].setPos( self.__CalcSlotPosition(idx) )
            self.__m_PortSlots[idx].SetSlotIndex( idx )



    def MoveBlank( self, item ):
        
        if( item in self.childItems() ):
            return

        src_idx = self.__m_BlankIndex
        dest_idx = self.__CalcSlotIndex( self.mapFromScene( item.scenePos() ) )
        
        if( src_idx==dest_idx ):
            return

        print('GroupFrame::MoveBlank', dest_idx)
        if( self.__m_BlankIndex !=-1 ):  del self.__m_PortSlots[self.__m_BlankIndex]
        self.__m_PortSlots.insert( dest_idx, None )
        self.__m_BlankIndex = dest_idx


        # 他の要素の位置を更新する
        idx_min, idx_max = 0, 0

        if( src_idx ==-1 ):
            idx_min, idx_max = dest_idx+1, len(self.__m_PortSlots)

            self.prepareGeometryChange()
            self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * len(self.__m_PortSlots) )
            self.__m_Shape = QPainterPath()
            self.__m_Shape.addRect( self.__m_Rect )
        else:
            idx_min, idx_max = (src_idx, dest_idx) if src_idx<=dest_idx else (dest_idx+1, src_idx+1)
        #print( src_idx, dest_idx )

        for idx in range(idx_min, idx_max):
            #print( 'updating pos at', idx )
            self.__m_PortSlots[idx].setPos( self.__CalcSlotPosition(idx) )
            self.__m_PortSlots[idx].SetSlotIndex( idx )



    def RemoveBlank( self ):
        try:
            if( self.__m_BlankIndex == -1):
                return

            print('GroupFrame::RemoveBlank...', self.__m_BlankIndex )
            del self.__m_PortSlots[ self.__m_BlankIndex ]
            
            for i in range(self.__m_BlankIndex, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

            self.prepareGeometryChange()

            self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * len(self.__m_PortSlots) )
            self.__m_Shape = QPainterPath()
            self.__m_Shape.addRect( self.__m_Rect )

            self.__m_BlankIndex = -1

            

        except:
            traceback.print_exc()


#TODO: Need to specify dimensions before implementation
    def __CalcSlotPosition( self, idx ):
        return QPointF( 0, g_SlotHeight * float( clamp(idx, 0, len(self.__m_PortSlots)-1) ) )


    def __CalcSlotIndex( self, pos ):
        return clamp(  round(pos.y()/g_SlotHeight), 0, len(self.__m_PortSlots)-1 )


    def GetSnapPoint( self, pos ):
        slot_idx = clamp(  round(pos.y()/g_SlotHeight), 0, len(self.__m_PortSlots)-1 )#round(pos.y()/g_SlotHeight)
        return int(slot_idx), QPointF( 0, slot_idx * g_SlotHeight )


    #def itemChange( self, change, value ):

    #    ## workaround for pyqt bug:
    #    ## http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
    #    if( change==QGraphicsItem.ItemParentChange ):
    #        return sip.cast(value, QGraphicsItem)

    #    return super(GroupFrame, self).itemChange( change, value )

    def shape(self):
        return self.__m_Shape
        


    def boundingRect(self):
        return self.__m_Rect


    def paint( self, painter, option, widget = None ):

        painter.setBrush( self.__m_Brush )
        painter.drawRect( self.__m_Rect )


        #return super().paint(QPainter, QStyleOptionGraphicsItem, widget)




    #def sceneEvent(self, QEvent):
    #    print('sceneevent')

    #    return super(GroupFrame, self).sceneEvent(QEvent)



    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        print('GroupFrame::mousePressEvent')
        return super().mousePressEvent(QGraphicsSceneMouseEvent)


    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        print('GroupFrame::mouseMoveEvent')
        return super().mouseMoveEvent(QGraphicsSceneMouseEvent)


    def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
        print('GroupFrame::mouseReleaseEvent')
        return super().mouseReleaseEvent(QGraphicsSceneMouseEvent)



    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        print('GroupFrame::hoverEnterEvent')
        return super().hoverEnterEvent(QGraphicsSceneHoverEvent)



    def hoverMoveEvent(self, QGraphicsSceneHoverEvent):
        print('GroupFrame::hoverMoveEvent')
        return super().hoverMoveEvent(QGraphicsSceneHoverEvent)



    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        print('GroupFrame::hoverLeaveEvent')
        return super().hoverLeaveEvent(QGraphicsSceneHoverEvent)