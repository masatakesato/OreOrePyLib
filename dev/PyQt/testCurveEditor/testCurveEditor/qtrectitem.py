import sys
from enum import IntEnum

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#from DoublyLinkedList import DLNode
from qtpathitem import CurveItem, LineSegmentItem



class AdjustmentPoint(QGraphicsEllipseItem):

    def __init__(self, *, pos=QPointF(), range=(0.0, 0.0), parent=None):
        super(AdjustmentPoint, self).__init__(parent=parent)
        
        self.__m_refPathItem = None
        self.__m_LineSegmentItem = LineSegmentItem( parent, self, parent=self )
        self.__m_MovableRange = range

        length = 10.0
        self.setRect(-length/2.0,-length/2.0,length,length)
        self.setPos( pos )

        self.Update()

        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )


    def Release( self ):
        self.__m_refPathItem = None
        self.__m_LineSegmentItem.Release()
        del self.__m_LineSegmentItem
        self.__m_LineSegmentItem = None


    def PathItem( self ):
        return self.__m_refPathItem


    def BindPathItem( self, item ):
        self.__m_refPathItem = item


    def UnbindPathItem( self ):
        self.__m_refPathItem = None


    def SetMovableRange( self, range ):
        self.__m_MovableRange = range


    def SetCurveMode( self, mode ):
        if( self.__m_refPathItem ):
            self.__m_refPathItem.SetCurveMode(mode)


    def Update( self ):
        if( self.__m_refPathItem ):
            self.__m_refPathItem.UpdatePath()
        self.__m_LineSegmentItem.UpdatePath()


    def itemChange( self, change, value ):
        if( change==QGraphicsItem.ItemScenePositionHasChanged ):
            self.Update()

        elif( change==QGraphicsItem.ItemPositionChange ):
            clamped_pos = value
            clamped_pos.setX( max(min(value.x(), self.__m_MovableRange[1]), self.__m_MovableRange[0]) )
            return clamped_pos

        return super(AdjustmentPoint, self).itemChange( change, value )


    def paint( self, painter, option, widget=None ):

        return super(AdjustmentPoint, self).paint(painter, option, widget)




class AnchorPoint(QGraphicsRectItem):

    def __init__(self, parent=None):
        super(AnchorPoint, self).__init__(parent=parent)

        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsScenePositionChanges )
        self.__m_AdjustmentPoints = {
            0: AdjustmentPoint( pos=QPointF(-50.0, 0.0), range=(-sys.float_info.max, 0.0), parent=self),
            1: AdjustmentPoint( pos=QPointF(50.0, 0.0), range=(0.0, sys.float_info.max), parent=self) }
        
        length = 15.0
        self.setRect(-length/2.0,-length/2.0,length,length)


    def Release( self ):
        self.__m_AdjustmentPoints[0].Release()
        del self.__m_AdjustmentPoints[0]
        self.__m_AdjustmentPoints[1].Release()
        del self.__m_AdjustmentPoints[1]

        self.setParentItem( None )


    def AdjustmentPoint( self, idx ):
        return self.__m_AdjustmentPoints[idx]


    def SetCurveMode( self, mode ):
        self.__m_AdjustmentPoints[1].SetCurveMode(mode)


    #def ConfirmOrder( self ):
        


    # 右側のAnchorPointと入れ替える
    def SwapRight( self ):
        print( 'AnchorPoint::SwapRight()...' )

        pathRight = self.childItems()[1].PathItem()
        if( pathRight==None ): return

        anchorRight = pathRight.EndAnchor() if pathRight else None
        pathRight2 = anchorRight.childItems()[1].PathItem() if anchorRight else None
        pathLeft = self.childItems()[0].PathItem()

        #============ pathItemが参照するAnchorPointを更新する ========#
        if( pathLeft ): pathLeft.SetEndAnchor( anchorRight )
        if( pathRight ): pathRight.SetAnchors( anchorRight, self )
        if( pathRight2 ): pathRight2.SetStartAnchor( self )

        #============ AdjustmentPointのパスをつなぎなおす ============#
        if( anchorRight ):
            anchorRight.childItems()[0].BindPathItem(pathLeft)
            anchorRight.childItems()[1].BindPathItem(pathRight)
        self.childItems()[0].BindPathItem(pathRight)
        self.childItems()[1].BindPathItem(pathRight2)

        #============ AdjustmentPointの可動範囲を再設定する ===========#
        self.__m_AdjustmentPoints[0].SetMovableRange( (-sys.float_info.max, 0.0) )
        self.__m_AdjustmentPoints[1].SetMovableRange( (0.0, sys.float_info.max) )



    # 左側のAnchorPointと入れ替える
    def SwapLeft( self ):
        print( 'AnchorPoint::SwapLeft()...' )

        pathLeft = self.childItems()[0].PathItem()
        if( pathLeft==None ): return

        anchorLeft = pathLeft.StartAnchor() if pathLeft else None
        pathLeft2 = anchorLeft.childItems()[0].PathItem() if anchorLeft else None
        pathRight = self.childItems()[1].PathItem()

        #============ pathItemが参照するAnchorPointを更新する ========#
        if( pathRight ): pathRight.SetStartAnchor( anchorLeft )
        if( pathLeft ): pathLeft.SetAnchors( self, anchorLeft )
        if( pathLeft2 ): pathLeft2.SetEndAnchor( self )

        #============ AdjustmentPointのパスをつなぎなおす ============#
        if( anchorLeft ):
            anchorLeft.childItems()[1].BindPathItem(pathRight)
            anchorLeft.childItems()[0].BindPathItem(pathLeft)
        self.childItems()[1].BindPathItem(pathLeft)
        self.childItems()[0].BindPathItem(pathLeft2)

        #============ AdjustmentPointの可動範囲を再設定する ===========#
        self.__m_AdjustmentPoints[0].SetMovableRange( (-sys.float_info.max, 0.0) )
        self.__m_AdjustmentPoints[1].SetMovableRange( (0.0, sys.float_info.max) )



    def Update( self ):
        self.__m_AdjustmentPoints[0].Update()
        self.__m_AdjustmentPoints[1].Update()


    def itemChange( self, change, value ):
        if( change==QGraphicsItem.ItemScenePositionHasChanged ):
            posx = self.scenePos().x()

            pathLeft = self.childItems()[0].PathItem()
            pathRight = self.childItems()[1].PathItem()

            if( pathLeft ):
                anchorLeft = pathLeft.StartAnchor()
                if( posx < anchorLeft.scenePos().x() ):
                    anchorLeft.SwapRight()
            
            #pathRight = self.childItems()[1].PathItem()
            if( pathRight ):
                anchorRight = pathRight.EndAnchor()
                if( anchorRight.scenePos().x() < posx ):
                    anchorRight.SwapLeft()
            
        return super(AnchorPoint, self).itemChange( change, value )



#TODO: QGraphicsPathItemの双方向リスト使った実装に切り替える。QGraphicsSceneクラスのメンバとして実装
#AnchorPoint <--> PathItem <--> AnchorPoint <--> PathItem の形