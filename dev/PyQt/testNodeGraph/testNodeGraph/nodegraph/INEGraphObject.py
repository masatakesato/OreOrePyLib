#class INEGraphObject:

#    def __init__( self, name ):
#        self.__m_Name = name
#        self.__m_Parent = None


#    def __del__( self ):
#        self.Clear()


#    def Clear( self ):
#        self.__m_Name = ''
#        self.__m_Parent = None


#    def SetName( self, name ):
#        self.__m_Name = name
   

#    def Name( self ):
#        #if( self.__m_Parent ): 
#        #    return self.__m_Parent.Name() + '.' + self.__m_Name
#        return self.__m_Name


#    def FullName( self ):
#        if( self.__m_Parent ): 
#            return self.__m_Parent.Name() + '.' + self.__m_Name
#        return self.__m_Name


#    def ParentName( self ):
#        if( self.__m_Parent ): 
#            return self.__m_Parent.Name()
#        return None


#    def SetParent( self, parent ):
#        self.__m_Parent = parent


#    def Parent( self ):
#        return self.__m_Parent





class INEGraphObject:

    def __init__( self, key, objtype, parent=None ):

        self.__m_Key = key
        self.__m_ObjectType = objtype
        self.__m_Parent = parent
        self.__m_Children = {}


    def __del__( self ):
        self.Clear()


    def Clear( self ):
        self.__m_Key = None
        self.__m_Parent = None
        self.__m_Children.clear()


    def ObjectType( self ):
        return self.__m_ObjectType


    def Children( self ):
        return self.__m_Children


    def Child( self, key ):
        if( key in self.__m_Children ):
            return self.__m_Children[key]
        else:
            return None


    def HasKey( self, key ):
        return key in self.__m_Children


    def AddChild( self, value, linkparent=True ):
        self.__m_Children[ value.__m_Key ] = value
        if( linkparent ): value.__m_Parent = self


    def RemoveChild( self, key ):

        if( key in self.__m_Children ):
            return self.__m_Children.pop( key )


    def ClearChildren( self ):
        self.__m_Children.clear()


    def Parent( self ):
        return self.__m_Parent


    def SetParent( self, parent ):
        if( self.__m_Parent ):
            self.__m_Parent.RemoveChild( self.FullKey() )

        self.__m_Parent = parent


    def SetKey( self, newkey ):

        if( self.__m_Parent ):
            dict = self.__m_Parent.Children()
            if( self.__m_Key in dict ):
                dict[ newkey ] = dict[ self.__m_Key ].pop()

        self.__m_Key = newkey


    def Key( self ):
        return self.__m_Key


    def FullKey( self ):
        if( self.__m_Parent ):
            return self.__m_Parent.FullKey() + '.' + self.__m_Key
        else:
            return self.__m_Key


    def Info( self ):
        print( 'ObjectType: ', self.__m_ObjectType )
        print(self.FullKey())
