from namedpipe import *


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

        if( self.__m_IsListening ):
            print("already listening...")
            return

        self.__m_IsListening = True
        self.__m_ListenThread = threading.Thread( target=self.__m_Receiver.run )
        self.__m_ListenThread.start()

        print("startListen...")



    def StopListen( self ):
        
        self.__m_Receiver.ReleasePipe()

        self.__m_IsListening = False

        if( self.__m_ListenThread ):
            self.__m_ListenThread.join()
        self.__m_ListenThread = None

        print("stopListen...")


