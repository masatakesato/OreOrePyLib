from NECommon import *



class AttribLayoutDesc:

    def __init__( self ):
        self.__m_AttribDescs = { DataFlow.Input:list(), DataFlow.Output:[] }


    def Release( self ):
        self.__m_AttribDescs[ DataFlow.Input ].clear()
        self.__m_AttribDescs[ DataFlow.Output ].clear()


    def AddAttribDesc( self, desc, index=None ):
        if( index==None ):
            self.__m_AttribDescs[ desc.DataFlow() ].append( desc )
        else:
            self.__m_AttribDescs[ desc.DataFlow() ].insert( index, desc ) 


    def RemoveAttribDesc( self, desc ):
        self.__m_AttribDescs[ desc.DataFlow() ].remove( desc )


    def NumInputAttribDescs( self ):
        return len( self.__m_AttribDescs[ DataFlow.Input ] )


    def InputAttribDescs( self ):
        return self.__m_AttribDescs[ DataFlow.Input ]


    def NumOutputAttribDescs( self ):
        return len( self.__m_AttribDescs[ DataFlow.Output ] )


    def OutputAttribDescs( self ):
        return self.__m_AttribDescs[ DataFlow.Output ]


    def ChangeOrder( self, src_idx, dst_idx, dataflow ):
        self.__m_AttribDescs[ dataflow ].insert( dst_idx, self.__m_AttribDescs[ dataflow ].pop(src_idx) )


    def Sort( self, order, dataflow ):
        self.__m_AttribDescs[ dataflow ] = [ x for _,x in sorted(zip(order, self.__m_AttribDescs[ dataflow ])) ]




class NodeDesc:

    def __init__( self, *, objectType='', layoutdesc=None, enabled=True, updater=None ):
        self.__m_ObjectType = objectType
        self.__m_AttribLayoutDesc = layoutdesc
        self.__m_Enabled = enabled

        self.__m_Updater = updater
        self.__m_ObjectID = None


    def Release( self ):
        self.__m_AttribLayoutDesc.Release()


    def ObjectID( self ):
        return self.__m_ObjectID


    def SetObjectType( self, objectType ):
        self.__m_ObjectType = objectType


    def ObjectType( self ):
        return self.__m_ObjectType


    def SetAttribLayoutDesc( self, layoutdesc ):
        self.__m_AttribLayoutDesc = layoutdesc


    def InputAttribDescs( self ):
        return self.__m_AttribLayoutDesc.InputAttribDescs()


    def OutputAttribDescs( self ):
        return self.__m_AttribLayoutDesc.OutputAttribDescs()


    def SetEnable( self, flag ):
        self.__m_Enabled = flag


    def Enabled( self ):
        return self.__m_Enabled


    def SetUpdater( self, updater ):
        self.__m_Updater = updater


    def Updater( self ):
        return self.__m_Updater




class NodeTypeManager:

    def __init__( self ):
        self.__m_NodeDescs = {}
        self.__m_Index = []


    def Release( self ):
        for desc in self.__m_NodeDescs.values(): desc.Release()
        self.__m_NodeDescs.clear()
        self.__m_Index.clear()


    def Register( self, objectType, layoutDesc, updater ):
        if( objectType in self.__m_NodeDescs ):
            print( 'Warning: NodeType "' + objectType +'" already exists. Canceling registration.' )
            return False
        else:
            self.__m_NodeDescs[ objectType ] = NodeDesc( objectType, layoutDesc, updater )
            self.__m_Index.append( objectType )
            return True

    
    def Unregister( self, objectType ):
        if( objectType in self.__m_NodeDescs ):
            del self.__m_NodeDescs[ objectType ]
            self.__m_Index.remove(objectType)
            return True
        else:
            print( 'Warning: NodeType "' + objectType +'" does not exists.' )
            return False


    def GetNodeDesc( self, objectType ):
        if( objectType in self.__m_NodeDescs ):
            return self.__m_NodeDescs[ objectType ]
        return None


    def GetNodeDescByIndex( self, idx ):
        try:
            return self.__m_NodeDescs[ self.__m_Index[idx] ]
        except:
            return None


    def NumNodeDescs( self ):
        return len(self.__m_Index)

