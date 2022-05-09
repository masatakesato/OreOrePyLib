# https://stackoverflow.com/questions/21071448/redirecting-stdout-and-stderr-to-a-pyqt4-qtextedit-from-a-secondary-thread

from oreorepylib.utils import environment

import sys
from queue import Queue
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream(object):
    def __init__(self,queue):
        self.queue = queue


    def write(self, text):
        self.queue.put(text)


    def flush( self ):
        pass


# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal 
class MyReceiver(QObject):
    mysignal = pyqtSignal(str)

    def __init__(self,queue,*args,**kwargs):
        QObject.__init__(self,*args,**kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)
            


# An example QObject (to be run in a QThread) which outputs information with print
class MyWorker(QObject):
    @pyqtSlot()
    def run(self):
        for i in range(1000):
            print( i )
            time.sleep(0.001)


# An Example application QWidget containing the textedit to redirect stdout to
class MyApp(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)

        self.layout = QVBoxLayout(self)
        self.textedit = QTextEdit()
        self.button = QPushButton('start long running thread')
        self.button.clicked.connect(self.start_thread)
        self.layout.addWidget(self.textedit)
        self.layout.addWidget(self.button)

    @pyqtSlot(str)
    def append_text(self,text):
        self.textedit.moveCursor(QTextCursor.End)
        self.textedit.insertPlainText( text )

    @pyqtSlot()
    def start_thread(self):
        self.thread = QThread()
        self.worker = MyWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect( self.worker.run )
        self.thread.start()



# Create Queue and redirect sys.stdout to this queue
queue = Queue()
sys.stdout = WriteStream(queue)

# Create QApplication and QWidget
qapp = QApplication(sys.argv)  
app = MyApp()
app.show()

# Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
thread = QThread()
my_receiver = MyReceiver(queue)
my_receiver.mysignal.connect(app.append_text)
my_receiver.moveToThread(thread)
thread.started.connect(my_receiver.run)
thread.start()

qapp.exec_()