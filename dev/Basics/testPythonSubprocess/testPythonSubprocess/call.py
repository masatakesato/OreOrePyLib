#import os
#print( os.environ["PATH"] )

import sys
from time import sleep

#from PyQt5.QtGui import *


print( sys.path )


sleep(1)  #一秒寝てもらう(非同期になっているか確認のため)
args = sys.argv[1]
print( "argv[1]",  args )