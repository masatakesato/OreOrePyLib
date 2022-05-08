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

    frame = Frame()
    frame.setLayout( QVBoxLayout() )

    # Manually set client area size.
    #w = 320 + frame.contentsMargins().left() + frame.contentsMargins().right()
    #h = 240 + frame.contentsMargins().top() + frame.contentsMargins().bottom() + frame.m_titleBar.height()
    #frame.resize( w, h )

    # Set client area size using wrapped methods( equivalent to manual resize ).
    #frame.Resize( 320, 240 )# OK
    frame.Resize_( QSize( 320, 240 ) )# OK

    w = QWidget()
    w.setStyleSheet( 'background-color: rgb(10,255,10);' )
    #w.setMinimumSize( 400, 300 )

    frame.layout().addWidget( w )
    frame.layout().setContentsMargins(0,0,0,0)

    frame.show()

    #w.resize(500,541)# OK
    #w.setGeometry( 100, 100, 300, 400)# OK
    #w.setFixedSize(1250, 250)# OK
    #w.setMinimumSize(1250, 250)# OK
    #w.setMaximumSize(1250, 250)# OK

    #frame.resize(500,541)# OK
    #frame.setGeometry( 100, 100, 300, 400)# OK
    #frame.setFixedSize(250, 250)# OK
    #frame.setMinimumSize(250, 250)# OK

    app.exec_()