﻿from namedpipe import *


import threading




class HalfDuplexNode:

    def __init__( self, in_pipe_name ):
        self.__m_Receiver = PipeServer( in_pipe_name )
        self.__m_Sender = PipeClient()

        self.__m_IsListening = False
        self.__m_ListenThread = None



    def Connect( self, out_pipe_name ):
        self.__m_Sender.connect( out_pipe_name )



    def Disconnect( self ):
        self.__m_Sender.disconnect()



    def Send( self, msg ):
        self.__m_Sender.send( msg )



    #def StartListen( self ):
    #    self.__m_Receiver.startListen()



    #def StopListen( self ):
    #    self.__m_Receiver.stopListen()




    def StartListen( self ):

        print( "HalfDuplexNode::StartListen()..." )

        self.__m_Receiver.Status()

        if( self.__m_IsListening ):
            print("already listening...")
            return

        print("StartListen::self.__m_Receiver.InitPipe()...")
        self.__m_Receiver.InitPipe()

        print("StartListen::running thread...")
        self.__m_IsListening = True
        self.__m_ListenThread = threading.Thread( target=self.__m_Receiver.run )
        self.__m_ListenThread.start()



    def StopListen( self ):
        
        print( "HalfDuplexNode::StopListen()..." )

        #self.__m_Receiver.SignalStopListen()

        print("StopListen::self.__m_Receiver.SetListen(False)...")
        self.__m_Receiver.SetListen( False )

        if( self.__m_ListenThread ):
            print("StopListen::Kernel32.OpenThread()...")
            hthread = Kernel32.OpenThread( 0x40000000, False, self.__m_ListenThread.ident )
            Kernel32.CancelSynchronousIo( hthread )
            Kernel32.CloseHandle( hthread )
            
            
        print("StopListen::self.__m_Receiver.ReleasePipe()...")
        #self.__m_Receiver.SignalStopListen()
        self.__m_Receiver.ReleasePipe()

        #if( self.__m_ListenThread ):
        #    self.__m_ListenThread.join()
        self.__m_ListenThread = None


 


        self.__m_IsListening = False


        self.__m_Receiver.Status()




