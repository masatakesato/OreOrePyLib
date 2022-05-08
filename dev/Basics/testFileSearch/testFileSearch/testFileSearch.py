
# python 3.x
import pathlib
root = './'
p_root = pathlib.Path( root ).resolve().as_posix()
print( "root directory:\n    ", p_root, "\n" )

# python 2.x
#import os
#root = './'
#p_root = os.path.abspath(root).replace('\\', '/')
#print( p_root )


import glob

print( "retrieving .../*_oreore.fbx from root directory..." )
sc2in_list = glob.glob( p_root + "/*_oreore.fbx" )
for path in sc2in_list:
	print( "  ", path.replace("\\", "/") )

print()

print( "retrieving .../*_oreore2.fbx from root directory..." )
sc2in_anim_list = glob.glob( p_root + "/*_oreore2.fbx" )
for path in sc2in_anim_list:
	print( "  ", path.replace("\\", "/") )

print()