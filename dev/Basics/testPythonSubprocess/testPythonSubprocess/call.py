import os
import sys
import pathlib



envpath = pathlib.Path( sys.executable ).parents[0]

#print( str(envpath).replace("\\", "\\\\") )

g_EnvSubpaths =(
    # Library
    "/Library/mingw-w64/bin;",
    "/Library/usr/bin;",
    "/Library/bin;",
    # Scripts
    "/Scripts;",
    # bin
    "/bin;",
    )

rootpath = str(envpath).replace("\\", "/")
for subpath in g_EnvSubpaths:
    print( rootpath + subpath )

    #sys.path.append( rootpath + subpath )# こっちじゃない
    os.environ["PATH"] += rootpath + subpath


print( os.environ["PATH"] )





from time import sleep

from PyQt5.QtCore import *
from PyQt5.QtGui import *


print( sys.version )
print( qVersion() )



sleep(1)  #一秒寝てもらう(非同期になっているか確認のため)
args = sys.argv[1]
print( "argv[1]",  args )
