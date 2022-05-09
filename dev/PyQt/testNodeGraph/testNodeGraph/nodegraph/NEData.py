from common.NECommon import DataType


class NEData:
    
    def __init__( self, dataType, value ):
        self.__m_DataType = dataType
        self.__m_Value = value


    def Value( self ):
        return self.__m_Value


    def SetValue( self, value ):
        self.__m_Value = value

