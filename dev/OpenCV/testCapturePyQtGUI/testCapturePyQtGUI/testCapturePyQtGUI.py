# https://stackoverflow.com/questions/29557143/how-to-capture-the-video-from-webcam-in-the-interval-of-2-minutes-using-opencv
# 一定時間間隔でスクリーンキャプチャする機能、、、FPSではなくシステム時間で計測

import os
import sys
import time
from datetime import datetime

import cv2

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *




g_FrameColor = (225, 225, 225)
g_FrameThickness = 1
g_FrameCenterRadius = 5





def clamp( x, min_val, max_val ):
    return min(max(x, min_val),max_val)






class Capture():

    def __init__( self, default_crop_size=(256, 256) ):
        self.__m_bCapturing = False
        self.__m_bSequential = False
        self.__m_bPaused = False
        self.__m_bMirror = False

        self.__m_Interval = 1000

        self.__m_Cap = cv2.VideoCapture(0)

        self.__m_Frame = None
        self.__m_ViewImg = None

        self.__m_CameraSize = ( int(self.__m_Cap.get(3)), int(self.__m_Cap.get(4)) )

        self.__m_DefaultCropSize = default_crop_size
        self.__m_CropSize = default_crop_size
        self.__m_CropCenter = None
        self.__m_CropStart = None
        self.__m_CropEnd = None

        self.InitCropRect()


    def __del__(self):
        del self.__m_Frame
        del self.__m_ViewImg


    def playCapture(self):
        print( 'play...' )

        self.__m_bCapturing = True
        self.__m_bPaused = False
        success = False
        self.__m_Frame = None
        self.__m_ViewImg = None

        t1 = datetime.now()


        while( self.__m_bCapturing ):

            # _ は画像を取得成功フラグ
            if( self.__m_bPaused==False ):
                success, self.__m_Frame = self.__m_Cap.read()

            # mirroring on/off
            if self.__m_bMirror is True:
                self.__m_Frame = cv2.flip( self.__m_Frame, 1 )

            if( self.__m_bSequential ):
                t2 = datetime.now()
                dt = t2 - t1
                ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
                if( ms >= self.__m_Interval ):
                    t1 = t2
                    self.__saveSequentialImage()
                    

            cv2.waitKey(5) # wait for 5ms

            # フレームを表示する
            self.__m_ViewImg = self.__m_Frame.copy()
            cv2.circle( self.__m_ViewImg, self.__m_CropCenter, g_FrameCenterRadius, g_FrameColor, g_FrameThickness )
            cv2.rectangle( self.__m_ViewImg, self.__m_CropStart, self.__m_CropEnd, g_FrameColor, g_FrameThickness )
            cv2.imshow( 'Capture', self.__m_ViewImg )

        cv2.destroyAllWindows()


    def stopCapture(self):
        print( 'stop...' )
        self.__m_bCapturing = False
        


    def pauseCapture(self):
        print( 'pause...' )
        self.__m_bPaused = not(self.__m_bPaused)


    def quitCapture(self):
        print( 'quit application' )
        cv2.destroyAllWindows()
        self.__m_Cap.release()
        #QCoreApplication.quit()


    def saveImage( self, dir ):
        fullpath = os.path.join( dir, 'img.png' )
        print( 'saving image...', fullpath )
        crop_img = self.__m_Frame[ self.__m_CropStart[1]:self.__m_CropEnd[1], self.__m_CropStart[0]:self.__m_CropEnd[0] ] # フレームをリサイズ
        cv2.imwrite( fullpath, crop_img )
       

    def saveSequentialImage( self, dir ):
        self.__m_bSequential = not(self.__m_bSequential ) 

        self.__m_Dir = dir
        self.__m_ImgCount = 0


    def __saveSequentialImage( self ):

        filename = 'img_' + str(self.__m_ImgCount).zfill(10) + '.png'
        fullpath = os.path.join( self.__m_Dir, filename )
        print( 'saving image...', fullpath )
        crop_img = self.__m_Frame[ self.__m_CropStart[1]:self.__m_CropEnd[1], self.__m_CropStart[0]:self.__m_CropEnd[0] ] # フレームをリサイズ
        cv2.imwrite( fullpath, crop_img ) 

        self.__m_ImgCount += 1




    def isReady( self ):
        return self.__m_Cap.isOpened()


    def MoveCropRect( self, delta ):
        if( (self.__m_CropStart[0]<=0 and delta[0]<0) or (self.__m_CropStart[1]<=0 and delta[1]<0) or
            (self.__m_CropEnd[0]>=self.__m_CameraSize[0] and delta[0]>0) or (self.__m_CropEnd[1]>=self.__m_CameraSize[1] and delta[1]>0) ):
            return
        self.__m_CropCenter = ( self.__m_CropCenter[0] + delta[0], self.__m_CropCenter[1] + delta[1] )
        self.__m_CropStart = ( self.__m_CropStart[0] + delta[0], self.__m_CropStart[1] + delta[1] )
        self.__m_CropEnd = ( self.__m_CropEnd[0] + delta[0], self.__m_CropEnd[1] + delta[1] )

        print( 'set center:(' + str(self.__m_CropCenter[0]) + ', ' + str(self.__m_CropCenter[1]) + ')' )


    def ScaleCropRect( self, delta ):
        if( ( self.__m_CropStart[0]<=0 or self.__m_CropStart[1]<=0 or self.__m_CropEnd[0]>=self.__m_CameraSize[0] or self.__m_CropEnd[1]>=self.__m_CameraSize[1] ) and delta>0 ):
            return

        self.__m_CropSize = ( int(clamp(self.__m_CropSize[0] + 2*delta, 0, self.__m_CameraSize[0])), int(clamp(self.__m_CropSize[1] + 2*delta, 0, self.__m_CameraSize[1])) )
        self.__m_CropStart = ( self.__m_CropStart[0] - delta, self.__m_CropStart[1] - delta )
        self.__m_CropEnd = ( self.__m_CropEnd[0] + delta, self.__m_CropEnd[1] + delta )

        print( 'set crop size:(' + str(self.__m_CropSize[0]) + ', ' + str(self.__m_CropSize[1]) + ')' )


    def InitCropRect( self ):
        self.__m_CropSize = ( int(clamp(self.__m_DefaultCropSize[0], 0, self.__m_CameraSize[0])),
                             int(clamp(self.__m_DefaultCropSize[1], 0, self.__m_CameraSize[1])) )

        self.__m_CropStart = ( int(clamp((self.__m_CameraSize[0]-self.__m_CropSize[0])/2, 0, self.__m_CameraSize[0])),
                              int(clamp((self.__m_CameraSize[1]-self.__m_CropSize[1])/2, 0, self.__m_CameraSize[1])) )

        self.__m_CropEnd = ( clamp(self.__m_CropStart[0]+self.__m_CropSize[0], 0, self.__m_CameraSize[0]),
                            clamp(self.__m_CropStart[1]+self.__m_CropSize[1], 0, self.__m_CameraSize[1]) )

        self.__m_CropCenter = ( int((self.__m_CropStart[0]+self.__m_CropEnd[0])/2),
                               int((self.__m_CropStart[1]+self.__m_CropEnd[1])/2) )

        self.__m_bMirror= False

        print( 'reset crop setteings...' )


    def SwitchMirrorMode( self ):
        self.__m_bMirror = not(self.__m_bMirror)
        print( 'set self.__m_bMirror mode: ', str(self.__m_bMirror) )




