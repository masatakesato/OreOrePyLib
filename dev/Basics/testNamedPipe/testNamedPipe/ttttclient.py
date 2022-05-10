from tttt import *


import threading
import time



if __name__=="__main__":

    client = PipeClient()# r"\\.\pipe\Foo" )

   
    input_text = ""

    while( input_text != "quit" ):

        input_text = input(">")
        #print( ">" + input_text )

        if( input_text=="disconnect" ):
            client.disconnect()
        elif( input_text=="connect" ):
            client.connect( r"\\.\pipe\Foo" )


    #client.send( "Message from client".encode() )

    #client.listen()

    #client.disconnect()






time.sleep(5)
