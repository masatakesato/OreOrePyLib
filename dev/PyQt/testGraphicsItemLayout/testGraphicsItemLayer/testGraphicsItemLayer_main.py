import sys


from graphicsitemlayer import *





if __name__ == "__main__":

    app = QApplication( sys.argv )

    scene = QGraphicsScene()
    view = QGraphicsView()
    view.setEnabled( True )
    view.setScene( scene )

    view.setGeometry( 0, 0, 800, 600 )
    view.show()


    layer = GraphicsItemLayer( scene )
    layer.AddLayer()
    layer.AddLayer()


    rect = QGraphicsRectItem()
    rect.setRect( 0, 0, 60, 20 )
    rect.setBrush( Qt.red )
    rect.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
    rect.setFlag( QGraphicsItem.ItemIsMovable )
    rect.setFlag( QGraphicsItem.ItemIsSelectable )
    #rect.setFlag( QGraphicsItem.ItemIsFocusable, False )

    layer.AddItem( rect, 0 )

    rect2 = QGraphicsRectItem()
    rect2.setRect( 10, 10, 60, 20 )
    rect2.setBrush( Qt.green )
    rect2.setFlag( QGraphicsItem.ItemSendsGeometryChanges )
    rect2.setFlag( QGraphicsItem.ItemIsMovable )
    rect2.setFlag( QGraphicsItem.ItemIsSelectable )
    #rect2.setFlag( QGraphicsItem.ItemIsFocusable, False )

    layer.AddItem( rect2, 1 )


    #layer.DeleteItem( rect, 0 )
    #del rect
    #layer.DeleteItem( rect2, 1 )
    #del rect2

    layer.MoveLayer(0, 1)
    layer.MoveLayer(1, 0)



    sys.exit( app.exec_() )
