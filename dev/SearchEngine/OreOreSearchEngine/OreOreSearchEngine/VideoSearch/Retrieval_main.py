import sys
import time

import pickle
import pathlib
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

from SearchUI import *




def progress( p, l ):
    sys.stdout.write("\r%d / 100" %(int(p * 100 / (l - 1))))
    sys.stdout.flush()




def Expand2Square( pil_img, background_color ):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new( pil_img.mode, (width, width), background_color )
        result.paste( pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new( pil_img.mode, (height, height), background_color )
        result.paste(pil_img, ((height - width) // 2, 0))
        return result



def LoadImage( path, bSquare=True, img_size=None, bg_color=(0,0,0) ):
    # load image
    img = Image.open( str(path) ).convert('RGB')
    if( bSquare ):  img = Expand2Square( img, bg_color )# alignt to square shape
    if( img_size ): img = img.resize( img_size, Image.LANCZOS )# resize image

    # construct numpy array
    img_np = np.array( img ).astype(np.float32) / 255.0 # normalize to [0, 1]
    while( img_np.shape[-1]>3): img_np = np.delete(img_np, -1, axis=-1)# align to 3 channel

    return img_np



def LoadFeatures( root_path ):

    #print( 'Loading features from: %s' % str(root_path) )

    i = 0
    feature_dict = {}
    npz_paths = list( root_path.glob( '**/*.npz' ) )
    for p in npz_paths:
        i += 1
        sys.stdout.write( '\r  %d / %d' %(i, len(npz_paths)) )
        sys.stdout.flush()

        mov_name = p.name.replace( p.suffix, '' )
        feature_dict[ mov_name ] = np.load( p.absolute() )['arr_0']
        
    return feature_dict



def LoadLinks( path ):

    print( 'Loading links from: %s' % str(path) )

    f = open( str(path), 'rb' )
    return pickle.load(f)




def SearchProc( sess, query_path, features, data_paths, feature_extractor, img_size ):
    
    #============= Extract feature vector from query image ============#
    print( '    Extracting query feature...', end='' )
    # load query image.
    print( str(query_path) )
    images = np.array( [ LoadImage( query_path, True, img_size ) ] )
    # extract feature vector using cnn.
    #sess.run( tf.global_variables_initializer() )
    query_feature = sess.run( feature_extractor, feed_dict={ x: images } )
    print( '    done.' )

    #================== Compare with dataset features =================#

    print( '    Retrieving...', end='' )
    result = [None] * len(features)
    dist = np.empty( len(features) )
    i=0
    for k, v in features.items():
        #print( '    %s:'% k, v.shape )

        norm_a = np.linalg.norm( query_feature[0] )
        norm_b = np.linalg.norm( v, axis=-1 )
    
        video_frame_distances = np.dot( v, query_feature[0] ) / np.fmax( norm_a * norm_b, 1.0e-6 )

        nearest = np.argmax( video_frame_distances )

        result[i] = (k, nearest, data_paths[k])
        dist[i] = video_frame_distances[ nearest ]
        i+=1

    order = np.argsort( -dist )# 降順で受け取りたいので、distの正負反転させた

    print( '    done.' )

    return result, order



g_FeaturePath = './features'#'V:/Moa/management/features/fx_reference'#
g_ThumbnailPath = './frames'#'V:/Moa/management/datasets/fx_reference/img'#


if __name__=='__main__':

    app = QApplication(sys.argv)

    #====================== Load pretrained model =====================#
    print( 'Loading pretrained model...' )
    module = hub.Module("https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1")
    height, width = hub.get_expected_image_size( module )
    x = tf.placeholder( dtype=tf.float32, shape=[None, height, width, 3] )    
    feature_extractor = module(x)
    

    #===================== Extract Dataset features ===================#
    feature_path = pathlib.Path( g_FeaturePath )
    thumbnail_path = pathlib.Path( g_ThumbnailPath )

    print( 'Loading data paths...' )
    data_paths = LoadLinks( thumbnail_path / 'links.pkl' )

    print( 'Loading features...%s' % str(feature_path) )
    features = LoadFeatures( feature_path )


    #===================== Init tensorflow session ===================#
    print( 'Initializing tensorflow...' )
    sess = tf.Session()
    sess.run( tf.global_variables_initializer() )


    serach_proc = functools.partial( SearchProc, sess=sess, features=features, data_paths=data_paths, feature_extractor=feature_extractor, img_size=(width, height) )

    window = Window( serach_proc, thumbnail_path )
    window.show()

    sys.exit(app.exec_())
