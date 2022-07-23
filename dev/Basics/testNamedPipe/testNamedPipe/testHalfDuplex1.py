import oreorepylib.utils.compat as compat
from oreorepylib.network.namedpipe.halfduplexnode import *
#from halfduplexnode import *



g_InPipeName = r"\\.\pipe\Foo"
g_OutPipeName = r"\\.\pipe\Bar"



if __name__=="__main__":

    node = HalfDuplexNode( g_InPipeName )
    node.StartListen()
   
    input_text = ""

    while( True ):

        input_text = compat.Input(">")

        if( input_text == "quit" ):
            break

        elif( input_text=="disconnect" ):
            node.Disconnect()

        elif( input_text=="connect" ):
            node.Connect( g_OutPipeName )

        elif( input_text=="startlisten" ):
            node.StartListen()

        elif( input_text=="stoplisten" ):
            node.StopListen()

        else:
            node.Send( input_text.encode() )
