from graphics.GraphicsSettings import *


import traceback
import urllib.request
from io import BytesIO

from PIL import Image, ImageGrab
from PIL.ImageQt import ImageQt


class ImageRect( QGraphicsPixmapItem ):

    def __init__( self, *args, **kwargs ):
        super(ImageRect, self).__init__(*args, **kwargs)

        # TODO: normalize item size
        length =max( self.boundingRect().width(), self.boundingRect().height() )
        if(length>0):
            self.setScale( 500.0 / length )
            self.setPos( -self.boundingRect().width()*self.scale()*0.5, -self.boundingRect().height()*self.scale()*0.5 )#self.moveBy( -self.boundingRect().width()*self.scale()*0.5, -self.boundingRect().height()*self.scale()*0.5 )

        self.rect_local = self.boundingRect()

        self.__m_ImageData = None


    # DO NOT CALL THIS METHOD DIRECDTLY!!!. QPixmap to PIL conversion process is not implemented. 2019.07.27
    def setPixmap( self, pixmap ):
        pass

    
    def Init( self, pixmap ):
        super(ImageRect, self).setPixmap(pixmap)

        length =max( self.boundingRect().width(), self.boundingRect().height() )
        #print( self.boundingRect() )
        if(length>0):
            self.setScale( 500.0 / length )
            self.setPos( -self.boundingRect().width()*self.scale()*0.5, -self.boundingRect().height()*self.scale()*0.5 )

        self.rect_local = self.boundingRect()

        # TODO: implement QPixmap to PIL conversion ?



    def GetImageData( self ):
        return self.__m_ImageData


    def SetRect( self, rect_scene ):
        #self.rect_local = self.mapRectFromScene( QRectF(rect_scene) )
        self.rect_local = self.boundingRect().intersected( self.mapRectFromScene( QRectF(rect_scene) ) )


    def ResetRect( self ):
        self.rect_local = self.boundingRect()


    def LoadImage( self, filepath ):
        try:
            self.__m_ImageData = Image.open( str(filepath) ).convert('RGB')
            qim = ImageQt( self.__m_ImageData.convert('RGBA') )
            if( qim ):
                #del self.__m_PixMap
                __m_PixMap = QPixmap.fromImage(qim)
                __m_PixMap.detach()
                self.Init( __m_PixMap )
                print( 'Image loaded: %s' % filepath )
        except:
            traceback.print_exc()



    def PasteFromClipboard( self ):
        try:
            im = ImageGrab.grabclipboard()
            if( isinstance(im, Image.Image) ):
                self.__m_ImageData = im.convert('RGB')
                qim = ImageQt( self.__m_ImageData.convert('RGBA') )
                if( qim ):
                    #del self.__m_PixMap
                    __m_PixMap = QPixmap.fromImage(qim)
                    __m_PixMap.detach()
                    self.Init( __m_PixMap )
                    print( 'Image loaded from clipboard' )
            else:
                string = QApplication.clipboard().text()

                f = BytesIO( urllib.request.urlopen(string).read() )
                self.__m_ImageData = Image.open(f).convert('RGB')
                qim = ImageQt( self.__m_ImageData.convert('RGBA') )
                if( qim ):
                    #del self.__m_PixMap
                    __m_PixMap = QPixmap.fromImage(qim)
                    __m_PixMap.detach()
                    self.Init( __m_PixMap )# TODO: add to ImageRect
                    print( 'Image loaded from clipboard' )

        except:
            traceback.print_exc()





    def SaveImage( self, rect_scene ):
        self.rect_local = self.mapRectFromScene( QRectF(rect_scene) )
        print( self.rect_local )
        cropPixmap = self.pixmap().copy( self.rect_local.toRect() )
        cropPixmap.save( 'output.png' )



    def paint( self, painter, QStyleOptionGraphicsItem, QWidget ):
        painter.setOpacity(0.5)
        painter.drawPixmap( self.boundingRect().toRect(), self.pixmap() )
        
        painter.setOpacity(1.0)
        painter.drawPixmap( self.rect_local.toRect(), self.pixmap(), self.rect_local.toRect() )



#class ImageRect(QGraphicsItem):
#    QGraphicsPixmapItem
#    def __init__( self, pixmap, *args, **kwargs ):
#        super(ImageRect, self).__init__(*args, **kwargs)

#        self.__m_refPixmap = pixmap.scaledToWidth( self.__m_DrawRect.width(), Qt.SmoothTransformation )
#        self.__m_DrawRect = QRectF( 0, 0, pixmap.width(), pixmap.height() )
#        self.__m_BoundingRect = QRectF( 0.0, 0.0, pixmap.width(), pixmap.height() )
        


#        self.__m_Shape = QPainterPath()
#        self.__m_Shape.addRect( self.__m_BoundingRect )

#        self.__m_Pen = QPen( QColor(48,48,48), 1.0 )



#    def boundingRect(self):
#        return self.__m_BoundingRect


#    def shape( self ):
#        return self.__m_Shape


#    def paint(self, painter, option, widget):
#        painter.setClipRect(option.exposedRect)
#        painter.setBrush( QColor(170,115,26) )
#        painter.setPen( self.__m_Pen )
#        painter.drawRect( self.__m_DrawRect )#, g_ButtonRoundRadius, g_ButtonRoundRadius )

#        painter.drawPixmap( self.__m_DrawRect, self.__m_refPixmap, self.__m_DrawRect )