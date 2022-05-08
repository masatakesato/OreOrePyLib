from oreorepylib.utils import environment

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from oreorepylib.ui.pyqt5.flowlayout import *



#class Container(QWidget):
#    def __init__(self):
#        super().__init__()
#        self.setLayout(QVBoxLayout())
#        self._widgets = []

#    def sizeHint(self):
#        w = self.size().width()
#        h = 0
#        for widget in self._widgets:
#            h += widget.layout().heightForWidth(w)

#        sh = super().sizeHint()
#        print(sh)
#        print(w, h)
#        return sh

#    def add_widget(self, widget):
#        self._widgets.append(widget)
#        self.layout().addWidget(widget)

#    def add_stretch(self):
#        self.layout().addStretch()



#if __name__ == '__main__':

#    app = QApplication(sys.argv)  # pylint: disable=invalid-name
#    container = QWidget()#Container()
#    container.setLayout( QVBoxLayout() )

#    for i in range(2):
#        w = QWidget()
#        w.setWindowTitle( 'Flow Layout' )
#        l = FlowLayout(w, 10)
#        l.heightChanged.connect(container.setMinimumHeight)
#        w.setLayout(l)
#        for j in range(5):
#            l.addWidget(QPushButton('Short'))
#            l.addWidget(QPushButton('Longer'))
#            l.addWidget(QPushButton('Different text'))
#            l.addWidget(QPushButton('More text'))
#            l.addWidget(QPushButton('Even longer button text'))
        
#        container.layout().addWidget(w)
#        #container.add_widget(w)
#    container.layout().addStretch()
#    #container.add_stretch()
    

#    sa = ScrollArea()#QScrollArea()
#    sa.setWidgetResizable(True)
#    sa.setWidget(container)
#    sa.show()

#    sys.exit(app.exec_())





#g_numItems = 500
g_batchSize = 25

g_ItemStrings = [ str(i) for i in range(100) ]



g_FlowLayoutFrame = None
g_ShowMoreButton = None


import time

def AddItems():

    g_ShowMoreButton.setParent(None)

    g_FlowLayoutFrame.parent().setEnabled(False)

    for i in range( g_batchSize ):
        button = QFrame()
        button.setFixedSize( 50, 50 )
        #button.setGeometry(0, 0, 50, 50)
        button.setStyleSheet( 'background-color: grey;' )
        button.setObjectName(str(i))

        g_FlowLayoutFrame.layout().addWidget( button )

    g_FlowLayoutFrame.layout().addWidget( g_ShowMoreButton )

    g_FlowLayoutFrame.parent().setEnabled(True)




if __name__ == '__main__':

    app = QApplication(sys.argv)  # pylint: disable=invalid-name

    g_ShowMoreButton = QPushButton( '...' )
    g_ShowMoreButton.setFixedSize( 50, 50 )
    font = g_ShowMoreButton.font()
    font.setPointSize(24)
    g_ShowMoreButton.setFont(font)


    g_ShowMoreButton.clicked.connect( AddItems )

    g_FlowLayoutFrame = QFrame()
    g_FlowLayoutFrame.setWindowTitle( 'Flow Layout' )
    g_FlowLayoutFrame.setGeometry( 100, 100, 500, 500)  
    g_FlowLayoutFrame.setLayout( FlowLayout(g_FlowLayoutFrame, 10) )
    g_FlowLayoutFrame.layout().addWidget( g_ShowMoreButton )


    scrollarea = ScrollArea()
    scrollarea.setGeometry( 100, 100, 500, 500)
    scrollarea.signal_v.connect( AddItems )
    scrollarea.setWidgetResizable(True)
    scrollarea.setWidget( g_FlowLayoutFrame )
    
    scrollarea.show()

   
    sys.exit(app.exec_())