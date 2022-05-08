# https://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window-of-desktop-application

import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from oreorepylib.ui.pyqt5.frame import Frame
from oreorepylib.ui.pyqt5.mainwindow import MainWindow



if __name__ == '__main__':

    app = QApplication( sys.argv )


#    #================== MainWindow test ======================#
#    window = MainWindow()
#    #window = QMainWindow()

#    print( window.centralWidget() )

#    window.setMenuBar( QMenuBar() )

#    menubar = window.menuBar()

#    menu = menubar.addMenu( 'File' )

#    action = QAction( 'Open', window )
#    action.setStatusTip( 'Open...' )
#    menu.addAction( action )
#    #menu.addAction( 'Open' )
    
#    edit = QLabel( """I would've did anything for you to show you how much I adored you
##But it's over now, it's too late to save our loveJust promise me you'll think of me
##Every time you look up in the sky and see a star 'cuz I'm  your star.""" )

#    edit.setStyleSheet( 'border: 0px none;background-color:rgb(128,0,0);')

#    layout = QVBoxLayout()
#    layout.setContentsMargins( 0, 0, 0, 0 )
#    layout.addWidget( edit )

#    window.setCentralWidget( edit )
#    #window.centralWidget().setLayout( layout )


#    window.setStatusBar( QStatusBar() )


#    window.show()


    #================== Frame/QFrame compatibility test ======================#
    frame = Frame()
    #frame = QFrame()

    print( frame.layout() )# None

    frame.show()
    #frame.resize(500,541)# OK
    #frame.setGeometry( 100, 100, 300, 400)# OK
    #frame.setFixedSize(250, 250)# OK
    frame.setMinimumSize(250, 250)# OK

    

    ##================== MainWindow/QMainWindow compatibility test ======================#
    #window = MainWindow()
    ##window = QMainWindow()

    #button = QPushButton('gdsa')
    #button.setStyleSheet( 'background-color: rgb(127,0,0);')

    #print( window.centralWidget() )# None

    ##window.setCentralWidget( button  )
    ##window.layout().addWidget( QPushButton('aaa') )
    ##window.layout().addWidget( QWidget() )

    #window.show()



    app.exec_()