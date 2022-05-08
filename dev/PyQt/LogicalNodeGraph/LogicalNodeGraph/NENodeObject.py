#from INEGraphObject import *
from NEAttributeObject import *
	

class NENodeObject(INEGraphObject):

    def __init__( self, name ):#, id=-1 ):
        super().__init__( name )#, id )

        self.__m_pInputAttribList = {}
        self.__m_pOutputAttribList = {}


    def __del__( self ):
        self.Clear()
        super().__del__()


    def Clear( self ):
        self.__m_pInputAttribList.clear()
        self.__m_pOutputAttribList.clear()


    def AddAttribute( self, attrib ):
        if( attrib.IsInput() ):
            self.__m_pInputAttribList[ attrib.Name() ] = attrib
        else:
            self.__m_pOutputAttribList[ attrib.Name() ] = attrib

        attrib.BindNode( self )
        

    def RemoveAttribute( self, attrib ):

        if( attrib.IsInput() and attrib.Name() in self.__m_pInputAttribList ):
            del self.__m_pInputAttribList[ attrib.Name() ]

        elif( attrib.IsOutput() and attrib.Name() in self.__m_pOutputAttribList ):
            del self.__m_pOutputAttribList[ attrib.Name() ]


    def InputAttributes( self ):
        return self.__m_pInputAttribList


    def OutputAttributes( self ):
        return self.__m_pOutputAttribList


    def InputAttribute( self, attribname ):

        if( attribname in self.__m_pInputAttribList ):
            return self.__m_pInputAttribList[ attribname ]

        else:
            return None


    def OutputAttribute( self, attribname ):

        if( attribname in self.__m_pOutputAttribList ):
            return self.__m_pOutputAttribList[ attribname ]

        else:
            return None


    def Attribute( self, attribname ):

        if( attribname in self.__m_pInputAttribList ):
            return self.__m_pInputAttribList[ attribname ]

        elif( attribname in self.__m_pOutputAttribList ):
            return self.__m_pOutputAttribList[ attribname ]

        else:
            return None