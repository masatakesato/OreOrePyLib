import sys
import time

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *




class QThread1( QThread ):

    sig1 = pyqtSignal(str)
    sig_quit = pyqtSignal()#

    def __init__(self, parent=None):
        QThread.__init__(self, parent)


    def on_source(self, lineftxt):
        self.source_txt = lineftxt


    def run(self):
        self.running = True
        #while self.running:
        for i in range(10):
            #if self.running is True:
            self.sig1.emit( '%d' % i )
            time.sleep(0.01)

        self.sig_quit.emit()





# https://stackoverflow.com/questions/9075837/pause-and-resume-a-qthread

#class QWorkerThread( QThread ):

#    procSignal = pyqtSignal(tuple, dict)


#    def __init__( self, parent=None ):
#        super(Qworker, self).__init__(parent=parent)

#        self.pause = False
#        self.pauseCond = QWaitCondition()
#        self.sync = QMutex()



#    def resume( self ):

#        self.sync.lock()
#        self.pause = False
#        self.sync.unlock()
#        self.pauseCond.wakeAll()



#    def pause( self ):
#        self.sync.lock()
#        self.pause = True
#        self.sync.unlock()



#    def end( self ):
#        self.requestInterruption()



#    def run( self ):

#        while( True ):
#            # wait while paused
#            self.sync.lock()
#            if( self.pause ):   self.pauseCond.wait(self.sync)
#            self.sync.unlock()

#            # teriminate if interrupted
#            if( self.isInterruptionRequested() ): break

#            # do the job
#            self.procSignal.emit()

#            self.usleep(1)





class MyWorker( QObject ):

    procedure = pyqtSignal(object)
    finished = pyqtSignal()

    @pyqtSlot()
    def process( self ):
        for i in range(1000):
            self.procedure.emit( str(i) )
            time.sleep(0.1)

        self.finished.emit()




class Widget():

    sig = pyqtSignal()

    def __init__(self):
        self.widget = QWidget()
        self.widget.setLayout( QHBoxLayout() )
        
        self.texedit = QTextEdit()
        self.button = QPushButton('button')

        self.texedit.setStyleSheet( 'background-color: rgb(128, 128, 128);' )
        self.texedit.setMinimumSize( 100, 100 )

        self.widget.layout().addWidget( self.texedit )
        self.widget.layout().addWidget( self.button )


        self.button.clicked.connect( self.on_button )

        
        #self.__m_thread = QThread1()
        #self.__m_thread.sig1.connect( self.update_label )
        #self.__m_thread.sig_quit.connect( self.unlock_button )



        self.__m_thread = QThread()

        self.worker = MyWorker()
        self.worker.moveToThread( self.__m_thread )

        self.worker.procedure.connect( self.update_label )
        self.worker.finished.connect( self.__m_thread.quit )
        self.worker.finished.connect( self.unlock_button )

        self.__m_thread.started.connect( self.worker.process )



    def show( self ):
        self.widget.show()


    def on_button( self ):
        self.button.setEnabled(False)
        self.__m_thread.start()


        
    def unlock_button( self ):
        #self.__m_thread.running = False
        self.button.setEnabled(True)


    def update_label( self, string ):
        self.texedit.append( string )

        



if __name__=='__main__':

    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())