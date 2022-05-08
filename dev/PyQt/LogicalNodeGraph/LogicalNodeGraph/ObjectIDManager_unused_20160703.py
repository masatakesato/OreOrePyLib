import heapq

from NECommon import *



class IDGenerator():

    def __init__( self ):

        self.__m_LatestID = 0
        self.__m_DiscardedIDs = [] # priority queue


    def Publish( self ):

        if( len(self.__m_DiscardedIDs) > 0 ):
            return heapq.heappop( self.__m_DiscardedIDs )            

        else:
            newid = self.__m_LatestID
            self.__m_LatestID += 1
            return newid


    def Discard( self, id ):

        if( id >= self.__m_LatestID ):
            return

        else:
            heapq.heappush( self.__m_DiscardedIDs, id )




class ObjectIDManager():

    def __init__( self ):
        self.__m_IDGenerator = {}
        self.__m_IDGenerator[ 'Global' ] = IDGenerator()


    def __del__( self ):
        self.Clear()


    def Clear( self ):
        self.__m_IDGenerator.clear()


    def Register( self, objTypeKey ):
        self.__m_IDGenerator[ objTypeKey ] = IDGenerator()


    def Unregister( self, objTypeKey ):
        if( objTypeKey in self.__m_IDGenerator ):
            del self.__m_IDGenerator[ objTypeKey ]


    def Publish( self, objTypeKey ):
        objID = ObjectID( self.__m_IDGenerator['Global'].Publish(),
                          self.__m_IDGenerator[objTypeKey].Publish(),
                         objTypeKey )
        return objID


    def Discard( self, objID ):
        self.__m_IDGenerator['Global'].Discard( objID.GlobalID )
        self.__m_IDGenerator[objID.ObjectTypeKey].Discard( objID.LocalID )