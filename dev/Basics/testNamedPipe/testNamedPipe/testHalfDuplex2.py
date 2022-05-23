import oreorepylib.utils.compat as compat

if( compat.Python3x ):
    def Input( prompt=None ):
        return input( prompt )
else:
    def Input( prompt=None ):
        return raw_input( prompt )





from halfduplexnode import *


g_InPipeName = r"\\.\pipe\Foo2"
g_OutPipeName = r"\\.\pipe\Foo1"



if __name__=="__main__":

    node = HalfDuplexNode( g_InPipeName )
    node.StartListen()
   
    input_text = ""

    while( True ):

        input_text = Input(">")

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
