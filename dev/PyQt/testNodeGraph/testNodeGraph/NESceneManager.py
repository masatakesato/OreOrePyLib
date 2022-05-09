from common.NodeTypeManager import *
from nodegraph.NENodeGraph import *
from nodegraph.INENodeUpdater import *
from nodegraph.PluginLoader import *

from graphics.NodeEditorUI import NodeEditorUI, GraphicsView
#from graphics.AttributeEditorUI import AttributeEditorUI


class NESceneManager:


    def __init__( self ):

        self.__m_NodeTypeManager = NodeTypeManager()
        self.__m_NodeGraph = None
        self.__m_NodeEditorUI = None
#        self.__m_AttributeEditorUI = None



        # Register TestNode
        LoadNodePlugin( self.__m_NodeTypeManager )


    #====================== SceneManager Setup ==============================#

    def BindNodeGraph( self, nodegraph ):
        self.__m_NodeGraph = nodegraph


    def UnbindNodeGraph( self ):
        self.__m_NodeGraph = None


    def BindNodeEditorUI( self, scene ):
        self.__m_NodeEditorUI = scene
        self.__m_NodeEditorUI.BindSceneManager( self )


    def UnbindNodeEditorUI( self ):
        self.__m_NodeEditorUI.UnbindSceneManager()
        self.__m_NodeEditorUI = None


    #def BindAttributeEditorUI( self, editorui ):
    #    self.__m_AttributeEditorUI = editorui
    #    self.__m_AttributeEditorUI.BindSceneManager( self )


    #def UnbindAttributeEditorUI( self ):
    #    self.__m_AttributeEditorUI.UnbindSceneManager()
    #    self.__m_AttributeEditorUI = None


    def NodeTypeManager( self ):
        return self.__m_NodeTypeManager


    
    #====================== NodeGraph Edit Command Execution =======================#
    # TODO: refactor parameters
    def ExecCommand( self, commandbuffer ):

        print( 'SceneManager::ExecComand: ', end='' )

        for string in commandbuffer:
            print( str(string) + ' ', end='' )
        print('')
        
        if( commandbuffer[0] == 'CreateNode' ):
            self.CreateNode_Exec( commandbuffer[1], commandbuffer[2], commandbuffer[3] )

        elif( commandbuffer[0] == 'Connect' ):
            self.Connect_Exec( commandbuffer[1], commandbuffer[2] )

        elif( commandbuffer[0] == 'Disconnect' ):
            self.Disconnect_Exec( commandbuffer[1] )

        elif( commandbuffer[0] == 'SetAttribute' ):# TODO: Refactor after marging 2016.08.09
            self.SetAttribute_Exec( commandbuffer[1], commandbuffer[2] )

        elif( commandbuffer[0] == 'SetName' ):# TODO: SetName to Rename!! 2016.08.09
            self.Rename_Exec( commandbuffer[1], commandbuffer[2] )

        elif( commandbuffer[0] == 'ConnectionInfo' ):
            self.ConnectionInfo_Exec( commandbuffer[1] )

        elif( commandbuffer[0] == 'Group' ):
            self.Group_Exec( commandbuffer[1:] )

        elif( commandbuffer[0] == 'Ungroup' ):
            self.Ungroup_Exec( commandbuffer[1] )

        #elif( commandbuffer[0] == 'RemoveNode' ):
        #    self.RemoveNode_Exec( commandbuffer )

        #elif( commandbuffer[0] == 'RemoveGroup' ):
        #    self.RemoveGroup_Exec( commandbuffer )


        elif( commandbuffer[0] =='Delete' ):
            self.Delete_Exec( commandbuffer )




    def CreateNode_Exec( self, nodetype, posx, posy ):
        
        # Create Node in NodeGraph
        nodeDesc = self.__m_NodeTypeManager.GetNodeDesc( nodetype )
        if( nodeDesc == None ):
            return False

        newNode = self.__m_NodeGraph.AddNode( nodeDesc )

        # Create Node in NodeEditorUI
        if( newNode ):
            self.__m_NodeEditorUI.CreateNode_Exec( newNode.Key(), nodetype, posx, posy )
            return True

        return False


    def RemoveNode_Exec( self, node_name ):

        result = False

        # Break connections from NodeGraph/NodeEditorUI
        conn_name_list = self.__m_NodeEditorUI.GatherRemoveCandidateConnections( node_name )
        for conn_name in conn_name_list:
            self.Disconnect_Exec( conn_name )

        # remove node in NodeGraph
        result = self.__m_NodeGraph.RemoveNode( node_name )
        # Remove node in NodeEditorUI 
        self.__m_NodeEditorUI.RemoveNode_Exec( node_name )

        return result



    def Connect_Exec( self, name_source, name_dest ):


        if( self.__m_NodeGraph.IsConnected( name_source, name_dest ) ):
            return False

        # Gather Remove candidates
        removeconns = self.__m_NodeGraph.ListOverlappedConnections( [name_source, name_dest] )

        # Create Connection in NodeGraph
        newConn = self.__m_NodeGraph.AddConnection( name_source, name_dest )

        if( newConn==None ):
            return False

        # Delete existing connection if needed
        for conn_name in removeconns:
            self.Disconnect_Exec( conn_name )

        # Create Connection in NodeEditorUI
        self.__m_NodeEditorUI.Connect_Exec( newConn.Key(), name_source, name_dest )

        return True



    def Disconnect_Exec( self, conn_name ):

        result = False

        # Disconnect in NodeGraph
        result = self.__m_NodeGraph.RemoveConnection( conn_name )
        # Disconnect in NodeEditorUI
        result &= self.__m_NodeEditorUI.Disconnect_Exec( conn_name )
        
        return result


    def SetAttribute_Exec( self, attrib_name, value ):

        result = False
        
        # Set Attribute in NodeGraph
        result = self.__m_NodeGraph.SetAttribute( attrib_name, value )
        
        # Set Attribute in AttributeEditorUI
        #if( result == True ):
        #    self.__m_AttributeEditorUI.SetValue_Exec( attrib_name, value )


        return result


    def Rename_Exec( self, currname, newname ):
        
        newname = newname.replace('.', '_') # convert irregal character'.' to '_'
        
        # Rename in NodeGraph
        result = self.__m_NodeGraph.Rename( currname, newname )
        
        # Rename in NodeEditorUI
        if( result == True ):
            result = self.__m_NodeEditorUI.Rename_Exec( currname, newname )

        # if failed, resotore to current name
        #if( result == False ):
        #    self.__m_AttributeEditorUI.Rename_Exec( currname )
        #elif( newname != commandbuffer[2] ):
        #    self.__m_AttributeEditorUI.Rename_Exec( newname )

        return result


        #if( self.__m_NodeGraph.Rename( currname, newname )==True ):
        #    # Setname in NodeEditorUI
        #    self.__m_NodeEditorUI.Rename_Exec( currname, newname )
        #    return True

        #return False
        

    def Select_Exec( self, commandbuffer ):

        result = False
        target_name = commandbuffer[1]
        
        #if( commandbuffer[1] =='-clear' ):
        #self.__m_AttributeEditorUI.DeinitializeWidget()

        # select node object 
        node = self.__m_NodeGraph.GetNode( target_name )
        if( node==None ):
            return False
        
        # initialize widget
        nodedesc = self.__m_NodeTypeManager.GetNodeDesc( node.ObjectType() )
        #self.__m_AttributeEditorUI.InitializeWidget( nodedesc, target_name )
        
        ## set in-values to widget
        #for desc in nodedesc.InputAttribDescs():
        #    attribname = target_name + '.' + desc.Name()
            
        #    data = self.__m_NodeGraph.GetData( attribname )
        #    self.__m_AttributeEditorUI.SetValue_Exec( desc.Name(), data.Value() )
        #    print( attribname + ': ' + str(data.Value()) )

        ## set out-values to widget
        #for desc in nodedesc.OutputAttribDescs():
        #    attribname = target_name + '.' + desc.Name()
            
        #    data = self.__m_NodeGraph.GetData( attribname )
        #    self.__m_AttributeEditorUI.SetValue_Exec( desc.Name(), data.Value() )
        #    print( attribname + ': ' + str(data.Value()) )

        return True


    #def ListConnections_Exec( self, commandbuffer ):

    #    objname = commmandbuffer[0]#: objname
    #    flow = commandbuffer[1]#: source/dest/all ?

    #    self.__m_NodeGraph.ListConnections()
    #    connList = []


    #    return 


    def ConnectionInfo_Exec( self, attrib_name ):
        
        connectioninfo = self.__m_NodeGraph.ConnectionInfo( attrib_name )

        print( connectioninfo )



    def Group_Exec( self, obj_name_list ):

        group_node = self.__m_NodeGraph.Group( obj_name_list )

        if( group_node==None ):
            return False

        self.__m_NodeEditorUI.Group_Exec( group_node.Key(), obj_name_list )

        return True



    def Ungroup_Exec( self, group_name ):

        result = False

        # Do Ungrouping in NodeGraph
        result = self.__m_NodeGraph.Ungroup( group_name )

        # Remove node in NodeEditorUI
        self.__m_NodeEditorUI.Ungroup_Exec( group_name )

        return result


    def RemoveGroup_Exec( self, conn_name ):

        # Gather Groups and Nodes to delete
        grouplist, nodelist = self.__m_NodeGraph.ListAllDescendants( conn_name )
        
        # Ungroup all group objects inside descendant_list
        for group in grouplist:
            self.Ungroup_Exec( group.FullKey() )

        # Then Remove all child objects
        for node in nodelist:
            self.RemoveNode_Exec( node.FullKey() )




    def Delete_Exec( self, commandbuffer ):

        obj_name_list = commandbuffer[1:]

        for obj_name in obj_name_list:

            obj = self.__m_NodeGraph.GetObject( obj_name )

            if( obj==None ):
                continue

            if( isinstance(obj, NENodeObject) ):
                self.RemoveNode_Exec( obj.FullKey() )

            elif( isinstance(obj, NEGroupObject) ):
                self.RemoveGroup_Exec( obj.FullKey() )

            elif( isinstance(obj, NEConnectionObject) ):
                self.Disconnect_Exec( obj.FullKey() )


    #def Duplicate_Exec( self, commandbuffer ):

    #    NodeEditorUIから、選択したオブジェクト名称のリストを取得

    #    NodeGraph.ConnectionInfo( dest)使って、選択オブジェクトが目的地の接続元オブジェクトリストを取得

    #    接続元オブジェクトリストから、選択オブジェクトに含まれるものだけ抽出して、コネクションオブジェクトを生成する





    #====================== NodeGraph Editing Functions ============================#

    def CreateNode( self, nodeType ):

        #print( 'NESceneManager::CreateNode' )
       
        nodeDesc = self.__m_NodeTypeManager.GetNodeDesc( nodeType )
        if( nodeDesc == None ):
            return ''

        # Create Node
        newNode = self.__m_NodeGraph.AddNode( nodeDesc )

        return newNode.Key()


    def DeleteNode( self, name ):
        
        #print( 'NESceneManager::DeleteNode' )

        self.__m_NodeGraph.RemoveNode( name )


    def Rename( self, currname, newname ):

         #print( 'NESceneManager::RenameNode' )

         self.__m_NodeGraph.RenameNode( currname, newname )


    def Connect( self, name_source, name_dest ):

        #print( 'NESceneManager::ConnectAttribute' )
        newConn = self.__m_NodeGraph.AddConnection( name_source, name_dest )

        if( newConn == None ):
            return ''

        return newConn.Key()


    def Reconnect( self, name_target, name_source, name_dest ):

        #print( 'NESceneManager::ReconnectAttribute' )

        return self.__m_NodeGraph.SetConnection( name_target, name_source, name_dest )


    def Disconnect( self, conn_name ):

        #print( 'NESceneManager::Disconnect' )
        self.__m_NodeGraph.RemoveConnection_( conn_name )


    def DisconnectByAttributes( self, name_source, name_dest ):

        #print( 'NESceneManager::DisconnectByAttributes' )

        self.__m_NodeGraph.RemoveConnectionByAttributes( name_source, name_dest )


