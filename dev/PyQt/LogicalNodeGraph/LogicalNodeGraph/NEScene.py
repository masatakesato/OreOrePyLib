#from ObjectIDManager import *
from NodeTypeManager import *

from NEAttributeObject import *
from NEConnectionObject import *
from NENodeObject import *



class NEScene:

    def __init__( self ):

        #self.__m_AttributeList = {}
        self.__m_ConnectionList = {}
        self.__m_NodeList = {}
        #self.__m_ObjectIDManager = ObjectIDManager()

        # TODO: 自動で一括登録する方法あるか
        #self.__m_ObjectIDManager.Register( 'TestNode' )
        #self.__m_ObjectIDManager.Register( 'Attribute' )
        #self.__m_ObjectIDManager.Register( 'Connection' )
        
        #self.__m_NodeKey = {} # key: node fullname, value: global id
        #self.__m_AttributeKey = {} # key: attrib fullname, value: global id
        #self.__m_ConnectionKey = {} # key: connection fullname, value: global id


    def __del__( self ):
        self.__Clear()


    def __Clear( self ):
        #self.__m_AttributeList.clear()
        self.__m_ConnectionList.clear()
        self.__m_NodeList.clear()


    #def RegisterNodeTypes( self, nodetypes ):
    #    for type in nodetypes:
    #        self.__m_ObjectIDManager.Register( type )


    #########################################################################
    #               Object Create/Delete Operation(public func)             #
    #########################################################################

    def AddNode( self, nodeType, nodeTypeInfo ):
        
        # Create Node
        newNode = self.__AddNode( nodeType )

        # Create Input Attributes
        for desc in nodeTypeInfo.InputAttribDescs():
            self.__AddAttribute( desc, newNode )

        # Create Output Attributes
        for desc in nodeTypeInfo.OutputAttribDescs():
            self.__AddAttribute( desc, newNode )

        return newNode


    def RenameNode( self, currname, newname ):

        if( currname==newname ):
            print( 'name unchanged. exiting.' )
            return False

        if( newname in self.__m_NodeList ): #__m_NodeKey ): # do not allow existing name
            print( 'target name ' + newname + ' already exists.' )
            return False

        node = self.GetNode( currname ) # node "currname" does not exist
        if( node == None ):
            print( 'currname ' + currname + ' does not exists.' )
            return False

        print( 'RenameNode ' + currname + ' ' + newname )

        # change node name
        node.SetName( newname )
        self.__m_NodeList[ node.Name() ] = self.__m_NodeList.pop( currname )
        #self.__m_NodeKey[ node.Name() ] = self.__m_NodeKey.pop( currname )


    def AddConnection( self, name_source, name_dest ):

        # Get Attribute
        attr_source = self.GetAttribute( name_source )
        attr_dest = self.GetAttribute( name_dest )

        # Check Connectivity
        if( self.__CheckConnectivity( attr_source, attr_dest )==False ):
            return None

        # Check existing connection
        newConn = self.__IsConnected( attr_source, attr_dest )
        if( newConn ):
            return newConn

        # Create Connection Object
        newConn = self.__AddConnection()
        
        print( 'AddConnection ' + attr_source.ParentNode().Name() + '.' + attr_source.Name() + ' ' + attr_dest.ParentNode().Name() + '.' + attr_dest.Name() )

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
        conn = self.__IsConnected( attr_source, attr_dest )
        if( conn ):
            return conn

        # Get Connection object
        conn = self.GetConnection( name_target )
        if( conn==None ):
            return None

        # Remove Exsisting connection
        self.__Disconnect( conn )


        # Establish new Connection
        self.__Connect( conn, attr_source, attr_dest )

        return conn


    def RemoveConnection( self, name_source, name_dest ):

        # Get Attribute
        attr_source = self.GetAttribute( name_source )
        attr_dest = self.GetAttribute( name_dest )

        # Check Connectivity
        if( self.__CheckConnectivity( attr_source, attr_dest )==False ):
            return False

        # Check existing connection
        conn = self.__IsConnected( attr_source, attr_dest )
        if( conn ):
            
            self.__RemoveConnection( conn )
            return True

        return False



    def RemoveNode( self, name ):

        print( 'RemoveNode ' + name )

        # Get node
        if( not(name in self.__m_NodeList) ):#if( not(name in self.__m_NodeKey) ):
            print( 'Node does not exist' )
            return False

        node = self.__m_NodeList[ name ]# self.__m_NodeKey[name] ]

        # Remove
        self.__RemoveNode( node )



    def GetConnection( self, name ):
        if( name in self.__m_ConnectionList ):
            return self.__m_ConnectionList[ name ]
        else:
            return None

    
    def GetAttribute( self, name ):

        nodename, attrname = name.split('.')

        node = self.GetNode( nodename )
        if( node == None ):
            print( 'Node ' + nodename + ' does not exist.' )
            return None

        return node.Attribute( attrname )

        #if( name in self.__m_AttributeKey ):
        #    return self.__m_AttributeList[ self.__m_AttributeKey[name] ]
        #else:
        #    return None


    def GetNode( self, name ):
        if( name in self.__m_NodeList ):
            return self.__m_NodeList[ name ]
        else:
            return None

        #if( name in self.__m_NodeKey ):
        #    return self.__m_NodeList[ self.__m_NodeKey[name] ]
        #else:
        #    return None



    #########################################################################
    #               Object Create/Delete Operation(private func)            #
    #########################################################################

    # Create new attribute object
    def __AddAttribute( self, desc, node ):

        #print( 'NEScene::__AddAttribute' )
        
        print( '  AddAttribute ' + node.Name() + '.' + desc.Name() )

        # Publish ObjectID
        #id = self.__m_ObjectIDManager.Publish( 'Attribute' )

        # Create attribute object
        attrib = NEAttributeObject( desc )#, id )

        # register attrib as node's child
        node.AddAttribute( attrib )

        # set attrib's parent node
        attrib.BindNode( node )

        return attrib


    def __AddConnection( self ):

        #print( 'NEScene::__AddConnection' )

        # Publish Object ID
        #id = self.__m_ObjectIDManager.Publish( 'Connection' )

        # Create connection Object. publish unique name
        idx = 1
        while 'connector_' + str(idx) in self.__m_ConnectionList: idx += 1
        conn = NEConnectionObject( 'connector_' + str(idx) )#, id )#NEConnectionObject( 'connector_' + str(id.GlobalID), id )

        # Add connection to scene
        self.__m_ConnectionList[ conn.Name() ] = conn#id.GlobalID ] = conn

        # Add fullname to dictionary
        #self.__m_ConnectionKey[ conn.Name() ] = id.GlobalID

        return conn


    def __AddNode( self, nodeType ):

        #print( 'NEScene::__AddNode' )

        # Publish ObjectID
        #id = self.__m_ObjectIDManager.Publish( nodeType )

        # Create node Object. publish unique name
        idx = 1
        while nodeType + str(idx).zfill(3) in self.__m_NodeList: idx += 1
        node = NENodeObject( nodeType + str(idx).zfill(3) )#, id )#nodeType + str(id.LocalID).zfill(3), id )

        # Add node to scene
        self.__m_NodeList[ node.Name() ] = node #id.GlobalID ] = node

        # Add full name of the node to dictionary
        #self.__m_NodeKey[ node.Name() ] = id.GlobalID

        print( 'AddNode ' + node.Name() )

        return node


    def __RemoveAttribute( self, attrib ):

        #print( 'NEScene::__RemoveAttribute' )

        fullname = attrib.ParentNode().Name() + '.' + attrib.Name()
        print( '  RemoveAttribute ' + fullname )

        # Remove linked Connections
        for conn in list(attrib.ConnectionList().values()):
            self.__RemoveConnection( conn )
        attrib.Clear()

        # Discard ObjectID
        #id = attrib.GlobalID()
        #self.__m_ObjectIDManager.Discard( attrib.ObjectID() )

        # Remove attribute from scene
        #del self.__m_AttributeKey[ fullname ]
        #del self.__m_AttributeList[ id ]

        
    def __RemoveConnection( self, conn ):

        #print( 'NEScene::__RemoveConnection' )
        src_name = conn.Source().ParentNode().Name() + '.' +  conn.Source().Name()
        dst_name = conn.Destination().ParentNode().Name() + '.' +  conn.Destination().Name()
        print( 'RemoveConnection ' + src_name + ' ' + dst_name )


        # Break attrib-to-conn and conn-to-attrib link
        self.__Disconnect( conn )

        # Discard ObjectID
        #id = conn.GlobalID()
        #self.__m_ObjectIDManager.Discard( conn.ObjectID() )


        # Remove attrib from scene
        #del self.__m_ConnectionKey[ conn.Name() ]
        del self.__m_ConnectionList[ conn.Name() ] #id ]


    def __RemoveNode( self, node ):

        #print( 'NEScene::__RemoveNode' )

        # Remove Attributes
        for attrib in node.InputAttributes().values():
            self.__RemoveAttribute( attrib )

        for attrib in node.OutputAttributes().values():
            self.__RemoveAttribute( attrib )

        # Discard ObjectID
        #id = node.GlobalID()
        #self.__m_ObjectIDManager.Discard( node.ObjectID() )

        # Remove node from scene
        #del self.__m_NodeKey[ node.Name() ]
        del self.__m_NodeList[ node.Name() ]# id ]


    def __Connect( self, pconn, src, dst ):

        print( 'Connect ' + src.ParentNode().Name() + '.' + src.Name() + ' ' + dst.ParentNode().Name() + '.' + dst.Name() )

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
                print( '  Connection already exists.' )
                return conn

        return None



    def __CheckConnectivity( self, attr_source, attr_dest ):

        if( attr_source==None or attr_dest==None ):
            print( '  Invalid connectivity: source and/or dest is empty.' )
            return False

        # Check if in and out are connectable
        if( attr_source.IsInput() or attr_dest.IsOutput() ):
            print( '  Invalid connectivity: Unable to connect. Specity Correct [Source] and [Dest].' )
            return False
           
        if( attr_source.DataType() != attr_dest.DataType() ):
            print( '  Invalid connectivity: Unable to connect. Different DataType.' )
            return False


        return True
