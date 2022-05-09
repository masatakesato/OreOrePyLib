from nodegraph.IPlugin import *


class Plugin3(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'Plugin3::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Text, False, True, 'In', 'Value' ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Float, True, False, 'Out', 2.5 ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Float, True, False, 'Out2', 2.5 ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'TestNode3', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'Plugin3::UninitializePlugin' )


    def Update(self, node):
        pass