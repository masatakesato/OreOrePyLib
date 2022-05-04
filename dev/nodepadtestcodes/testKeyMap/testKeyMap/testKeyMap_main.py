import queue


from KeyMap import KeyMap



######################## Node Hierarchy #######################
class Node:

    def __init__( self, key, parent=None ):

        self.__m_ID = id(self)
        self.__m_Key = key
        self.__m_Parent = parent
        self.__m_Children = {}


    def __del__( self ):
        print( 'Node::__del__ : ', self.__m_Key )
        self.Clear()


    def Clear( self ):
        self.SetParent(None)
        self.ClearChildren()
        self.__m_Key = None


    def Children( self ):
        return self.__m_Children


    def Child( self, key ):
        if( key in self.__m_Children ):
            return self.__m_Children[key]
        else:
            return None


    def HasChildren( self ):
        return any(self.__m_Children)


    def HasKey( self, key ):
        return key in self.__m_Children


    def AddChild( self, value ):
        self.__m_Children[ value.__m_Key ] = value#
        value.__m_Parent = self


    def PopChild( self, key ):# key指定した子供をリストから除外する

        if( id in self.__m_Children ):
            child = self.__m_Children.pop( key )
            child.__m_Parent = None
            return child

        return None


    def RemoveChild( self, key ):# key指定した子供を削除する.ついでに孫も削除する

        if( key in self.__m_Children ):
            child = self.__m_Children.pop( key )
            child.ClearChildren()
            del child


    def ClearChildren( self ):

        for child in self.Children().values():
            if( child.HasChildren() ):  child.ClearChildren()

        print( self.Key() + '.ClearChildren()...' )
        self.__m_Children.clear()


    def Parent( self ):
        return self.__m_Parent


    def SetParent( self, parent ):

        if( self.__m_Parent ):
            self.__m_Parent.RemoveChild( self.__m_Key )

        self.__m_Parent = parent
        if( self.__m_Parent ):
            self.__m_Parent.AddChild( self )


    def SetKey( self, newkey ):

        if( self.__m_Parent ):
            dict = self.__m_Parent.Children()
            if( self.__m_Key in dict ):
                dict[ newkey ] = dict.pop( self.__m_Key )

        self.__m_Key = newkey


    def ID( self ):
        return self.__m_ID


    def Key( self ):
        return self.__m_Key


    def FullKey( self ):
        if( self.__m_Parent ):
            return self.__m_Parent.FullKey() + '.' + self.__m_Key
        else:
            return self.__m_Key


    def Info( self ):
        print(self.FullKey())



######################### Scene Scanning #########################

def BreadsFirstScan( root ):

    q = queue.Queue()

    q.put( root )

    while not q.empty():

        data = q.get()
        if( isinstance( data, Node) ):
            data.Info()

        for child in data.Children().values():
            q.put( child )


# 自分を登録してから子ノードを探索する処理
def DepthFirstScan( node ):

    node.Info()

    if( len(node.Children()) < 1 ):
        return

    for child in node.Children().values():
        DepthFirstScan( child )


# 実験. 葉ノードまで探索してからリストにノード登録する処理.できる？？？？
def DepthFirstScan2( node ):

    for child in node.Children().values():
        DepthFirstScan2( child )

    node.Info()



def GatherChildren( node, nodeList ):

    nodeList.append( node )

    if( len(node.Children()) < 1 ):
        return

    for child in node.Children().values():
        GatherChildren( child, nodeList )



def ClearChildren( node ):

    for child in node.Children().values():
        ClearChildren( child )

    if( len(node.Children())>0 ):
        print( node.Key() + '.ClearChildren()...' )
        node.Children().clear()








if __name__ == '__main__':

    ##################### Node Structure #####################

    #rootNode = Node('Scene')
    #counter = 0

    ## Create new Object
    #for i in range(10):
    #    node = Node( 'Node' + str(counter) )
    #    rootNode.AddChild( node )
    #    #node.SetParent( rootNode )

    #    counter += 1

    #    for j in range(1):
    #        node2 = Node( 'Attrib' + str(counter) )
    #        node.AddChild(node2)
    #        #node2.SetParent(node)

    #        counter+=1

    #BreadsFirstScan( rootNode )
    ##DepthFirstScan( rootNode )


    ################# Node and Key Structure ##################
    # Node Structure
    rootNode = Node('Root')
    counter = 0

    # Key Array
    #keyMap = defaultdict(dict)
    #keyMap[ rootNode.Key() ][ rootNode.ID() ] = rootNode

    keyMap = KeyMap( rootNode )


    
    # Create new Object
    for i in range(4):
        # CreateNode
        node = Node( 'Node' + str(i) )#Node('Node1')#
        rootNode.AddChild(node)

        # Create keymap
        keyMap.Add(node)#keyMap[ node.Key() ][ node.ID() ] = node

        for j in range(3):
            # CreateNode
            node2 = Node( 'Attrib' + str(j) )#Node('Node2')#
            node.AddChild(node2)
            counter+=1

            # Creater keymap
            keyMap.Add(node2)#keyMap[ node2.Key() ][ node2.ID() ] = node2

            if( i==2 and j==2 ):
                # CreateNode
                node3 = Node( 'SPECIAL' )
                node2.AddChild(node3)

                # Creater keymap
                keyMap.Add(node3)#keyMap[ node3.Key() ][ node3.ID() ] = node3

    #BreadsFirstScan( rootNode )
    DepthFirstScan( rootNode )

    print( '' )

    DepthFirstScan2( rootNode )

    
    sys.exit()

    ################## Search query ########################
    query = 'Node3'
    node = keyMap.GetFullKey(query)#GetFullKey( query, keyMap )

    ############ Remove Node1 and its' children ############
    deleteNodeList = []
    GatherChildren( node, deleteNodeList )# Gather all children

    for delnode in deleteNodeList:
        keyMap.Remove( delnode )#RemoveNodesfromKeyMap( node, keyMap )

    #ClearChildren( node )
    #node.ClearChildren()
    rootNode.RemoveChild( node )

    ################### Rename Node ########################
    oldkey = node.Key()
    newkey = "OreOre"
    node.SetKey( newkey )

    DepthFirstScan( rootNode )

    result = keyMap.Rename( node.ID(), oldkey, newkey )#RenameKeyMap( node.ID(), oldkey, newkey )

    ################## Search query ########################
    query = 'Attrib2.SPECIAL'
    node = keyMap.GetFullKey( query )
    
    pass