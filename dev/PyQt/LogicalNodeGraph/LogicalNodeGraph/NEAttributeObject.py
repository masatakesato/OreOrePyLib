from NECommon import *
from INEGraphObject import *




class NEAttributeObject(INEGraphObject):


    def __init__( self, desc ):#, id ):
        super().__init__( desc.Name() )#, id )

        self.__m_AttribDesc = desc
        self.__m_Data = None
        self.__m_pNode = None
        self.__m_pConnectionList	= {}


    def __del__( self ):
        self.Clear()
        super().__del__()

    
    def Clear( self ):
        self.__m_pNode = None
        self.__m_pConnectionList.clear()


    def BindNode( self, pnode ):
        self.__m_pNode = pnode


    def UnbindNode( self ):
        self.__m_pNode = None


    def	BindConnection( self, pconn ):
        self.__m_pConnectionList[ pconn.Name() ] = pconn


    def UnbindConnection( self, pconn ):
        if( pconn.Name() in self.__m_pConnectionList ):
            del self.__m_pConnectionList[ pconn.Name()] #pconn.Name() ]


    def ClearConnection( self ):
        self.__m_pConnectionList.clear()


    def IsInput( self ):
        return self.__m_AttribDesc.AttributeType() == AttributeType.Input


    def IsOutput( self ):
        return self.__m_AttribDesc.AttributeType() == AttributeType.Output


    def ConnectionList( self ):
        return self.__m_pConnectionList


    def ParentNode( self ):
        return self.__m_pNode


    def Data( self ):
        return self.__m_Data


    def DataType( self ):
        return self.__m_AttribDesc.DataType()

