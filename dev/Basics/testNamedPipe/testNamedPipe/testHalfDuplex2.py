from halfduplexnode import *


g_InPipeName = r"\\.\pipe\Foo2"
g_OutPipeName = r"\\.\pipe\Foo1"



if __name__=="__main__":

    node = HalfDuplexNode( g_InPipeName )
    node.StartListen()
   
    input_text = ""

    while( True ):

        input_text = input(">")

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
