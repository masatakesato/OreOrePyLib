import math
import random
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

    def __init__(self, parent=None):
        super(GroupFrame, self).__init__(parent=parent)

        self.__m_Rect = QRectF()
        self.__m_Shape = QPainterPath()
        self.__m_Brush = QBrush( QColor( random.randint(128,255), random.randint(128,255), random.randint(128,255) ) )
        
        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )

        self.__m_PortSlots = []
        self.__m_BlankIndex = -1
        self.__m_LastSlotIndex = 0#max(len(self.__m_PortSlots)-1,0)

        self.__UpdateBoundingRect( len(self.__m_PortSlots) )


    def SetColor( self, color ):
        self.__m_Brush.setColor(color)


    # Add Item
    def AddItem( self, item, idx=None ):

        if( item in self.__m_PortSlots ):
            return
        
        slot_idx = None
        snap_pos = None        

        if( self.__m_BlankIndex != -1 ):
            slot_idx = self.__m_BlankIndex
            snap_pos = self.__CalcSlotPosition( self.__m_BlankIndex )
            print('GroupFrame::AddItem...replace blank', slot_idx, self.__m_BlankIndex)
            self.__m_PortSlots[slot_idx] = item
            self.__m_BlankIndex = -1

        else:
            if( idx ):
                slot_idx = clamp( idx, 0, len(self.__m_PortSlots) )
                snap_pos = self.__CalcSlotPosition( slot_idx )
            else:
                slot_idx, snap_pos = self.__GetSnapPoint( self.mapFromScene(item.scenePos()) )
            self.__m_PortSlots.insert(slot_idx, item)
            print('GroupFrame::AddItem...insert new element', slot_idx, self.__m_BlankIndex)

        item.setParentItem( self )
        item.setPos( snap_pos )
        item.SetSlotIndex( slot_idx )

        self.__UpdateBoundingRect( len(self.__m_PortSlots) )

        for i in range(slot_idx+1, len(self.__m_PortSlots)):
            self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
            self.__m_PortSlots[i].SetSlotIndex(i)





    # AppendItem
    def AppendItem( self, item ):

        if( item in self.__m_PortSlots ):
            return

        item.setParentItem( self )
        self.__m_PortSlots.append(item)

        slot_idx = len(self.__m_PortSlots) - 1
        item.setPos( self.__CalcSlotPosition( slot_idx ) )
        item.SetSlotIndex(slot_idx)

        self.__UpdateBoundingRect( len(self.__m_PortSlots) )


    def RemoveItem( self, item ):
        try:
            print('GroupFrame::RemoveItem...')
            idx = self.__m_PortSlots.index(item)
            self.__m_PortSlots.remove(item)
            item.setParentItem( self.parentItem() )
            
            itempos = self.mapToParent( item.pos() )
            item.setPos( itempos)

            self.__UpdateBoundingRect( len(self.__m_PortSlots) )

            for i in range(idx, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

            

        except:
            traceback.print_exc()


    def RemoveItemByIndex( self, idx ):
        try:
            item = self.__m_PortSlots.pop(idx)
            item.setParentItem( self.parentItem() )

            self.__UpdateBoundingRect( len(self.__m_PortSlots) )

            for i in range(idx, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

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
        dest_idx, snap_pos = self.__GetSnapPoint(pos)
        
        if( src_idx != dest_idx ):
            #print('changing self.__m_PortSlots element order',  src_idx, dest_idx)
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
        dest_idx, snap_pos = self.__GetSnapPoint( item.pos() )#pos)
        item.setPos( snap_pos )


    def AddBlank( self, scenePos ):

        src_idx = self.__m_BlankIndex
        dest_idx = self.__CalcSlotIndex( self.mapFromScene( scenePos ), 0, len(self.__m_PortSlots) )

        if( src_idx==dest_idx ):
            return

        print('GroupFrame::AddBlank', dest_idx)
        if( self.__m_BlankIndex !=-1 ):  del self.__m_PortSlots[self.__m_BlankIndex]
        self.__m_PortSlots.insert( dest_idx, None )
        self.__m_BlankIndex = dest_idx

        # 他の要素の位置を更新する
        idx_min, idx_max = 0, 0

        if( src_idx ==-1 ):
            idx_min, idx_max = dest_idx+1, len(self.__m_PortSlots)
            self.__UpdateBoundingRect( len(self.__m_PortSlots) )
        else:
            idx_min, idx_max = (src_idx, dest_idx) if src_idx<=dest_idx else (dest_idx+1, src_idx+1)
        #print( src_idx, dest_idx )

        for idx in range(idx_min, idx_max):
            #print( 'updating pos at', idx )
            self.__m_PortSlots[idx].setPos( self.__CalcSlotPosition(idx) )
            self.__m_PortSlots[idx].SetSlotIndex( idx )


    def MoveBlank( self, scenePos ):

        if( self.__m_BlankIndex==-1 ):
            return

        src_idx = self.__m_BlankIndex
        dest_idx = self.__CalcSlotIndex( self.mapFromScene( scenePos ), 0, self.__m_LastSlotIndex )#len(self.__m_PortSlots)-1 )

        if( src_idx==dest_idx ):
            return

        print('GroupFrame::MoveBlank', dest_idx)
        self.__m_PortSlots.insert( dest_idx, self.__m_PortSlots.pop(src_idx) )
        self.__m_BlankIndex = dest_idx

        # 他の要素の位置を更新する
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

            self.__UpdateBoundingRect( len(self.__m_PortSlots) )

            for i in range(self.__m_BlankIndex, len(self.__m_PortSlots)):
                self.__m_PortSlots[i].setPos(self.__CalcSlotPosition(i))
                self.__m_PortSlots[i].SetSlotIndex(i)

            self.__m_BlankIndex = -1
            

        except:
            traceback.print_exc()


# TODO: __CalcSlotPositionのslot_idx勝手にクランプしない。呼び出し側で必要に応じてidxを予めクランプすること. 2017.05.31
    def __CalcSlotPosition( self, idx ):
        return QPointF( 0, g_SlotHeight * float(idx) )


    def __CalcSlotIndex( self, pos, min_val, max_val ):
        return clamp(  round(pos.y()/g_SlotHeight), min_val, max_val )


    def __GetSnapPoint( self, pos ):
        slot_idx = clamp(  round(pos.y()/g_SlotHeight), 0, self.__m_LastSlotIndex )
        return int(slot_idx), QPointF( 0, slot_idx * g_SlotHeight )


    def __UpdateBoundingRect( self, numslots ):
        self.prepareGeometryChange()
        self.__m_Rect.setRect( 0, 0, 150, g_SlotHeight * max(1, numslots) )
        self.__m_Shape = QPainterPath()
        self.__m_Shape.addRect( self.__m_Rect )
        self.__m_LastSlotIndex = max(numslots-1, 0)


    def itemChange( self, change, value ):

        # workaround for pyqt bug: http://www.riverbankcomputing.com/pipermail/pyqt/2012-August/031818.html
        if( change==QGraphicsItem.ItemParentChange and isinstance(value, QGraphicsItem) ): 
            return sip.cast(value, QGraphicsItem)

        return super(GroupFrame, self).itemChange( change, value )


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