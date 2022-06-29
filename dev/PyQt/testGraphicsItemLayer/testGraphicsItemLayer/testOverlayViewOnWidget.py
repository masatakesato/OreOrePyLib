import sys
import time
import traceback
import subprocess

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import WindowHandleHelper
import graphicsitemlayer





class ExternalAppWidget( QWidget ):

    def __init__( self, parent=None ):
        super( ExternalAppWidget, self ).__init__( parent=parent )

        self.setLayout( QVBoxLayout() ) 
        self.layout().setContentsMargins( 0, 0, 0, 0 )

        self.__m_AppWindow = None
        self.__m_WindowWidget = None


    #def __del__( self ):
    #    #self.__p.terminate()
    #    if( self.__m_AppWindow ):
    #        self.__m_AppWindow.close()


    def BindHwnd( self, window_handle, processhandle ):
        
        self.__m_AppWindow =  QWindow.fromWinId( window_handle )
        self.__m_WindowWidget = QWidget.createWindowContainer( self.__m_AppWindow, self )

        self.layout().addWidget( self.__m_WindowWidget )


    def UnbindHWnd( self ):
        try:
            # 外部アプリ埋め込んだwindowと、はめ込んでる__m_WindowWidgetを、下記の順番でSetParentする必要がある
            if( self.__m_WindowWidget ):
                self.__m_WindowWidget.setParent( None )
                self.__m_AppWindow.setParent( None )

                self.__m_WindowWidget = None
                self.__m_AppWindow = None

        except Exception as e:
            import traceback
            traceback.print_exc()


    def mousePressEvent( self, event ):
        print( "ExternalAppWidget::mousePressEvent" )
        return super(ExternalAppWidget, self).mousePressEvent(event)


    def mouseReleaseEvent( self, event ):
        print( "ExternalAppWidget::mouseReleaseEvent" )
        return super(ExternalAppWidget, self).mouseReleaseEvent(event)


    def keyPressEvent( self, event ):
        print( "ExternalAppWidget::keyPressEvent" )
        return super(ExternalAppWidget, self).keyPressEvent( event )


    def closeEvent( self, event ):
        print( "MyWidget::closeEvent" )
        self.UnbindHWnd()
        return super(ExternalAppWidget, self).closeEvent( event )




class CanvasFrame( QFrame ):

    def __init__(self, parent=None):
        super(CanvasFrame, self).__init__(parent=parent)
        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins( 0, 0, 0, 0 )

        self.nonlayoutwidgets = []


#TODO: Add self.__m_BackgroundWidget
#TODO: Add self.__m_OverlayWidget
#TODO


    def resizeEvent( self, event ):
        print( "CanvasFrame::resizeEvent()..." )
        r = self.rect()#self.layout().contentsRect()#
        gpos = self.mapToGlobal(r.topLeft())

        for w in self.nonlayoutwidgets:
            w.setGeometry( gpos.x(), gpos.y(), r.width(), r.height() )#w.resize( r.width(), r.height() )# event.size() )#
            print( "resizing: ", w.geometry() )
        event.accept()


    def AddChildWidget( self, w ):
        w.setParent( self )
        self.nonlayoutwidgets.append(w)


    def RemoveChildWidget( self, w ):
        self.nonlayoutwidgets.remove(w)
        w.setParent( None )


    def mousePressEvent( self, event ):
        print( "CanvasFrame::mousePressEvent" )
        return super(CanvasFrame, self).mousePressEvent( event )



    def FindTopLevelWidget( self ):
        top_widget = self
        while( top_widget.parentWidget() ):
            top_widget = top_widget.parentWidget()

        # TODO: Install EventFilter
        if( top_widget ):
            print( "installing event filter...", top_widget )
            top_widget.installEventFilter( self )# MyEventFilter(top_widget, self) )



    def eventFilter( self, obj: 'QObject', event: 'QEvent') -> bool:
        gpos = self.mapToGlobal( self.rect().topLeft() )
        for w in self.nonlayoutwidgets:
            w.move( gpos )

        return super(CanvasFrame, self).eventFilter(obj, event)




class MyView( QGraphicsView ):

    def __init__( self, parent=None ):
        super(MyView, self).__init__(parent=parent)
        self.setEnabled(True)

        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute( Qt.WA_TransparentForMouseEvents, False )
        #self.setOptimizationFlags( QGraphicsView.DontSavePainterState )
        #self.setViewportUpdateMode( QGraphicsView.SmartViewportUpdate )
        #self.setCacheMode( QGraphicsView.CacheBackground )

        self.setContentsMargins( 0, 0, 0, 0 )


    def mousePressEvent( self, event ):
        print( "MyView::mousePressEvent" )
        print( self.isActiveWindow() )
        return super(MyView, self).mousePressEvent(event)


    def keyPressEvent( self, event ):
        print( "MyView::keyPressEvent" )
        return super(MyView, self).keyPressEvent(event)


    def drawBackground( self, painter, rect ):

        painter.setBrush( Qt.lightGray )
        #painter.drawRect( QRect(0, 0, 100, 100) )
        painter.fillRect(rect, QBrush(QColor(128, 128, 255, 64)))






