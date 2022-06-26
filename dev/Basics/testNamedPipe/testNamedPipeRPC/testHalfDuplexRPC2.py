﻿import oreorepylib.utils.compat as compat

from halfduplexrpcnode import *

import os



g_InPipeName = r"\\.\pipe\Foo2"
g_OutPipeName = r"\\.\pipe\Foo1"




class Procedure:

    def NoReturn( self ):
        print( "Procedure::NoReturn()..." )


    def Test( self ):
        print( "Procedure::Test()..." )
        return "OK..."


    def Add( self, a, b ):
        print( "Procedure::Add( %d, %d )..." % (a, b) )
        return a + b


    def TestArrayTransfer( self, arr ):
        print( "Procedure::TestArrayTransfer()..." )

        for v in arr:
            print( v )




if __name__=="__main__":

    os.system( "title " + g_InPipeName )

    proc = Procedure()
    node = HalfDuplexRPCNode( g_InPipeName )

    node.BindProcInstance( proc )

    if( not node.StartListen() ):
        sys.exit()

   
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

        elif( input_text=="testrpc" ):
            print( node.Call( compat.ToUnicode("Str"), u"Key" ) )
            #print( node.Call( "Add", 4, 6 ) )

    del node