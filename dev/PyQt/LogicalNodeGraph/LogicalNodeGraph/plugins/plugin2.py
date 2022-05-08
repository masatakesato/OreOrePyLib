from IPlugin import *


class Plugin2(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'Plugin2::InitializePlugin' )

        # Create NodeLayoutDesc
        layoutDesc = NodeLayoutDesc()
        layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Input, DataType.Float, 'In', 0.0 ) )
        layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Output, DataType.Float, 'Out', 2.5 ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'TestNode2', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'Plugin2::UninitializePlugin' )


    def Update(self, node):
        pass