from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class CanvasFrame( QFrame ):

    def __init__(self, parent=None):
        super(CanvasFrame, self).__init__(parent=parent)
        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins( 0, 0, 0, 0 )

        self.__m_refBackground = None   # Background QWidget 
        self.__m_refOverlay = None      # Overlay QGraphicsView


    def resizeEvent( self, event ):
        print( "CanvasFrame::resizeEvent()..." )
        r = self.rect()#self.layout().contentsRect()#
        gpos = self.mapToGlobal(r.topLeft())

        if( self.__m_refOverlay ):
            self.__m_refOverlay.setGeometry( gpos.x(), gpos.y(), r.width(), r.height() )#w.resize( r.width(), r.height() )# event.size() )#
        #for w in self.nonlayoutwidgets:
        #    w.setGeometry( gpos.x(), gpos.y(), r.width(), r.height() )#w.resize( r.width(), r.height() )# event.size() )#
        #    print( "resizing: ", w.geometry() )
        event.accept()


    def BindBackground( self, widget: "QWidget" ):

        self.UnbindBackground()

        self.layout().addWidget( widget )
        self.__m_refBackground = widget


    def UnbindBackground( self ):
        if( self.__m_refBackground ):
            self.__m_refBackground.setParent( None )
            self.__m_refBackground = None


    def BindOverlay( self, view: "QGraphicsView" ):

        self.UnbindOverlay()

        self.__m_refOverlay = view
        self.__m_refOverlay.setParent( self )        
        self.__m_refOverlay.setAttribute( Qt.WA_NoSystemBackground )# バックグラウンドなし
        self.__m_refOverlay.setAttribute( Qt.WA_TranslucentBackground )# ビューの背景を完全透明化する
        self.__m_refOverlay.setWindowFlags( Qt.Tool | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus )# 枠なしカバーウィンドウにする. Qt.WindowStaysOnTopHint: 全画面上で常に最前面にView表示させるフラグ.これは外す
        # プラットフォーム依存のQt.CoverWindowの代わりにQt.Toolを使っている


    def UnbindOverlay( self ):
        if( self.__m_refOverlay ):
            self.__m_refOverlay.setParent( None )
            self.__m_refOverlay = None


    def SetupOverlayMoveEvent( self ):
        # Find top level widget
        top_widget = self
        while( top_widget.parentWidget() ):
            top_widget = top_widget.parentWidget()
        # install event filter for moveEvent
        if( top_widget ):
            print( "installing event filter...", top_widget )
            top_widget.installEventFilter( self )



    def mousePressEvent( self, event ):
        print( "CanvasFrame::mousePressEvent" )
        return super(CanvasFrame, self).mousePressEvent( event )

    
    def eventFilter( self, obj: "QObject", event: "QEvent" ) -> bool:

        if( event.type() == QEvent.Move and self.__m_refOverlay ):
            gpos = self.mapToGlobal( self.rect().topLeft() )
            self.__m_refOverlay.move( gpos )
            #for w in self.nonlayoutwidgets:
            #    w.move( gpos )

        return super(CanvasFrame, self).eventFilter(obj, event)
