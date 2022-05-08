import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



if __name__=='__main__':

    print( "//================= Displaying printscreened image using PyQt ===================//")
    app = QApplication(sys.argv)

    clip = QApplication.clipboard()
    #print( clip )
    qimg = clip.image()

    if( qimg.isNull() ):# クリップボードが画像を保持しているかどうかチェックする
        print( "No clipboard image found. Please printscreen before running this program." )
        sys.exit(0)


    image_frame = QLabel()
    image_frame.setPixmap( QPixmap.fromImage(qimg) )

    frame = QFrame()
    frame.setLayout( QVBoxLayout() )
    frame.layout().addWidget( image_frame )

    frame.show()


    sys.exit(app.exec_())