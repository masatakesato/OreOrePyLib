# -*- coding: utf-8 -*-

# https://www.kazetest.com/vcmemo/pipe/pipe.htm
# 複数クライアントを扱う場合は、
#   ->CreateNamedPipeWでnMaxInstancesを2以上にする
#   ->マルチスレッド化が必須


import oreorepylib.utils.environment

import sys
import threading
import struct
import ctypes
from ctypes.wintypes import DWORD
import traceback

import oreorepylib.utils.compat as compat
from oreorepylib.network.message_protocol import SendMessageError, ReceiveMessageError
from oreorepylib.network.serializer import Serializer


Kernel32 = ctypes.windll.kernel32


if( compat.Python3x ):
    CreateNamedPipe = Kernel32.CreateNamedPipeW
    CreateFile = Kernel32.CreateFileW
else:
    CreateNamedPipe = Kernel32.CreateNamedPipeA
    CreateFile = Kernel32.CreateFileA






def send_message( pipe_handle, msg ):

    if( not msg ):  return

    # Send data length
    if( not Kernel32.WriteFile( pipe_handle, struct.pack( 'I', len(msg) ), 4, None, None ) ):
        raise SendMessageError()

    # Send data
    #numBytes = DWORD()
    if( not Kernel32.WriteFile( pipe_handle, msg, len(msg), None, None ) ):#ctypes.byref(numBytes), None )#win32file.WriteFile( pipe, msg )
        raise SendMessageError()#ctypes.WinError()




def receive_message( pipe_handle ):

    # Read buffer size first
    msg_len = DWORD()
    if( not Kernel32.ReadFile( pipe_handle, ctypes.byref(msg_len), 4, None, None ) ):
        raise ReceiveMessageError( traceback.format_exc() )
        return None#b''

    #print( "message length:", msg_len.value )
    #if( msg_len.value==0 ):
    #    return None

    # Then read actual buffer#return receive_all( pipe_handle, msg_len )
    # https://github.com/ipython/ipython/blob/master/IPython/utils/_process_win32_controller.py
    data = ( ctypes.c_byte * msg_len.value )()
    if( not Kernel32.ReadFile( pipe_handle, data, msg_len, ctypes.byref(msg_len), None ) ):
        raise ReceiveMessageError( traceback.format_exc() )
        return None#b''

    return data



# helper function to receive n bytes or return None if EOF is hit
#def receive_all( pipe_handle, n ):

#    data = b''

#    while( len(data) < n ):
#        packet = pipe_handle.recv( n - len(data) )
#        if( not packet ):
#            return None
#        data += packet
#        #print( packet, n - len(data) )

#    #print( data )
#    return data



class Win32Constant:

    GENERIC_READ = -2147483648
    GENERIC_WRITE = 1073741824

    OPEN_EXISTING = 3

    PIPE_ACCESS_INBOUND = 1
    PIPE_ACCESS_OUTBOUND = 2
    PIPE_ACCESS_DUPLEX = 3

    PIPE_WAIT = 0
    PIPE_NOWAIT = 1
    PIPE_READMODE_BYTE = 0
    PIPE_READMODE_MESSAGE = 2
    PIPE_TYPE_BYTE = 0
    PIPE_TYPE_MESSAGE = 4




