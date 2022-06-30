import sys
import time
import traceback
import subprocess

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import WindowHandleHelper

import graphicsitemlayer
import externalappwidget




class CanvasFrame( QFrame ):

    def __init__(self, parent=None):
        super(CanvasFrame, self).__init__(parent=parent)
        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins( 0, 0, 0, 0 )

        self.__m_refBackground = None   # Background QWidget 
        self.__m_refOverlay = None      # Overlay QGraphicsView


    def resizeEvent( self, event ):
        print( "CanvasFrame::resizeEvent()..." )
        r = self.rect()#self.layout().contentsRect()#
        gpos = self.mapToGlobal(r.topLeft())

        if( self.__m_refOverlay ):
            self.__m_refOverlay.setGeometry( gpos.x(), gpos.y(), r.width(), r.height() )#w.resize( r.width(), r.height() )# event.size() )#
        #for w in self.nonlayoutwidgets:
        #    w.setGeometry( gpos.x(), gpos.y(), r.width(), r.height() )#w.resize( r.width(), r.height() )# event.size() )#
        #    print( "resizing: ", w.geometry() )
        event.accept()


    def BindBackground( self, widget: 'QWidget' ):

        self.UnbindBackground()

        self.layout().addWidget( widget )
        self.__m_refBackground = widget


    def UnbindBackground( self ):
        if( self.__m_refBackground ):
            self.__m_refBackground.setParent( None )
            self.__m_refBackground = None


    def BindOverlay( self, view: 'QGraphicsView' ):

        self.UnbindOverlay()

        self.__m_refOverlay = view
        self.__m_refOverlay.setParent( self )        
        self.__m_refOverlay.setAttribute( Qt.WA_NoSystemBackground )# バックグラウンドなし
        self.__m_refOverlay.setAttribute( Qt.WA_TranslucentBackground )# ビューの背景を完全透明化する
        self.__m_refOverlay.setWindowFlags( Qt.Tool | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus )# 枠なしカバーウィンドウにする. Qt.WindowStaysOnTopHint: 全画面上で常に最前面にView表示させるフラグ.これは外す
        # プラットフォーム依存のQt.CoverWindowの代わりにQt.Toolを使っている


    def UnbindOverlay( self ):
        if( self.__m_refOverlay ):
            self.__m_refOverlay.setParent( None )
            self.__m_refOverlay = None


    def SetupOverlayMoveEvent( self ):
        # Find top level widget
        top_widget = self
        while( top_widget.parentWidget() ):
            top_widget = top_widget.parentWidget()
        # install event filter for moveEvent
        if( top_widget ):
            print( "installing event filter...", top_widget )
            top_widget.installEventFilter( self )# MyEventFilter(top_widget, self) )



    def mousePressEvent( self, event ):
        print( "CanvasFrame::mousePressEvent" )
        return super(CanvasFrame, self).mousePressEvent( event )

    
    def eventFilter( self, obj: 'QObject', event: 'QEvent') -> bool:

        if( event.type() == QEvent.Move and self.__m_refOverlay ):
            gpos = self.mapToGlobal( self.rect().topLeft() )
            self.__m_refOverlay.move( gpos )
            #for w in self.nonlayoutwidgets:
            #    w.move( gpos )

        return super(CanvasFrame, self).eventFilter(obj, event)




class MyView( QGraphicsView ):

    def __init__( self, parent=None ):
        super(MyView, self).__init__(parent=parent)
        #self.setEnabled(True)

        #self.setOptimizationFlags( QGraphicsView.DontSavePainterState )
        #self.setViewportUpdateMode( QGraphicsView.SmartViewportUpdate )
        #self.setCacheMode( QGraphicsView.CacheBackground )


    def mousePressEvent( self, event ):
        print( "MyView::mousePressEvent" )
        print( self.isActiveWindow() )
        return super(MyView, self).mousePressEvent(event)


    def keyPressEvent( self, event ):
        print( "MyView::keyPressEvent" )
        return super(MyView, self).keyPressEvent(event)


    def drawBackground( self, painter, rect ):
        painter.fillRect(rect, QBrush(QColor(128, 128, 255, 64)))




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

        self.backgroundWidget = externalappwidget.ExternalAppWidget()
        self.backgroundWidget.BindHwnd( window_handles[0], notepad.pid )
        #self.backgroundWidget.show()

        #================ Setup GraphicsScene/View ===============#
        self.scene = graphicsitemlayer.LayeredGraphicsScene()
        self.view = MyView()

        self.view.setStyleSheet( 'background: rgba(255, 255, 64, 50);' )#self.view.setStyleSheet( 'background: transparent;' )
        self.view.setScene( self.scene )

        #================ compose canvasFrame ==================#
        self.canvasFrame = CanvasFrame()
        self.canvasFrame.BindBackground( self.backgroundWidget )
        self.canvasFrame.BindOverlay( self.view )#



        self.button = QPushButton("Toggle Overlay")
        self.button.setFixedHeight(50)

        self.button2 = QPushButton("Swap Layer")
        self.button2.setFixedHeight(50)


        self.verticalLayout = QVBoxLayout( self )
        self.verticalLayout.addWidget( self.canvasFrame )#self.view )#
        self.verticalLayout.addWidget( self.button )
        self.verticalLayout.addWidget( self.button2 )

        self.layout().setContentsMargins( 0, 0, 0, 0 )

        

        # レイヤー作成テスト
        layer_id = self.scene.AddLayer()

        # define rect item
        rect = QGraphicsRectItem()
        rect.setRect( 0, 0, 250, 160 )
        rect.setBrush( Qt.red )
        rect.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        rect.setFlag( QGraphicsItem.ItemIsMovable )
        rect.setFlag( QGraphicsItem.ItemIsSelectable )
        rect.setFlag( QGraphicsItem.ItemIsFocusable, False )

        self.scene.AddItem( rect, layer_id )


        layer_id = self.scene.AddLayer()

        # define rect item
        rect2 = QGraphicsRectItem()
        rect2.setRect( 0, 0, 60, 20 )
        rect2.setBrush( Qt.green )
        rect2.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
        rect2.setFlag( QGraphicsItem.ItemIsMovable )
        rect2.setFlag( QGraphicsItem.ItemIsSelectable )
        rect2.setFlag( QGraphicsItem.ItemIsFocusable, False )

        self.scene.AddItem( rect2, layer_id )
        #self.scene.DeleteItem( rect2, layer_id )


       
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
        self.scene.MoveLayer(0, self.scene.NumLayers()-1 )


    def AAAA( self ):
        self.canvasFrame.SetupOverlayMoveEvent()
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