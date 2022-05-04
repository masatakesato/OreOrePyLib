
class INode():

    def __init__( self, name='' ):
        self.__m_ClassName = name
        #self.__m_LayoutDesc = AttribLayoutDesc()

        self.Initialize()


    def SetClassName( self, name ):
        self.__m_ClassName = name


    #def AddAttribute( self, attribtype, dataflow, datatype, allowmultconnect, editable, name, defaultval, connectableTypes=None ):
    #    if( connectableTypes is None ):
    #        connectableTypes = { datatype }
    #    self.__m_LayoutDesc.AddAttribDesc( AttribDesc( attribtype, dataflow, datatype, allowmultconnect, editable, name, defaultval, connectableTypes ) )


    #def Register( self, nodeTypeManager ):
    #    nodeTypeManager.Register( self.__m_ClassName, self.__m_LayoutDesc, self.Compute )


    #def Unregister( self, nodeTypeManager ):
    #    nodeTypeManager.Unregister( self.__m_ClassName )



    def Initialize( self ):
        print( 'IPlugin::Initialize()... Must be overrriden.' )


    def Compute( self, dataBlock ):
        print( 'IPlugin::Compute()... Must be overrriden.' )