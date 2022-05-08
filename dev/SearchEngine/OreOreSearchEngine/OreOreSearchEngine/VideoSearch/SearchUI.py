import pathlib
import functools
import numpy as np
import subprocess


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



# image viewer
class ImageViewer(QFrame):


    def __init__( self, parent=None ):
        super(ImageViewer, self).__init__(parent)
        self.setAcceptDrops(True)

        #self.setMinimumSize(256, 256)
        self.setStyleSheet( 'background-color:black;' )
        self.__m_ImagePath = ''

        self.__m_Label = QLabel()
        self.__m_Label.setStyleSheet("QLabel {background-color: black;}")

        self.__m_PixMap = None

        self.setLayout( QGridLayout() )
        self.layout().addWidget(self.__m_Label, 0, 0, Qt.AlignCenter)

        #self.setContextMenuPolicy( Qt.CustomContextMenu )
        #self.customContextMenuRequested.connect( self.openMenu )



    def dragEnterEvent( self, event ):# QDragEnterEvent
        if( event.mimeData().hasUrls() ):
            event.accept()
        else:
            event.ignore()


    def dropEvent( self, event ):# QDropEvent
        for url in event.mimeData().urls():
            #filepath = str(url.toLocalFile())
            self.LoadImage( str(url.toLocalFile()) )
            #img = QImage(filepath)
            #if( img ):
            #    del self.__m_PixMap
            #    self.__m_PixMap = QPixmap.fromImage(img)
            #    self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
            #    self.__m_ImagePath = filepath


    def resizeEvent( self, event ):
        if( self.__m_PixMap ):
            self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) ) 
        return super(ImageViewer, self).resizeEvent(event)


    def GetImagePath( self ):
        return self.__m_ImagePath


    def LoadImage( self, filepath ):
        img = QImage( filepath )
        if( img ):
            del self.__m_PixMap
            self.__m_PixMap = QPixmap.fromImage(img)
            self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
            self.__m_ImagePath = filepath
            print( 'ImageViewer loaded: %s' % filepath )


class Thumbnail(QFrame):

    def __init__( self, parent=None ):
        super(Thumbnail, self).__init__(parent)
        
        #self.setMinimumSize(256, 256)
        self.setStyleSheet( 'background-color:black;' )

        self.__m_ThumbnailPath = ''
        self.__m_MediaPath = ''

        self.__m_Label = QLabel()
        self.__m_Label.setStyleSheet("QLabel {background-color: black;}")

        self.__m_TextLabel = QLabel()
        self.__m_TextLabel.setStyleSheet("QLabel {color: white; background-color: black;}")

        self.__m_PixMap = None

        self.setLayout( QGridLayout() )
        self.layout().addWidget( self.__m_Label, 0, 0, Qt.AlignCenter )
        self.layout().addWidget( self.__m_TextLabel, 1, 0, Qt.AlignCenter )


    def resizeEvent( self, event ):
        if( self.__m_PixMap ):
            self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) ) 
        return super(Thumbnail, self).resizeEvent(event)


    def LoadImage( self, path_thumbnail, path_media ):
        img = QImage( path_thumbnail )
        if( img ):
            del self.__m_PixMap
            self.__m_PixMap = QPixmap.fromImage(img)
            self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
            self.__m_ThumbnailPath = path_thumbnail
            self.__m_MediaPath = path_media
            #print( 'Thumbnail loaded: %s' % self.__m_MediaPath )


    def PlayMedia( self ):
        print( 'Open file %s' % self.__m_MediaPath )
        cmd = '"%s"' % self.__m_MediaPath
        returncode = subprocess.Popen( cmd, shell=True )


    def SetLabel( self, label_text ):
        self.__m_TextLabel.setText( label_text )


    def contextMenuEvent( self, event ):
        
        menu = QMenu()

        action = QAction( 'Open' )
        action.triggered.connect( self.PlayMedia )

        menu.addAction( action )
        
        menu.exec( self.mapToGlobal( event.pos() ) )




# line edit
#class MyLineEdit(QLineEdit):