class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle( 'VideoCapture Control Panel' )

        self.__m_OutputDir = os.path.dirname(os.path.abspath(__file__))
        self.__m_Capture = Capture()

        if( self.__m_Capture.isReady()==False ):
            print( 'webacmaera not connected.' )
            sys.exit()


        self.__m_PlayButton = QPushButton(self)
        self.__m_PlayButton.setFixedSize( 36, 36 )
        self.__m_PlayButton.clicked.connect( self.__play )
        pixmap = QPixmap( 'play.png' )
        playIcon = QIcon( pixmap )
        self.__m_PlayButton.setIcon( playIcon )
        self.__m_PlayButton.setIconSize( pixmap.rect().size() )


        self.__m_PauseButton = QPushButton(self)
        self.__m_PauseButton.setFixedSize( 36, 36 )
        self.__m_PauseButton.clicked.connect( self.__pause )
        pixmap = QPixmap( 'pause.png' )
        playIcon = QIcon( pixmap )
        self.__m_PauseButton.setIcon( playIcon )
        self.__m_PauseButton.setIconSize( pixmap.rect().size() )


        self.__m_StopButton = QPushButton(self)
        self.__m_StopButton.setFixedSize( 36, 36 )
        self.__m_StopButton.clicked.connect( self.__stop )
        pixmap = QPixmap( 'stop.png' )
        playIcon = QIcon( pixmap )
        self.__m_StopButton.setIcon( playIcon )
        self.__m_StopButton.setIconSize( pixmap.rect().size() )


        self.__m_CaptureButton = QPushButton(self)
        self.__m_CaptureButton.setFixedSize( 36, 36 )
        self.__m_CaptureButton.clicked.connect( self.__save )
        pixmap = QPixmap( 'capture.png' )
        playIcon = QIcon( pixmap )
        self.__m_CaptureButton.setIcon( playIcon )
        self.__m_CaptureButton.setIconSize( pixmap.rect().size() )


        self.__m_SeqCaptureButton = QPushButton(self)
        self.__m_SeqCaptureButton.setFixedSize( 36, 36 )
        self.__m_SeqCaptureButton.clicked.connect( self.__seq_save )
        pixmap = QPixmap( 'seq_capture.png' )
        playIcon = QIcon( pixmap )
        self.__m_SeqCaptureButton.setIcon( playIcon )
        self.__m_SeqCaptureButton.setIconSize( pixmap.rect().size() )



        # set default button states
        self.__m_PlayButton.setEnabled( True )
        self.__m_StopButton.setEnabled( False )
        self.__m_PauseButton.setEnabled( False )
        self.__m_CaptureButton.setEnabled( False )
        self.__m_SeqCaptureButton.setEnabled( False )


        self.select_dir_edit = QLineEdit( self.__m_OutputDir )
        self.select_dir_edit.setFixedHeight( 25 );
        self.select_dir_edit.returnPressed.connect( self.__setOutputDir )


        self.select_dir_button = QPushButton( '...', self )
        self.select_dir_button.setFixedSize( 20, 25 )
        self.select_dir_button.clicked.connect( self.__selectOutputDir )


        vbox = QGridLayout(self)
        vbox.addWidget( self.select_dir_edit, 0, 0, 1, 5 )
        vbox.addWidget( self.select_dir_button, 0, 5 )
        vbox.addWidget( self.__m_PlayButton, 1, 0, Qt.AlignLeft )
        vbox.addWidget( self.__m_PauseButton, 1, 1, Qt.AlignLeft )
        vbox.addWidget( self.__m_StopButton, 1, 2, Qt.AlignLeft )
        vbox.addWidget( self.__m_CaptureButton, 1, 3, Qt.AlignLeft )
        vbox.addWidget( self.__m_SeqCaptureButton, 1, 4, Qt.AlignLeft )

        vbox.setColumnStretch(4, 2)
        vbox.setRowStretch(2, 1)

        self.setLayout( vbox )
        self.setGeometry( 100, 100, 400, 100 )
        #self.show()



    def __selectOutputDir( self ):
        newdir = str( QFileDialog.getExistingDirectory( self, 'Select Directory', self.__m_OutputDir ) )
        if( newdir != '' ):
            self.__m_OutputDir = newdir
            self.select_dir_edit.setText( self.__m_OutputDir )


    def __setOutputDir( self ):
        self.__m_OutputDir = self.select_dir_edit.text()
        self.select_dir_edit.clearFocus()


    def __play( self ):
        # update button states
        self.__m_PlayButton.setEnabled( False )
        self.__m_StopButton.setEnabled( True )
        self.__m_PauseButton.setEnabled( True )
        self.__m_CaptureButton.setEnabled( True )
        self.__m_SeqCaptureButton.setEnabled( True )

        self.__m_Capture.playCapture()


    def __pause( self ):
        # update button states
        self.__m_PlayButton.setEnabled( True )
        self.__m_StopButton.setEnabled( True )
        self.__m_PauseButton.setEnabled( False )
        self.__m_CaptureButton.setEnabled( True )
        self.__m_SeqCaptureButton.setEnabled( True )

        self.__m_Capture.pauseCapture()



    def __stop( self ):
        # update button states
        self.__m_PlayButton.setEnabled( True )
        self.__m_StopButton.setEnabled( False )
        self.__m_PauseButton.setEnabled( False )
        self.__m_CaptureButton.setEnabled( False )
        self.__m_SeqCaptureButton.setEnabled( False )

        self.__m_Capture.stopCapture()


    def __save( self ):
        if( os.path.exists(self.__m_OutputDir) ):
            self.__m_Capture.saveImage( self.__m_OutputDir )
        else:
            print( 'cannot save image...invalid file path.' )


    def __seq_save( self ):
        if( os.path.exists(self.__m_OutputDir) ):
            self.__m_Capture.saveSequentialImage( self.__m_OutputDir )
        else:
            print( 'cannot save image...invalid file path.' )


    def play( self ):
        self.__play()


    ################ override QWidget's virtual functions  #################

    #def showEvent(self, event):
    #    return super(Window, self).showEvent(event)



    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        
        if( focused_widget == self.select_dir_edit ):
            focused_widget.clearFocus()

        return super(Window, self).mousePressEvent(event)


    def closeEvent( self, event ):

        self.__m_Capture.stopCapture()
        self.__m_Capture.quitCapture()

        return super(Window, self).closeEvent( event )



    def keyPressEvent( self, event ):

        if( event.key() == Qt.Key_Right ):
            self.__m_Capture.MoveCropRect( (1,0) )

        elif( event.key() == Qt.Key_Left ):
            self.__m_Capture.MoveCropRect( (-1,0) )

        elif( event.key() == Qt.Key_Up ):
            self.__m_Capture.MoveCropRect( (0,-1) )

        elif( event.key() == Qt.Key_Down ):
            self.__m_Capture.MoveCropRect( (0,1) )

        elif( event.key() == Qt.Key_R ):# r key... reset
            self.__m_Capture.InitCropRect()

        elif( event.key() == Qt.Key_M ): # m key... self.__m_bMirror image
            self.__m_Capture.SwitchMirrorMode()

        elif( event.key() == Qt.Key_Plus ): # + key... expand crop area
            self.__m_Capture.ScaleCropRect( 1 )

        elif( event.key() == Qt.Key_Minus ): # - key... shrink crop area
            self.__m_Capture.ScaleCropRect( -1 )

        elif( event.key() == Qt ):
            self.__m_Capture.MoveCropRect( (1,0) )

        else:
            return super(Window, self).keyPressEvent(event)



if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())