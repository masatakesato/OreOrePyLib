import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from oreorepylib.ui.pyqt5.frame import Frame
from oreorepylib.ui.pyqt5.tabbedmdi import TabWidget, DockableFrame, TabbedMDIManager




def onTabFocusChanged( old: QWidget, new: QWidget, propertyName: str ) -> None:
    #print( '{} -> {}'.format( old, new ) )

    #print( '/---------------- old -----------------------/')
    while( isinstance(old, QWidget) ):
        #print( old )
        if( isinstance( old, QTabWidget ) ):
            old.setProperty( propertyName, False )
            old.setStyle( old.style() )
            tabBar = old.tabBar()
            tabBar.setProperty( propertyName, False )
            tabBar.setStyle( tabBar.style() )
            break
        old = old.parentWidget()

    #print( '/---------------- new -----------------------/')
    while( isinstance(new, QWidget) ):
        #print( new )
        if( isinstance( new, QTabWidget ) ):
            new.setProperty( propertyName, True )
            new.setStyle( new.style() )
            tabBar = new.tabBar()
            tabBar.setProperty( propertyName, True )
            tabBar.setStyle( tabBar.style() )
            break
        new = new.parentWidget()       
    #print( '' )




class MyButton(QScrollArea):

    def __init__( self, parent=None ):
        super(MyButton, self).__init__(parent=parent)

        self.setWidgetResizable( True )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )


        self.setLayout( QVBoxLayout() )

        self.layout().setSpacing(0)
        self.layout().addStretch()


        self.__m_Button = QPushButton('Button')

        self.layout().addWidget( self.__m_Button )




if __name__=='__main__':

    app = QApplication( sys.argv )
    QApplication.setStyle( 'Fusion' )# Required for overriding QTabBartab::paintEvent.

    app.focusChanged.connect( lambda old, new: onTabFocusChanged( old, new, 'TabWidgetFocus' ) )


    # main window
    w = Frame()
    w.setLayout( QVBoxLayout() )

    splitter = QSplitter()
    w.layout().addWidget( splitter)


    # tab frames
    tabFrame1 = TabWidget()
    tabFrame1.setWindowTitle( 'tabFrame1' )
    
    tabFrame2 = TabWidget()
    tabFrame2.setWindowTitle( 'tabFrame2' )


    # attach content widgets to tabFrame1
    widget1 = QWidget()
    widget1.setLayout( QVBoxLayout() )

    widget1.layout().addWidget( QCheckBox( 'CheckBox' ) )
    widget1.layout().addWidget( QTextEdit('test1') )

    tabFrame1.addTab( widget1, '????' )
    tabFrame1.setCurrentIndex(0)


    # attach content widgets to tabFrame2
    widget2 = QWidget()
    widget2.setLayout( QVBoxLayout() )
    widget2.layout().addWidget( MyButton() )
    widget2.layout().addWidget( QSlider( Qt.Horizontal ) )

    tabFrame2.addTab( widget2, '!!!!' )
    tabFrame2.addTab( QWidget(), '<<>><' )
    tabFrame2.setCurrentIndex(0)


    view = QGraphicsView()

    # construct all widgets
    splitter.addWidget( tabFrame1 )
    splitter.addWidget( tabFrame2 )
    splitter.addWidget( view )

    w.show()

    sys.exit( app.exec_() )