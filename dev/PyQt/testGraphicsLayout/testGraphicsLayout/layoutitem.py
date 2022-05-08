from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class LayoutItem(QGraphicsLayoutItem, QGraphicsItem):

    def __init__( self, parent=None ):
        super(LayoutItem, self).__init__(parent)
        super(QGraphicsLayoutItem, self).__init__()
        super(QGraphicsItem, self).__init__(parent)

        self.m_pix = QPixmap("./images/block.png")
        print( self.m_pix.width() )
        self.setGraphicsItem(self)


    def __del__( self ):
        del self.m_pix


    def paint( self, painter, option, widget=None ):

        frame = QRectF( QPointF(0,0), self.geometry().size() )
        w = self.m_pix.width()
        h = self.m_pix.height()
        stops = []

        # paint a background rect (with gradient)
        gradient = QLinearGradient( frame.topLeft(), frame.topLeft() + QPointF(200,200) )
        stops.append( (0.0, QColor(60, 60, 60)) )
        stops.append( (frame.height() / 2 / frame.height(), QColor(102, 176, 54)) )

        #stops << QGradientStop(((frame.height() + h)/2 )/frame.height(), QColor(157, 195,  55));
        stops.append( (1.0, QColor(215, 215, 215)) )
        gradient.setStops(stops)
        painter.setBrush( QBrush(gradient) )
        painter.drawRoundedRect(frame, 10.0, 10.0)

        # paint a rect around the pixmap (with gradient)
        pixpos = frame.center() - (QPointF(w, h) / 2)
        innerFrame = QRectF(pixpos, QSizeF(w, h))
        innerFrame.adjust(-4, -4, 4, 4)
        gradient.setStart(innerFrame.topLeft())
        gradient.setFinalStop(innerFrame.bottomRight())
        stops.clear()
        stops.append( (0.0, QColor(215, 255, 200)) )
        stops.append( (0.5, QColor(102, 176, 54)) )
        stops.append( (1.0, QColor(0, 0, 0)) )
        gradient.setStops(stops)
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(innerFrame, 10.0, 10.0)
        painter.drawPixmap(pixpos, self.m_pix)


    def boundingRect( self ):
        return QRectF(QPointF(0,0), self.geometry().size())


    def setGeometry( self, geom ):
        self.prepareGeometryChange()
        QGraphicsLayoutItem.setGeometry(geom)
        self.setPos( geom.topLeft() )
 

    def sizeHint(self, which, constraint ):

        if( which==Qt.MinimumSize or which==Qt.PreferredSize ):
            return QSizeF( self.m_pix.size() + QSize(12, 12) )
        elif( which==Qt.MaximumSize ):
            return QSizeF(1000,1000)
        else:
            return constraint


    #switch (which) {
    #case Qt.MinimumSize:
    #case Qt.PreferredSize:
    #    // Do not allow a size smaller than the pixmap with two frames around it.
    #    return m_pix->size() + QSize(12, 12);
    #case Qt.MaximumSize:
    #    return QSizeF(1000,1000);
    #default:
    #    break;
    #}
    #return constraint;
#}
