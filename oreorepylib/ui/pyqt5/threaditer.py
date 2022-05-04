import time
from PyQt5.QtCore import *



class ThreadIter( QThread ):

    def __init__(self, parent=None):
        super(ThreadIter, self).__init__(parent=parent)

        self.iters = []
        self.sig_exec = []



    def AddSignal( self, sig, numiter ):
        self.sig_exec.append( sig )
        self.iters.append(numiter)



    def run( self ):
        self.running = True
        for i, sig in enumerate(self.sig_exec):
            for j in range(self.iters[i]):
                if( self.running==False ): return
                sig.emit()
                self.usleep(1)# sleepしないとウィジェットのビジー状態が開放されない
                #time.sleep(0.005)# time.sleepしないとウィジェットのビジー状態が開放されない
        self.running = False