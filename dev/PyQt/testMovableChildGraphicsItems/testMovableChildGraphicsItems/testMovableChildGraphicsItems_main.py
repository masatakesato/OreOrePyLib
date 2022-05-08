import math
import random
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


    def AddBoxItem( self, item ):
        self.__m_BoxItems[ id(item) ] = item


    def mousePressEvent( self, event ):
        #event = QGraphicsSceneMouseEvent()
        return super(GraphicsScene, self).mousePressEvent(event)


    def mouseMoveEvent( self, event ):
        #event = QGraphicsSceneMouseEvent()
        grabitem = self.mouseGrabberItem()

        if( event.buttons() & Qt.LeftButton and grabitem ):
            groupitem = next( (item for item in self.items(event.scenePos()) if isinstance(item, GroupFrame) ), None )


            if( groupitem==None and self.__m_refTouchedFrame==None ):
                print('nothing...')

            elif( self.__m_refTouchedFrame and groupitem==None ):
                print( 'mouseDownLeaved', self.__m_refTouchedFrame )
                if( isinstance(grabitem, MyBox) ):
                    self.__m_refTouchedFrame.RemoveBlank()
                self.__m_refTouchedFrame = groupitem

            elif( groupitem and self.__m_refTouchedFrame==None ):
                print( 'mouseDownEntered', groupitem )
                self.__m_refTouchedFrame = groupitem
                if( isinstance(grabitem, MyBox) ):
                    self.__m_refTouchedFrame.MoveBlank( grabitem )

            elif( groupitem == self.__m_refTouchedFrame ):
                print( 'mouseDownHover', self.__m_refTouchedFrame )
                if( isinstance(grabitem, MyBox) ):
                    self.__m_refTouchedFrame.MoveBlank( grabitem )


        super(GraphicsScene, self).mouseMoveEvent(event)



    def mouseReleaseEvent( self, event ):
        #event = QGraphicsSceneMouseEvent()
        print( 'GraphicsScene::mouseReleaseEvent...' )
        
        item = self.mouseGrabberItem()
        groupitem = next( (item for item in self.items(event.scenePos()) if isinstance(item, GroupFrame) ), None )

        if( groupitem and isinstance(item, MyBox) ):
            groupitem.AddItem( item )

        super(GraphicsScene, self).mouseReleaseEvent(event)





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

    group = GroupFrame(0, 0, 200, 200)
    group.setPos( 50, 50 )
    group.SetColor( QColor( random.randint(128,255), random.randint(128,255), random.randint(128,255) ) )
    scene.addItem(group)

    for i in range(5):
        item = MyBox(0, 0, 130, 25)
        item.SetColor( QColor( random.randint(128,255), random.randint(128,255), random.randint(128,255) ) )
        #scene.addItem(item)
        scene.AddBoxItem(item)
        group.AppendItem(item)

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
