from NEScene import *

from NodeTypeManager import *
from INENodeUpdater import *

from PluginLoader import *


class NESceneManager:


    def __init__( self ):

        self.__m_Scene = None
        self.__m_NodeTypeManager = NodeTypeManager()

        # Register TestNode
        LoadNodePlugin( self.__m_NodeTypeManager )


    def BindScene( self, scene ):
        self.__m_Scene = scene
        #self.__m_Scene.RegisterNodeTypes( self.__m_NodeTypeManager.GetNodeTypes() )


    def UnbindScene( self ):
        self.__m_Scene = None


    def CreateNode( self, nodeType ):

        #print( 'NESceneManager::CreateNode' )
       
        nodeTypeInfo = self.__m_NodeTypeManager.GetNodeTypeInfo( nodeType )
        if( nodeTypeInfo == None ):
            return

        # Create Node
        newNode = self.__m_Scene.AddNode( nodeType, nodeTypeInfo )


    def DeleteNode( self, name ):
        
        #print( 'NESceneManager::DeleteNode' )

        self.__m_Scene.RemoveNode( name )



    def Rename( self, currname, newname ):

         #print( 'NESceneManager::RenameNode' )

         self.__m_Scene.RenameNode( currname, newname )


    def ConnectAttribute( self, name_source, name_dest ):

        #print( 'NESceneManager::ConnectAttribute' )

        return self.__m_Scene.AddConnection( name_source, name_dest )



    def ReconnectAttribute( self, name_target, name_source, name_dest ):

        #print( 'NESceneManager::ReconnectAttribute' )

        return self.__m_Scene.SetConnection( name_target, name_source, name_dest )


    def DisconnectAttribute( self, name_source, name_dest ):

        #print( 'NESceneManager::DisconnectAttribute' )

        self.__m_Scene.RemoveConnection( name_source, name_dest )


