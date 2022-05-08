import traceback
import math
import pathlib
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub





def ExtractFeatures( images, module, x, batch_size, sess ):

    print( '    Extracting features...' )
    num_batches = int( math.ceil( images.shape[0] / batch_size ) )
    feature_batches = []
    for batch_i in range(num_batches):
        
        start_idx = batch_i * batch_size
        end_idx = min( start_idx + batch_size, images.shape[0] )
        
        #print( '%d: %d - %d' % (batch_i, start_idx, end_idx ) )
        #feature_extractor = module( images[start_idx:end_idx] )
        #features = sess.run( feature_extractor )

        features = sess.run( module, feed_dict={ x: images[start_idx:end_idx] } )

        feature_batches.append( features )

    return np.concatenate( feature_batches )



path_wrangled = pathlib.Path( '../data/wrangled' )
path_features = pathlib.Path( '../data/features' )



if __name__=='__main__':


    #================================= 分類器を読み込む ========================================#
    g = tf.Graph()
    with g.as_default():
        module = hub.Module("https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1")
        height, width = hub.get_expected_image_size( module )
        x = tf.placeholder( dtype=tf.float32, shape=[None, height, width, 3] )
        feature_extractor = module(x)
        init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
    g.finalize()

    batch_size = 50


    #================ 動画毎にフレーム画像群を読み込んで特徴ベクトルを抽出する =================#
    paths_img = path_wrangled.glob( '**/*.npz' )

    filepath_log = path_features / 'features.log'
    log_strings = []    


    config = tf.ConfigProto()
    config.gpu_options.allow_growth=True
    sess = tf.Session( config=config, graph=g )
    sess.run( init_op )

    for path in paths_img:
        try:
            print( '//================ processing', str(path),'================//' )
            # Load npz image array
            img_array = np.load( str(path) )['arr_0'].astype(np.float32) / 255.0 # must be normalized because of model specification

            # Extract feature vectors
            features = ExtractFeatures( img_array, feature_extractor, x, batch_size, sess )
        
            # Save features
            file_path = path_features / path.name
            print( '    saving feature: %s' % file_path, features.shape )
            np.savez_compressed( file_path, features )
    
        except:            
            log_strings.append( traceback.format_exc() )


    sess.close()

    filepath_log.touch()
    filepath_log.write_text( '\n'.join( log_strings ), encoding='utf-8' )
