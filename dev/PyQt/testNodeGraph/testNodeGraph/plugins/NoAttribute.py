from nodegraph.IPlugin import *


class NoAttribute(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'NoAttribute::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        #layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Input, DataType.Bool, False, True, 'Boolean', False ) )
        #layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Input, DataType.Float, True, True, 'Input1', 0.0 ) )
        #layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Input, DataType.Text, False, True, 'Input2', 'textvalue' ) )
        #layoutDesc.AddAttribDesc( AttribDesc( AttributeType.Output, DataType.Float, True, False, 'Output', 2.5 ) )


        # Register to nodeTypeManager
        nodeTypeManager.Register( 'NoAttribute', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'NoAttribute::UninitializePlugin' )


    def Update(self, node):
        pass