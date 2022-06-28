import sys
import time
import traceback
import subprocess
import ctypes
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import *

from OpenGL.GL import *
from OpenGL.GLU import *

import WindowHandleHelper
import graphicsitemlayer




class OpenGLWidget(QOpenGLWidget):

    def __init__( self, parent=None):
        super().__init__( parent=parent )
        self.setWindowTitle("Triangle, PyQt5, OpenGL ES 2.0")
        self.resize(300, 300)

    def initializeGL(self):
        glClearColor(0.5, 0.8, 0.7, 1.0)
        vertShaderSrc = """
            attribute vec3 aPosition;
            void main()
            {
                gl_Position = vec4(aPosition, 1.0);
            }
        """
        fragShaderSrc = """
            void main()
            {
                gl_FragColor = vec4(0.5, 0.2, 0.9, 1.0);
            }
        """
        program = QOpenGLShaderProgram()
        program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertShaderSrc)
        program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragShaderSrc)
        program.link()
        program.bind()
        vertPositions = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0], dtype=np.float32)
        self.vertPosBuffer = QOpenGLBuffer()
        self.vertPosBuffer.create()
        self.vertPosBuffer.bind()
        self.vertPosBuffer.allocate(vertPositions, len(vertPositions) * 4)
        program.bindAttributeLocation("aPosition", 0)
        program.setAttributeBuffer(0, GL_FLOAT, 0, 3)
        program.enableAttributeArray(0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 3)




class glWidget(QGLWidget):
    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-4.5, 0.5, -6.0)
        glColor3f( 1.0, 1.5, 0.0 );
        glPolygonMode(GL_FRONT, GL_FILL);
        glBegin(GL_TRIANGLES)
        glVertex3f(2.0,-1.2,0.0)
        glVertex3f(2.6,0.0,0.0)
        glVertex3f(2.9,-1.2,0.0)
        glEnd()
        glFlush()

    def initializeGL(self):
        glClearDepth(1.0)              
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()                    
        gluPerspective(45.0,1.33,0.1, 100.0) 
        glMatrixMode(GL_MODELVIEW)


    def paintEvent( self, event ):
        print( "glWidget::paintEvent()..." )
        return super(glWidget, self).paintEvent( event )




class ExternalAppWidget( QWidget ):

    def __init__( self, parent=None ):
        super( ExternalAppWidget, self ).__init__( parent=parent )

        self.setLayout( QVBoxLayout() ) 

        self.layout().setSpacing(0)
        #self.layout().setMargin(0)
        self.layout().setContentsMargins (0, 0, 0, 0)

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




class BackgroundWidget( QWidget ):

    def __init__(self, parent=None):
        super(BackgroundWidget, self).__init__(parent=parent)
        self.nonlayoutwidgets = []


    def mousePressEvent( self, event ):
        print( "BackgroundWidget::mousePressEvent" )
        return super(BackgroundWidget, self).mousePressEvent( event )




class MyFrame( QFrame ):

    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent=parent)
        self.nonlayoutwidgets = []


    def resizeEvent( self, event ):
        print( "MyFrame::resizeEvent()..." )
        r = self.rect()#self.layout().contentsRect()
        for w in self.nonlayoutwidgets:
            w.resize( r.width(), r.height() )# event.size() )#
            print( w.geometry() )
        event.accept()


    def moveChildren( self, pos ):
        print( "MyFrame::moveChildren()..." )
        r = self.layout().contentsRect()
        for w in self.nonlayoutwidgets:
            w.move( pos.x() + r.x(), pos.y() + r.y() )
            print( w.geometry() )


    def AddChildWidget( self, w ):
        w.setParent(self)
        self.nonlayoutwidgets.append(w)


    def RemoveChildWidget( self, w ):
        self.nonlayoutwidgets.remove(w)
        w.setParent( None )


    def mousePressEvent( self, event ):
        print( "MyFrame::mousePressEvent" )
        return super(MyFrame, self).mousePressEvent( event )




