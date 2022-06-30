from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class ExternalAppWidget( QWidget ):

    def __init__( self, parent=None ):
        super( ExternalAppWidget, self ).__init__( parent=parent )

        self.setLayout( QVBoxLayout() ) 
        self.layout().setContentsMargins( 0, 0, 0, 0 )

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

