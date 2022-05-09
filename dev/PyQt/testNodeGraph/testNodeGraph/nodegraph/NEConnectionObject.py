from .INEGraphObject import *



class NEConnectionObject(INEGraphObject):

    def __init__( self, name ):
        super().__init__( name, 'Connection' )

        self.__m_pSource = None
        self.__m_pDestination = None


    def __del__( self ):
        super().__del__()
        self.Clear()


    def Clear( self ):
        self.__m_pSource = None
        self.__m_pDestination = None


    def BindSource( self, source ):
        self.__m_pSource = source


    def BindDestination( self, dest ):
        self.__m_pDestination = dest


    def UnbindSource( self ):
        self.__m_pSource = None


    def UnbindDestination( self ):
        self.__m_pDestination = None


    def Source( self ):
        return self.__m_pSource


    def Destination( self ):
        return self.__m_pDestination

