from common.NodeTypeManager import *

from .NEAttributeObject import *
from .NEConnectionObject import *
from .NENodeObject import *
from .NEGroupObject import *




#================== Node Traversal ====================#

def DepthFirstScan( node, grouplist, nodelist ):
    
    if( isinstance(node,NENodeObject) ):
        nodelist.append( node )
    elif( isinstance(node,NEGroupObject) ):
        grouplist.append( node )
    else:
        return

    #node.Info()

    if( len(node.Children()) < 1 ):
        return

    for child in node.Children().values():
        DepthFirstScan( child, grouplist, nodelist )


#def BreadsFirstScan( root ):

#    q = queue.Queue()

#    q.put( root )

#    while not q.empty():

#        data = q.get()
#        if( isinstance( data, Node) ):
#            data.Info()

#        for child in data.Children().values():
#            q.put( child )






class NENodeGraph:

    def __init__( self ):

        self.__m_ConnectionList = {}
        self.__m_NodeList = {}


    def __del__( self ):
        self.__Clear()


    def __Clear( self ):
        self.__m_ConnectionList.clear()
        self.__m_NodeList.clear()



    #########################################################################
    #               Object Create/Delete Operation(public func)             #
    #########################################################################

    def AddNode( self, nodeDesc ):
        
        # Create Node
        newNode = self.__AddNode( nodeDesc.ObjectType() )

        # Create Input Attributes
        for desc in nodeDesc.InputAttribDescs():
            newNode.AddAttribute( desc )

        # Create Output Attributes
        for desc in nodeDesc.OutputAttribDescs():
            newNode.AddAttribute( desc )

        return newNode


    def Rename( self, currname, newname ):

        if( currname==newname ):
            print( 'name unchanged. exiting.' )
            return False

        if( newname in self.__m_NodeList ): # do not allow to overwrite to existing node
            print( 'target name ' + newname + ' already exists.' )
            return False

        node = self.GetNode( currname ) # node "currname" does not exist
        if( node == None ):
            print( 'currname ' + currname + ' does not exists.' )
            return False

        # change node key
        node.SetKey( newname )
        self.__m_NodeList[ node.Key() ] = self.__m_NodeList.pop( currname )

        return True


    def AddConnection( self, name_source, name_dest ):

        # Get Attribute
        attr_source = self.GetAttribute( name_source )
        attr_dest = self.GetAttribute( name_dest )

        # Check Connectivity
        if( self.__CheckConnectivity( attr_source, attr_dest )==False ):
            return None

        # Check existing connection
        if( self.__IsConnected( attr_source, attr_dest )==True ):
            return None

        # Create Connection Object
        newConn = self.__AddConnection()
        
        print( 'AddConnection ' + attr_source.FullKey() + ' ' + attr_dest.FullKey() )
        #print( 'AddConnection ' + attr_source.ParentName() + '.' + attr_source.Name() + ' ' + attr_dest.ParentName() + '.' + attr_dest.Name() )

        # Establish Connection
        self.__Connect( newConn, attr_source, attr_dest )

        return newConn


    def SetConnection( self, name_target, name_source, name_dest ):

        # Get Attribute
        attr_source = self.GetAttribute( name_source )
        attr_dest = self.GetAttribute( name_dest )

        # Check Connectivity
        if( self.__CheckConnectivity( attr_source, attr_dest )==False ):
            return None

        # Check existing connection
        if( self.__IsConnected( attr_source, attr_dest )==True ):
            return None

        # Get Connection object
        conn = self.GetConnection( name_target )
        if( conn==None ):
            return None

        # Remove Exsisting connection
        self.__Disconnect( conn )


        # Establish new Connection
        self.__Connect( conn, attr_source, attr_dest )

        return conn


    def SetAttribute( self, attrib_name, value ):

        attrib = self.GetAttribute( attrib_name )
        if( attrib ):
            attrib.SetValue( value )
            return True

        return False


    def RemoveConnection( self, conn_name ):

        # Check existing connection
        conn = self.GetConnection(conn_name)
        if( conn ):
            self.__RemoveConnection( conn )
            return True

        print( conn_name + ' does not exist on NodeGraph' )
        return False



    def RemoveConnectionByAttributes( self, name_source, name_dest ):

        # Get Attribute
        attr_source = self.GetAttribute( name_source )
        attr_dest = self.GetAttribute( name_dest )

        # Check Connectivity
        if( self.__CheckConnectivity( attr_source, attr_dest )==False ):
            return False

        # Check existing connection
        self.__
        conn = self.__GetConnectionByAttributes( attr_source, attr_dest )
        if( conn ):
            self.__RemoveConnection( conn )
            return True

        return False



    def RemoveNode( self, name ):

        print( 'NENodeGraph::RemoveNode ' + name )

        # Get node
        if( not(name in self.__m_NodeList) ):
            print( 'Node does not exist' )
            return False

        node = self.__m_NodeList[ name ]

        # Remove
        self.__RemoveNode( node )

        return True


    def GetConnection( self, name ):
        if( name in self.__m_ConnectionList ):
            return self.__m_ConnectionList[ name ]
        else:
            return None


    def GetAttribute( self, name ):

        #nodename, attrname = name.split('.')
        # Extract nodename and attrname
        name_components = name.split('.')
        if( len(name_components)<=1 ):
            print( 'Cannot get attribute: Invalid name. ')
            return None

        nodename = name_components[0]
        attrname = name_components[1]

        # retrieve node
        node = self.GetNode( nodename )
        if( node == None ):
            print( 'Cannot get attribute: Node ' + nodename + ' does not exist.' )
            return None
        
        # return node attribute
        return node.Attribute( attrname )


    def GetNode( self, name ):
        if( name in self.__m_NodeList ):
            return self.__m_NodeList[ name ]
        else:
            return None


    def GetObject( self, name ):
        
        obj = self.GetNode( name )

        if( obj == None ):
            obj = self.GetConnection( name )

        return obj
    

    def GetData( self, name ):

        #nodename, attrname = name.split('.')
        name_components = name.split('.')
        if( len(name_components)<=1 ):
            print( 'Cannot get attribute: Invalid name. ')
            return None

        nodename = name_components[0]
        attrname = name_components[1]


        node = self.GetNode( nodename )
        if( node == None ):
            print( 'Node ' + nodename + ' does not exist.' )
            return None

        return node.Attribute( attrname ).Data()



    def Group( self, obj_name_list ):

        # Gather Objetcs
        obj_list = []
        for obj_name in obj_name_list:
            obj_list.append( self.GetObject( obj_name ) )

        # Create Group
        newGroup = self.__Group( obj_list )

        ## Create Input Attributes
        #for desc in nodeDesc.InputAttribDescs():
        #    newNode.AddAttribute( desc )

        ## Create Output Attributes
        #for desc in nodeDesc.OutputAttribDescs():
        #    newNode.AddAttribute( desc )

        return newGroup



    def Ungroup( self, group_name ):

        print( 'NENodeGraph::Ungroup ' + group_name )

        # Get group
        group = self.GetNode( group_name )

        if( group==None ):
            return False

        # Remove group
        self.__Ungroup( group )

        return True



    #TODO: 接続先オブジェクト/アトリビュート名称のリストを出力する関数. オブジェクト名が引数
    #def ListConnections( self, object_name, flow,  ):

    #    conn_list = []

    #    self.GetNode( object_name )
    #    for attrib_name in attrib_names:
    #        conn_list += list( self.GetAttribute( attrib_name ).ConnectionList().keys() )

    #    return conn_list


    def ConnectionInfo( self, attrib_name ):

        conn_info = []

        attrib = self.GetAttribute( attrib_name )
        connectionList = attrib.ConnectionList().values()

        if( attrib.IsInput() ):
            for connection in connectionList:
                conn_info.append( connection.Source().FullKey() )

        elif( attrib.IsOutput() ):
            for connection in connectionList:
                conn_info.append( connection.Destination().FullKey() )
        
        return conn_info


    def IsConnected( self, attrib_name1, attrib_name2  ):

        attrib1 = self.GetAttribute( attrib_name1 )
        attrib2 = self.GetAttribute( attrib_name2 )

        if( attrib1==None or attrib2==None ):
            return False

        if( attrib1.IsOutput() and attrib2.IsInput() ):
            return self.__IsConnected( attrib1, attrib2 )

        elif( attrib1.IsInput() and attrib2.IsOutput() ):
            return self.__IsConnected( attrib2, attrib1 )

        else:
            return


    
    def ListOverlappedConnections( self, attrib_names ):

        conn_list = []

        for attrib_name in attrib_names:

            attrib = self.GetAttribute( attrib_name )
            if( attrib==None ): continue
            if( attrib.AllowMultiConnect()==True ): continue

            conn_list += list( self.GetAttribute( attrib_name ).ConnectionList().keys() )

        return conn_list



    def ListAllDescendants( self, node_name ):

        root_node = self.GetNode( node_name )

        if( root_node==None ):
            return None, None

        grouplist = []
        nodelist = []

        DepthFirstScan( root_node, grouplist, nodelist )

        return grouplist, nodelist



    #########################################################################
    #               Object Create/Delete Operation(private func)            #
    #########################################################################


    def __AddConnection( self ):

        #print( 'NENodeGraph::__AddConnection' )

        # Create connection object. publish unique name
        idx = 1
        while 'connector_' + str(idx) in self.__m_ConnectionList: idx += 1
        conn = NEConnectionObject( 'connector_' + str(idx) )

        # Add connection to scene
        self.__m_ConnectionList[ conn.Key() ] = conn

        return conn


    def __AddNode( self, nodeType ):

        #print( 'NENodeGraph::__AddNode' )

        # Create node Object. publish unique name
        idx = 1
        while nodeType + str(idx).zfill(3) in self.__m_NodeList: idx += 1
        node = NENodeObject( nodeType + str(idx).zfill(3), nodeType )

        # Add node to scene
        self.__m_NodeList[ node.Key() ] = node

        print( 'AddNode ' + node.Key() )

        return node



    def __Group( self, obj_list ):

        # Create group Object. publish unique name
        idx = 1
        while 'Group' + str(idx).zfill(3) in self.__m_NodeList: idx += 1
        group = NEGroupObject( 'Group' + str(idx).zfill(3), obj_list )

        # Add group to scene
        self.__m_NodeList[ group.Key() ] = group

        print( 'CreateGroup ' + group.Key() )

        return group


    def __Ungroup( self, group ):
        
        parent = group.Parent()

        # Reassign children to group's parent
        for child in group.Children().values():
            child.SetParent( parent )
        group.ClearChildren()

        # Remove gropu object
        del self.__m_NodeList[ group.Key() ]

        
    def __RemoveConnection( self, conn ):

        #print( 'NENodeGraph::__RemoveConnection' )
        src_name = conn.Source().FullKey()#conn.Source().ParentName() + '.' +  conn.Source().Key()
        dst_name = conn.Destination().FullKey()#conn.Destination().ParentName() + '.' +  conn.Destination().Key()
        print( 'RemoveConnection ' + src_name + ' ' + dst_name )

        # Break attrib-to-conn and conn-to-attrib link
        self.__Disconnect( conn )

        # Remove connection from scene
        del self.__m_ConnectionList[ conn.Key() ]



    def __RemoveNode( self, node ):

        #print( 'NENodeGraph::__RemoveNode' )
        node.ClearAttributes()
        
        # Remove node from scene
        del self.__m_NodeList[ node.Key() ]


    def __Connect( self, pconn, src, dst ):

        print( 'Connect ' + src.FullKey() + ' ' + dst.FullKey() )
        #print( 'Connect ' + src.ParentName() + '.' + src.Name() + ' ' + dst.ParentName() + '.' + dst.Name() )

        # add attrib-to-connection link
        src.BindConnection( pconn )

        # add connection-to-attrib link
        pconn.BindSource( src )

        # add attrib-to-connection link
        dst.BindConnection( pconn )

        # add connection-to-attrib link
        pconn.BindDestination( dst )


    def __ConnectSource( self, pconn, src ):

        # add attrib-to-connection link
        src.BindConnection( pconn )

        # add connection-to-attrib link
        pconn.BindSource( src )


    def __ConnectDestination( self, pconn, dst ):

        # add attrib-to-connection link
        dst.BindConnection( pconn )

        # add connection-to-attrib link
        pconn.BindDestination( dst )


    def __Disconnect( self, pconn ):

        # remove attrib-to-connection link
        pconn.Source().UnbindConnection( pconn )

        # remove connection-to-attrib link
        pconn.UnbindSource()

        # remove attrib-to-connection link
        pconn.Destination().UnbindConnection( pconn )

        # remove connection-to-attrib link
        pconn.UnbindDestination()


    def __DisconnectSource( self, pconn ):

        # remove attrib-to-connection link
        pconn.Source().UnbindConnection( pconn )

        # remove connection-to-attrib link
        pconn.UnbindSource()


    def __DisconnectDestination( self, pconn ):

        # remove attrib-to-connection link
        pconn.Destination().UnbindConnection( pconn )

        # remove connection-to-attrib link
        pconn.UnbindDestination()



    #########################################################################
    #                      Rule Check Operation(private func)               #
    #########################################################################


    def __IsConnected( self, attr_source, attr_dest ):

        for conn in attr_dest.ConnectionList().values():
            if( conn.Source() == attr_source ):
                print( ' Connection exists.' )
                return True

        return False

    
    def __GetConnectionByAttributes( self, attr_source, attr_dest ):

        for conn in attr_dest.ConnectionList().values():
            if( conn.Source() == attr_source ):
                return conn

        return None


    def __CheckConnectivity( self, attr_source, attr_dest ):

        # Check attributes' existence
        if( attr_source==None or attr_dest==None ):
            print( '  Invalid connectivity: source and/or dest is empty.' )
            return False

        # Check if in and out are connectable
        if( attr_source.IsInput() or attr_dest.IsOutput() ):
            print( '  Invalid connectivity: Unable to connect. Specity Correct [Source] and [Dest].' )
            return False
           
        # Check attribute rule
        if( attr_source.DataType() != attr_dest.DataType() ):
            print( '  Invalid connectivity: Unable to connect. Different DataType.' )
            return False


        return True
