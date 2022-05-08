import math
import sys
import sip
import traceback

from oreorepylib.utils import environment

from GroupFrameItem import GroupFrame
from MyBoxItem import MyBox


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *




class GraphicsScene(QGraphicsScene):

    def __init__(self):
        super(GraphicsScene, self).__init__()

        self.__m_Groups = {}
        self.__m_BoxItems = {}

        self.__m_refTouchedFrame = None

        self.__m_bNothingPicked = True



    def AddBoxItem( self, item ):
        self.__m_BoxItems[ id(item) ] = item


    def mousePressEvent( self, event ):
        super(GraphicsScene, self).mousePressEvent(event)

        self.__m_refTouchedFrame = next( (item for item in self.items(event.scenePos()) if isinstance(item, GroupFrame) ), None )
        grabitem = self.mouseGrabberItem()
        self.__m_bNothingPicked = False if grabitem else True


    def mouseMoveEvent( self, event ):
        #event = QGraphicsSceneMouseEvent()
        grabitem = self.mouseGrabberItem()

        #print( event.scenePos().x(), event.scenePos().y() , event.pos().x(), event.pos().y() )

        if( event.buttons() & Qt.LeftButton and isinstance(grabitem, GroupFrame)==False ):# and item
            groupitem = next( (item for item in self.items(event.scenePos()) if isinstance(item, GroupFrame) ), None )

            if( groupitem==None and self.__m_refTouchedFrame==None ):
                print('nothing...')

            elif( self.__m_refTouchedFrame and groupitem==None ):
                print( 'mouseDownLeaved', self.__m_refTouchedFrame )
                self.__m_refTouchedFrame.RemoveBlank()
                self.__m_refTouchedFrame = groupitem

            elif( groupitem and self.__m_refTouchedFrame==None ):
                print( 'mouseDownEntered', groupitem )
                self.__m_refTouchedFrame = groupitem
                if( not grabitem in self.__m_refTouchedFrame.childItems() ):
                    self.__m_refTouchedFrame.AddBlank( event.scenePos() )

            elif( groupitem == self.__m_refTouchedFrame ):
                print( 'mouseDownHover', self.__m_refTouchedFrame )

                if( grabitem in self.__m_refTouchedFrame.childItems() ):
                    self.__m_refTouchedFrame.MoveItem( grabitem )
                elif( isinstance(grabitem, MyBox) ):
                    self.__m_refTouchedFrame.MoveBlank( grabitem.scenePos() )
                else:#( grabitem==None ):
                    self.__m_refTouchedFrame.MoveBlank( event.scenePos() )


        super(GraphicsScene, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        #event = QGraphicsSceneMouseEvent()
        print( 'GraphicsScene::mouseReleaseEvent...' )
        
        bRemoveGrabber = False
        grabitem = self.mouseGrabberItem() if isinstance(self.mouseGrabberItem(), MyBox) else None

        # GroupFrame内部でマウスボタンをリリースした場合
        if( self.__m_refTouchedFrame ):
            if( grabitem ):# 掴んでいたMyBoxを__m_refTouchedFrameの上で離した場合
               self.AssignMyBoxToGroup( grabitem, self.__m_refTouchedFrame )

            elif( self.__m_bNothingPicked==True ):# マウスボタン押したときに何もアイテムを掴まなかった -> self.__m_refTouchedFrameにMyBox追加
                newbox = MyBox(0, 0, 130, 25)
                newbox.setPos( event.scenePos() )
                self.__m_BoxItems[ id(newbox) ] = newbox
                self.__m_refTouchedFrame.AddItem( newbox )

        # GroupFrame外でマウスボタンをリリースした場合
        elif( grabitem ):
            if( grabitem.parentItem() ): grabitem.parentItem().RemoveItem(grabitem)
            bRemoveGrabber = True

        self.__m_refTouchedFrame = None
        self.__m_bNothingPicked = True

        super(GraphicsScene, self).mouseReleaseEvent(event)

        if( bRemoveGrabber==True ):
            self.removeItem(grabitem)
            del self.__m_BoxItems[ id(grabitem) ]



    def AssignMyBoxToGroup( self, item, group ):

        if( item.parentItem()==group ):
            item.parentItem().SnapItem(item )
            return False

        if( item.parentItem() ):
            item.parentItem().RemoveItem(item)

        group.AddItem( item )

        return True



class GraphicsView(QGraphicsView):

    def __init__(self):
        super(GraphicsView, self).__init__()

        self.setOptimizationFlags( QGraphicsView.DontSavePainterState )
        #self.setViewportUpdateMode( QGraphicsView.BoundingRectViewportUpdate )
        self.setViewportUpdateMode( QGraphicsView.SmartViewportUpdate )
        self.setCacheMode( QGraphicsView.CacheBackground )
        

        self.setMouseTracking( True )
        self.viewport().setMouseTracking( True)





if __name__=='__main__':

    app = QApplication( sys.argv )

    scene = GraphicsScene()
    view = GraphicsView()
    view.setScene(scene)

    group = GroupFrame()
    group.setPos( 50, 50 )
    scene.addItem(group)

    group2 = GroupFrame()
    group2.setPos( -100, -200 )
    scene.addItem(group2)


    for i in range(5):
        item = MyBox(0, 0, 130, 25, str(i))
        scene.AddBoxItem(item)
        group.AddItem(item, 3)

    for i in range(1):
        item = MyBox(0, 0, 130, 25, str(i))
        scene.AddBoxItem(item)
        group2.AppendItem(item)


#TODO: アイテムが消える。なんで？？？？
#->GroupFrameをQGraphicsRectItem継承で実装すると発生. 基本QGraphicsItem継承して実装するので、一旦は問題解消
#->pythonのオブジェクト管理の仕様。
#　->MyBoxインスタンスを明示的に保持してるのは、GroupFrame::__m_PortSlotsのみ(作成時のitemはループ内のローカル変数で消える)
#　->GroupFrame::__m_PortSlotsから消すと、メモリ上からも消える
#　->MyBoxがリストから消される -> メモリから削除 -> QGraphicsItemデストラクタ -> QGraphicsSceneからも削除 -> 消える
#　->リスト最終要素だけ残せるのはなぜ？？？？listの仕様？


    layout = QVBoxLayout()
    layout.addWidget(view)

    mainWindow = QFrame()
    mainWindow.setGeometry( 50, 50, 600, 600 )
    mainWindow.setLayout(layout)
    mainWindow.show()

    sys.exit( app.exec_())
