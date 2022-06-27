import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



 
class GraphicsItemLayer:

    def __init__( self ):
        self.__m_ItemGroups = []
        self.__m_CurrentIdx = -1


    def __del__( self ):
        pass


    def AddLayer( self ):
        group = QGraphicsItemGroup()
        group.setZValue( len(self.__m_ItemGroups) )
        self.__m_ItemGroups.append( group )
        return len( self.__m_ItemGroups )


    def InsertLayer( self, idx ):
        self.__m_ItemGroups.insert( idx, QGraphicsItemGroup() )
        self.__UpdateDepth( idx, len(self.__m_ItemGroups) )


    def DeleteLayer( self, idx ):
        if( idx < len(self.__m_ItemGroups) ):
            del self.__m_ItemGroups[ idx ]
            self.__UpdateDepth( idx, len(self.__m_ItemGroups) )


    def MoveLayer( self, idx, new_idx ):
        if( idx != idx_new ):
            # move element
            elm = self.__m_ItemGroups.pop( idx )
            self.__m_ItemGroups.insert( new_idx, elm )
            # update depth
            self.__UpdateDepth( min(idx, new_idx), max(idx, new_idx) + 1 )


    def SetVisible( self, idx, visible ):
        self.__m_ItemGroups[idx].setVisible( visible )


    def SetEditable( self, idx, editable ): pass


    def CurrentLayer( self ): pass



    def NumLayers( self ):
        return len( self.__m_ItemGroups )



    def AddItem( self, item, idx ):
        if( isinstance( item, QGraphicsItem ) ):
            self.__m_ItemGroups[idx].append( item )


    def RemoveItem( self, item, idx ):
        if( item in self.__m_ItemGroups[idx] ):
            self.__m_ItemGroups[idx].remove( item )



    def __UpdateDepth( self, begin_, end_ ):
        for i in range(begin_, end_):
            self.__m_ItemGroups[i].setZValue(i)






if __name__ == "__main__":

    app = QApplication( sys.argv )

    scene = QGraphicsScene()
    view = QGraphicsView()
    view.setEnabled( True )
    view.setScene( scene )


    view.setGeometry( 0, 0, 800, 600 )
    view.show()


    rect = QGraphicsRectItem()
    rect.setRect( 0, 0, 60, 20 )
    #rect.setOpacity( 0.5 )
    rect.setBrush( Qt.red )
    rect.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
    rect.setFlag( QGraphicsItem.ItemIsMovable )
    rect.setFlag( QGraphicsItem.ItemIsSelectable )
    rect.setFlag( QGraphicsItem.ItemIsFocusable, False )

    group1 = QGraphicsItemGroup()
    group1.addToGroup( rect )
    group1.setZValue( 0 )

    scene.addItem( group1 )
    print( group1.zValue() )



    rect2 = QGraphicsRectItem()
    rect2.setRect( 10, 10, 60, 20 )
    #rect2.setOpacity( 0.5 )
    rect2.setBrush( Qt.green )
    rect2.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
    rect2.setFlag( QGraphicsItem.ItemIsMovable )
    rect2.setFlag( QGraphicsItem.ItemIsSelectable )
    rect2.setFlag( QGraphicsItem.ItemIsFocusable, False )

    group2 = QGraphicsItemGroup()
    group2.addToGroup( rect2 )
    group2.setZValue( 1 )

    scene.addItem( group2 )
    print( group2.zValue() )



    group1.setZValue( 0 )
    group2.setZValue( 1 )


    sys.exit( app.exec_() )
