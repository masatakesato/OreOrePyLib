import oreorepylib.utils.compat as compat
from oreorepylib.network.namedpipe.halfduplexrpcnode import *

import os
import time



g_InPipeName = r"\\.\pipe\Foo"
g_OutPipeName = r"\\.\pipe\Bar"




class RemoteProcedure( RemoteProcedureBase ):

    def __init__( self, node: HalfDuplexRPCNode ):
        super(RemoteProcedure, self).__init__( node )


    def NoReturn( self ):
        print( "RemoteProcedure::NoReturn()..." )


    def Test( self ):
        print( "RemoteProcedure::Test()..." )
        return "OK..."


    def Add( self, a, b ):
        print( "RemoteProcedure::Add( %d, %d )..." % (a, b) )
        return a + b


    def Str( self, string ):
        time.sleep(1)
        d = { "Key": 55555 }

        print( d[string] )




if __name__=="__main__":

    os.system( "title " + g_InPipeName )

    node = HalfDuplexRPCNode( g_InPipeName )
    proc = RemoteProcedure( node )

    node.BindProcInstance( proc )

    if( not node.StartListen() ):
        sys.exit()

   
    input_text = ""

    while( True ):

        input_text = compat.Input(">")

        if( input_text == "quit" ):
            break

        elif( input_text=="connectto" ):
            node.Connect( g_OutPipeName )

        elif( input_text=="disconnectto" ):
            node.Disconnect()

        elif( input_text=="connectfrom" ):
            node.Call( "Connect", g_InPipeName )

        elif( input_text=="disconnectfrom" ):
            node.Call( "Disconnect" )

        elif( input_text=="startlisten" ):
            node.StartListen()

        elif( input_text=="stoplisten" ):
            node.StopListen()

        elif( input_text=="testrpc" ):
            print( node.Call( "Add", 4, 6 ) )
        #else:
        #    node.Send( input_text.encode() )

    del node