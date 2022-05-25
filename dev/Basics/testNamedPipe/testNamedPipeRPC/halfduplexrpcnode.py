from namedpiperpc import *


import threading




class HalfDuplexRPCNode:

    def __init__( self, in_pipe_name ):
        self.__m_Receiver = PipeServerRPC( in_pipe_name )
        self.__m_Sender = PipeClientRPC()

        self.__m_ListenThread = None



    def Connect( self, out_pipe_name ):
        self.__m_Sender.Connect( out_pipe_name )



    def Disconnect( self ):
        self.__m_Sender.Disconnect()



    def Call( self, msg ):
        return self.__m_Sender.Call( msg )



    def StartListen( self ):

        print( "HalfDuplexNode::StartListen()..." )

        if( self.__m_Receiver.IsListening() ):
            print("  Aborting: already listening...")
            return

        # Init pipe
        self.__m_Receiver.InitPipe()

        # Start listen thread
        #print("StartListen::running thread...")
        self.__m_ListenThread = threading.Thread( target=self.__m_Receiver.Run )
        self.__m_ListenThread.start()



    def StopListen( self ):
        
        print( "HalfDuplexNode::StopListen()..." )

        # Set polling flag to false
        #print("StopListen::self.__m_Receiver.SetListen(False)...")
        self.__m_Receiver.SetListen( False )

        if( self.__m_ListenThread ):
            #print("StopListen::Kernel32.OpenThread()...")
            hthread = Kernel32.OpenThread( 0x40000000, False, self.__m_ListenThread.ident )
            Kernel32.CancelSynchronousIo( hthread )
            Kernel32.CloseHandle( hthread )
            self.__m_ListenThread.join()
        self.__m_ListenThread = None

        # Release pipe instances
        #print("StopListen::self.__m_Receiver.ReleasePipe()...")
        self.__m_Receiver.ReleasePipe()

        # Check status
        #self.__m_Receiver.Status()




