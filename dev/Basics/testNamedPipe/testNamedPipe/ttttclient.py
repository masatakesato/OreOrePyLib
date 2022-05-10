from tttt import *


import threading
import time



if __name__=="__main__":

    client = PipeClient()# r"\\.\pipe\Foo" )

   
    input_text = ""

    while( True ):

        input_text = input(">")

        if( input_text == "quit" ):
            break

        elif( input_text=="disconnect" ):
            client.disconnect()

        elif( input_text=="connect" ):
            client.connect( r"\\.\pipe\Foo" )

        else:
            client.send( input_text.encode() )

    #client.send( "Message from client".encode() )

    #client.listen()

    #client.disconnect()






time.sleep(5)
