# https://stackoverflow.com/questions/31455546/qt-removing-stretches-from-a-qhboxlayout

import sys
import functools
import traceback

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



#g_LineEditStyleSheet = """
#QLineEdit
#{
#    color: rgb(235,235,235);
#    background: rgb(42,42,42);
#    selection-background-color: darkgray;
    
#    height: 18px;

#    border-left: 1px solid rgb(32,32,32);
#    border-top: 1px solid rgb(32,32,32);
#    border-right: 1px solid rgb(100,100,100);
#    border-bottom: 1px solid rgb(100,100,100);

#    border-radius: 2px;
#    padding: 0px 2px;
#}

#QLineEdit:disabled
#{
#    color: rgb(118,118,118);
#    background: rgb(42,42,42);
#    selection-background-color: darkgray;
    
#    height: 18px;

#    border-left: 1px solid rgb(32,32,32);
#    border-top: 1px solid rgb(32,32,32);
#    border-right: 1px solid rgb(100,100,100);
#    border-bottom: 1px solid rgb(100,100,100);

#    border-radius: 2px;
#    padding: 0px 2px;
#}

#QLineEdit:focus
#{
#    border: 1px solid darkgray;
#}

#QLineEdit:read-only
#{
#    color: rgb(100,100,100);
#}

#"""


g_ExpandWidgetHeaderStyleSheet = """
QLabel
{
    color: rgb(235, 235, 235);
    background: rgb(80,80,80);

    margin: 0px 0px 0px 0px;
    border: 1px solid rgb(80,80,80);
    padding: 0px 0px 0px 0px;

    border-radius: 2px;
}
"""


g_ExpandWidgetBodyStyleSheet = """
QFrame
{
    background: rgb(64,64,64);

    margin: 0px 0px 0px 0px;
    border: 0px solid rgb(0,0,0);
    padding: 0px 0px 0px 0px;
}
"""


g_ExpandWidgetStyleSheet = """
QFrame
{
    color: rgb(235, 235, 235);
    background: rgb(60,60,60);

    margin: -5px -8px -5px -8px;
    border: 0px solid rgb(0,0,0);
    padding: 0px 0px 0px 0px;
}
"""


g_ScrollAreaWidgetStyleSheet = """
QFrame
{
    background: rgb(60,60,60);

    margin: 0px 0px 0px 0px;
    border: 0px solid rgb(0,0,0);
    padding: 0px 0px 0px 0px;
}

QScrollBar:vertical
{
    /*border: 2px solid green;*/
    color: rgb(196,196,196);
    background: rgb(60,60,60);
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
     background: none;
}

"""




class ExpandWidgetHeader(QLabel):

    headerClicked = pyqtSignal()# bool )

    def __init__( self, caption='', parent=None ):
        super(ExpandWidgetHeader, self).__init__(parent=parent)

        self.setText( caption )
        self.setStyleSheet( g_ExpandWidgetHeaderStyleSheet )
        self.setFixedHeight(20)# self.setGeometry(QRect(0, 0, 330, 25))
        self.setAlignment(Qt.AlignCenter)


    def mousePressEvent( self, event ):
        self.headerClicked.emit()
        



class ExpandWidgetBody(QFrame):

    def __init__(self, parent=None):
        super(ExpandWidgetBody, self).__init__(parent=parent)

        self.setStyleSheet( g_ExpandWidgetBodyStyleSheet )
        self.__m_Layout = QVBoxLayout()
        #self.__m_Layout.setSpacing(10)        
        self.setLayout( self.__m_Layout )


    def AddWidget( self, widget ):
        try:
            self.__m_Layout.insertWidget( self.__m_Layout.count()-1, widget )
        except:
            traceback.print_exc()


    def RemoveWidget( self, widget ):
        try:
            self.__m_Layout.removeWidget( widget )
        except:
            traceback.print_exc()




