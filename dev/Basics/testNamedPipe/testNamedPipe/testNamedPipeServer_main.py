from oreorepylib.network.namedpipe.namedpipe import *


import threading
import time


pipe_prefix = "\\\\.\\pipe\\"
pipe_name = "Foo"

print( pipe_prefix + pipe_name )

server = PipeServer( r"\\.\pipe\Foo" )#pipe_prefix + pipe_name )#
server.Run()
