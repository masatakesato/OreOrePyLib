#from INEGraphObject import *
from .NEAttributeObject import *
from .NENodeObject import *


class NEGroupObject(INEGraphObject):

    def __init__( self, name, graphobjlist ):
        super(NEGroupObject, self).__init__( name, 'Group' )

        self.__m_SymbolicLinks = {}# key: fullname including group name, val: reference to node attribute

        for obj in graphobjlist:

            for attrib in obj.Attributes().values():
                localkey = attrib.FullKey().replace('.', '_')
                self.__m_SymbolicLinks[ localkey ] = attrib

            self.AddChild( obj )


    def __del__( self ):
        super(NEGroupObject, self).__del__()


    def Attributes( self ):
        return self.__m_SymbolicLinks 


    def Attribute( self, attribname ):
       
        if( attribname in self.__m_SymbolicLinks ):
            return self.__m_SymbolicLinks[ attribname ]


        return None
    
    # シンボリックリンクを作る. こっちでやる？？？→ポートの可視/不可視の設定だけなので、NodeEditorUIの仕事