class PipeServerRPC:

    def __init__( self, pipe_name ):

        self.__m_IsListening = False
        self.__m_PipeName = pipe_name

        self.__m_PipeHandle = None

        self.__m_Serializer = Serializer( pack_encoding=None, unpack_encoding=None )

        self.__m_ProcInstance = None




    def __del__( self ):
        self.ReleasePipe()



    def BindProcInstance( self, proc ):
        self.__m_ProcInstance = proc



    def InitPipe( self ):

        print( "PipeServer::InitPipe()..." )

        # Disconnect existing named pipe
        self.ReleasePipe()

        self.__m_PipeHandle = CreateNamedPipe(
            self.__m_PipeName, #r'\\.\pipe\Foo',
            Win32Constant.PIPE_ACCESS_DUPLEX,
            Win32Constant.PIPE_TYPE_BYTE | Win32Constant.PIPE_READMODE_BYTE | Win32Constant.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None )

        # Check error after file creation
        err = ctypes.GetLastError()
        if( err > 0 ):
            print( "error check after client::CreateNamedPipe(): %d" % ctypes.GetLastError() )
            self.__m_PipeHandle = None
            return

        print( "Successfully created named pipe: %s" % self.__m_PipeName )

        self.__m_IsListening = True



    def ReleasePipe( self ):

        print( "PipeServer::ReleasePipe()..." )

        if( self.__m_PipeHandle ):
            Kernel32.DisconnectNamedPipe( self.__m_PipeHandle )
            Kernel32.CloseHandle( self.__m_PipeHandle )

        self.__m_PipeHandle = None
        self.__m_IsListening = False



    def SetListen( self, flag ):
        self.__m_IsListening = flag



    def IsListening( self ):
        return self.__m_IsListening



    def Status( self ):
        print( "//============ PipeServer Status ===========//" )
        print( "PipeName: %s" % self.__m_PipeName )
        print( "PipeHandle: %d" % self.__m_PipeHandle )
        print( "IsListening: %r\n" % self.__m_IsListening )



    def Run( self ):

        self.__m_IsListening = True

        while self.__m_IsListening:#True:#

            print( "waiting for client connection..." )
            result = Kernel32.ConnectNamedPipe( self.__m_PipeHandle, None )#win32pipe.ConnectNamedPipe( pipe, None )

            # クライアント側で閉じたらサーバー側でも名前付きパイプの作り直しが必要.
            if( result==0 ):
                err = ctypes.GetLastError()
                print( "PipeServer::Run()...Error occured while ConnectNamedPipe(): %d" % err )

                if( self.__m_IsListening==False ):#err==6 and 
                    self.ReleasePipe()
                    return

                self.InitPipe()
                continue

            print( "established connection. starts listening." )
            self.__Listen()



    def __Listen( self ):

        while( self.__m_IsListening ):

            try:
                # Receive message
                print( "waiting for message..." )
                recv_data = receive_message( self.__m_PipeHandle )

                #dataからbytearrayへ# https://stackoverflow.com/questions/29291624/python-convert-ctypes-ubyte-array-to-string/29293102#29293102
                char_array = ctypes.cast( recv_data, ctypes.c_char_p )
                #print( ">>", char_array.value )

                # Deserialize data
                msg = self.__m_Serializer.Unpack( char_array.value )
                proc_name = msg[0]
                args = msg[1]               
                kwargs = msg[2] if len(msg)==3 else {}

                # Do something
                ret = getattr( self.__m_ProcInstance, proc_name )( *args, **kwargs )

                #print( ">>", msg )
                # Send back result to client
                if( proc_name!='echo' ): send_message( self.__m_PipeHandle, self.__m_Serializer.Pack( ret ) )


            except SendMessageError as e:
                print( 'PipeServerRPC::__Listen()... SendMessageError occured.' )
                break

            except ReceiveMessageError as e:
                print( 'PipeServerRPC::__Listen()... ReceiveMessageError occured.' )
                break

            except:
                print( 'PipeServerRPC::__Listen()... Callback exception occured...%s' % traceback.format_exc() )
                send_message( self.__m_PipeHandle, self.__m_Serializer.Pack( traceback.format_exc() ) )




class PipeClientRPC:

    def __init__( self ):

        self.__m_PipeName = ""
        self.__m_PipeHandle = None
        self.__m_MaxTrials = 5

        self.__m_Serializer = Serializer( pack_encoding=None, unpack_encoding=None )



    def __del__( self ):
        self.Disconnect()



    def Connect( self, pipe_name ):

        self.__m_PipeName = pipe_name

        # https://programtalk.com/vs4/python/7855/conveyor/src/main/python/conveyor/address.py/
        # Establish pipe connection
        self.__m_PipeHandle = CreateFile(
            self.__m_PipeName,#r'\\.\pipe\Foo',
            Win32Constant.GENERIC_READ | Win32Constant.GENERIC_WRITE,
            0,
            None,
            Win32Constant.OPEN_EXISTING,
            0,
            None
        )

        # Check error after file creation
        err = ctypes.GetLastError()
        if( err > 0 ):
            print( "PipeClient::Connect()...Error occured while CreateFile(): %d" % ctypes.GetLastError() )
            return

        lpMode = DWORD( Win32Constant.PIPE_READMODE_BYTE )#Win32Constant.PIPE_READMODE_MESSAGE )
        res = Kernel32.SetNamedPipeHandleState( self.__m_PipeHandle, ctypes.byref(lpMode), None, None )

        if( res == 0 ):
            print( "PipeClient::Connect()...Error occured while SetNamedPipeHandleState(): %d" % ctypes.GetLastError() )
            return


        print( "Successfully connected to named pipe: %s" % self.__m_PipeName )



    def Disconnect( self ):
        if( self.__m_PipeHandle ):
            Kernel32.DisconnectNamedPipe ( self.__m_PipeHandle )
            Kernel32.CloseHandle( self.__m_PipeHandle )
        self.__m_PipeHandle = None

        self.__m_PipeName = ""



    def Call( self, proc_name, *args, **kwargs ):

        trial = 0

        while( trial < self.__m_MaxTrials ):
            try:

                send_data = self.__m_Serializer.Pack( ( proc_name, args, kwargs ) )

                # Send message to server
                send_message( self.__m_PipeHandle, send_data )

                # Receive data from server
                recv_data = receive_message( self.__m_PipeHandle )
                char_array = ctypes.cast( recv_data, ctypes.c_char_p )
                #print( ">>", char_array.value )

                # Deserialize and return data
                return self.__m_Serializer.Unpack( char_array.value )


            except SendMessageError as e:#pywintypes.error as e::
                print( "Client::Send()...SendMessageError occured.... trial %d" % trial )
                trial += 1

