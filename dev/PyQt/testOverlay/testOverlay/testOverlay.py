import sys
import traceback

from oreorepylib.utils import environment

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class Overlay(QWidget):

    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)

        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins(0, 0, 0, 0)

        movie = QMovie('./test.gif')
        movie.start()
        movie.setPaused(True)
        self.label = QLabel( self)
        self.label.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
        self.label.setStyleSheet( 'background-color: rgba(118,118,0,127);' )
        self.label.setMovie( movie )
        
        self.layout().addWidget( self.label )


    def show(self):
        self.label.movie().setPaused(False)
        return super(Overlay, self).show()


    def hide(self):
        self.label.movie().setPaused(True)
        return super(Overlay, self).hide()


    #def resize(self, w, h):
    #    return super(Overlay, self).resize(w, h)


    #def resize(self, size):
    #    return super(Overlay, self).resize(size)



    def mousePressEvent( self, event ):
        print( "Overlay::mousePressEvent" )
        return super(Overlay, self).mousePressEvent( event )




class MyFrame(QFrame):

    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent=parent)
        self.nonlayoutwidgets = []


    def resizeEvent(self, event):
        for w in self.nonlayoutwidgets:
            w.resize(event.size())
        event.accept()


    def addChildWidget(self, w):
        w.setParent(self)
        self.nonlayoutwidgets.append(w)


    def mousePressEvent( self, event ):
        print( "MyFrame::mousePressEvent" )
        return super(MyFrame, self).mousePressEvent( event )




class windowOverlay(QWidget):
    def __init__(self, parent=None):
        super(windowOverlay, self).__init__(parent)

        self.editor = MyFrame()
        #self.editor.setMinimumSize( 500, 500 )
        self.editor.setStyleSheet('background-color: rgb(130,130,130);')
        
        self.editor.setLayout( QGridLayout() )

        for i in range(3):
            for j in range(4):
                w = QWidget()
                w.setFixedSize(50, 50)
                w.setStyleSheet('background-color: rgb(30,30,30);')
                #self.editor.layout().addWidget(w)
                self.editor.layout().addWidget(w, i,j)

        self.button = QPushButton("Toggle Overlay")
        self.button.setFixedHeight(200)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.editor)
        self.verticalLayout.addWidget(self.button)

        self.Overlay = Overlay()
        self.Overlay.hide()

        self.editor.addChildWidget( self.Overlay )# set parent widget without applying layout


        #self.button.clicked.connect( lambda: self.Overlay.hide() if self.Overlay.isVisible() else self.Overlay.show() )
        self.button.clicked.connect( lambda: self.button_off() if self.Overlay.isVisible() else self.button_on() )
        


    def button_on( self ):
        self.Overlay.show()
        for i in range(3):
            for j in range(4):
                w = QWidget()
                w.setFixedSize(50, 50)
                w.setStyleSheet('background-color: rgb(30,30,30);')
                #self.editor.layout().addWidget(w)
                self.editor.layout().addWidget(w, i,j)
                w.lower()
        #self.Overlay.raise_()

        #self.Overlay.activateWindow()

    def button_off( self ):
        self.Overlay.hide()
        



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main = windowOverlay()
    main.show()
    sys.exit(app.exec_())