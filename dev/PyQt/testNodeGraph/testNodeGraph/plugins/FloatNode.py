from nodegraph.IPlugin import *


class FloatNode(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'FloatNode::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        #layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Float, False, 'Input1', 0.0 ) )
        #layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Text, False, 'Input2', 'textvalue' ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Float, True, True, 'Output', 1.0 ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'Float', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'FloatNode::UninitializePlugin' )


    def Update(self, node):
        pass