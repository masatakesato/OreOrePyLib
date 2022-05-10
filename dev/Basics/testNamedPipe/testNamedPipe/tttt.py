
# サーバー
# inputで入力した文字列をクライアントに送る
# クライアントからの受信は無限ループでポーリングして待つ
# ポーリングは別スレッドに分離しておく



# クライアント
# inputで入力した文字列をサーバーに送る
# サーバーからの受信は無限ループでポーリングして待つ
# ポーリングは別スレッドに分離しておく

import oreorepylib.utils.environment

import traceback

import struct
import win32con
import ctypes
from ctypes.wintypes import DWORD

from oreorepylib.network.message_protocol import SendMessageError, ReceiveMessageError


Kernel32 = ctypes.windll.kernel32






def send_message( pipe_handle, msg ):

    try:
        if( not msg ):  return

        numBytes = DWORD()
        # send data length
        if( not Kernel32.WriteFile( pipe_handle, struct.pack( 'I', len(msg) ), 4, None, None ) ):
            raise SendMessageError()

        # send data
        result = Kernel32.WriteFile( pipe_handle, msg, len(msg), ctypes.byref(numBytes), None )#win32file.WriteFile( pipe, msg )

        if( not result ):
            raise SendMessageError()#ctypes.WinError()

    except:
        print( 'send_message... Error occured.' )




def receive_message( pipe_handle ):
    try:
        # Extract 4-byte length
        numBytes = DWORD(4)
        #result = Kernel32.PeekNamedPipe( pipe_handle, None, 0, None, ctypes.byref(numBytes), None )
        result = Kernel32.ReadFile( pipe_handle, None, 0, ctypes.byref(numBytes), None )
        if( not result ):
            raise Exception()

        msglen = int( numBytes ) #receive_all( pipe_handle, 4 )
        if( not msglen ):
            return None
        
        # Read message data
        return receive_all( pipe_handle, msg_len )
        
## TODO: Read buffer size first
#                Kernel32.ReadFile( self.__m_PipeHandle, ctypes.byref(byteread), 4, None, None )
#                print( "DatSize:", byteread )

## TODO: Then read actual buffer
#                # https://github.com/ipython/ipython/blob/master/IPython/utils/_process_win32_controller.py
#                if( not Kernel32.ReadFile( self.__m_PipeHandle, data, 64*1024, ctypes.byref(byteread), None ) ):
#                    break



    except:
        #print( 'Exception occured at receive_message' )
        #traceback.print_exc()
        raise ReceiveMessageError( traceback.format_exc() )
        return None#b''


# helper function to receive n bytes or return None if EOF is hit
def receive_all( pipe_handle, n ):

    data = b''




    while( len(data) < n ):
        packet = pipe_handle.recv( n - len(data) )
        if( not packet ):
            return None
        data += packet
        #print( packet, n - len(data) )

    #print( data )
    return data





#data = (ctypes.c_byte * 64 * 1024)()
#byteread = DWORD()

## https://github.com/ipython/ipython/blob/master/IPython/utils/_process_win32_controller.py
#if( not Kernel32.ReadFile( self.__m_PipeHandle, data, 64*1024, ctypes.byref(byteread), None ) ):
#    break
#    #err = ctypes.GetLastError()
#    #print( "Error occured while ReadFile...", err )# 109 pipe 終了しました.
#    #raise ReceiveMessageError( traceback.format_exc() )#raise ctypes.WinError()

##dataからbytearrayへ# https://stackoverflow.com/questions/29291624/python-convert-ctypes-ubyte-array-to-string/29293102#29293102
#char_array = ctypes.cast( data, ctypes.c_char_p )
#print( ">", char_array.value )
##print(f"message: {data.value}")








