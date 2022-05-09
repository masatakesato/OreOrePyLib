from common.NECommon import *



class AttribLayoutDesc:

    def __init__( self ):
        self.__m_InputAttribDescs = []
        self.__m_OutputAttribDescs = []


    def AddAttribDesc( self, desc ):

        if( desc.DataFlow()==DataFlow.Input ):
            self.__m_InputAttribDescs.append( desc )

        elif( desc.DataFlow()==DataFlow.Output ):
            self.__m_OutputAttribDescs.append( desc )


    def RemoveAttribDesc( self, desc ):

        if( desc.DataFlow()==DataFlow.Input ):
            self.__m_InputAttribDescs.remove( desc )

        elif( desc.DataFlow()==DataFlow.Output ):
            self.__m_OutputAttribDescs.remove( desc )


    def InputAttribDescs( self ):
        return self.__m_InputAttribDescs


    def OutputAttribDescs( self ):
        return self.__m_OutputAttribDescs



class NodeDesc:

    def __init__( self, objtype, layoutdesc, updater ):
        self.__m_ObjectType = objtype
        self.__m_AttribLayoutDesc = layoutdesc
        self.__m_Updater = updater


    def ObjectType( self ):
        return self.__m_ObjectType


    def InputAttribDescs( self ):
        return self.__m_AttribLayoutDesc.InputAttribDescs()


    def OutputAttribDescs( self ):
        return self.__m_AttribLayoutDesc.OutputAttribDescs()


    def Updater( self ):
        return self.__m_Updater




class NodeTypeManager:

    def __init__( self ):
        self.__m_NodeDescs = {}


    def Register( self, objType, layoutDesc, updater ):
        if( objType in self.__m_NodeDescs ):
            print( 'Warning: ObjectType "' + objType +'" already exists. Canceling registration.' )
            return False
        else:
            self.__m_NodeDescs[ objType ] = NodeDesc( objType, layoutDesc, updater )
            return True

    
    def Unregister( self, objType ):
        if( nodeType in self.__m_NodeDescs ):
            del self.__m_NodeDescs[ objType ]
            return True
        else:
            print( 'Warning: ObjectType "' + objType +'" does not exists.' )
            return False


    def GetNodeDesc( self, objType ):
        if( objType in self.__m_NodeDescs ):
            return self.__m_NodeDescs[ objType ]
        return None


    def GetNodeTypes( self ):
        return self.__m_NodeDescs.keys()