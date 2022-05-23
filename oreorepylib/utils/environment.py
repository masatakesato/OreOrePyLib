import sys
import os

if sys.version_info.major >= 3:
    import pathlib



def AddPythonEnvironmentPaths( executable=None ):

    subDirectories =(
        # Library
        "Library/mingw-w64/bin",
        "Library/usr/bin",
        "Library/bin",
        # Scripts
        "Scripts",
        # bin
        "bin",
        )

    envroot = pathlib.Path( sys.executable ).parents[0] \
       if sys.version_info.major >= 3 \
       else os.path.dirname( sys.executable )


    for subdir in subDirectories:
        subpath = pathlib.Path.joinpath( envroot, subdir ) \
            if sys.version_info.major >= 3 \
            else os.path.join( envroot, subdir )
        print( subpath )
        os.environ["PATH"] += str(subpath) + ";"



AddPythonEnvironmentPaths( sys.executable )#pathlib.Path( sys.executable ) )#None )#