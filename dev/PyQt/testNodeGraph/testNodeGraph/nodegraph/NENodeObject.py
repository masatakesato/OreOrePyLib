#from INEGraphObject import *
from .NEAttributeObject import *
	

class NENodeObject(INEGraphObject):

    def __init__( self, name, nodetype ):
        super(NENodeObject, self).__init__( name, nodetype )


    def __del__( self ):
        super(NENodeObject, self).__del__()


    def ClearAttributes( self ):
        self.ClearChildren()


    def AddAttribute( self, desc ):
        print( '  AddAttribute ' + desc.Name() )
        self.AddChild( NEAttributeObject( desc ) )


    def RemoveAttribute( self, name ):
        self.RemoveChild( self, name )


    def Attributes( self ):
        return self.Children()


    def Attribute( self, attribname ):

        if( attribname in self.Children() ):
            return self.Children()[ attribname ]
        else:
            return None