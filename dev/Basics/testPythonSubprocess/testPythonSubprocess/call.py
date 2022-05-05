from utils import environment
environment.AddPythonEnvironmentPaths( None )#pathlib.Path( sys.executable ).parents[0] )

import os
import sys


from time import sleep

from PyQt5.QtCore import *
from PyQt5.QtGui import *



if __name__=="__main__":

    print( sys.version )
    print( qVersion() )

    sleep(1)  #一秒寝てもらう(非同期になっているか確認のため)
    args = sys.argv[1]
    print( "argv[1]",  args )
