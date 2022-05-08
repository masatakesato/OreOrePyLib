import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from window import Window


if __name__=='__main__':

    #app = QApplication(sys.argv)

    #scene = QGraphicsScene()
    #window = Window()
    #scene.addItem(window)
    #view = QGraphicsView(scene)
    #view.resize(600, 600)
    #view.show()

    #


# http://www.qtcentre.org/threads/56749-QGraphicsViews-how-to-arrange-items-using-QGraphicsLinearLayout-(or-other-layout)
    a = QApplication(sys.argv)
    view = QGraphicsView()
    scene = QGraphicsScene()
    widget = QGraphicsWidget()
    layout =  QGraphicsLinearLayout(Qt.Vertical)
 
    for i in range(10):
        label = QLabel()
        pix = QPixmap("./images/block.png")
        label.setPixmap( pix )
        label.setGeometry(0, i*pix.height() + 10, pix.width(), pix.height())
        w = scene.addWidget(label)
        layout.addItem(w)

 
    widget.setLayout(layout)
    scene.addItem(widget)
    view.setScene(scene)
    view.show()
 
    sys.exit(a.exec_())
