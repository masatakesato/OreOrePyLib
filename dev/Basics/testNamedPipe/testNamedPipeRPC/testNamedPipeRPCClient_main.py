from namedpiperpc import *

import threading
import time


import oreorepylib.utils.compat as compat

if( compat.Python3x ):
    def Input( prompt=None ):
        return input( prompt )
else:
    def Input( prompt=None ):
        return raw_input( prompt )



g_PipeName = r"\\.\pipe\Foo"



if __name__=="__main__":

    client = PipeClientRPC()# r"\\.\pipe\Foo" )
    client.Connect( g_PipeName )


    print( client.Call( "NoReturn" ) )
    print( client.Call( "Test" ) )

    print( client.Call( "Ahgfdd", 4, 6 ) )

    print( client.Call( "Add", 4, 6 ) )

    #input_text = ""

    #while( True ):

    #    input_text = Input(">")

    #    if( input_text == "quit" ):
    #        break

    #    elif( input_text=="disconnect" ):
    #        client.Disconnect()

    #    elif( input_text=="connect" ):
    #        client.Connect( g_PipeName )

    #    else:
    #        client.Send( input_text.encode() )
