from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MySignal(QObject):
    sig = pyqtSignal(tuple, dict)


    def connect(self, f):
        self.sig.connect(f)

    def emit(self, *args, **kwargs):
        self.sig.emit(args, kwargs)

    def resolve(self, f):
        def wrapper(*args):
            return f(args[0], *args[1], **args[2])
        return wrapper



class Test(QObject):
    m = MySignal()

    def __init__(self):
        QObject.__init__(self)
        self.m.connect(self.out)


    def run(self):
        self.m.emit('AAAAAAA', b=42)


    @m.resolve
    def out(self, a, b):
        print( a, b)



t = Test()
t.run()






#class MySignal(QObject):
#    sig = pyqtSignal(tuple, dict)



#def func( a, b ):
#    print( a, b )


#sig = MySignal()

#sig.sig.connect(func)

#sig.sig.emit( 0, 1 )