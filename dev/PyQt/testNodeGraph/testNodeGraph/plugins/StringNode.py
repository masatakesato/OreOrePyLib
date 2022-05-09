from nodegraph.IPlugin import *


class StringNode(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'StringNode::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        #layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Text, False, True, 'String', 'dss' ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Text, True, True, 'Out', 'ggg' ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'String', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'StringNode::UninitializePlugin' )


    def Update(self, node):
        pass