﻿from graphics.GraphicsSettings import *
import oreorepylib.ui.pyqt5.stylesheet as UIStyle



# https://wiki.qt.io/Smooth_Zoom_In_QGraphicsView/ja
class GraphicsView(QGraphicsView):

    WidgetClosed = pyqtSignal()
    FocusViewIdChanged = pyqtSignal(object)
    RenderViewIdChanged = pyqtSignal(object)
    RubberbandSelectionFinished = pyqtSignal(object, object)


    def __init__( self, key, gridstep ):
        super(GraphicsView, self).__init__()

        self.__m_Key = key
        self.__m_GridStep = gridstep
        self.__m_ZoomScale = 1.0
        
        self.__m_MouseMode = MouseMode.DoNothing
        self.__m_RubberBand = QRubberBand( QRubberBand.Rectangle, self )

        self.setStyleSheet( UIStyle.g_EditorStyleSheet )
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        pal = QPalette()
        pal.setBrush( QPalette.Highlight, QColor(170,115,26) )#QColor(255,127,39)
        self.__m_RubberBand.setPalette(pal)

        #self.setViewport(QOpenGLWidget())# これ使うと遅くない?
        self.setOptimizationFlags( QGraphicsView.DontSavePainterState )
        self.setViewportUpdateMode( QGraphicsView.SmartViewportUpdate )
        self.setCacheMode( QGraphicsView.CacheBackground )

        self.setResizeAnchor( QGraphicsView.AnchorViewCenter )

        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )

        self.setAcceptDrops(True)


    def Release( self ):
        self.setViewport(None)
        self.FocusViewIdChanged.disconnect()
        self.RenderViewIdChanged.disconnect()



    def CenterOn( self, pos, zoom ):

        # reset scale transform
        self.setTransform( QTransform().scale( 1.0, 1.0 ) )
        
        # fit view
        w = self.viewport().width()
        h = self.viewport().height()

        wf = self.mapToScene( QPoint(w-1, 0) ).x() - self.mapToScene(QPoint(0,0)).x()
        hf = self.mapToScene( QPoint(0, h-1) ).y() - self.mapToScene(QPoint(0,0)).y()

        lf = -0.5 * w + pos.x()
        tf = -0.5 * h + pos.y()
        
        print( lf, tf, wf, hf )
        self.setSceneRect( lf, tf, wf, hf )
        self.fitInView( lf, tf, wf, hf )# using instead of buggy QGraphicsView::centerOn. 2019.8.03

        # set scaling
        self.__m_ZoomScale = zoom
        self.setTransform( QTransform().scale( self.__m_ZoomScale, self.__m_ZoomScale ) )

        

    ######################## QGraphicsView func override #########################

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

            self.__m_ZoomScale *= by
            self.__m_ZoomScale = min(max(self.__m_ZoomScale,0.1), 5.0)
            #self.scale(by, by)
            self.setTransform( QTransform().scale( self.__m_ZoomScale, self.__m_ZoomScale ) )


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
        super(GraphicsView, self).mousePressEvent(event)
        self.prevPos = event.pos()

        if( event.modifiers() == Qt.AltModifier and event.button() == Qt.MiddleButton ):# View Translation
            self.__m_MouseMode = MouseMode.MoveViewport
            self.setCursor(Qt.SizeAllCursor)
            return

        elif( event.button() == Qt.LeftButton and not self.scene().selectedItems() ):# Rubberband Selection
            self.__m_MouseMode = MouseMode.RubberBandSelection
            
        
 

    def mouseMoveEvent(self, event):

        if( self.__m_MouseMode == MouseMode.MoveViewport ):
            delta = (self.mapToScene(event.pos()) - self.mapToScene(self.prevPos)) * -1.0
            center = QPoint( self.viewport().width()/2 + delta.x(), self.viewport().height()/2 + delta.y() )
            newCenter = self.mapToScene(center)
            
            self.prevPos = event.pos()
            self.centerOn(newCenter)

            rect = self.sceneRect()
            self.setSceneRect( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height() )
            #self.ensureVisible( rect.x() + delta.x(), rect.y() + delta.y(), rect.width(), rect.height(), 0, 0 )

        elif( self.__m_MouseMode == MouseMode.RubberBandSelection ):
            self.__m_RubberBand.setGeometry( QRect(self.prevPos, event.pos()).normalized() )
            self.__m_RubberBand.show()

        super(GraphicsView, self).mouseMoveEvent(event)
 

    def mouseReleaseEvent(self, event):

        if( self.__m_MouseMode == MouseMode.MoveViewport ):
            self.setCursor(Qt.ArrowCursor)

        elif( self.__m_MouseMode == MouseMode.RubberBandSelection ):
            
            if( self.__m_RubberBand.isVisible() ):
                self.__m_RubberBand.hide()
                rect = self.__m_RubberBand.geometry()

                self.scene().blockSignals(True)

                rect_scene = self.mapToScene(rect).boundingRect()
                #print( rect_scene )
                self.RubberbandSelectionFinished.emit( rect_scene, self.items( rect, Qt.IntersectsItemShape ) )

                for item in self.items( rect, Qt.IntersectsItemShape ):
                    #print( 'SELECTED ITEM SHAPE....', item.shape().boundingRect() )
                    item.setSelected(True)
                self.scene().blockSignals(False)
                self.scene().selectionChanged.emit()
        
        self.__m_MouseMode = MouseMode.DoNothing

        super(GraphicsView, self).mouseReleaseEvent(event)


       
    def drawBackground( self, painter, rect ):
        # draw horizontal grid
        painter.setPen( QPen( QColor(42, 42, 42), 1.0/self.__m_ZoomScale ) )
        
        start = int(rect.top()) + self.__m_GridStep / 2
        start -= start % self.__m_GridStep

        if(start > rect.top()):
            start -= self.__m_GridStep
        
        y = start - self.__m_GridStep
        while( y < rect.bottom() ):
            y += self.__m_GridStep
            painter.drawLine(rect.left(), y, rect.right(), y)

        # now draw vertical grid
        #start = rect.left() % self.__m_GridStep
        start = int(rect.left()) + self.__m_GridStep / 2
        start -= start % self.__m_GridStep

        if(start > rect.left()):
            start -= self.__m_GridStep
        
        x = start - self.__m_GridStep
        while( x < rect.right() ):
            x += self.__m_GridStep
            painter.drawLine(x, rect.top(), x, rect.bottom())


    # moved to GraphicsScene class. 2019.07.23
    #def dragEnterEvent( self, event ):
    #    if event.mimeData().hasUrls():
    #        event.accept()
    #    else:
    #        event.ignore()
    #    return super(GraphicsView, self).dragEnterEvent(event)
    

    # moved to GraphicsScene class. 2019.07.23
    #def dropEvent( self, event ):
    #    pos = self.mapToScene( event.pos() )
    #    for url in event.mimeData().urls():
    #        filepath = str(url.toLocalFile())
    #        self.scene().Import( filepath, pos )
    #    return super(GraphicsView, self).dropEvent(event)


    def dragMoveEvent( self, event ):
        pass
        #return super(GraphicsView, self).dragMoveEvent(event)


    def dragLeaveEvent( self, event ):
        pass
        #return super(GraphicsView, self).dragLeaveEvent(event)


    def resizeEvent( self, event ):
        self.viewport().update()
        return super(GraphicsView, self).resizeEvent(event)


    def focusInEvent( self, event ):
        self.FocusViewIdChanged.emit( self.__m_Key )
        return super(GraphicsView, self).focusInEvent(event)


    def paintEvent( self, event ):
        self.RenderViewIdChanged.emit( self.__m_Key )
        super(GraphicsView, self).paintEvent(event)



    def keyPressEvent( self, event ):
        super(GraphicsView, self).keyPressEvent(event)

        if( event.key()==Qt.Key_F ):
            if( not self.scene().items() ):
                self.CenterOn( QPointF(0.0,0.0), 1.0 )
                return

            itemsRect = QRectF()
            items = self.scene().selectedItems()
            if( items ):# unite selected items' boundengRects
                for item in self.scene().selectedItems():
                    itemsRect |= item.sceneBoundingRect()
            else:# use all items' rects if nothing selected.
                itemsRect = self.scene().itemsBoundingRect()

            zoom = 1.0 if itemsRect.isEmpty() else min( min( self.width() / itemsRect.width(), self.height() / itemsRect.height() ), 1.0 )
            self.CenterOn( itemsRect.center(), zoom )

        # Implemented for debug purpose. pillow is required
        #elif( event.key()==Qt.Key_S ):
        #    print( 'save' )
        #    for item in self.items():
        #        if( type(item) == ImageRect ):
        #            item.SaveImage( rect )



    def closeEvent( self, event ):
        super(GraphicsView, self).closeEvent(event)
        self.WidgetClosed.emit()