class ExpandWidget(QFrame):

    def __init__( self, caption='', hidden=False, parent=None ):
        super(ExpandWidget, self).__init__(parent=parent)

        self.setStyleSheet( g_ExpandWidgetStyleSheet )
        self.__m_Header = ExpandWidgetHeader( caption )
        self.__m_Body = ExpandWidgetBody()
        self.__m_Hidden = hidden
        
        layout = QVBoxLayout()
        self.setLayout( layout )

        layout.setSpacing(2)
        layout.addWidget( self.__m_Header )
        layout.addWidget( self.__m_Body )

        self.__m_Header.headerClicked.connect( self.SwitchBodyVisibility )
        

    def Body( self ):
        return self.__m_Body


    def SetExpand( self, flag ):
        self.__m_Hidden = flag
        if( self.__m_Hidden==True ):
            self.__m_Body.hide()
        else:
            self.__m_Body.show()


    def SwitchBodyVisibility( self ):
        self.__m_Hidden = not self.__m_Hidden
        if( self.__m_Hidden==True ):
            self.__m_Body.hide()
        else:
            self.__m_Body.show()


    def AddWidget( self, widget ):
        self.__m_Body.AddWidget( widget )


    def RemoveWidget( self, widget ):
        self.__m_Body.RemoveWidget( widget )



    # QWidgetクラス継承したカスタムウィジェットの場合は、以下paintEventオーバーライドでスタイルシート有効化できる
    #def paintEvent( self, event ):
    #    StyleOpt = QStyleOption()
    #    StyleOpt.initFrom(self)
    #    painter = QPainter(self)
        
    #    self.style().drawPrimitive(QStyle.PE_Widget, StyleOpt, painter, self)







class ScrollAreaWidget(QScrollArea):

    def __init__( self, *args, **kwargs ):
        super(ScrollAreaWidget, self).__init__(*args, **kwargs)

        self.setStyleSheet( g_ScrollAreaWidgetStyleSheet )

        self.setWidgetResizable( True )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

        self.__m_InnerLayout = QVBoxLayout()
        self.__m_InnerLayout.setSpacing(0)
        self.__m_InnerLayout.addStretch()

        self.__m_InnerWidget = QFrame()
        self.__m_InnerWidget.setLayout( self.__m_InnerLayout )

        self.setWidget( self.__m_InnerWidget )


    def AddWidget( self, widget ):
        try:
            self.__m_InnerLayout.insertWidget( self.__m_InnerLayout.count()-1, widget )
        except:
            traceback.print_exc()


    def RemoveWidget( self, widget ):
        try:
            self.__m_InnerLayout.removeWidget( widget )
        except:
            traceback.print_exc()




if __name__=='__main__':

    app = QApplication( sys.argv )
    
    areawidget = ScrollAreaWidget()

    for i in range(0, 4):
        label = '------------- Group' + str(i) + '------------'
        collapsibleWidget = ExpandWidget( label )
        collapsibleWidget.AddWidget( QPushButton('Button') )
        collapsibleWidget.AddWidget( QLineEdit() )

        areawidget.AddWidget( collapsibleWidget )
        if( i%2==0 ): collapsibleWidget.SetExpand(False)
    

    mainlayout = QVBoxLayout()
    mainlayout.addWidget( QPushButton('Button') )
    mainlayout.addWidget( QLineEdit('LineEdit') )
    mainlayout.addWidget( areawidget )

    mainWidget = QFrame()
    mainWidget.setLayout( mainlayout )
    mainWidget.setGeometry( 300, 300, 500, 600 )
    



    mainWidget.show()

    sys.exit( app.exec_() )




######################### QScrollAreaのサンプルコード #######################

# http://nealbuerger.com/2013/11/pyside-qvboxlayout-with-qscrollarea/
# https://stackoverflow.com/questions/18223031/prevent-widgets-stretching-in-qvboxlayout-and-have-scrollbar-appear-in-qscrollar
# https://stackoverflow.com/questions/28818323/qscrollarea-not-working-as-expected-with-qwidget-and-qvboxlayout


#if __name__=='__main__':

#    app = QApplication( sys.argv )

#    mainWidget = QFrame()
#    mainWidget.setGeometry( 100, 100, 260, 260 )

#    scrollArea = QScrollArea()
#    scrollArea.setWidgetResizable( True )
#    scrollArea.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )
#    scrollArea.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
#    scrollArea.setGeometry( 10, 10, 240, 240 )
#    scrollArea.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

#    mainlayout = QVBoxLayout()
#    mainWidget.setLayout( mainlayout )
#    mainlayout.addWidget( scrollArea )

#    innerwidget = QWidget()
#    scrollArea.setWidget( innerwidget )

#    innerlayout = QVBoxLayout()
#    innerwidget.setLayout( innerlayout )

#    for i in range(10):
#        button = QPushButton( str(i) )
#        innerlayout.addWidget( button )

#    innerlayout.addStretch()

#    mainWidget.show()

#    sys.exit( app.exec_() )

##################################################################################