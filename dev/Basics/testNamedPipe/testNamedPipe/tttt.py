
# サーバー
# inputで入力した文字列をクライアントに送る
# クライアントからの受信は無限ループでポーリングして待つ
# ポーリングは別スレッドに分離しておく



# クライアント
# inputで入力した文字列をサーバーに送る
# サーバーからの受信は無限ループでポーリングして待つ
# ポーリングは別スレッドに分離しておく

import oreorepylib.utils.environment

import win32con
import ctypes
from ctypes.wintypes import DWORD

from oreorepylib.network.message_protocol import SendMessageError, ReceiveMessageError


Kernel32 = ctypes.windll.kernel32




class PipeServer:

    def __init__( self, pipe_name ):

        self.__m_PipeName = pipe_name

        self.__m_PipeHandle = Kernel32.CreateNamedPipeW(
            self.__m_PipeName, #r'\\.\pipe\Foo',
            win32con.PIPE_ACCESS_DUPLEX,
            win32con.PIPE_TYPE_MESSAGE | win32con.PIPE_READMODE_MESSAGE | win32con.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None )

        # CHeck error after file creation
        err = ctypes.GetLastError()
        if( err > 0 ):
            print( "error check after client::CreateNamedPipeW:", ctypes.GetLastError(), self.__m_PipeHandle )
            self.__m_PipeHandle = None
            return


        print( "Successfully created named pipe:", self.__m_PipeName )



    def __del__( self ):
        if( self.__m_PipeHandle ):
            Kernel32.CloseHandle( self.__m_PipeHandle )



    def listen( self ):

        print( "waiting for client connection..." )
        #win32pipe.ConnectNamedPipe( pipe, None )
        Kernel32.ConnectNamedPipe( self.__m_PipeHandle, None )

        print( "established connection. starts listening." )

        while( self.__m_IsListening ):

            try:
                data = (ctypes.c_byte * 64 * 1024)()
                byteread = DWORD()

                # https://github.com/ipython/ipython/blob/master/IPython/utils/_process_win32_controller.py
                if( not ctypes.windll.kernel32.ReadFile( self.__m_PipeHandle, data, 64*1024, ctypes.byref(byteread), None ) ):
                    raise ReceiveMessageError( traceback.format_exc() )#raise ctypes.WinError()

                #dataからbytearrayへ# https://stackoverflow.com/questions/29291624/python-convert-ctypes-ubyte-array-to-string/29293102#29293102
                char_array = ctypes.cast( data, ctypes.c_char_p )
                print( ">", char_array.value )
                #print(f"message: {data.value}")


            except ReceiveMessageError as e:
                print( 'Client::call()... ReceiveMessageError occured.' )
                break








class PipeClient:

    def __init__( self ):

        self.__m_PipeName = ""
        self.__m_PipeHandle = None
        self.__m_MaxTrials = 5

        self.__m_IsListening = False



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

        # CHeck error after file creation
        err = ctypes.GetLastError()
        if( err > 0 ):
            print( "error check afer client::CreateFileW:", ctypes.GetLastError(), self.__m_PipeHandle )
            return

        lpMode = DWORD( win32con.PIPE_READMODE_MESSAGE )
        res = Kernel32.SetNamedPipeHandleState( self.__m_PipeHandle, ctypes.byref(lpMode), None, None )

        if( res == 0 ):
            print(f"SetNamedPipeHandleState return code: {ctypes.GetLastError()}")
            return

        print( "Successfully connected to named pipe:", self.__m_PipeName )




    def disconnect( self ):
        pass



    def send( self, msg ):

        trial = 0

        while( trial < self.__m_MaxTrials ):
            try:

                print( f"writing message {count}" )
                # convert to bytes
                #msg = str.encode( f"{count}" )

                #win32file.WriteFile( pipe, msg )
                numBytes = DWORD()
                result = ctypes.windll.kernel32.WriteFile( self.__m_PipeHandle, some_data, len(msg), ctypes.byref(numBytes), None )

                if( not result ):
                    raise SendMessageError()#ctypes.WinError()

                return

            except SendMessageError as e:#pywintypes.error as e::
                print( 'Client::send()... SendMessageError occured.' )
                trial += 1



    def listen( self ):

        while( self.__m_IsListening ):

            try:
                data = (ctypes.c_byte * 64 * 1024)()
                byteread = DWORD()

                # https://github.com/ipython/ipython/blob/master/IPython/utils/_process_win32_controller.py
                if( not ctypes.windll.kernel32.ReadFile( self.__m_PipeHandle, data, 64*1024, ctypes.byref(byteread), None ) ):
                    raise ReceiveMessageError( traceback.format_exc() )#raise ctypes.WinError()

                #dataからbytearrayへ# https://stackoverflow.com/questions/29291624/python-convert-ctypes-ubyte-array-to-string/29293102#29293102
                char_array = ctypes.cast( data, ctypes.c_char_p )
                print( ">", char_array.value )
                #print(f"message: {data.value}")


            except ReceiveMessageError as e:
                print( 'Client::call()... ReceiveMessageError occured.' )
                break




import threading
import time


server = PipeServer( r"\\.\pipe\Foo" )
server.listen()







#def func():

#    for i in range( 10):
#        print("----------" )
#        time.sleep(1)




#if __name__=="__main__":

#    th = threading.Thread( target=func )
#    th.start()

#    input_text = ""

#    while( input_text != "quit" ):

#        input_text = input(">")
#        print( ">" + input_text )