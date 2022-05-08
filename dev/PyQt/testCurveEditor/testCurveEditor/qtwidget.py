import functools
from math import *

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from qtrectitem import AnchorPoint, AdjustmentPoint
from qtpathitem import CurveItem, CurveMode


class ItemGroup(QGraphicsItem):

    def __init__( self ):
        super(ItemGroup, self).__init__()


    def boundingRect(self):
        return QRectF()#return self.childrenBoundingRect()#return super(ItemGroup, self).boundingRect()


    def paint( self, painter, option, widget=None ):
        pass


class CurveEditorScene(QGraphicsScene):

    def __init__( self ):
        super(CurveEditorScene, self).__init__()


        self.__m_ControlPoints = ItemGroup()
        self.__m_Curves = ItemGroup()

        self.addItem(self.__m_ControlPoints)
        self.addItem(self.__m_Curves)

        anchorPoints = []

        for i in range(2):
            x = float(i * 300)
            y = 0.0
            anchor = AnchorPoint()
            anchor.setPos(x,y)
            anchor.setParentItem(self.__m_ControlPoints)#self.addItem(anchor)
            anchorPoints.append(anchor)
            #print( itemGroup.boundingRect() )

        item = CurveItem( anchorPoints[0], anchorPoints[1] )
        item.SetCurveMode( CurveMode.Cubic )
        anchorPoints[0].AdjustmentPoint(1).BindPathItem( item )
        anchorPoints[1].AdjustmentPoint(0).BindPathItem( item )
        item.setParentItem(self.__m_Curves)#item.setParentItem(itemGroup) #self.addItem(item)
        

    def NumAnchorPoints( self ):
        return len( self.__m_ControlPoints.childItems() )


    def NumPathItems( self ):
        return len( self.__m_Curves.childItems() )


    def __AddAnchorPoint( self, mousePos ):

        # Searach for closest item
        sceneRect = self.sceneRect()

        path = QPainterPath()
        
        # Clamp path pos to item's boundary
        curveBB = self.__m_Curves.childrenBoundingRect()
        p0 = QPointF( max( curveBB.left(), min(curveBB.right(), mousePos.x()) ),
               max( curveBB.top(), min(curveBB.bottom(), sceneRect.top()) ) )
        p1 = QPointF( max( curveBB.left(), min(curveBB.right(), mousePos.x()) ),
               max( curveBB.top(), min(curveBB.bottom(), sceneRect.bottom()) ) )

        path.moveTo( p0 )
        path.lineTo( p1 )

        print( curveBB.width(), curveBB.height() )

        intersectedItems = self.items( path )
        curve = next( (item for item in intersectedItems if isinstance(item, CurveItem)), None )
        if( curve==None ):
            print( 'No intersected CurveItem found...' )
            return

        # Add AnchorPoint to self.__m_ControlPoints
        newanchor = AnchorPoint()
        newanchor.setPos( mousePos )
        newanchor.setParentItem( self.__m_ControlPoints )


        # マウスダブルクリック位置がカーブバウンディングボックスの左側(境界値含む)にある場合
        if( mousePos.x() <= curveBB.left() ):
            print( 'Adding new pathItem to leftside' )
            rightanchor = curve.StartAnchor()
            rightadj = rightanchor.AdjustmentPoint(0)
            newcurve = CurveItem( newanchor, rightanchor )
            newanchor.AdjustmentPoint(1).BindPathItem( newcurve )
            rightadj.BindPathItem( newcurve )
            newcurve.setParentItem( self.__m_Curves )
            
        # マウスダブルクリック位置がカーブバウンディングボックスの右側(境界値含む)にある場合
        elif( mousePos.x() >= curveBB.right() ):
            print( 'Adding new pathItem to rightside' )
            leftanchor = curve.EndAnchor()
            leftadj = leftanchor.AdjustmentPoint(1)
            newcurve = CurveItem( leftanchor, newanchor )
            newanchor.AdjustmentPoint(0).BindPathItem( newcurve )
            leftadj.BindPathItem( newcurve )
            newcurve.setParentItem( self.__m_Curves )
        
        # マウスダブルクリック位置がカーブバウンディングボックス内部にある場合
        else:
            print( 'Adding new pathItem to rightside' )
            rightanchor = curve.EndAnchor()
            rightadj = rightanchor.AdjustmentPoint(0)

            curve.SetEndAnchor( newanchor )
            newcurve = CurveItem( newanchor, rightanchor )

            newanchor.AdjustmentPoint(0).BindPathItem( curve )
            newanchor.AdjustmentPoint(1).BindPathItem( newcurve )

            rightadj.BindPathItem( newcurve )
            newcurve.setParentItem( self.__m_Curves )

        newanchor.Update()


    def __RemoveAnchorPoint( self, anchorPoint ):
        
        if( self.NumPathItems() < 2 ):
            print('At least two AnchorPoints needed. Aborting AnchorPoint removal process.')
            return

        # Get PathItems
        rightPath = anchorPoint.AdjustmentPoint(1).PathItem()
        leftPath = anchorPoint.AdjustmentPoint(0).PathItem()

        # Get AnchorPoints
        rightAnchor = rightPath.EndAnchor() if rightPath else None
        leftAnchor = leftPath.StartAnchor() if leftPath else None

        # Remove rightside PathItem
        if( rightPath ):
            rightAnchor.AdjustmentPoint(0).UnbindPathItem()
            rightPath.Release()
            self.removeItem( rightPath )
            del rightPath

        # Reconnect leftside PathItem
        if( leftPath ):
            if( rightAnchor ):
                leftPath.SetEndAnchor( rightAnchor )
                rightAnchor.AdjustmentPoint(0).BindPathItem( leftPath )
            else:
                leftAnchor.AdjustmentPoint(1).BindPathItem(None)
                leftPath.Release()
                self.removeItem( leftPath )
                del leftPath

        # 左側パスがある & 右側アンカーがある -> 左側パスと右側アンカーをつなぐ
        # 左側パスがある & 右側アンカーがない -> 左側パスを削除する
        # 左側パスがない & 右側アンカーがある -> 何もしない
        # 左側パスがない & 右側アンカーがない -> 何もしない

        # Remove AnchorPoint
        anchorPoint.Release()
        anchorPoint.setParentItem( None )
        self.removeItem( anchorPoint )
        del anchorPoint


    def SetCurveMode( self, mode ):
        selectedAnchors = [ item for item in self.selectedItems() if isinstance(item, AnchorPoint) ]
        for anchor in selectedAnchors:
            anchor.SetCurveMode( mode )


    def RemoveAnchor( self ):
        selectedAnchors = [ item for item in self.selectedItems() if isinstance(item, AnchorPoint) ]
        for anchor in selectedAnchors:
            self.__RemoveAnchorPoint( anchor )



    def mousePressEvent( self, event ):

        # Searach for closest item
        mousePos = event.scenePos()
        sceneRect = self.sceneRect()

        path = QPainterPath()

        curveBB = self.__m_Curves.childrenBoundingRect()
        p0 = QPointF( max( curveBB.left(), min(curveBB.right(), mousePos.x()) ),
               max( curveBB.top(), min(curveBB.bottom(), sceneRect.top()) ) )
        p1 = QPointF( max( curveBB.left(), min(curveBB.right(), mousePos.x()) ),
               max( curveBB.top(), min(curveBB.bottom(), sceneRect.bottom()) ) )

        path.moveTo( p0 )
        path.lineTo( p1 )
        
        intersectedItems = self.items( path )
        #print( intersectedItems )

        curve = next( (item for item in intersectedItems if isinstance(item, CurveItem)), None )
        if( curve ):
            print( 'intersected CurveItem found.' )

        return super(CurveEditorScene, self).mousePressEvent(event)


    def mouseDoubleClickEvent( self, event ):

        self.__AddAnchorPoint( event.scenePos() )

        return super(CurveEditorScene, self).mouseDoubleClickEvent(event)





