from NECommon import *



class NodeLayoutDesc:

    def __init__( self ):
        self.__m_InputAttribDescs = []
        self.__m_OutputAttribDescs = []


    def AddAttribDesc( self, desc ):

        if( desc.AttributeType()==AttributeType.Input ):
            self.__m_InputAttribDescs.append( desc )

        elif( desc.AttributeType()==AttributeType.Output ):
            self.__m_OutputAttribDescs.append( desc )


    def RemoveAttribDesc( self, desc ):

        if( desc.AttributeType()==AttributeType.Input ):
            self.__m_InputAttribDescs.remove( desc )

        elif( desc.AttributeType()==AttributeType.Output ):
            self.__m_OutputAttribDescs.remove( desc )


    def InputAttribDescs( self ):
        return self.__m_InputAttribDescs


    def OutputAttribDescs( self ):
        return self.__m_OutputAttribDescs



class NodeTypeInfo:

    def __init__( self, name, layputdesc, updater ):
        self.__m_Name = name
        self.__m_NodeLayoutDesc = layputdesc
        self.__m_Updater = updater


    def Name( self ):
        return self.__m_Name


    def InputAttribDescs( self ):
        return self.__m_NodeLayoutDesc.InputAttribDescs()


    def OutputAttribDescs( self ):
        return self.__m_NodeLayoutDesc.OutputAttribDescs()


    def Updater( self ):
        return self.__m_Updater




class NodeTypeManager:

    def __init__( self ):
        self.__m_NodeTypes = {}


    def Register( self, nodeType, layoutDesc, updater ):
        if( nodeType in self.__m_NodeTypes ):
            print( 'Warning: NodeType "' + nodeType +'" already exists. Canceling registration.' )
            return False
        else:
            self.__m_NodeTypes[ nodeType ] = NodeTypeInfo( nodeType, layoutDesc, updater )
            return True

    
    def Unregister( self, nodeType ):
        if( nodeType in self.__m_NodeTypes ):
            del self.__m_NodeTypes[ nodeType ]
            return True
        else:
            print( 'Warning: NodeType "' + nodeType +'" does not exists.' )
            return False


    def GetNodeTypeInfo( self, nodeType ):
        if( nodeType in self.__m_NodeTypes ):
            return self.__m_NodeTypes[ nodeType ]
        return None


    def GetNodeTypes( self ):
        return self.__m_NodeTypes.keys()