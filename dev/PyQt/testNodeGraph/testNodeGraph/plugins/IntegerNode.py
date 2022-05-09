from nodegraph.IPlugin import *


class IntegerNode(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'IntegerNode::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        #layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Float, False, 'Input1', 0.0 ) )
        #layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Text, False, 'Input2', 'textvalue' ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Int, True, True, 'Output', 0 ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'Integer', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'IntegerNode::UninitializePlugin' )


    def Update(self, node):
        pass