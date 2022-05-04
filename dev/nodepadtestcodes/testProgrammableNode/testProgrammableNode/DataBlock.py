from collections import defaultdict


# Data calss
class Data:

    def __init__( self, dataType, value ):
        self.__m_DataType = dataType
        self.__m_Value = value


    def Value( self ):
        return self.__m_Value


    def SetValue( self, value ):
        self.__m_Value = value



# DataBlock class
class DataBlock:

    def __init__( self ):
        
        self.__m_Inputs = defaultdict([])# 
        self.__m_Outputs = {}
        self.__m_Constants = {}


    def GetInput( self, query ):
        pass


    def SetOutput( self, query ):
        pass


    def GetConstant( self, query ):
        pass


    def SetConstant( self, query, value ):
        pass