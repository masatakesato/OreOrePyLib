import math
import traceback

from NodeTypeManager import *



class INodePlugin:

    def __init__( self, objtype ):
        self.__m_LayoutDesc = AttribLayoutDesc()
        self.__m_NodeDesc = NodeDesc( objectType=objtype, layoutdesc=self.__m_LayoutDesc )
        self.__m_Data = {}

        # 内部変数の定義もできるようにしておきたい


    def AddAttrib( self, attribtype, dataflow, datatype, allowmultconnect, editable, name, val ):
        self.__m_LayoutDesc.AddAttribDesc( AttribDesc( attribtype, dataflow, datatype, allowmultconnect, editable, name, val ) )
        self.__m_Data[ name ] = val


    def GetAttrib( self, query ):# 上流ノードと接続がある場合はそちらから値を取得する
        try:
            return self.__m_Data[ query ]
        except:
            traceback.print_exc()
            return None


    def SetAttrib( self, query, val ):
        self.__m_Data[ query ] = val


    def compute_( self, In, Out ):
        pass


    def CreateInstance( self ):
        print( 'INodePlugin::CreateInstance()...' )
        #newnode = Node( self.__m_NodeDesc )
        #newnode.BindDataBlock()
        #return newnode
        pass
