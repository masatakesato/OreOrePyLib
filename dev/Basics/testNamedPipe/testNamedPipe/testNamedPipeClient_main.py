import oreorepylib.utils.compat as compat
from oreorepylib.network.namedpipe.namedpipe import *

import threading
import time



g_PipeName = r"\\.\pipe\Foo"


if __name__=="__main__":

    client = PipeClient()# r"\\.\pipe\Foo" )

   
    input_text = ""

    while( True ):

        input_text = compat.Input(">")

        if( input_text == "quit" ):
            break

        elif( input_text=="disconnect" ):
            client.Disconnect()

        elif( input_text=="connect" ):
            client.Connect( g_PipeName )

        else:
            client.Send( input_text.encode() )
