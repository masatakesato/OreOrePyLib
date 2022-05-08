class INEGraphObject:

    def __init__( self, name ):#, id ):
        #self.__m_ID = id
        self.__m_Name = name


    def __del__( self ):
        self.Release()


    def Release( self ):
        #self.__m_ID = -1
        self.__m_Name = ''


    #def SetID(self, id):
        #self.__m_ID = id
        

    def SetName( self, name ):
        self.__m_Name = name


    #def ObjectID( self ):
    #    return self.__m_ID


    #def GlobalID( self ):
    #    return self.__m_ID.GlobalID


    #def LocalID( self ):
    #    return self.__m_ID.LocalID
   

    def Name( self ):
        return self.__m_Name