#    def __init__( self, str='', parent=None ):
#        super(MyLineEdit, self).__init__(str, parent)

#        self.setDragEnabled(True)
#        self.setAcceptDrops(True)


#    def dragEnterEvent( self, event ):
#        if event.mimeData().hasUrls():
#            event.accept()
#        else:
#            event.ignore()


#    def dropEvent( self, event ):
#        for url in event.mimeData().urls():
#            filepath = str(url.toLocalFile())
#            self.setText( filepath.replace('\\', '/') )
#            self.returnPressed.emit()




# main widget
class Window(QWidget):

    def __init__( self, search_proc, thumbnail_paths ):
        super(Window, self).__init__()


        self.__m_SearchProc = search_proc


        self.setWindowTitle( 'OreOre Asset Search' )
        self.setAcceptDrops(True)



        self.__m_PushButton = {}
        self.__m_Label = {}
        self.__m_TableWidget = {}

       


        self.__m_PushButton['Search'] = QPushButton( 'Search' )
        #self.__m_PushButton['Search'].setFixedSize( 100, 25 )
        self.__m_PushButton['Search'].clicked.connect( self.__Search )



        buttonFrame = QFrame()
        buttonFrame.setFixedHeight(50)
        buttonFrame.setLayout( QHBoxLayout() )
        buttonFrame.layout().addWidget( self.__m_PushButton['Search'] )


        self.resultFrame = QFrame()
        self.resultFrame.setLayout( QGridLayout() )
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget( self.resultFrame )


        hsplitter = QSplitter( Qt.Vertical )
        hsplitter.addWidget( buttonFrame )
        hsplitter.addWidget( scroll )#self.resultFrame )


        self.__m_numcols = 5
        self.__m_numrows = 10
        
        for row in range( self.__m_numrows ):
            for col in range( self.__m_numcols ):
                im_view = Thumbnail( self.resultFrame )
                im_view.setFixedSize( 150, 150 )
                self.resultFrame.layout().addWidget( im_view, row, col )
                

        self.imageViewer = ImageViewer(self)
        self.imageViewer.setMinimumSize(300, 300)
        self.imageViewer.setStyleSheet( 'background-color:black;' )



        vsplitter = QSplitter(Qt.Horizontal)

        vsplitter.addWidget( self.imageViewer )
        vsplitter.addWidget( hsplitter )

        # create 
        vboxlayout = QVBoxLayout()
        vboxlayout.addWidget( vsplitter )

        self.setLayout( vboxlayout )
        self.setGeometry( 100, 100, 1200, 400 )
        

        self.__m_Paths = { 'thumbnail': thumbnail_paths }



    def SetPath( self, key, path ):
        self.__m_Paths[key] = path



    def __Search( self ):

        query_img_path = pathlib.Path( self.imageViewer.GetImagePath() )
        
        if( query_img_path.is_file()==False ):
           print( 'Aborting prediction: invalid image path...' )
           return 
        
        # TODO: データセットの特徴量と比較して類似度順に並べる
        print( 'Searching media files...' )
        result, order = self.__m_SearchProc( query_path=query_img_path )

        #for i in range(20):
        #    idx = order[i]
        #    print( result[idx][0], result[idx][1], result[idx][2] )


        # TODO: 類似度上位N個分を表示する
        for row in range( self.__m_numrows ):
            for col in range( self.__m_numcols ):
                idx = order[ col + self.__m_numcols * row ]
                im_view = Thumbnail( self.resultFrame )

                # サムネイル画像の絶対パス
                mov_name = result[idx][0]
                frame_id = str(result[idx][1]).zfill(6)
                thumbnail_path = '%s/%s/img_%s.png' % ( str(self.__m_Paths['thumbnail']), mov_name, frame_id )
                movie_path = result[idx][2]
                #print( thumbnail_path )
                im_view.LoadImage( thumbnail_path, str(movie_path) )
                im_view.setFixedSize( 150, 150 )
                im_view.SetLabel( movie_path.name )
                self.resultFrame.layout().addWidget( im_view, row, col )