class MyScene( QGraphicsScene ):

    def __init__( self, *args, **kwargs ):
        super(MyScene, self).__init__(*args, **kwargs)

        self.m_Layers = graphicsitemlayer.GraphicsItemLayer( self )



    def mousePressEvent( self, event ):
        print( "MyScene::mousePressEvent" )
        return super().mousePressEvent(event)




class windowOverlay(QWidget):

    view = None

    def __init__(self, parent=None):
        super(windowOverlay, self).__init__(parent)

        self.resize( 0, 0 )

        ############### Embedded application background test ###############

        notepad = subprocess.Popen( r"D:/Program Files (x86)/sakura/sakura.exe" )

        window_handles = []
        while( WindowHandleHelper.GetWindowHandlesFromPID( notepad.pid, window_handles ) == False ):
            print( window_handles )
            time.sleep(0.05)

        time.sleep(0.5)

        self.backgroundWidget = ExternalAppWidget()
        self.backgroundWidget.BindHwnd( window_handles[0], notepad.pid )
        #self.backgroundWidget.show()

        #================ Setup GraphicsScene/View ===============#
        self.scene = MyScene()
        self.view = MyView( )

        self.view.setStyleSheet( 'background: rgba(255, 255, 64, 50);' )#self.view.setStyleSheet( 'background: transparent;' )
        self.view.setScene( self.scene )

        #================ compose canvasFrame ==================#
        self.canvasFrame = CanvasFrame()
        
        self.canvasFrame.layout().addWidget( self.backgroundWidget )# 埋め込みアプリ背景ウィンドウはQLayoutに登録する

        self.canvasFrame.AddChildWidget( self.view )# QLayoutではなく直接QWidgetの子供にする & viewのアトリビュートを変更する
        self.view.setAttribute( Qt.WA_NoSystemBackground )# バックグラウンドなし
        self.view.setAttribute( Qt.WA_TranslucentBackground )# ビューの背景を完全透明化する
        self.view.setWindowFlags( Qt.Tool | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus )# 枠なしカバーウィンドウにする. Qt.WindowStaysOnTopHint: 全画面上で常に最前面にView表示させるフラグ.これは外す
        # プラットフォーム依存のQt.CoverWindowの代わりにQt.Toolを使っている

        self.button = QPushButton("Toggle Overlay")
        self.button.setFixedHeight(50)

        self.button2 = QPushButton("Swap Layer")
        self.button2.setFixedHeight(50)


        self.verticalLayout = QVBoxLayout( self )
        self.verticalLayout.addWidget( self.canvasFrame )#self.view )#
        self.verticalLayout.addWidget( self.button )
        self.verticalLayout.addWidget( self.button2 )

        #self.layout().setContentsMargins( 0, 0, 0, 0 )

        

        # レイヤー作成テスト
        layer_id = self.scene.m_Layers.AddLayer()

        # define rect item
        rect = QGraphicsRectItem()
        rect.setRect( 0, 0, 250, 160 )
        rect.setBrush( Qt.red )
        rect.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        rect.setFlag( QGraphicsItem.ItemIsMovable )
        rect.setFlag( QGraphicsItem.ItemIsSelectable )
        rect.setFlag( QGraphicsItem.ItemIsFocusable, False )

        self.scene.m_Layers.AddItem( rect, layer_id )


        layer_id = self.scene.m_Layers.AddLayer()

        # define rect item
        rect2 = QGraphicsRectItem()
        rect2.setRect( 0, 0, 60, 20 )
        rect2.setBrush( Qt.green )
        rect2.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        rect2.setFlag( QGraphicsItem.ItemIsMovable )
        rect2.setFlag( QGraphicsItem.ItemIsSelectable )
        rect2.setFlag( QGraphicsItem.ItemIsFocusable, False )

        self.scene.m_Layers.AddItem( rect2, layer_id )
        #self.scene.m_Layers.DeleteItem( rect2, layer_id )


       
        self.button.clicked.connect( self.change_view_visibility )
        self.button2.clicked.connect( self.swap_layer )

        #self.view.show()



    def change_view_visibility( self ):
        print( "windowOverlay::change_view_visibility()..." )
        if( self.view.isVisible()==False ):
            self.view.show()
            print( "On")
        else:
            self.view.hide()
            print("Off")


    def swap_layer( self ):
        print( "windowOverlay::swap_layer()..." )
        self.scene.m_Layers.MoveLayer(0, self.scene.m_Layers.NumLayers()-1 )


    def AAAA( self ):
        self.canvasFrame.FindTopLevelWidget()
        main.view.show()



if __name__ == "__main__":

    app = QApplication( sys.argv )

    w = QWidget()
    w.resize( 500, 500 )
    w.setLayout( QVBoxLayout() )

    main = windowOverlay()

    
    w.layout().addWidget( main )
    main.AAAA()
    
    w.show()
    

    #main.show()

    sys.exit( app.exec_() )