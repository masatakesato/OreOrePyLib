import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


import oreorepylib.ui.pyqt5.stylesheet as StyleSheet
from oreorepylib.ui.pyqt5.frame import Frame



# Dockable Widget's Opacity. Overlapped with parent tab: 0.5, No overlap: 1.0.
g_DockableWidgetOpacity = (1.0, 0.5)

# Position offset of detaced dockable widget.
g_DockableWidgetDetachOffset = QPoint(-10, -10)




g_TabWidgetStyleSheet = """ 

/*====================== TabWidget settings ==========================*/
QTabWidget::pane
{
    /*background-color: transparent;*/ /* valid inside padding area */
    margin: 0px 0px 0px 0px;
    
    border-top: 2px solid rgb(72,72,72);
    border-right: 1px solid rgb(72,72,72);
    border-bottom: 1px solid rgb(72,72,72);
    border-left: 1px solid rgb(72,72,72);

    padding: 0px 0px 0px 0px;
}

QTabWidget::pane:active
{
    border-top: 2px solid rgb(191,77,0);
}


/*======================== TabBar settings ==========================*/
QTabBar::tab
{
    color: rgb(235,235,235);
    background-color: rgb(42,42,42);

    height: 17px;

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 2px 24px 2px 12px; /*top, right, bottom, left*/
}

QTabBar::tab:hover
{
    background-color: rgb(60,60,60);
}

QTabBar::tab:selected
{
    background-color: rgb(72,72,72);
}

QTabBar::tab:selected:active
{
    background-color: rgb(191,77,0);
}

QTabBar::close-button
{
    image: url(:/resource/images/close.png);
}


/*============== TabBar close button Settings ======================*/
QTabBar::close-button:hover
{
    background-color: rgb(96,96,96);
}

QTabBar::close-button:pressed
{
    background-color: rgb(32,32,32);
}

QTabBar::close-button:selected:hover
{
    background-color: rgb(128,128,128);
}

QTabBar::close-button:selected:pressed
{
    background-color: rgb(48,48,48);
}

QTabBar::close-button:selected:active:hover
{
    background-color: rgb(255,127,39);
}

QTabBar::close-button:selected:active:pressed
{
    background-color: rgb(125,50,0);
}


/*===================== Left/Right arrow icons Settings ======================*/
QTabBar QToolButton
{
    background-color: rgb(42,42,42);

    margin: 0px 0px 0px 0px;
    border: 0px none;
    padding: 0px 0px 0px 0px;
}


QTabBar QToolButton::left-arrow
{
    background-color: rgb(60,60,60);

    width: 14px;
    height: 14px;
    image: url(:/resource/images/arrow-left.png);
}

QTabBar QToolButton::left-arrow:hover
{
    background-color: rgb(72,72,72);
}

QTabBar QToolButton::left-arrow:pressed
{
    background-color: rgb(32,32,32);
}


QTabBar QToolButton::right-arrow
{
    background-color: rgb(60,60,60);

    width: 14px;
    height: 14px;
    image: url(:/resource/images/arrow-right.png);
}

QTabBar QToolButton::right-arrow:hover
{
    background-color: rgb(72,72,72);
}

QTabBar QToolButton::right-arrow:pressed
{
    background-color: rgb(32,32,32);
}

"""