class PipeServer:

    def __init__( self, pipe_name ):

        self.__m_IsListening = False
        self.__m_PipeName = pipe_name

        self.__m_PipeHandle = None


        self.InitPipe()



    def __del__( self ):
        if( self.__m_PipeHandle ):
            Kernel32.DisconnectNamedPipe ( self.__m_PipeHandle )
            Kernel32.CloseHandle( self.__m_PipeHandle )



    def InitPipe( self ):

        # TODO: disconnect existing named pipe
        self.ReleasePipe()

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



    def ReleasePipe( self ):
        if( self.__m_PipeHandle ):
            Kernel32.DisconnectNamedPipe ( self.__m_PipeHandle )
            Kernel32.CloseHandle( self.__m_PipeHandle )




    def run( self ):

        while True:

            print( "waiting for client connection..." )
            result = Kernel32.ConnectNamedPipe( self.__m_PipeHandle, None )#win32pipe.ConnectNamedPipe( pipe, None )

            # クライアント側で閉じたらサーバー側でも名前付きパイプの作り直しが必要.
            if( result==0 ):
                err = ctypes.GetLastError()
                print( "Error occured while connecting named pipe...", err )
                #return
                self.InitPipe()

                continue

            print( "established connection. starts listening." )
            self.__m_IsListening = True

            self.listen()



    def listen( self ):

        while( self.__m_IsListening ):

            try:
                data = (ctypes.c_byte * 64 * 1024)()
                msg_len = DWORD()

                #Kernel32.PeekNamedPipe( self.__m_PipeHandle, None, 0, None, ctypes.byref(byteread), None )

# TODO: Read buffer size first
                Kernel32.ReadFile( self.__m_PipeHandle, ctypes.byref(msg_len), 4, None, None )
                print( "message length:", msg_len.value )

# TODO: Then read actual buffer
                # https://github.com/ipython/ipython/blob/master/IPython/utils/_process_win32_controller.py
                if( not Kernel32.ReadFile( self.__m_PipeHandle, data, msg_len, ctypes.byref(msg_len), None ) ):
                    break
                    #err = ctypes.GetLastError()
                    #print( "Error occured while ReadFile...", err )# 109 pipe 終了しました.
                    #raise ReceiveMessageError( traceback.format_exc() )#raise ctypes.WinError()
                #print( "ReadFile:", msg_len )

                #dataからbytearrayへ# https://stackoverflow.com/questions/29291624/python-convert-ctypes-ubyte-array-to-string/29293102#29293102
                char_array = ctypes.cast( data, ctypes.c_char_p )
                print( ">", char_array.value )
                #print(f"message: {data.value}")


            except ReceiveMessageError as e:
                #print( 'Client::call()... ReceiveMessageError occured.' )
                break








class PipeClient:

    def __init__( self ):

        self.__m_PipeName = ""
        self.__m_PipeHandle = None
        self.__m_MaxTrials = 5

        self.__m_IsListening = False



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


        #result = Kernel32.ConnectNamedPipe( self.__m_PipeHandle, None )

        print( "Successfully connected to named pipe:", self.__m_PipeName )



    def disconnect( self ):
        if( self.__m_PipeHandle ):
            Kernel32.DisconnectNamedPipe ( self.__m_PipeHandle )
            Kernel32.CloseHandle( self.__m_PipeHandle )
        self.__m_PipeHandle = None

        self.__m_PipeName = ""
        self.__m_IsListening = False



    def send( self, msg ):

        trial = 0

        while( trial < self.__m_MaxTrials ):
            try:

                print( f"writing message {trial}" )
                # convert to bytes
                ##msg = str.encode( f"{count}" )

                
                #numBytes = DWORD( len(msg) )
                #print( numBytes, len(msg) )
                #result = ctypes.windll.kernel32.WriteFile( self.__m_PipeHandle,
                #                                          struct.pack( 'I', len(msg) ),
                #                                          4, ctypes.byref(numBytes), None )

                #result = ctypes.windll.kernel32.WriteFile( self.__m_PipeHandle, msg, len(msg), ctypes.byref(numBytes), None )#win32file.WriteFile( pipe, msg )
                ##print( numBytes )

                #if( not result ):
                #    raise SendMessageError()#ctypes.WinError()


                send_message( self.__m_PipeHandle, msg )


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