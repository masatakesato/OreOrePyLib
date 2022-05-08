import sys
import traceback

from oreorepylib.utils import environment

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from graphics.GraphicsView import GraphicsView
from graphics.ImageRect import ImageRect









class Scene(QGraphicsScene):

    def __init__( self, *args, **kwargs ):
        super(Scene, self).__init__(*args, **kwargs)

        self.__m_ImageRect = ImageRect()
        self.addItem( self.__m_ImageRect )

        self.action_paste = QAction( 'Paste from Clipboard' )
        self.action_paste.setShortcut( QKeySequence(Qt.CTRL + Qt.Key_V) )
        self.action_paste.triggered.connect( self.__m_ImageRect.PasteFromClipboard )



    def print_( self, rect, item_list ):
        for item in item_list:
            item.SetRect( rect )
            item.update()
            #item.SaveImage( rect )
            #print( item.pixmap().rect().intersected( rect ) )


    #def keyPressEvent( self, event ):

    #    if( event.key()==Qt.Key_F ):
            
    #        itemsRect = self.itemsBoundingRect()
    #        pos = itemsRect.center()#self.__m_ImageRect.sceneBoundingRect().center()
    #        w_item = itemsRect.width()# * self.__m_ImageRect.scale()
    #        h_item = itemsRect.height()# * self.__m_ImageRect.scale()

    #        for view in self.views():
    #            w_view = view.width()
    #            h_view = view.height()
    #            zoom = min( w_view/w_item, h_view/h_item )
    #            view.CenterOn( pos, zoom )

    #    elif( event.key()==Qt.Key_S ):
    #        print( 'save' )
    #        for item in self.items():
    #            if( type(item) == ImageRect ):
    #                item.SaveImage( rect )

    #    return super(Scene, self).keyPressEvent(event)



    def dragEnterEvent( self, event ):
        if( event.mimeData().hasUrls() ):
            event.accept()
        else:
            event.ignore()
        return super(Scene, self).dragEnterEvent(event) 



    # moved from GraphicsView class. 2019.07.23
    def dropEvent( self, event ):
        try:
            pos = event.scenePos()
            for url in event.mimeData().urls():
                filepath = str(url.toLocalFile())
                print( filepath )
                self.__m_ImageRect.LoadImage( filepath )
                #self.Import( filepath, pos )
        except:
            traceback.print_exc()

        return super(Scene, self).dropEvent(event)



    def contextMenuEvent( self, event ):
        pos = event.scenePos()

        menu = QMenu()
        menu.addAction( self.action_paste )
        menu.exec(event.screenPos())









if __name__=='__main__':

    app = QApplication( sys.argv )

    #item = ImageRect(  )#QPixmap('input.png')
    #item.setPixmap( QPixmap('input.png') )
    #item.setFlag(QGraphicsItem.ItemIsMovable, True)
    #item.setFlag(QGraphicsItem.ItemIsSelectable, True)

    scene = Scene()
    scene.setSceneRect(-400, -400, 800, 800)
    #scene.addItem( item )

    view = GraphicsView( '', 50 )
    view.setScene( scene )

    view.RubberbandSelectionFinished.connect( scene.print_ )


    widget = QFrame()
    widget.setGeometry( 300, 50, 800, 800 )
    widget.setLayout( QVBoxLayout() )
    widget.layout().addWidget( view )
    widget.show()
    
    sys.exit( app.exec_() )
    




#import sys
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *


#class QExampleLabel (QLabel):
#    def __init__(self, parentQWidget = None):
#        super(QExampleLabel, self).__init__(parentQWidget)
#        self.initUI()

#    def initUI (self):
#        self.setPixmap(QPixmap('input.png'))

#    def mousePressEvent (self, eventQMouseEvent):
#        self.originQPoint = eventQMouseEvent.pos()
#        self.currentQRubberBand = QRubberBand(QRubberBand.Rectangle, self)
#        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QSize()))
#        self.currentQRubberBand.show()

#    def mouseMoveEvent (self, eventQMouseEvent):
#        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())

#    def mouseReleaseEvent (self, eventQMouseEvent):
#        self.currentQRubberBand.hide()
#        currentQRect = self.currentQRubberBand.geometry()
#        self.currentQRubberBand.deleteLater()
#        cropQPixmap = self.pixmap().copy(currentQRect)
#        cropQPixmap.save('output.png')

#if __name__ == '__main__':
#    myQApplication = QApplication(sys.argv)
#    myQExampleLabel = QExampleLabel()
#    myQExampleLabel.show()
#    sys.exit(myQApplication.exec_())