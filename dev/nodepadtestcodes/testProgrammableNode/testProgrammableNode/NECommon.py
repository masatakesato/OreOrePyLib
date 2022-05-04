from enum import *


################### Types #######################

class DataFlow(IntEnum):
    Unknown         = -1
    Input           = 0
    Output          = 1
    Internal        = 2 # internal.


class DataType(IntEnum):
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



class ConnectionMode:
    Disabled = 0
    Single = 1
    Multiple = 2



############### Attribute Descriptor ###############

class AttribDesc:

    def __init__( self, attribtype, flow, datatype, allowmultconnect, editable, name, val ):
        self.__m_AttribType = attribtype
        self.__m_DataFlow = flow
        self.__m_DataType = datatype
        self.__m_bEditable = editable
        self.__m_Enabled = True
        self.__m_AllowMultiConnect = allowmultconnect
        self.__m_Name = name
        self.__m_DefaultValue = val

        self.__m_ObjectID = None


    def SetAttributeType( self, attribtype ):
        self.__m_AttribType = attribtype


    def SetDataFlow( self, flow ):
        self.__m_DataFlow = flow


    def SetDataType( self, datatype ):
        self.__m_DataType = datatype


    def SetEditable( self, flag ):
        self.__m_bEditable = flag


    def SetEnable( self, flag ):
        self.__m_Enabled = flag


    def SetAllowMultiConnect( self, flag ):
        self.__m_AllowMultiConnect = flag


    def SetName( self, name ):
        self.__m_Name = name


    def SetDefaultValue( self, value ):
        self.__m_DefaultValue = value



    def ObjectID( self ):
        return self.__m_ObjectID


    def AttributeType( self ):
        return self.__m_AttribType


    def DataFlow( self ):
        return self.__m_DataFlow


    def IsInputFlow( self ):
        return self.__m_DataFlow==DataFlow.Input


    def IsOutputFlow( self ):
        return self.__m_DataFlow == DataFlow.Output


    def DataType( self ):
        return self.__m_DataType


    def IsEditable( self ):
        return self.__m_bEditable


    def Enabled( self ):
        return self.__m_Enabled


    def MultipleConnectAllowed( self ):
        return self.__m_AllowMultiConnect


    def Name( self ):
        return self.__m_Name


    def DefaultValue( self ):
        return self.__m_DefaultValue