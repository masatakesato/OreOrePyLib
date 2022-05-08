# https://wiki.python.org/moin/PyQt/Exporting%20a%20file%20to%20other%20applications

import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *






class ParentFrame(QFrame):

    def __init__( self, *args, **kwargs ):
        super(ParentFrame, self).__init__(*args, **kwargs)

        self.setStyleSheet( 'background-color:black;' )
        self.setAcceptDrops(True)


    def mousePressEvent(self, event):
        print( 'ParentFrame::mousePressEvent' )
        return super(ParentFrame, self).mousePressEvent(event)
        


    def dragEnterEvent(self, event ):
        print( 'ParentFrame::dragEnterEvent' )
        event.acceptProposedAction()
        return super(ParentFrame, self).dragEnterEvent(event)



    #def dragMoveEvent( self, event ):
    #    print( 'ParentFrame::dragMoveEvent' )
    #    return super(ParentFrame, self).dragMoveEvent(event)




    def dropEvent( self, event ):
        print( 'ParentFrame::dreopEvent' )
        return super(ParentFrame, self).dropEvent(event)



    def checkOverlap( self, globalPos, style ):
        #print( '//=========== checkOverlap ===========//' )
        #print( '  globalPos:', globalPos.x(), globalPos.y() )
        pos = self.mapFromGlobal( globalPos )
        #print( '  local_pos:', pos.x(), pos.y() )
        #print( '  rect_size:', self.rect().width(), self.rect().height() )
        #print( '  ParentFrame::checkOverlap: %r' % self.rect().contains( pos ) )
        
        if( self.rect().contains( pos ) ):
            self.setStyleSheet( style )
        else:
            self.setStyleSheet( 'background-color:black;' )




class Frame(QFrame):

    movedSignal = pyqtSignal(QPoint, str)

    def __init__( self, *args, **kwargs ):
        super(Frame, self).__init__(*args, **kwargs)

        #self.setAcceptDrops(True)

        self.installEventFilter( self )



    #def mousePressEvent(self, event):
    #    print( 'Frame::mousePressEvent' )
    #    return super(Frame, self).mousePressEvent(event)


    #def mouseReleaseEvent(self, event):
    #    print( 'Frame::mouseReleaseEvent' )
    #    return super(Frame, self).mouseReleaseEvent(event)



    #def dragEnterEvent(self, event ):
    #    print( 'Frame::dragEnterEvent' )
    #    return super(Frame, self).dragEnterEvent(event)



    #def dropEvent( self, event ):
    #    print( 'Frame::dreopEvent' )
    #    return super(Frame, self).dropEvent(event)



    def moveEvent( self, event ):
        #print( '//=========== Frame::moveEvent ==============//' )
        #print( '  event.pos():', event.pos().x(), event.pos().y() )
        self.movedSignal.emit( self.pos(), 'background-color:rgb(128,128,0);' )
        
        super(Frame, self).moveEvent(event)



    def eventFilter( self, widget, event ):
        if( event.type()==QEvent.NonClientAreaMouseButtonRelease ):# Catch non client area mouse release
            globalPos = widget.pos()
            self.movedSignal.emit( globalPos, 'background-color:rgb(0,128,0);' )

        return False






if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    parentframe = ParentFrame()
    parentframe.setWindowTitle( 'ParentFrame' )
    #parentframe.setGeometry( 100, 100, 640, 480 )

    parentframe.show()



    subframe = Frame()
    subframe.setWindowTitle( 'SubFrame' )
    subframe.setGeometry( 100, 100, 200, 100 )

    subframe.movedSignal.connect( parentframe.checkOverlap )


    subframe.show()


    sys.exit(app.exec_())