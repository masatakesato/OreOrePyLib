from Snapshot import Snapshot
from FileInfo import FileInfo


import traceback
import pathlib
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
#import time



class FileLoader:
    
    def __init__( self, path_root ):
        self.__m_Root = path_root


    def Load( self, file_name ):
        path_file = self.__m_Root / file_name

        if( not path_file.is_file() ):
            return None
        
        return open( path_file, 'rb' ).read()




class Searcher:

    def __init__( self, path_root=None ):
        self.__m_Snapshot = None
        self.__m_FeatureExtractor = None
        self.__m_Sess = None
        self.__m_refFeatureDatabase = []
        self.__m_ThumbnailLoader = None

        if( path_root ): self.Init( path_root )



    def Init( self, path_root ):        
        self.LoadSnapshot( path_root / 'snapshot/snapshot.pkl' )
        self.LoadFeatureDatabase( path_root / 'features' )
        self.LoadFeatureExtractor()

        self.__m_ThumbnailLoader = FileLoader( path_root / 'thumbnails' )



    def LoadSnapshot( self, path_snapshot ):
        self.__m_Snapshot = Snapshot()
        self.__m_Snapshot.Import( path_snapshot )



    def LoadFeatureExtractor( self ):
        module = hub.Module( 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1' )
        height, width = hub.get_expected_image_size( module )
        x = tf.placeholder( dtype=tf.float32, shape=[None, height, width, 3] )    
        self.__m_FeatureExtractor = { 'in': x, 'out': module(x) }

        self.__m_Sess = tf.Session()
        self.__m_Sess.run( tf.global_variables_initializer() )



    def LoadFeatureDatabase( self, path_features ):

        if( self.__m_Snapshot is None ):
            return
        
        self.__m_refFeatureDatabase.clear()
        
        for i, info in enumerate( self.__m_Snapshot.FileInfos() ):            
            feature_name = '%d_%s.npz' % ( i, info.FileName() )
            path_feature = path_features / feature_name
            
            if( path_feature.is_file() is False ):
                print( 'feature is invalid: %s' % str(feature_name) )
                self.__m_refFeatureDatabase.append( np.full( (1, 2048), -1.0 ) )
            else:
                print( str( path_feature ) )
                self.__m_refFeatureDatabase.append( np.load( str( path_feature ) )[ 'arr_0' ] )

            #sys.stdout.write( '\r  %d / %d' %(i, len(self.__m_Snapshot.FileInfos())) )
            #sys.stdout.flush()


    def IsReady( self ):
        return True



    def InputShape( self ):
        return self.__m_FeatureExtractor['in'].get_shape().as_list()



    # query_img: numpy image data
    def Search( self, pixel_arrays ):
    
        #======== Setup numpy image data from pixel array =======#
        input_shape = self.InputShape()
        query_images = []
        for pixel_data in pixel_arrays:
            # must be normalized because of feature extractor's specification
            np_img = np.array( pixel_data ).reshape( input_shape[2], input_shape[1], input_shape[3] ).astype(np.float32) / 255.0
            # align to 3 channel
            while( np_img.shape[-1]>3): np_img = np.delete( np_img, -1, axis=-1 )
            query_images.append( np_img )


        #=============== Extract feature vector =================#
        print( 'Extracting query features...', end='' )
        query_feature = self.__m_Sess.run( self.__m_FeatureExtractor['out'], feed_dict={ self.__m_FeatureExtractor['in']: np.array( query_images ) } )
        print( 'done.' )


        #============ Compare with dataset features =============#
        print( '    Retrieving...', end='' )
        result = [None] * len( self.__m_refFeatureDatabase )
        dist = np.empty( len(self.__m_refFeatureDatabase) )

        for ID in range( len(self.__m_refFeatureDatabase) ):
            norm_a = np.linalg.norm( query_feature[0] )
            norm_b = np.linalg.norm( self.__m_refFeatureDatabase[ID], axis=-1 )
    
            # get closest distance from all frames
            video_frame_distances = np.dot( self.__m_refFeatureDatabase[ID], query_feature[0] ) / np.fmax( norm_a * norm_b, 1.0e-6 )
            nearest_frame = np.argmax( video_frame_distances )
            
            # store result
            fileinfo = self.__m_Snapshot.FileInfo(ID)
            result[ID] = ( fileinfo.FileName(), int(nearest_frame), fileinfo.FilePath(), ID )#( fileinfo.FileName(), int(nearest_frame), str(fileinfo.FilePath().resolve().absolute()), ID )
            dist[ID] = video_frame_distances[ nearest_frame ]

        order = np.argsort( -dist ).tolist()# 降順で受け取りたいので、distの正負反転させた

        print( '    done.' )

        #time.sleep(5)

        return [ result[i] for i in order ]



    def GetThumbnailStream( self, ID ):
        try:
            thumbnail_name = '%d_%s.gif' % (ID, self.__m_Snapshot.FileInfo(ID).FileName())
            print( 'GetThumbnailStream...%s' % thumbnail_name )
            return self.__m_ThumbnailLoader.Load( thumbnail_name )
        except:
            return None


    def GetThumbnailStreams( self, ids=[] ):
        streams = []
        for id_ in ids: streams.append( self.GetThumbnailStream(id_) )
        return streams
    