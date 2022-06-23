import sys

from oreorepylib.ui.pyqt5 import stylesheet

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class ScrollBar( QScrollBar ):

    signal_maxlimit = pyqtSignal()
    signal_minlmit = pyqtSignal()


    def __init__( self, parent=None ):
        super( ScrollBar, self ).__init__( parent )


    def wheelEvent( self, event ):
        super(ScrollBar, self).wheelEvent(event)

        if( self.value() == self.maximum() and event.angleDelta().y() < 0 ):
            print( 'scrollbar at max limit' )
            self.signal_maxlimit.emit()

        if( self.value() == self.minimum() and event.angleDelta().y() > 0 ):
            print( 'scrollbar at min limit' )
            self.signal_minlmit.emit()


    def mouseMoveEvent(self, QMouseEvent):
        super(ScrollBar, self).mouseMoveEvent(QMouseEvent)

        if( self.value() == self.maximum() ):
            print( 'scrollbar at max limit' )
            self.signal_maxlimit.emit()

        if( self.value() == self.minimum() ):
            print( 'scrollbar at min limit' )
            self.signal_minlmit.emit()


    def mousePressEvent( self, QMouseEvent ):
        super(ScrollBar, self).mousePressEvent(QMouseEvent)

        if( self.value() == self.maximum() ):
            print( 'scrollbar at max limit' )
            self.signal_maxlimit.emit()

        if( self.value() == self.minimum() ):
            print( 'scrollbar at min limit' )
            self.signal_minlmit.emit()





class ScrollArea( QScrollArea ):

    def __init__( self, parent=None ):
        super(ScrollArea, self).__init__( parent )

        self.setVerticalScrollBar( ScrollBar(self) ) 
        self.setHorizontalScrollBar( ScrollBar(self) )
        self.signal_v = self.verticalScrollBar().signal_maxlimit
        self.signal_h = self.horizontalScrollBar().signal_maxlimit

        self.setStyleSheet( stylesheet.g_DynamicFrameStyleSheet )

        self.verticalScrollBar().setStyleSheet( stylesheet.g_ScrollBarStyleSheet )
        self.horizontalScrollBar().setStyleSheet( stylesheet.g_ScrollBarStyleSheet )



g_list = [ 'a', 'b', 'c' ]

def proc_extend():
    list = g_list[0:1]

    print( 'proc_extend...', list )






if __name__=='__main__':

    app = QApplication(sys.argv)

    frame = QFrame()
    frame.setGeometry( 100, 100, 600, 300 )
    frame.setLayout( QGridLayout() )

    scroll = ScrollArea()
    scroll.setWidgetResizable(False)
    scroll.setWidget( frame )

    scroll.signal_v.connect( proc_extend )

    scroll.show()


    sys.exit(app.exec_())
    