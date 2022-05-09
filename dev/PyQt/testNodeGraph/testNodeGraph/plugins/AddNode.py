from nodegraph.IPlugin import *


class AddNode(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'AddNode::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Float, False, True, 'Value1', 0.0 ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Float, False, True, 'Value2', 0.0 ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Float, True, False, 'Result', 1.0 ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'Add', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'AddNode::UninitializePlugin' )


    def Update(self, node):
        pass