class CurveEditorView(QGraphicsView):

    def __init__(self, scene=None, parent=None):
        super(CurveEditorView, self).__init__(scene, parent)

        # QActions
        curveImpulseAction = QAction( '&Impulse', self )
        curveImpulseAction.setShortcut( 'i' )
        curveImpulseAction.triggered.connect( functools.partial(self.SetCurveMode, mode=CurveMode.Impulse) )
        
        curveLinearAction = QAction( '&Linear', self )
        curveLinearAction.setShortcut( 'o' )
        curveLinearAction.triggered.connect( functools.partial(self.SetCurveMode, mode=CurveMode.Linear) )

        curveCubicAction = QAction( '&Cubic', self )
        curveCubicAction.setShortcut( 'p' )
        curveCubicAction.triggered.connect( functools.partial(self.SetCurveMode, mode=CurveMode.Cubic) )

        removeAnchorAction = QAction( '&RemoveAnchor', self )
        removeAnchorAction.setShortcut( 'Del' )
        removeAnchorAction.triggered.connect( self.RemoveAnchor )


        self.addAction( curveImpulseAction )
        self.addAction( curveLinearAction )
        self.addAction( curveCubicAction )
        self.addAction( removeAnchorAction )


    def SetCurveMode( self, mode ):
        self.scene().SetCurveMode( mode )


    def RemoveAnchor( self ):
        self.scene().RemoveAnchor()