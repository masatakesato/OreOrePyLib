﻿import oreorepylib.utils.compat as compat
from oreorepylib.network.namedpipe.halfduplexrpcnode import *

import os
import time
import weakref


g_InPipeName = r"\\.\pipe\Foo"
g_OutPipeName = r"\\.\pipe\Bar"




class Procedure:

    m_refNode = None


    def NoReturn( self ):
        print( "Procedure::NoReturn()..." )


    def Test( self ):
        print( "Procedure::Test()..." )
        return "OK..."


    def Add( self, a, b ):
        print( "Procedure::Add( %d, %d )..." % (a, b) )
        return a + b


    def Str( self, string ):
        time.sleep(1)
        d = { "Key": 55555 }

        print( d[string] )


    def ConnectSender( self, out_pipe_name ):
        self.m_refNode().Connect( out_pipe_name )




if __name__=="__main__":

    os.system( "title " + g_InPipeName )

    proc = Procedure()
    node = HalfDuplexRPCNode( g_InPipeName )

    proc.m_refNode = weakref.ref(node)

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
            print( node.Call( "Add", 4, 6 ) )
        #else:
        #    node.Send( input_text.encode() )

    del node