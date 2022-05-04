import subprocess

import os
import sys

#print( os.environ["PATH"] )



if __name__=="__main__":

    #command = [ "python","call.py", "argument from main process" ]
    #proc = subprocess.Popen(command)
    #print("Calling...")
    #proc.communicate()


    print( sys.version )

    # command using specific python environment
    command = [ "D:/ProgramData/Anaconda3/envs/testpyqt/python.exe", "call.py", "argument from main process" ]
    proc = subprocess.Popen(command)
    print("Calling...")
    proc.communicate()    



    ## D:\ProgramData\Anaconda3
    ## Root
    #D:\ProgramData\Anaconda3;

    ## Library
    #D:\ProgramData\Anaconda3\Library\mingw-w64\bin;
    #D:\ProgramData\Anaconda3\Library\usr\bin;
    #D:\ProgramData\Anaconda3\Library\bin;

    ## Scripts
    #D:\ProgramData\Anaconda3\Scripts;

    ## bin
    #D:\ProgramData\Anaconda3\bin;

    #D:\ProgramData\Anaconda3\condabin;# コマンドラインから実行するバッチが入ってる. conda activate的なやつ




    ## testpyqt
    ## Root
    #D:\ProgramData\Anaconda3\envs\testpyqt;

    ## Library
    #D:\ProgramData\Anaconda3\envs\testpyqt\Library\mingw-w64\bin;
    #D:\ProgramData\Anaconda3\envs\testpyqt\Library\usr\bin;
    #D:\ProgramData\Anaconda3\envs\testpyqt\Library\bin;

    ## Scripts
    #D:\ProgramData\Anaconda3\envs\testpyqt\Scripts;

    ## bin
    #D:\ProgramData\Anaconda3\envs\testpyqt\bin;

    #D:\ProgramData\Anaconda3\condabin;
    


# sys.path in this code
#'D:\\Repository\\OreOrePyLib\\dev\\Basics\\testPythonSubprocess\\testPythonSubprocess',
#'D:\\Repository\\OreOrePyLib\\dev\\Basics\\testPythonSubprocess\\testPythonSubprocess',
#'D:\\ProgramData\\Anaconda3\\python37.zip', 'D:\\ProgramData\\Anaconda3\\DLLs',
#'D:\\ProgramData\\Anaconda3\\lib',
#'D:\\ProgramData\\Anaconda3',
#'D:\\ProgramData\\Anaconda3\\lib\\site-packages',
#'D:\\ProgramData\\Anaconda3\\lib\\site-packages\\win32',
#'D:\\ProgramData\\Anaconda3\\lib\\site-packages\\win32\\lib',
#'D:\\ProgramData\\Anaconda3\\lib\\site-packages\\Pythonwin'


# sys.path in cal..py subprocess
'D:\\Repository\\OreOrePyLib\\dev\\Basics\\testPythonSubprocess\\testPythonSubprocess',
'D:\\Repository\\OreOrePyLib\\dev\\Basics\\testPythonSubprocess\\testPythonSubprocess',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt\\python37.zip',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt\\DLLs',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt\\lib',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt\\lib\\site-packages',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt\\lib\\site-packages\\win32',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt\\lib\\site-packages\\win32\\lib',
'D:\\ProgramData\\Anaconda3\\envs\\testpyqt\\lib\\site-packages\\Pythonwin'