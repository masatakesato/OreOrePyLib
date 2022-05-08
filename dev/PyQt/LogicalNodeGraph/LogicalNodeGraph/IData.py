from enum import *

class DATA_TYPE(Enum):

	DATA_TYPE_UNKNOWN   = -1

	DATA_TYPE_BOOL      = 0
	DATA_TYPE_BOOL2     = 1
	DATA_TYPE_BOOL3     = 2
	DATA_TYPE_BOOL4     = 3

	DATA_TYPE_FLOAT     = 4
	DATA_TYPE_FLOAT2    = 5
	DATA_TYPE_FLOAT3    = 6
	DATA_TYPE_FLOAT4    = 7

	DATA_TYPE_INT       = 8
	DATA_TYPE_INT2      = 9
	DATA_TYPE_INT3      = 10
	DATA_TYPE_INT4      = 11




class IData:

    def __init__(self):
        self.m_dataTypeInfo = DATA_TYPE.DATA_TYPE_UNKNOWN