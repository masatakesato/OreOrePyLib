
# http://stackoverflow.com/questions/487971/is-there-a-standard-way-to-list-names-of-python-modules-in-a-package

import os.path, pkgutil
import importlib

from IPlugin import IPlugin
from Node import Node


# import package
import plugins


def GetSubclass( module, base_class ):

    for name in dir(module):
        
        # avoid base_class - base_class comparison at issubclass()
        if( name == base_class.__name__ ):
            continue
        obj = getattr( module, name )
        try:
            if( issubclass(obj, base_class) ):
                return obj
        except TypeError:  # If 'obj' is not a class
            pass
    return None


if __name__ == '__main__':

    nnn = Node()

    # get package path
    pkgpath = os.path.dirname(plugins.__file__)

    # get package name
    pkg_name = plugins.__name__
    #print( pkg_name )

    # 
    for importer, modname, ispkg in pkgutil.iter_modules([pkgpath]):
        print( "Found submodule %s (is a package: %s)" % (modname, ispkg) )
        module = importlib.import_module( '.' + modname, pkg_name )

        # Get IPlugin's subclass
        classObj = GetSubclass( module, IPlugin )
        
        # Create Instance
        pluginInstance = classObj()
        
        pluginInstance.InitializePlugin()
        pluginInstance.Update(nnn)