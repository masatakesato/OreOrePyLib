from common.NECommon import *
from .INEGraphObject import *

from .NEData import NEData


class NEAttributeObject(INEGraphObject):


    def __init__( self, desc ):
        super().__init__( desc.Name(), 'Attribute' )

        self.__m_AttribDesc = desc
        self.__m_Data = NEData( desc.DataFlow(), desc.DefaultValue() )
        #self.__m_pNode = None
        self.__m_pConnectionList	= {}


    def __del__( self ):
        self.Clear()
        super().__del__()

    
    def Clear( self ):
        super(NEAttributeObject, self).Clear()
        #self.__m_pNode = None
        self.__m_pConnectionList.clear()


    #def BindNode( self, pnode ):
    #    self.__m_pNode = pnode


    #def UnbindNode( self ):
    #    self.__m_pNode = None


    def	BindConnection( self, pconn ):
        self.__m_pConnectionList[ pconn.Key() ] = pconn


    def UnbindConnection( self, pconn ):
        if( pconn.Key() in self.__m_pConnectionList ):
            del self.__m_pConnectionList[ pconn.Key() ]


    def ClearConnection( self ):
        self.__m_pConnectionList.clear()


    def IsInput( self ):
        return self.__m_AttribDesc.DataFlow() == DataFlow.Input


    def IsOutput( self ):
        return self.__m_AttribDesc.DataFlow() == DataFlow.Output


    def IsSymbolicLink( self ):
        return self.__m_AttribDesc.DataFlow() == DataFlow.SymbolicLink


    def AllowMultiConnect( self ):
        return self.__m_AttribDesc.AllowMultiConnect()


    def ConnectionList( self ):
        return self.__m_pConnectionList


    def Value( self ):
        return self.__m_Data.Value()

    def SetValue( self, value ):
        self.__m_Data.SetValue( value )

    def Data( self ):
        return self.__m_Data

    def SetData( self, data ):
        del self.__m_Data
        self.__m_Data = data


    def DataType( self ):
        return self.__m_AttribDesc.DataType()

