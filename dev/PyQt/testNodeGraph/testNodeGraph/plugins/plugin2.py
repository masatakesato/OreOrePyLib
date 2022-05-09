from nodegraph.IPlugin import *


class Plugin2(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'Plugin2::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Float, False, True, 'In', 0.0 ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Float, True, False, 'Out', 2.5 ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'TestNode2', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'Plugin2::UninitializePlugin' )


    def Update(self, node):
        pass