# -*- coding: utf-8 -*-

from oreorepylib.utils import environment

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import weakref


# ノード間を接続する線分
class Line(QGraphicsItem):

    def __init__(self, sourceNode, dstNode, layer_id=0):
        super(Line, self).__init__()

        self.layer_id = layer_id
        self.source = weakref.ref(sourceNode) #始点ノードへの参照
        self.dest = weakref.ref(dstNode)# 終点ノードへの参照

        self.sourcePoint = QPointF()#始点座標
        self.destPoint = QPointF()#終点座標

        self.source().addEdge(self) #始点ノードにエッジを登録する
        self.dest().addEdge(self)# 終点ノードにエッジを登録する

        self.setFlags(QGraphicsItem.ItemIsSelectable);
        #self.setFlag(QGraphicsItem.ItemIsMovable)

        self.adjust()


    def paint(self, painter, option, widget):

        if( self.scene().render_view_id != self.layer_id ):
            return

        if not self.source() or not self.dest():
            return

        p = QPen(Qt.black, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        p.setColor( QColor(200 * int(self.isSelected()), 0, 0) )
        
        line = QLineF(self.sourcePoint, self.destPoint)
        painter.setPen(p)
        painter.drawLine(line)
        

    def boundingRect(self):
        if not self.source() or not self.dest():
            return QRectF()

        return QRectF(self.sourcePoint,
                             QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())).normalized()

    #def shape(self):
    #    path = QPainterPath()
    #    path.addEllipse( -10, -10, 20, 20 )#-10, -10, 10, 10)
    #    return path

    #def boundingRect(self):
    #    if not self.source() or not self.dest():
    #        return QRectF()

    #    return QRectF( QPointF(self.sourcePoint.x()-10.0, self.sourcePoint.y()-10.0 ),
    #                         QSizeF(self.destPoint.x() - self.sourcePoint.x() + 20.0,
    #                                       self.destPoint.y() - self.sourcePoint.y() + 20.0)).normalized()

    def shape(self):

#        if( self.scene().focus_view_id != self.layer_id ):# フォーカスビュー上で見えている
##            if( self.scene().render_view_id != self.layer_id ):# レンダービュー上で見えていない
#            return QPainterPath()

        if( self.scene().focus_view_id != self.layer_id ):# フォーカスビュー上で見えていない
            return QPainterPath()

        #if( self.scene().render_view_id != self.layer_id ):# レンダービュー上で見えていない
        #    return QPainterPath()

        path = QPainterPath()
        #path.addEllipse( self.sourcePoint.x()-10, self.sourcePoint.y()-10, 
        #                    self.destPoint.x() - self.sourcePoint.x()+20, self.destPoint.y() - self.sourcePoint.y()+20 )#-10, -10, 10, 10)
        path.addRect(self.sourcePoint.x()-10.0, self.sourcePoint.y()-10.0,
                    self.destPoint.x() - self.sourcePoint.x() + 20.0, self.destPoint.y() - self.sourcePoint.y() + 20.0 )
        return path



    # 線分の始点終点をノード位置にセットする関数。
    def adjust(self):

        # ノード接続してない場合は処理中止
        if not self.source() or not self.dest():
            return

        #print( "adjust" )

        # 始点ノード座標系の(0, 0)、終点ノード座標系の(0, 0)それぞれを、Lineの座標空間に変換する
        line = QLineF( self.mapFromItem(self.source(), QPointF(0, 0)), self.mapFromItem(self.dest(), QPointF(0, 0)) )
        
        length = line.length()
        if length == 0.0:
            return
        #edgeOffset = QPointF((line.dx() * 5) / length, (line.dy() * 5) / length)
        self.prepareGeometryChange()
        self.sourcePoint = line.p1()# + edgeOffset
        self.destPoint = line.p2()# - edgeOffset


