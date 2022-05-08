# https://stackoverflow.com/questions/11426335/qthread-execution-freezes-my-gui

#https://gist.github.com/WEBMAMOFFICE/fea8e52c8105453628c0c2c648fe618f

import sys
import functools
import threading
import time


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 


from oreorelib.ui.pyqt5 import ThreadIter



#class QThread1(QThread):

#    sig1 = pyqtSignal(str, int, int)

#    def __init__(self, parent=None):
#        QThread.__init__(self, parent)



#    def on_source(self, lineftxt):
#        self.source_txt = lineftxt



#    def run(self):
#        self.running = True
#        while self.running:
#            try:
#                for i in range(10):
#                    if self.running is True:
#                        self.sig1.emit(self.source_txt, i, 10)
#                        time.sleep(0.25)
#            except Exception as err:
#                self.sig1.emit(str(err), 0, 1)
#        self.running = False




class QthreadApp(QWidget):

    sig = pyqtSignal()

    def __init__(self, parent=None):
        super(QthreadApp, self).__init__(parent)
        
        self.linef = QLineEdit(self)
        self.linef.setPlaceholderText("Connect to www.example.com")

        self.textf = QTextEdit(self)
        self.textf.setPlaceholderText("Results...")

        self.but1 = QPushButton(self)
        self.but1.setText( 'play' )
        self.but1.setFixedWidth(72)

        self.but1_async = QPushButton(self)
        self.but1_async.setText( 'play_async' )
        self.but1_async.setFixedWidth(72)

        self.but2 = QPushButton(self)
        self.but2.setText( 'stop' )
        self.but2.setFixedWidth(72)

        self.but2_async = QPushButton(self)
        self.but2_async.setText( 'stop_async' )
        self.but2_async.setFixedWidth(72)

        self.grid1 = QGridLayout()
        self.grid1.addWidget(self.linef, 0, 0, 1, 12)
        self.grid1.addWidget(self.but1, 0, 12, 1, 1)
        self.grid1.addWidget(self.but2, 0, 13, 1, 1)

        self.grid1.addWidget(self.but1_async, 0, 14, 1, 1)
        self.grid1.addWidget(self.but2_async, 0, 15, 1, 1)
        self.grid1.addWidget(self.textf, 1, 0, 13, 14)

        self.setLayout(self.grid1)
        self.but1.clicked.connect( functools.partial( self.play ) )
        self.but2.clicked.connect( functools.partial( self.stop ) )
        self.but1_async.clicked.connect( functools.partial( self.play_async ) )
        self.but2_async.clicked.connect( functools.partial( self.stop_async ) )



        self.__m_Count = 500


        self.sig.connect( self.update_textfield )



    # playボタンクリック時にキックされるメソッド
    def play( self ):
        self.textf.clear()

        #self.thread1 = QThread1()
        #self.thread1.on_source( self.linef.text() )
        #self.thread1.sig1.connect( self.update_textfield )
        #self.thread1.start()# Qthread::start()はスレッド生成してQthread::run()呼び出すまで自動でやってくれる.

        self.th2 = ThreadIter()
        self.th2.AddSignal( self.sig, self.__m_Count )
        self.th2.run()
        #self.th2.wait()
        self.but1.setEnabled(False)


    # stopボタンクリック時にキックされるメソッド
    def stop( self ):
        try:
            self.th2.running = False
            #self.thread1.running = False
            #time.sleep(1)
            self.but1.setEnabled(True)
            
        except:
            pass




    #def play_async( self ):

    #    self.but1_async.setEnabled(False)

    #    self.textf.clear()
    #    thread = threading.Thread( target=self.__play_async_threadfunc )
    #    thread.start()



    def play_async( self ):#def __play_async_threadfunc( self ):
        #self.thread1 = QThread1()
        #self.thread1.on_source( self.linef.text() )
        #self.thread1.sig1.connect( self.update_textfield )
        #self.thread1.run()# Qthread::run()はスレッド生成なしで処理を直接呼び出すだけ. 自前でthreading.Thread生成してる場合はこれでOK
        
        self.th2 = ThreadIter()
        self.th2.AddSignal( self.sig, self.__m_Count )
        self.th2.start()#self.th2.run()
        #th2.wait()




    def stop_async( self ):
        try:

            self.th2.running = False
            self.but1_async.setEnabled(True)

        except:
            pass



    def update_textfield( self ):
        #self.textf.clear()
        self.textf.append( self.linef.text()  )









if __name__ == "__main__":

    app = QApplication(sys.argv)

    myapp = QthreadApp()
    myapp.show()

    sys.exit(app.exec_())
