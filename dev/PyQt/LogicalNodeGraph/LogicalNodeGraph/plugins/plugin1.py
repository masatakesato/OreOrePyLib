from IPlugin import *


class Plugin1(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'Plugin1::InitializePlugin' )

        # Create NodeLayoutDesc
        layoutDesc = NodeLayoutDesc()
        layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Input, DataType.Float, 'Input1', 0.0 ) )
        layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Input, DataType.Text, 'Input2', 'textvalue' ) )
        layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Output, DataType.Float, 'Output', 2.5 ) )

        # Register to nodeTypeManager
        nodeTypeManager.Register( 'TestNode', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'Plugin1::UninitializePlugin' )


    def Update(self, node):
        pass