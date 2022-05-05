import sys
import os
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

    envroot = pathlib.Path( executable if executable else sys.executable ).parents[0]#pathlib.Path( sys.executable ).parents[0]

    for subdir in subDirectories:
        subpath = pathlib.Path.joinpath( envroot, subdir )
        #print( subpath )
        os.environ["PATH"] += str(subpath) + ";"