class MyView( QGraphicsView ):

    def __init__( self, parent=None ):
        super(MyView, self).__init__(parent=parent)
        self.setEnabled(True)

        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute( Qt.WA_TransparentForMouseEvents, False )
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

        painter.setBrush( Qt.lightGray )
        #painter.drawRect( QRect(0, 0, 100, 100) )
        painter.fillRect(rect, QBrush(QColor(128, 128, 255, 1)))




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

        ############### Embedded application background test ###############

        notepad = subprocess.Popen( r"D:/Program Files (x86)/sakura/sakura.exe" )

        window_handles = []
        while( WindowHandleHelper.GetWindowHandlesFromPID( notepad.pid, window_handles ) == False ):
            print( window_handles )
            time.sleep(0.05)

        time.sleep(0.5)

        self.backgroundWidget = ExternalAppWidget( self )
        self.backgroundWidget.BindHwnd( window_handles[0], notepad.pid )
        #self.backgroundWidget.show()

        #================ Setup GraphicsScene/View ===============#
        self.scene = MyScene()
        self.view = MyView( )
        self.view.setStyleSheet( 'background: rgba(255, 255, 64, 50);' )#self.view.setStyleSheet( 'background: transparent;' )
        self.view.setScene( self.scene )

        #================ compose myFrame ==================#
        self.myFrame = MyFrame()
        self.myFrame.setLayout( QVBoxLayout() )
        
        self.myFrame.AddChildWidget( self.view )# QLayoutではなく直接QWidgetの子供にする & viewのアトリビュートを変更する
        self.view.setAttribute( Qt.WA_NoSystemBackground )# バックグラウンドなし
        self.view.setAttribute( Qt.WA_TranslucentBackground )# ビューの背景を完全透明化する
        self.view.setWindowFlags( Qt.Tool | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus )# 枠なしカバーウィンドウにする. Qt.WindowStaysOnTopHint: 全画面上で常に最前面にView表示させるフラグ.これは外す
        # プラットフォーム依存のQt.CoverWindowの代わりにQt.Toolを使っている

        self.myFrame.layout().addWidget( self.backgroundWidget )# 埋め込みアプリ背景ウィンドウはQLayoutに登録する


        self.button = QPushButton("Toggle Overlay")
        self.button.setFixedHeight(50)

        self.button2 = QPushButton("Swap Layer")
        self.button2.setFixedHeight(50)


        self.verticalLayout = QVBoxLayout( self )# QStackedLayout(self)#
        #self.layout().setStackingMode( QStackedLayout.StackAll )
        self.verticalLayout.addWidget( self.myFrame )#self.view )#
        self.verticalLayout.addWidget( self.button )
        self.verticalLayout.addWidget( self.button2 )


        #self.scene.addItem( rect )

        # レイヤー作成テスト
        layer_id = self.scene.m_Layers.AddLayer()

        # define rect item
        rect = QGraphicsRectItem()
        rect.setRect( 0, 0, 60, 20 )
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



        self.scene.m_Layers.DeleteItem( rect2, layer_id )



       
        self.button.clicked.connect( lambda: self.button_off() if self.view.isVisible() else self.button_on() )
        self.button2.clicked.connect( self.swap_layer )


    def button_on( self ):
        self.view.show()


    def button_off( self ):
        self.view.hide()


    def swap_layer( self ):
        print( "windowOverlay::swap_layer()..." )
        self.scene.m_Layers.MoveLayer(0, self.scene.m_Layers.NumLayers()-1 )


    def moveEvent( self, event ):
        super(windowOverlay, self).moveEvent( event )
        print( "windowOverlay::moveEvent()..." )
        if( self.view ): self.myFrame.moveChildren( event.pos() )
        event.accept()





if __name__ == "__main__":

    app = QApplication( sys.argv )

    main = windowOverlay()

    #app.focusChanged.connect( lambda old, new: main.onTabFocusChanged( old, new ) )

    main.show()

    sys.exit( app.exec_() )