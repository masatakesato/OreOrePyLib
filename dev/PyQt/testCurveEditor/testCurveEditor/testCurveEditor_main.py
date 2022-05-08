import sys

from oreorepylib.utils import environment

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

#from qtwidget import CurveEditorView
from CurveEditorWidget import CurveEditorWidget


if __name__ == "__main__":

    app = QApplication(sys.argv)

    widget = CurveEditorWidget()
    
    screen = QApplication.desktop().screenGeometry()
    widget.move( screen.center() - widget.rect().center() )
    widget.setWindowTitle( 'Curve editor v0.0.1' )
    widget.show()


    sys.exit(app.exec_())
