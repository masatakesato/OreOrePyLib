import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#import oreorelib.ui.pyqt5.frame.TitleButton as TitleButton_
from oreorepylib.ui.pyqt5.frame import Frame, TitleButton



def buttonPressed():
    print( 'Button Pressed.' )



if __name__=='__main__':

    app = QApplication( sys.argv )

    w = Frame()
    w.setLayout( QVBoxLayout() )
    w.resize( 300, 300 )

    for i in range(10):
        button = TitleButton()
        button.SetStyleProperty('icon', 'close' )
        button.clicked.connect( buttonPressed )
        w.layout().addWidget( button )

    w.show()

    sys.exit( app.exec_() )