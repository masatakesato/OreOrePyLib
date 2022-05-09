import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from oreorepylib.ui.pyqt5.frame import Frame
from oreorepylib.ui.pyqt5.tabbedmdi import Duration, TabWidget, DockableFrame, TabbedMDIManager



def onTabFocusChanged( old: QWidget, new: QWidget, propertyName: str ) -> None:
    #print( '{} -> {}'.format( old, new ) )
    
    #print( '/---------------- old -----------------------/')
    while( old ):#isinstance(old, QWidget) ):
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
    while( new ):#isinstance(new, QWidget) ):
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

    #================= Create TabbedMDIManager instance ====================#
    tmdiManager = TabbedMDIManager()


    #=========== Create DockableFrame and register =============#
    frame_id = tmdiManager.AddDockable( DockableFrame )

    edit1 = QTextEdit( 'Text1' )
    edit1.setWindowTitle( 'Tab1' )

    edit2 = QTextEdit( 'Text2' )
    edit2.setWindowTitle( 'Tab2' )

    edit3 = QTextEdit( 'Text3' )
    edit3.setWindowTitle( 'Tab3' )
        
    edit4 = QWidget( )#QTextEdit( 'Text4' )
    edit4.setWindowTitle( 'Tab4' )


    edit4.setLayout( QVBoxLayout() )
    edit4.layout().addWidget( MyButton() )#QPushButton('Button'))
    edit4.layout().addWidget( QSlider() )


    tmdiManager.AddTab( frame_id, edit1, edit1.windowTitle(), id(edit1) )
    tmdiManager.AddTab( frame_id, edit2, edit2.windowTitle(), id(edit2) )
    tmdiManager.AddTab( frame_id, edit3, edit3.windowTitle(), id(edit3) )
    tmdiManager.AddTab( frame_id, edit4, edit4.windowTitle(), id(edit4) )

    tmdiManager.Info()

    #=========== Create DockableFrame and register =============#
    frame2_id = tmdiManager.AddDockable( DockableFrame, Duration.Persistent )

    edit5 = QTextEdit( 'Text5' )
    edit5.setWindowTitle( 'Tab5' )

    tmdiManager.AddTab( frame2_id, edit5, edit5.windowTitle(), id(edit5) )
    
    tmdiManager.Info()

    #=========== Create TabWidget and register =============#
    tabWidget_id = tmdiManager.AddDockable( TabWidget, Duration.Volatile )

    edit6 = QTextEdit( 'Text6' )
    edit6.setWindowTitle( 'Tab6' )

    edit7 = QTextEdit( 'Text7' )
    edit7.setWindowTitle( 'Tab7' )

    tmdiManager.AddTab( tabWidget_id, edit7, edit7.windowTitle(), id(edit7) )
    tmdiManager.AddTab( tabWidget_id, edit6, edit6.windowTitle(), id(edit6) )

    tmdiManager.Info()

    widget_ = tmdiManager.DetachTab( id(edit7)  )
    widget_.show()
    tmdiManager.Info()
    print( widget_.windowTitle() )

    #widget_ = tmdiManager.DetachTab( id(edit6)  )
    #widget_.show()
    #tmdiManager.Info()

    #============ Insert QGraphicsView after edit5 ============#
    view = QGraphicsView()
    view.setWindowTitle( 'GraphicsView' )

    dockable_id, _ = tmdiManager.FindParentDockable( id(edit5) )
    
    tmdiManager.AddTab( dockable_id, view, view.windowTitle(), id(view) )

    tmdiManager.Info()

    #============ Insert QGraphicsView at edit6 index position ============#
    view2 = QGraphicsView()
    view2.setWindowTitle( 'GraphicsView2' )

    dockable_id, index = tmdiManager.FindParentDockable( id(edit6) )

    tmdiManager.InsertTab( dockable_id, index, view2, view2.windowTitle(), id(view2) )

    tmdiManager.SetTabClosable( dockable_id, index, False )
    tmdiManager.SetTabDetachable( dockable_id, index, False )

    tmdiManager.Info()



    tmdiManager.Activate( frame2_id, 0 )

    tmdiManager.Show()


    tmdiManager.Activate( dockable_id, 0 )

    tmdiManager.SetTabTitle( id(edit4), 'BBMIGDS' )

    tmdiManager.Info()

    #tmdiManager.Clear()
    #tmdiManager.Info()

    #tmdiManager.Release()

    sys.exit( app.exec_() )
