import math
import traceback

from NodeTypeManager import *
from INodePlugin import INodePlugin

from DataBlock import *



class SqrdSqrtNode(INodePlugin):

    def __init__( self ):
        super(SqrdSqrtNode, self).__init__( 'SqrdSqrt' )


    def initialize( self ):
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Input, datatype=float, allowmultconnect=False, editable=True, name='Value1', val=1.0 )# 'Attribute', DataFlow.Input, DataType.Bool, False, True, 'Boolean', False )
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Output, datatype=float, allowmultconnect=True, editable=False, name='Sqrd', val=1.0 )# Output Attribute
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Output, datatype=float, allowmultconnect=True, editable=False, name='Sqrt', val=1.0  )# Output Attribute

        # Define Constant variables
        #self.a = -1000.0


    def compute( self ):
        val1 = self.GetAttrib( 'Value1' )
        return val1 * val1, math.sqrt( val1 )



    # compute callback function
    def compute_( self, datablock ):
        val = datablock.GetInput( '' )
        datablock.Output( '' )
        datablock.Constant( '' )
    #    val1 = self.GetAttrib( 'Value1' )
    #    return val1 * val1, math.sqrt( val1 )





class AddNode(INodePlugin):

    def __init__( self ):
        super(AddNode, self).__init__( 'AddNode' )


    def initialize( self ):
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Input, datatype=float, allowmultconnect=False, editable=True, name='Value1', val=1.0 )
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Input, datatype=float, allowmultconnect=False, editable=True, name='Value2', val=1.0 )
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Output, datatype=float, allowmultconnect=True, editable=False, name='Result', val=0.0 )


    def compute( self ):
        val1 = self.GetAttrib( 'Value1' )
        val2 = self.GetAttrib( 'Value2' )

        return val1 + val2




class MultNode(INodePlugin):

    def __init__( self ):
        super(MultNode, self).__init__( 'MultNode' )


    def initialize( self ):
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Input, datatype=float, allowmultconnect=False, editable=True, name='Value1', val=1.0 )
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Input, datatype=float, allowmultconnect=False, editable=True, name='Value2', val=1.0 )
        self.AddAttrib( attribtype='Attribute', dataflow=DataFlow.Output, datatype=float, allowmultconnect=True, editable=False, name='Result', val=0.0 )

    a = 33.0

    def compute( self ):
        val1 = self.GetAttrib( 'Value1' )
        val2 = self.GetAttrib( 'Value2' )

        return val1 * val2 + a