from enum import *


################### Types #######################

class GRAPHOBJ_TYPE(IntEnum):

    GRAPHOBJ_TYPE_UNKNOWN       = -1
    GRAPHOBJ_TYPE_NODE          = 0
    GRAPHOBJ_TYPE_ATTRIB          = 1
    GRAPHOBJ_TYPE_CONNECTION    = 2



class AttributeType(Enum):
	Unknown     = -1
	Input       = 0
	Output      = 1
	Internal    = 2 # internal.


class DataType(Enum):
    Unknown = -1
    Text    = 0
    Int     = 1
    Float   = 2
    Double  = 3
    Bool    = 4



################# Object ID ##################

class ObjectID:

    def __init__( self, gid, lid, typekey ):
        self.GlobalID = gid
        self.LocalID = lid
        self.ObjectTypeKey = typekey


############### Attribute Descriptor ###############

class AttribDesc:

    def __init__( self, attribtype, datatype, name, val ):
        self.__m_AttribType = attribtype
        self.__m_DataType = datatype
        self.__m_Name = name
        self.__m_DefaultValue = val


    def AttributeType( self ):
        return self.__m_AttribType


    def DataType( self ):
        return self.__m_DataType


    def Name( self ):
        return self.__m_Name


    def DefaultValue( self ):
        return self.__m_DefaultValue
