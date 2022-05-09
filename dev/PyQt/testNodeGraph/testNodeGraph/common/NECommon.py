from enum import *


################### Types #######################

class DataFlow(Enum):
    Unknown         = -1
    Input           = 0
    Output          = 1
    Internal        = 2 # internal.
    SymbolicLink    = 3


class DataType(Enum):
    Unknown = -1

    Bool    = 0
    Bool2   = 1
    Bool3   = 2
    Bool4   = 3

    Int     = 4
    Int2    = 5
    Int3    = 6
    Int4    = 7

    Float   = 8
    Float2  = 9
    Float3  = 10
    Float4  = 11

    Double  = 12
    Double2 = 13
    Double3 = 14
    Double4 = 15

    Text    = 16
    Enum    = 17

    Generic = 18


############### Attribute Descriptor ###############

class AttribDesc:

    def __init__( self, flow, datatype, allowmulticonn, editable, name, val ):
        self.__m_DataFlow = flow
        self.__m_DataType = datatype
        self.__m_bEditable = editable
        self.__m_AllowMultiConnect = allowmulticonn
        self.__m_Name = name
        self.__m_DefaultValue = val


    def DataFlow( self ):
        return self.__m_DataFlow


    def DataType( self ):
        return self.__m_DataType


    def IsEditable( self ):
        return self.__m_bEditable


    def AllowMultiConnect( self ):
        return self.__m_AllowMultiConnect


    def Name( self ):
        return self.__m_Name


    def DefaultValue( self ):
        return self.__m_DefaultValue