class Port(QGraphicsItem):

    edgeList = []

    def __init__(self, layer_id=1):
        super(Port, self).__init__()

        self.layer_id = layer_id
        self.__pressedButton = None
        self.setFlag( QGraphicsItem.ItemIsSelectable )
        self.setFlag( QGraphicsItem.ItemIsMovable )
        self.setFlag( QGraphicsItem.ItemSendsGeometryChanges )

    #def itemChange( self, change, value ):
    #    return QGraphicsEllipseItem.itemChange( self, change, value )


    def boundingRect(self):
        penWidth = 10.0

        #return QRectF(-10 - penWidth / 2, -10 - penWidth / 2,
        #                     30 + penWidth, 30 + penWidth)
        return QRectF( -10, -10, 20+penWidth, 20+penWidth)


    # 図形を描画するQGraphicsItemの関数オーバーライド
    def paint(self, painter, option, widget):

        if( self.scene().render_view_id != self.layer_id ):
            return

        #if ( option.state & QStyle.State_Sunken ):
        painter.setBrush( QColor(0, 200, 0) if self.isSelected() else QColor(64, 64, 64) )
        painter.drawRoundedRect( -10, -10, 20, 20, 10, 10 )#-10, -10, 10, 10, 5, 5)
        #print( "Port::paint" )


    # BoundingVolumeを返すQGraphicsItemの関数。円形のBV返すようにオーバーライドしている
    def shape(self):

        #if( self.scene().render_view_id != self.layer_id and self.scene().focus_view_id != self.layer_id ):
        #    return QPainterPath()

        if( self.scene().focus_view_id != self.layer_id ):# フォーカスビュー上で見えていない
            return QPainterPath()

        #if( self.scene().render_view_id != self.layer_id ):
        #    return QPainterPath()

        path = QPainterPath()
        path.addEllipse( -10, -10, 20, 20 )#-10, -10, 10, 10)
        return path

    # エッジのリスト
    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()

    def edges(self):

        return self.edgeList

    def mousePressEvent(self, event):
        self.cPos = event.scenePos()
        self.__pressedButton = event.button()

        if self.__pressedButton == Qt.RightButton:
            cursorShape = Qt.SizeAllCursor
        else:
            cursorShape = Qt.ClosedHandCursor
        qApp.setOverrideCursor(QCursor(cursorShape))

        self.update()


    def mouseReleaseEvent(self, event):
        self.cPos = None
        self.__pressedButton = None
        qApp.restoreOverrideCursor()

        self.update()
        super(Port, self).mouseReleaseEvent(event)
        print( "Port::mouseReleaseEvent" )

        

    def mouseMoveEvent(self, event):

        if not self.cPos:
            return

        # 描画位置を変更
        cur = event.scenePos()
        value = cur - self.cPos
        self.cPos = cur
        transform = self.transform()
        transform *= QTransform().translate(value.x(), value.y())

        # 変更を適用
        self.setTransform(transform)

        # Edgeの更新
        for edge in self.edgeList:
            edge.adjust()

        # print( "Port::mouseMoveEvent" )


class graphicView(QGraphicsView):

    nodes = []

    def __init__(self, view_id):
        super(graphicView, self).__init__()

        self.view_id = view_id

        self.mousePos = QPointF()

        self.setDragMode(QGraphicsView.RubberBandDrag)


    def mouseDoubleClickEvent(self, event):

        node = Port()
        self.scene().addItem(node)
        self.nodes.append(node)
        pos = event.pos()
        node.moveBy(pos.x() - 200, pos.y() - 200)


    def mousePressEvent(self, event):
        
        self.mousePos = self.mapToScene(event.pos())

        pickedItem = self.scene().itemAt( self.mousePos, QTransform() )
        pickedItemList = self.scene().items( self.mousePos )
        #pickedItem.type()
        print( str(len(pickedItemList) ) )

        self.update()

        super( graphicView, self ).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        #print("graphicView::mouseMoveEvent")
        super(graphicView,self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        #print("graphicView::mouseReleaseEvent")
        super(graphicView,self).mouseReleaseEvent(event)


    #http://www.qtcentre.org/threads/46648-Draw-Line-QGraphicsView


    def paintEvent( self, event ):
        print( 'GraphicsView::paintEvent()...' )
        self.scene().SetRenderViewID( self.view_id )
        super(graphicView, self).paintEvent(event)


    def focusInEvent( self, event ):
        print( 'GraphicsView::focusInEvent()...' )
        self.scene().SetFocusViewID( self.view_id )
        return super(graphicView, self).focusInEvent(event)



class MyScene(QGraphicsScene):

    def __init__(self):
        super(MyScene, self).__init__()

        self.selectionChanged.connect( self.mySelectonChanged )

        self.render_view_id = 0
        self.focus_view_id = -1


    def mySelectonChanged( self ):
        print( 'mySelectonChanged:', self )


    def SetRenderViewID( self, view_id ):
        self.render_view_id = view_id


    def SetFocusViewID( self, view_id ):
        self.focus_view_id = view_id



# TODO: マウスでオブジェクト選択した際の挙動を追加する
# mousePressEventで始点、終点、線分を追加
# mouseMoveEventで終点を移動
# mouseReleaseEventで
# http://www.walletfox.com/course/customqgraphicslineitem.php


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Setup QGraphicsScene
    scene = MyScene()
    scene.setSceneRect(-200, -200, 400, 400)

    # Create and add QGraphicsItems to QGraphgicsScene
    port0 = Port(1)
    port0.setPos(50, 50)
    scene.addItem(port0)

    port1 = Port(1)
    port1.setPos(100, 100)
    scene.addItem(port1)
        
    port0.setZValue(1)
    port1.setZValue(1)

    line0 = Line(port0, port1)
    scene.addItem(line0)


    # Setup QGraphicsView
    widget = graphicView(0)
    widget.setWindowTitle("Widget1")
    
    widget2 = graphicView(1)
    widget2.setWindowTitle("Widget2")

    widget.setScene(scene)
    widget2.setScene(scene)

    # Show
    widget.show()
    widget2.show()

    sys.exit(app.exec_())