# TabBar
class MyTabBar(QTabBar):

    # Signals
    DetachWidgetSignal = pyqtSignal(int)
    AttachWidgetSignal = pyqtSignal(int)

    # Drag mode
    __DRAG_NONE__ = -1
    __DRAG_TAB__ = 0
    __DRAG_WIDGET__ = 1

    # State change patterns...
    # __DRAG_NONE__ -> __DRAG_NONE__
    # __DRAG_NONE__ -> __DRAG_TAB__ -> __DRAG_NONE__
    # __DRAG_NONE__ -> __DRAG_TAB__ -> __DRAG_WIDGET__ -> __DRAG_NONE__



    def __init__( self, *args, **kwargs ):
        super(MyTabBar, self).__init__(*args, **kwargs)
        
        self.__m_TabIndex = -1
        self.frame = None
        self.__m_DragMode = self.__DRAG_NONE__



    def mousePressEvent( self, event ):
        #print( 'MyTabBar::mousePressEvent' )

        self.__m_TabIndex = self.tabAt( event.pos() )

        # Triggers tab drag operations ONLY WHEN LEFT MOUSE PRESSED.
        if( event.button()==Qt.LeftButton ):
            self.setCurrentIndex( self.__m_TabIndex )
            self.__m_DragMode = self.__DRAG_TAB__

        return super(MyTabBar, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        #print( 'MyTabBar::mouseMoveEvent' )

        if( self.__m_DragMode==self.__DRAG_WIDGET__ ):
            event.ignore()

        elif( self.__m_DragMode==self.__DRAG_TAB__ ):
            pos = event.pos()
            # Mouse is moving inside QTabBar area
            if( self.rect().contains(pos) ):
                index = self.tabAt(pos)
                if( index != self.__m_TabIndex ):
                    self.moveTab( self.__m_TabIndex, index )
                    self.__m_TabIndex = index
            # Mouse has just moved outside QTabBar area
            else:
                self.__m_DragMode = self.__DRAG_WIDGET__
                self.DetachWidgetSignal.emit( self.__m_TabIndex )


        #else:# self.__DRAG_NONE__
        #    pass

        return super(MyTabBar, self).mouseMoveEvent(event)
        


    def mouseReleaseEvent( self, event ):
        #print( 'MyTabBar::mouseReleaseEvent' )
        
        # Detached widget has been released inside QTabBar area
        pos = event.pos()
        if( self.__m_DragMode==self.__DRAG_WIDGET__ and self.rect().contains(pos) ):
            self.AttachWidgetSignal.emit( self.tabAt(pos) )

        self.__m_DragMode = self.__DRAG_NONE__

        return super(MyTabBar, self).mouseReleaseEvent(event)





class MyDockableFrame(Frame):

    # Signals
    moveSignal = pyqtSignal(object, QPoint)
    releaseSignal_ = pyqtSignal(object, QPoint)


    def __init__( self, *args, **kwargs ):
        super(MyDockableFrame, self).__init__(*args, **kwargs)



    #def mousePressEvent(self, event):
    #    return super(MyDockableFrame, self).mousePressEvent(event)


    
    def mouseMoveEvent( self, event ):
        #print( 'MyDockableFrame::mouseMoveEvent()...' )
        # Avoid docking at the end of widget resize operation
        if( self.handleSelected is None ):
            self.moveSignal.emit( self, event.globalPos() )

        return super(MyDockableFrame, self).mouseMoveEvent(event)



    def mouseReleaseEvent(self, event):
        #print( 'MyDockableFrame::mouseReleaseEvent()...' )

        # Avoid docking at the end of widget resize operation
        if( self.handleSelected is None ):
            self.releaseSignal_.emit( self, event.globalPos() )

        return super(MyDockableFrame, self).mouseReleaseEvent(event)





# TabWidget
class MyTabWidget(QTabWidget):
    
    def __init__( self, *args, **kwargs ):
        super(MyTabWidget, self).__init__(*args, **kwargs)
        
        # Setup custom QTabBar
        self.tabBar = MyTabBar(self)
        self.tabBar.DetachWidgetSignal.connect( self.DetachWidget )
        self.tabBar.AttachWidgetSignal.connect( self.AttachWidget )

        self.setTabBar( self.tabBar )

        self.setTabsClosable(True)# Put close button on each tabs
        self.setMovable(False)# Disable default tab drag feature.


        self.setStyleSheet( g_TabWidgetStyleSheet )

        self.__m_Frames = {}
        self.__m_CurrID = None



    def DetachWidget( self, index ):
        print( 'MyTabWidget::DetachWidget()...%d' % index )

        newFrame = MyDockableFrame()
        newFrame.setLayout( QVBoxLayout() )
        newFrame.moveSignal.connect( self.__CheckInteraction )
        newFrame.releaseSignal_.connect( self.__CheckAttach )

        contentWidget = self.widget( index )

        newFrame.setWindowTitle( contentWidget.windowTitle() )
        newFrame.resize( contentWidget.width(), contentWidget.height() )
        newFrame.layout().addWidget( contentWidget )
        contentWidget.setVisible(True)# MUST SET VISIBLE. Widgets detached from QTabWidget are INVISIBLE.

        newFrame.show()

        self.__m_CurrID = id(newFrame)
        self.__m_Frames[ self.__m_CurrID ] = newFrame



    def AttachWidget( self, index ):
        print( 'MyTabWidget::AttachWidget()...%d' % index )

        currFrame = self.__m_Frames[ self.__m_CurrID ]

        if( currFrame.layout().count() > 0 ):
            contentWidget = currFrame.layout().itemAt(0).widget()
            self.insertTab( index, contentWidget, contentWidget.windowTitle() )
        
        del self.__m_Frames[ self.__m_CurrID ]

        self.__m_CurrID = None



    def __SetCurrenID( self, id_ ):
        self.__m_CurrID = id_



    def __CheckInteraction( self, widget, globalPos ):
        pos = self.tabBar.mapFromGlobal( globalPos )
        widget.setWindowOpacity( g_DockableWidgetOpacity[ int(self.tabBar.rect().contains(pos)) ] )



    def __CheckAttach( self, widget, globalPos ):
        pos = self.tabBar.mapFromGlobal( globalPos )
        index = self.tabBar.tabAt(pos)
        if( index != -1 ):
            self.__m_CurrID = id(widget)
            self.AttachWidget(index)





    #def mousePressEvent( self, event ):
    #    print( 'MyTabWidget::mousePressEvent' )
    #    return super(MyTabWidget, self).mousePressEvent(event)



    def mouseMoveEvent( self, event ):
        #print( 'MyTabWidget::mouseMoveEvent' )

        if( self.__m_CurrID ):
            index = self.tabBar.tabAt( event.pos() )
            if( index !=-1 ):
                self.__m_Frames[ self.__m_CurrID ].setWindowOpacity(0.5)
            else:
                self.__m_Frames[ self.__m_CurrID ].setWindowOpacity(1.0)
            self.__m_Frames[ self.__m_CurrID ].move( event.globalPos() + g_DockableWidgetDetachOffset )

        return super(MyTabWidget, self).mouseMoveEvent(event)



    #def mouseReleaseEvent( self, event ):
    #    print( 'MyTabWidget::mouseReleaseEvent' )
    #    return super(MyTabWidget, self).mouseReleaseEvent(event)







if __name__=='__main__':

    app = QApplication( sys.argv )


    frame = Frame()

    layout = QVBoxLayout()
    layout.setContentsMargins(4,4,4,4)

    frame.setLayout( layout )

    

    w = MyTabWidget()
    
    edit1 = QTextEdit( 'Text1' )
    edit1.setWindowTitle( 'Tab1' )

    edit2 = QTextEdit( 'Text2' )
    edit2.setWindowTitle( 'Tab2' )

    edit3 = QTextEdit( 'Text3' )
    edit3.setWindowTitle( 'Tab3' )
        
    edit4 = QTextEdit( 'Text4' )
    edit4.setWindowTitle( 'Tab4' )


    w.addTab( edit1, edit1.windowTitle() )
    w.addTab( edit2, edit2.windowTitle() )
    w.addTab( edit3, edit3.windowTitle() )
    w.addTab( edit4, edit4.windowTitle() )


    frame.layout().addWidget(w)

    frame.show()


    sys.exit( app.exec_() )
