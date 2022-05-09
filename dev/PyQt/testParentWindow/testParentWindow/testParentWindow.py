import sys

from oreorepylib.utils import environment

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *





class ChildWindow(QWidget):
    """"""

    myClosedSignal = pyqtSignal()

    def __init__(self):
        super(ChildWindow, self).__init__()

        self.initUI()

    def initUI(self):

        # set up this window
        self.setGeometry(100,100,200,100)
        self.setWindowTitle("Child Window")
        # button
        acButton = QPushButton('A Child Button', self)
        acButton.clicked.connect(self.onButton)
        acButton.move(10, 10)
        #
        #self.show()


    #----------------------------------------------------------------------
    def onButton(self):
        print( "ChildWindow::onButton" )


    def closeEvent(self, event):
        print( "ChildWindow::closeEvent" )

        self.myClosedSignal.emit()

        super(ChildWindow, self).closeEvent(event)




class ParentWindow(QMainWindow):

    def __init__(self):
        super(ParentWindow, self).__init__()
        self.initUI()
        # self.childWindow = ChildWindow()
        self.childWindow = None


    def initUI(self):
        # set up parent window
        self.setGeometry(850,100,200,100)
        self.setWindowTitle("Parent Window")
        # button
        aButton = QPushButton('A Button', self)
        aButton.clicked.connect(self.onButton)
        aButton.move(10, 10)
        #
        self.show()


    def closeEvent(self, event ):
        print( "ParentWindow::closeEvent" )
        if( self.childWindow ):
            self.childWindow.hide()
            del self.childWindow
            self.childWindow = None
        pass


    def mySlot( self ):
        print( "ParentWindow::mySlot" )


   #----------------------------------------------------------------------
    def onButton(self):
        print( "ParentWindow::onButton" )
        if( self.childWindow==None ):
            self.childWindow = ChildWindow()
            self.childWindow.myClosedSignal.connect(self.mySlot)

        self.childWindow.show()

        #self.childWindow = ChildWindow(self)







if __name__ == '__main__':

    app = QApplication(sys.argv)

    form = ParentWindow()

    sys.exit(app.exec_())


