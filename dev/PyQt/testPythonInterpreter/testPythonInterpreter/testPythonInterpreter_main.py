import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from oreorepylib.ui.pyqt5.pythoninterpreter import InputConsole, OutputConsole


import time


def testPrint():

    for i in range(1000):
        print( i )
        time.sleep(0.1)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    inconsole = InputConsole()# locals()
    inconsole.setWindowTitle( 'Input Console' )
    inconsole.setGeometry( 200, 200, 500, 300 )

    outconsole = OutputConsole()
    outconsole.setWindowTitle( 'Output Console' )
    outconsole.setGeometry( 750, 200, 500, 300 )

    inconsole.show()
    outconsole.show()

    #from threading import Thread

    #thread = Thread( target=testPrint )
    #thread.start()



    sys.exit(app.exec_())