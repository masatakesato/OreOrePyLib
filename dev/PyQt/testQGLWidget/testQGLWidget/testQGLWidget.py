import sys

#from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *


class GraphicsView(QGraphicsView):

    def __init__(self):

        super(GraphicsView, self).__init__()

        self.wid = QGLWidget()

        self.setViewport( self.wid )

        self.setWindowTitle("Test Node Graph")
        #self.setStyleSheet( stylesheet.NodeEditorStyleSheet )
        #self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        ##view->setOptimizationFlags(QGraphicsView::DontSavePainterState);
        self.setViewportUpdateMode( QGraphicsView.SmartViewportUpdate )
        self.setCacheMode( QGraphicsView.CacheBackground )
        
        self.setResizeAnchor( QGraphicsView.AnchorViewCenter )

        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )

        ##self.__m_RubberBand = QRubberBand(self)
        #self.setAcceptDrops(True)

        self.zoomScale = 1.0
        # Background config
        self.gridStep = 50#g_GridStep


    def Release( self ):
        self.setViewport(None)
        del self.wid


    ######################### QGraphicsView func override #########################

    # zoom in/out using mouse wheel: http://stackoverflow.com/questions/19113532/qgraphicsview-zooming-in-and-out-under-mouse-position-using-mouse-wheel
    # deprecated (07.08.2016)

    # new reference implementation: http://blog.automaton2000.com/2014/04/mouse-centered-zooming-in-qgraphicsview.html
    def wheelEvent( self, event ):

        if( event.angleDelta().x() == 0 ):

            pos  = event.pos()
            posf = self.mapToScene(pos)

            by = 1.0
            angle = event.angleDelta().y()

            if( angle > 0 ):    by = 1 + ( angle / 360 * 0.2)
            elif( angle < 0 ):  by = 1 - (-angle / 360 * 0.2)
            else:               by = 1

            self.zoomScale *= by
            #self.scale(by, by)
            self.setTransform( QTransform().scale( self.zoomScale, self.zoomScale ) )


            w = self.viewport().width()
            h = self.viewport().height()

            wf = self.mapToScene( QPoint(w-1, 0) ).x() - self.mapToScene(QPoint(0,0)).x()
            hf = self.mapToScene( QPoint(0, h-1) ).y() - self.mapToScene(QPoint(0,0)).y()

            lf = posf.x() - pos.x() * wf / w
            tf = posf.y() - pos.y() * hf / h

            # try to set viewport properly
            self.setSceneRect( lf, tf, wf, hf )
            #self.ensureVisible( lf, tf, wf, hf, 0, 0 )

            newPos = self.mapToScene(pos)
           
            # readjust according to the still remaining offset/drift. I don't know how to do this any other way
            self.setSceneRect( QRectF( QPointF(lf, tf) - newPos + posf, QSizeF(wf, hf)) )
            #self.ensureVisible( QRectF( QPointF(lf, tf) - newPos + posf, QSizeF(wf, hf)), 0, 0 )
            
            event.accept()


    def mousePressEvent(self, event):

        self.prevPos = QPoint()
        self.drag = False

        if( event.modifiers() == Qt.AltModifier and event.button() == Qt.MiddleButton  ):

            self.setDragMode(QGraphicsView.NoDrag)
            self.drag = True
            self.prevPos = event.pos()
            self.setCursor(Qt.SizeAllCursor)

            #self.setDragMode( QGraphicsView.ScrollHandDrag )

        elif( event.button() == Qt.LeftButton ):

            self.setDragMode(QGraphicsView.RubberBandDrag)

        super(GraphicsView, self).mousePressEvent(event)
 

    def mouseMoveEvent(self, event):

        if( self.drag == True ):

            delta = (self.mapToScene(event.pos()) - self.mapToScene(self.prevPos)) * -1.0
            center = QPoint( self.viewport().width()/2 + delta.x(), self.viewport().height()/2 + delta.y() )
            newCenter = self.mapToScene(center)
            
            self.prevPos = event.pos()
            self.centerOn(newCenter)

            rect = self.sceneRect()
            self.setSceneRect( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height() )
            #self.ensureVisible( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height(), 0, 0 )

            event.accept()

            return

        super(GraphicsView, self).mouseMoveEvent(event)
 

    def mouseReleaseEvent(self, event):

        if( self.drag==True ):
            self.drag = False
            self.setCursor(Qt.ArrowCursor)

        super(GraphicsView, self).mouseReleaseEvent(event)


       
    def drawBackground( self, painter, rect ):
        #print( "GraphicsView::drawBackground" )

        # set background color
        #painter.fillRect( rect, QColor(42,42,42) ) # deprecated. defined using stylesheet (2016.07.16)

        # draw horizontal grid
        painter.setPen( QPen( QColor(64, 64, 64), 1.0/self.zoomScale ) )
        
        start = int(rect.top()) + self.gridStep / 2
        start -= start % self.gridStep

        if(start > rect.top()):
            start -= self.gridStep
        
        y = start - self.gridStep
        while( y < rect.bottom() ):
            y += self.gridStep
            painter.drawLine(rect.left(), y, rect.right(), y)

        # now draw vertical grid
        #start = rect.left() % self.gridStep
        start = int(rect.left()) + self.gridStep / 2
        start -= start % self.gridStep

        if(start > rect.left()):
            start -= self.gridStep
        
        x = start - self.gridStep
        while( x < rect.right() ):
            x += self.gridStep
            painter.drawLine(x, rect.top(), x, rect.bottom())



    def dragEnterEvent( self, event ):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def dropEvent( self, event ):
        pos = self.mapToScene( event.pos() )
        print( pos.x(), pos.y() )
        
        for url in event.mimeData().urls():
            filepath = str(url.toLocalFile())
            self.scene().ExecCommand( ['Import', filepath, (pos.x(), pos.y())] )




    def dragMoveEvent( self, event ):
        pass
        #return super(GraphicsView, self).dragMoveEvent(event)


    def dragLeaveEvent( self, event ):
        pass
        #return super(GraphicsView, self).dragLeaveEvent(event)



class MainWidget(QMainWindow):

    def __init__( self ):
        super(MainWidget,self).__init__()


        #========== Graphic Components ===========#
        self.__m_NodeEditorUI = QGraphicsScene()
        self.__m_NodeEditorUI.setSceneRect(-400, -400, 800, 800)

        # create view(graphics)
        self.view = GraphicsView()
        self.view.setScene( self.__m_NodeEditorUI )


        #self.vsplitter = QSplitter(Qt.Vertical)
        #self.vsplitter.addWidget(self.view)


        #self.hsplitter = QSplitter(Qt.Horizontal)
        #self.hsplitter.addWidget(self.vsplitter)


        #Pal = QPalette()
        #Pal.setColor( QPalette.Background, QColor(80,80,80) )
        #self.hsplitter.setAutoFillBackground(True)
        #self.hsplitter.setPalette(Pal)
        

        self.setCentralWidget(self.view )

        self.setGeometry( 300, 50, 1280, 768 )
        

    def SceneManager( self ):
        return self.__m_SceneManager

  
    def closeEvent(self, QCloseEvent):
        self.view.Release()
        return super().closeEvent(QCloseEvent)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWindow = MainWidget()
    mainWindow.setWindowTitle('Test QGLWidget')
    mainWindow.show()
        
    sys.exit(app.exec_())