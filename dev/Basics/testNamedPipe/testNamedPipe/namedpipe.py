
# サーバー
# inputで入力した文字列をクライアントに送る
# クライアントからの受信は無限ループでポーリングして待つ
# ポーリングは別スレッドに分離しておく



# クライアント
# inputで入力した文字列をサーバーに送る
# サーバーからの受信は無限ループでポーリングして待つ
# ポーリングは別スレッドに分離しておく


# https://www.kazetest.com/vcmemo/pipe/pipe.htm
# 複数クライアントを扱う場合は、
#   ->CreateNamedPipeWでnMaxInstancesを2以上にする
#   ->マルチスレッド化が必須


import oreorepylib.utils.environment

import traceback

import threading
import struct
import win32con
import ctypes
from ctypes.wintypes import DWORD

from oreorepylib.network.message_protocol import SendMessageError, ReceiveMessageError


Kernel32 = ctypes.windll.kernel32






def send_message( pipe_handle, msg ):

    if( not msg ):  return

    # send data length
    if( not Kernel32.WriteFile( pipe_handle, struct.pack( 'I', len(msg) ), 4, None, None ) ):
        raise SendMessageError()

    # send data
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
    data = ( ctypes.c_byte * msg_len.value )()#64 * 1024)()
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





class PipeServer:

    def __init__( self, pipe_name ):

        self.__m_IsListening = False
        self.__m_PipeName = pipe_name

        self.__m_PipeHandle = None



    def __del__( self ):
        self.ReleasePipe()



    def InitPipe( self ):

        print( "PipeServer::InitPipe()..." )

        # Disconnect existing named pipe
        self.ReleasePipe()

        self.__m_PipeHandle = Kernel32.CreateNamedPipeW(
            self.__m_PipeName, #r'\\.\pipe\Foo',
            win32con.PIPE_ACCESS_DUPLEX,
            win32con.PIPE_TYPE_BYTE | win32con.PIPE_READMODE_BYTE | win32con.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None )

        # Check error after file creation
        err = ctypes.GetLastError()
        if( err > 0 ):
            print( "error check after client::CreateNamedPipeW:", ctypes.GetLastError(), self.__m_PipeHandle )
            self.__m_PipeHandle = None
            return

        print( "Successfully created named pipe:", self.__m_PipeName )

        self.__m_IsListening = True



    def ReleasePipe( self ):

        if( self.__m_PipeHandle ):
            print( "ReleasePipe::DisconnectNamedPipe", self.__m_PipeHandle )
            Kernel32.DisconnectNamedPipe( self.__m_PipeHandle )

            print( "ReleasePipe:", ctypes.GetLastError() )
            Kernel32.CloseHandle( self.__m_PipeHandle )

        print( "ReleasePipe::", ctypes.GetLastError() )
        self.__m_PipeHandle = None
        self.__m_IsListening = False



    def SetListen( self, flag ):
        self.__m_IsListening = flag



    def IsListening( self ):
        return self.__m_IsListening



    def Status( self ):
        print( "//============ PipeServer Status ===========//" )
        print( "PipeName:", self.__m_PipeName )
        print( "PipeHandle:", self.__m_PipeHandle )
        print( "IsListening:", self.__m_IsListening )
        print("")



    def run( self ):

        while self.__m_IsListening:#True:#

            print( "waiting for client connection..." )
            result = Kernel32.ConnectNamedPipe( self.__m_PipeHandle, None )#win32pipe.ConnectNamedPipe( pipe, None )

            print("++++++++++++++++")
            # クライアント側で閉じたらサーバー側でも名前付きパイプの作り直しが必要.
            if( result==0 ):
                err = ctypes.GetLastError()
                print( "PipeServer::run()...Error occured while connecting named pipe...", err, self.__m_PipeHandle )

                if( self.__m_IsListening==False ):#err==6 and 
                    self.ReleasePipe()
                    return

                self.InitPipe()
                continue

            print( "established connection. starts listening." )
            self.listen()



    def listen( self ):

        while( self.__m_IsListening ):

            try:

                print( "waiting for message..." )
                data = receive_message( self.__m_PipeHandle )

                #dataからbytearrayへ# https://stackoverflow.com/questions/29291624/python-convert-ctypes-ubyte-array-to-string/29293102#29293102
                char_array = ctypes.cast( data, ctypes.c_char_p )
                print( ">>", char_array.value )


            except ReceiveMessageError as e:
                #print( 'Client::call()... ReceiveMessageError occured.' )
                break








class PipeClient:

    def __init__( self ):

        self.__m_PipeName = ""
        self.__m_PipeHandle = None
        self.__m_MaxTrials = 5



    def __del__( self ):
        self.disconnect()



    def connect( self, pipe_name ):

        self.__m_PipeName = pipe_name

        # https://programtalk.com/vs4/python/7855/conveyor/src/main/python/conveyor/address.py/
        # Establish pipe connection
        self.__m_PipeHandle = Kernel32.CreateFileW(
            self.__m_PipeName,#r'\\.\pipe\Foo',
            win32con.GENERIC_READ | win32con.GENERIC_WRITE,
            0,
            None,
            win32con.OPEN_EXISTING,
            0,
            None
        )

        # Check error after file creation
        err = ctypes.GetLastError()
        if( err > 0 ):
            print( "error check afer client::CreateFileW:", ctypes.GetLastError(), self.__m_PipeHandle )
            return

        lpMode = DWORD( win32con.PIPE_READMODE_BYTE )#win32con.PIPE_READMODE_MESSAGE )
        res = Kernel32.SetNamedPipeHandleState( self.__m_PipeHandle, ctypes.byref(lpMode), None, None )

        if( res == 0 ):
            print(f"SetNamedPipeHandleState return code: {ctypes.GetLastError()}")
            return


        print( "Successfully connected to named pipe:", self.__m_PipeName )



    def disconnect( self ):
        if( self.__m_PipeHandle ):
            Kernel32.DisconnectNamedPipe ( self.__m_PipeHandle )
            Kernel32.CloseHandle( self.__m_PipeHandle )
        self.__m_PipeHandle = None

        self.__m_PipeName = ""



    def send( self, msg ):

        trial = 0

        while( trial < self.__m_MaxTrials ):
            try:

                #print( f"writing message {trial}" )
                # convert to bytes
                ##msg = str.encode( f"{count}" )

                send_message( self.__m_PipeHandle, msg )

                return

            except SendMessageError as e:#pywintypes.error as e::
                print( "Client::send()... SendMessageError occured.... trial", trial )
                trial += 1

