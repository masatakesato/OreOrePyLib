import json




class_type = 'AddNode'
class_key = 'Add'

code = '''
from nodegraph.IPlugin import *


class AddNode(IPlugin):

    def __init__(self):
        super(AddNode, self).__init__( 'Add' )


    def Initialize( self ):
        print( 'AddNode::Initialize()...' )
        
        # Set Classname
        #self.SetClassName( 'Add' )

        # Add attributes
        self.AddAttribute( 'Attribute', DataFlow.Input, float, False, True, 'Value1', 5.0, {int, float, bool} )
        self.AddAttribute( 'Attribute', DataFlow.Input, float, False, True, 'Value2', 0.5, {int, float, bool} )
        self.AddAttribute( 'Attribute', DataFlow.Output, float, True, False, 'Result', 1.0 )


    def Compute( self, dataBlock ):
        print( 'AddNode::Compute()...' )
        
        value1 = dataBlock.GetInput( 'Value1' )# 複数ある場合はlistに詰めたデータがほしい
        value2 = dataBlock.GetInput( 'Value2' )# 複数ある場合はlistに詰めたデータがほしい

        dataBlock.SetOutput( 'Result', float(value1) + float(value2) )

        print( 'Value1:', value1 )
        print( 'Value2:', value2 )

        print( 'Result:', dataBlock.GetOutput('Result') )


'''


print( "//================== Saving code to sample.json file ====================//" )
json_str = { 'class_name': class_type, 'key': class_key, 'impl': code  }

with open( 'sample.json', 'w' ) as f:
    json.dump( json_str, f )

print( "...Done\n" )


print( "//================== Loading sample.json file ====================//\n" )
with open( 'sample.json', 'r' ) as f:
    code_dict = json.load(f)


for k, v in code_dict.items():
    print( "--------------------", k, "--------------------\n" )
    print( v )
    print()
