from oreorepylib.utils import environment

import sys
import time

from oreorepylib.ui.pyqt5.flowlayout import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


#g_numItems = 500
g_batchSize = 25



class QThread1( QThread ):

    sig1 = pyqtSignal(str)
    sig_quit = pyqtSignal()#

    def __init__(self, parent=None):
        QThread.__init__(self, parent)


    def BindSource( self, data ):
        self.source_txt = data


    def run( self ):
        self.running = True
        for i in range(g_batchSize):#data:
            self.sig1.emit( '%d' % i )
            time.sleep(0.25)

        self.sig_quit.emit()








g_ItemStrings = [ str(i) for i in range(100) ]




class Widget():

    sig = pyqtSignal()

    def __init__(self):
        self.widget = QWidget()
        self.widget.setWindowTitle( 'Flow Layout' )
        self.widget.setGeometry( 100, 100, 500, 500)  
        self.widget.setLayout( FlowLayout(mergin=10) )        

        self.button = QPushButton( '...' )
        self.button.setFixedSize( 50, 50 )
        font = self.button.font()
        font.setPointSize(24)
        self.button.setFont(font)
        self.button.clicked.connect( self.on_button )

        self.scrollarea = ScrollArea()
        self.scrollarea.setWidgetResizable( True )
        self.scrollarea.setWidget( self.widget )
        self.scrollarea.signal_v.connect( self.on_button )# connect mouse viertical wheel signal

        #self.texedit = QTextEdit()
        #self.button = QPushButton('button')

        


    def show( self ):
        self.scrollarea.show()


    def on_button( self ):
        self.button.setParent(None)

        self.__m_thread = QThread1()
        self.__m_thread.sig1.connect( self.update_flowlayout )
        self.__m_thread.sig_quit.connect( self.unlock_flowlayout )

        self.__m_thread.start()
        self.scrollarea.setEnabled( False )#self.button.setEnabled(False)

        
    def unlock_flowlayout( self ):
        self.__m_thread.running = False
        self.widget.layout().addWidget( self.button )
        self.scrollarea.setEnabled( True )#self.button.setEnabled(True)
        


    def update_flowlayout( self, string ):

        frame = QFrame()
        frame.setFixedSize( 50, 50 )
        #frame.setGeometry(0, 0, 50, 50)
        frame.setStyleSheet( 'background-color: grey;' )
        frame.setObjectName( string )
        
        
        self.widget.layout().addWidget( frame )


        #self.texedit.append( string )



if __name__ == '__main__':

    print( "Wheel down to extend scroll area..." )

    app = QApplication(sys.argv)  # pylint: disable=invalid-name

    widget = Widget()
    widget.show()
   
    sys.exit(app.exec_())