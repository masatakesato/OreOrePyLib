from collections import defaultdict


class KeyMap:

    def __init__( self, root=None ):

        self.__m_LookupTable = defaultdict(dict)

        if( root ):
            self.__m_LookupTable[ root.Key() ][ root.ID() ] = root


    def __del__( self ):
        self.Clear()


    def Clear( self ):
        self.__m_LookupTable.clear()


    def GetFullKey( self, query_key ):

        partialKeys = tuple( reversed(query_key.split('.')) )

        if( not(partialKeys[0] in self.__m_LookupTable) ):
            print( 'No localKey entry found... ')
            return None

        #print( 'LocalKey entry found... ')
        localkey = partialKeys[0]
        localList = list(self.__m_LookupTable[ partialKeys[0] ].values())

        # Check if single element completely matches with query_key
        if( len(localList)==1 and query_key==localList[0].FullKey() ):
            print( 'Found unique result: ', localList[0].FullKey() )
            return localList[0]
        
        # Try to find completely matched element from multiple elements
        filtered = [ v for v in localList if(query_key==v.FullKey()) ]
        if( len(filtered)==1 ): # found unique element
            print( 'Filtered completely matched result: ', filtered[0].FullKey() )
            return filtered[0]

        # Try to find partially matched element from localList
        filtered = [ v for v in localList if(query_key in v.FullKey()) ]
        if( len(filtered)==1 ): # found unique element
            print( 'Found partially matched result: ', filtered[0].FullKey() )
            return filtered[0]
        
        # multiple candicates
        print( 'Multiple partially matched candicates. Which one?' )
        for obj in filtered: print( '  ', obj.FullKey(), '(', obj.ID(), ')' )

        return None


    def Add( self, obj ):
        self.__m_LookupTable[ obj.Key() ][ obj.ID() ] = obj


    def Remove( self, obj ):

        # disable obj references
        del self.__m_LookupTable[ obj.Key() ][ obj.ID() ]
    
        # cleanup. remove empty local key entry
        if( not self.__m_LookupTable[ obj.Key() ] ):
            print( 'Removing empty keyMap entry: ', obj.Key() )
            del self.__m_LookupTable[ obj.Key() ]


    def Rename( self, obj_id, old_key, new_key ):

        try:
            self.__m_LookupTable[new_key][obj_id] = self.__m_LookupTable[old_key].pop(obj_id)
            if( not self.__m_LookupTable[old_key] ):   del self.__m_LookupTable[old_key]
            return True
        except:
            return False



#def GetFullKey( query_key, keyMap ):

#    partialKeys = tuple( reversed(query_key.split('.')) )

#    if( not(partialKeys[0] in keyMap) ):
#        print( 'No localKey entry found... ')
#        return None

#    #print( 'LocalKey entry found... ')
#    localkey = partialKeys[0]
#    localList = list(keyMap[ partialKeys[0] ].values())

#    # found unique matching result from localList
#    if( len(localList)==1 and query_key==localList[0].FullKey() ):
#        print( 'Found completely matched result...' )
#        localList[0].Info()
#        return localList[0]

#    # filter completely matched elements from localList
#    filtered = [ v for v in localList if(query_key==v.FullKey()) ]

#    if( len(filtered)==1 ): # found unique element
#        print( 'Found completely matched result...' )
#        print( '  ', filtered[0].FullKey() )
#        return filtered[0]

#    # filter partially matched elements from localList
#    filtered = [ v for v in localList if(query_key in v.FullKey()) ]
           
#    if( len(filtered)==1 ): # found unique element
#        print( 'Found partially matched result...' )
#        print( '  ', filtered[0].FullKey() )
#        return filtered[0]
        
#    # multiple candicates
#    print( 'Multiple partially matched candicates. Which one?' )
#    for node in filtered: print( '  ', node.FullKey(), '(', node.ID(), ')' )

#    return None


#def RemoveNodesfromKeyMap( node, keyMap ):

#    if( node==None ):    return

#    deleteNodeList = []
#    GatherChildren( node, deleteNodeList )# Gather all children

#    print( 'deleteNodeList:' )
#    for node in deleteNodeList:
#        print( '  ', node.FullKey() )

#    # disable node references
#    for node in deleteNodeList:
#        del keyMap[ node.Key() ][ node.ID() ]
    
#    # cleanup. remove empty local key entry
#    print( 'Removing keyMapentry:' )
#    keyMap = { k: v for k, v in keyMap.items() if(len(v)>0) }


#def RenameKeyMap( node_id, old_key, new_key ):
#    try:
#        keyMap[new_key][node_id] = keyMap[old_key].pop(node_id)
#        if( len(keyMap[old_key])==0 ):   del keyMap[old_key]
#        return True
#    except:
#        return False