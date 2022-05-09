from common.NodeTypeManager import *
from .INENodeUpdater import INENodeUpdater


class IPlugin():

    def InitializePlugin( self, nodeTypeManager ):
        pass


    def UninitializePlugin( self, nodeTypeManager ):
        pass
