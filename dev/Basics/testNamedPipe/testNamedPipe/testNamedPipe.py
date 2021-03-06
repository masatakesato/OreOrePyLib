# https://itecnote.com/tecnote/python-and-windows-named-pipes/

import time
import sys
#import win32pipe, win32file, pywintypes
import win32con
import ctypes
import ctypes.wintypes

import traceback

import oreorepylib.utils.environment
from oreorepylib.network.message_protocol import SendMessageError, ReceiveMessageError




def pipe_server():

    print("pipe server")
    count = 0

    #pipe = win32pipe.CreateNamedPipe(
    #    r'\\.\pipe\Foo',
    #    win32pipe.PIPE_ACCESS_DUPLEX,
    #    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    #    1, 65536, 65536,
    #    0,
    #    None)


    pipe = ctypes.windll.kernel32.CreateNamedPipeW(
        r'\\.\pipe\Foo',
        win32con.PIPE_ACCESS_DUPLEX,
        win32con.PIPE_TYPE_MESSAGE | win32con.PIPE_READMODE_MESSAGE | win32con.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None )

    print( "owner pipe handle:", pipe )

    try:
        print("waiting for client")
        #win32pipe.ConnectNamedPipe( pipe, None )
        ctypes.windll.kernel32.ConnectNamedPipe( pipe, None )

        print("got client")

        while count < 10:
            print( f"writing message {count}" )
            # convert to bytes
            some_data = str.encode( f"{count}" )

            #win32file.WriteFile( pipe, some_data )
            numBytes = ctypes.wintypes.DWORD()
            bsuccess = ctypes.windll.kernel32.WriteFile( pipe, some_data, len(some_data), ctypes.byref(numBytes), None )

            if( not bsuccess ):
                raise ctypes.WinError()

            time.sleep(1)
            count += 1

        print("finished now")
    finally:
        #win32file.CloseHandle( pipe )
        ctypes.windll.kernel32.CloseHandle( pipe )




def pipe_client():

    print("pipe client")
    quit = False

    # https://programtalk.com/vs4/python/7855/conveyor/src/main/python/conveyor/address.py/
    # Establish pipe connection
    #handle = win32file.CreateFile(
    #    r'\\.\pipe\Foo',
    #    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
    #    0,
    #    None,
    #    win32file.OPEN_EXISTING,
    #    0,
    #    None
    #)
    #res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)

    handle = ctypes.windll.kernel32.CreateFileW(
        r'\\.\pipe\Foo',
        win32con.GENERIC_READ | win32con.GENERIC_WRITE,
        0,
        None,
        win32con.OPEN_EXISTING,
        0,
        None
    )

    print( "user pipe handle:", handle )

    # CHeck error after file creation
    err = ctypes.GetLastError()
    if( err > 0 ):
        print( "error check afer client::CreateFileW:", ctypes.GetLastError(), handle )
        return

    lpMode = ctypes.wintypes.DWORD( win32con.PIPE_READMODE_MESSAGE )
    res = ctypes.windll.kernel32.SetNamedPipeHandleState( handle, ctypes.byref(lpMode), None, None )

    if( res == 0 ):
        print(f"SetNamedPipeHandleState return code: {ctypes.GetLastError()}")
        return


    print( "--------------------------" )

    maxtrials = 5
    trial = 0

    while True:

        try:
            #resp = win32file.ReadFile(handle, 64*1024)
            data = (ctypes.c_byte * 64 * 1024)()
            byteread = ctypes.wintypes.DWORD()
        

            # https://github.com/ipython/ipython/blob/master/IPython/utils/_process_win32_controller.py
            if( not ctypes.windll.kernel32.ReadFile( handle, data, 64*1024, ctypes.byref(byteread), None ) ):
                raise ReceiveMessageError( traceback.format_exc() )
                print( "Failed reading from named pipe." )
                #raise ctypes.WinError()

            #data??????bytearray???# https://stackoverflow.com/questions/29291624/python-convert-ctypes-ubyte-array-to-string/29293102#29293102
            filename = ctypes.cast( data, ctypes.c_char_p )
            print( "client received message:", filename.value )
            #print(f"message: {data.value}")


        except SendMessageError as e:#pywintypes.error as e:
            print( 'Client::call()... SendMessageError occured.' )
            trial += 1
            if( trial >= maxtrials ): break


        except ReceiveMessageError as e:
            print( 'Client::call()... ReceiveMessageError occured.' )
            break


    #        if( e.args[0] == 2 ):
    #            print("no pipe, trying again in a sec")
    #            time.sleep(1)
    #        elif( e.args[0] == 109 ):
    #            print("broken pipe, bye bye")
    #            quit = True

    #        elif( e.args[0] == 22 ):
    #            print("cannot detect command.")
    #            quit=True


import threading


server_thread = threading.Thread( target=pipe_server )
server_thread.start()

time.sleep(1.0)

pipe_client()


#if __name__ == '__main__':
#    if len(sys.argv) < 2:
#        print("need s or c as argument")
#    elif sys.argv[1] == "s":
#        pipe_server()
#    elif sys.argv[1] == "c":
#        pipe_client()
#    else:
#        print(f"no can do: {sys.argv[1]}")