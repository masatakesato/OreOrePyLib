from namedpipe import *


import threading
import time


server = PipeServer( r"\\.\pipe\Foo" )
server.run()
