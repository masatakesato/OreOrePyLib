from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class LayerRoot( QGraphicsItem ):
    pass

    def __init__( self ):
        super(LayerRoot, self).__init__()

        #self.__m_refItems = {}



    def AddItem( self, item ):
        if( isinstance( item, QGraphicsItem ) ):
            print( "LayerRoot::AddItem ", item )
            item.setParentItem( self )
            # self.__m_refItems[ item.ID() ] = item


    def DeleteItem( self, item ):
        #if( item.ID() in self.__m_refItems ):
        #    del self.__m_refItems[ item.ID() ]
        print( "LayerRoot::DeleteItem ", item )
        item.setParentItem( None )


    ######################### QGraphicsItem func override ################################

    def boundingRect( self ):
        return self.childrenBoundingRect()


    def paint( self, painter, option, widget ):
        pass



class GraphicsItemLayer:

    def __init__( self, parent ):
        self.__m_LayerRoots = []
        self.__m_CurrentIdx = -1
        self.__m_ParentScene = parent


    def __del__( self ):
        self.__m_LayerRoots.clear()
        self.__m_CurrentIdx = -1
        self.__m_ParentScene = None


    def AddLayer( self ):
        group = LayerRoot()
        group.setZValue( len(self.__m_LayerRoots) )
        self.__m_ParentScene.addItem( group )
        self.__m_LayerRoots.append( group )

        return len( self.__m_LayerRoots ) - 1


    def InsertLayer( self, idx ):
        self.__m_LayerRoots.insert( idx, QGraphicsItemGroup() )
        self.__UpdateDepth( idx, len(self.__m_LayerRoots) )


    def DeleteLayer( self, idx ):
        if( idx < len(self.__m_LayerRoots) ):
            self.__m_ParentScene.removeItem( self.__m_LayerRoots[ idx ] )
            del self.__m_LayerRoots[ idx ]
            self.__UpdateDepth( idx, len(self.__m_LayerRoots) )


    def MoveLayer( self, idx, new_idx ):
        if( idx != new_idx ):
            # move element
            elm = self.__m_LayerRoots.pop( idx )
            self.__m_LayerRoots.insert( new_idx, elm )
            # update depth
            self.__UpdateDepth( min(idx, new_idx), max(idx, new_idx) + 1 )


    def SetVisible( self, idx, visible ):
        self.__m_LayerRoots[idx].setVisible( visible )


    def SetEditable( self, idx, editable ): pass


    def CurrentLayer( self ): pass


    def NumLayers( self ):
        return len( self.__m_LayerRoots )


    def AddItem( self, item, idx ):
        if( idx < len(self.__m_LayerRoots) ):
            self.__m_LayerRoots[idx].AddItem( item )


    def DeleteItem( self, item, idx ):
        if( idx < len(self.__m_LayerRoots) ):
            self.__m_LayerRoots[idx].DeleteItem( item )


    def __UpdateDepth( self, begin_, end_ ):
        for i in range(begin_, end_):
            self.__m_LayerRoots[i].setZValue(i)





# ボツ. QGraphicsItemGroupの子itemを個別編集できない. 2022.06.28
#class GraphicsItemLayer:

#    def __init__( self, parent ):
#        self.__m_ItemGroups = []
#        self.__m_CurrentIdx = -1
#        self.__m_ParentScene = parent


#    def __del__( self ):
#        self.__m_ItemGroups.clear()
#        self.__m_CurrentIdx = -1
#        self.__m_ParentScene = None


#    def AddLayer( self ):
#        group = QGraphicsItemGroup()
#        group.setFlag( QGraphicsItem.ItemSendsScenePositionChanges )

#        group.setZValue( len(self.__m_ItemGroups) )
#        self.__m_ParentScene.addItem( group )
#        self.__m_ItemGroups.append( group )
#        return len( self.__m_ItemGroups )


#    def InsertLayer( self, idx ):
#        self.__m_ItemGroups.insert( idx, QGraphicsItemGroup() )
#        self.__UpdateDepth( idx, len(self.__m_ItemGroups) )


#    def DeleteLayer( self, idx ):
#        if( idx < len(self.__m_ItemGroups) ):
#            self.__m_ParentScene.removeItem( self.__m_ItemGroups[ idx ] )
#            del self.__m_ItemGroups[ idx ]
#            self.__UpdateDepth( idx, len(self.__m_ItemGroups) )


#    def MoveLayer( self, idx, new_idx ):
#        if( idx != new_idx ):
#            # move element
#            elm = self.__m_ItemGroups.pop( idx )
#            self.__m_ItemGroups.insert( new_idx, elm )
#            # update depth
#            self.__UpdateDepth( min(idx, new_idx), max(idx, new_idx) + 1 )


#    def SetVisible( self, idx, visible ):
#        self.__m_ItemGroups[idx].setVisible( visible )


#    def SetEditable( self, idx, editable ): pass


#    def CurrentLayer( self ): pass



#    def NumLayers( self ):
#        return len( self.__m_ItemGroups )



#    def AddItem( self, item, idx ):
#        if( isinstance( item, QGraphicsItem ) and idx < len(self.__m_ItemGroups) ):
#            print( "GraphicsItemLayer::AddItem ", item )
#            self.__m_ItemGroups[idx].addToGroup( item )


#    def DeleteItem( self, item, idx ):
#        #print( item.parentItem() )
#        #print( self.__m_ItemGroups[idx] )
#        if( item in self.__m_ItemGroups[idx].childItems() ):
#            print( "GraphicsItemLayer::DeleteItem ", item )
#            self.__m_ItemGroups[idx].removeFromGroup( item )
#            #del item
#            #print( self.__m_ItemGroups[idx].childItems() )
            


#    def __UpdateDepth( self, begin_, end_ ):
#        for i in range(begin_, end_):
#            self.__m_ItemGroups[i].setZValue(i)



