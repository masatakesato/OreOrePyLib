import oreorepylib.utils.compat as compat
from oreorepylib.network.namedpipe.halfduplexrpcnode import *

import os



g_InPipeName = r"\\.\pipe\Bar"
g_OutPipeName = r"\\.\pipe\Foo"




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


    def TestArrayTransfer( self, arr ):
        print( "RemoteProcedure::TestArrayTransfer()..." )

        for v in arr:
            print( v )




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
            #print( node.Call( compat.ToUnicode("Str"), u"Key" ) )
            print( node.Call( "Add", 4, 6 ) )

    del node