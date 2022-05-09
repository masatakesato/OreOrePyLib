from nodegraph.IPlugin import *


class Plugin1(IPlugin):

    def InitializePlugin( self, nodeTypeManager ):

        print( 'Plugin1::InitializePlugin' )

        # Create AttribLayoutDesc
        layoutDesc = AttribLayoutDesc()
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Bool, False, True, 'Boolean', False ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Float, True, True, 'Input1', 0.0 ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Input, DataType.Text, False, True, 'Input2', 'textvalue' ) )
        layoutDesc.AddAttribDesc( AttribDesc( DataFlow.Output, DataType.Float, True, False, 'Output', 2.5 ) )

 #TODO: Init AttribDesc using dict(key + value) like blow
 #       interface_widgets = [
 #              {'type': Text,  'name': 'Name', 'value': 'Node.002'},
 #              {'type': Float, 'name': 'x', 'value': 0.0},
 #              {'type': Float, 'name': 'y', 'value': 0.0},
 #              {'type': Float, 'name': 'z', 'value': 0.0},
 #          ]

 #       { 'Flow': In, 'Type': Float, 'Name': 'Input1', 'Value': , 'bMultiConnect': False, 'bEditable': False,  }




        # Register to nodeTypeManager
        nodeTypeManager.Register( 'TestNode', layoutDesc, INENodeUpdater() )


    def UninitializePlugin( self ):
        print( 'Plugin1::UninitializePlugin' )


    def Update(self, node):
        pass