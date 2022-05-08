import pickle
import pathlib
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub



def LoadFeatures( root_path ):

    print( 'Loading features from: %s' % str(root_path) )

    feature_dict = {}
    npz_paths = root_path.glob( '**/*.npz' )
    for p in npz_paths:
        mov_name = p.name.replace( p.suffix, '' )
        feature_dict[ mov_name ] = np.load( p.absolute() )['arr_0']
        
    return feature_dict


def LoadLinks( path ):

    print( 'Loading links from: %s' % str(path) )

    f = open( str(path), 'rb' )
    return pickle.load(f)



def LoadImage( path, bSquare=True, resize=None ):

    print( str(path) )

    img = Image.open( str(path) ).convert('RGB')
    if( bSquare ):  img = Expand2Square( img, (0, 0, 0) )# alignt to square shape
    if( resize ):   img = img.resize( (resize[0], resize[1]), Image.LANCZOS )# resize image

    # construct numpy array
    img_np = np.array( img ).astype(np.float32) / 255.0 # normalize to [0, 1]
    while( img_np.shape[-1]>3): img_np = np.delete(img_np, -1, axis=-1)# align to 3 channel

    return img_np



def Expand2Square( pil_img, background_color ):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new( pil_img.mode, (width, width), background_color )
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new( pil_img.mode, (height, height), background_color )
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def cos_sim( v1, v2 ):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))



if __name__ == '__main__':

    module = hub.Module("https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1")
    height, width = hub.get_expected_image_size( module )
    x = tf.placeholder( dtype=tf.float32, shape=[None, height, width, 3] )    
    feature_extractor = module(x)

    

    #================== Load query image to numpy =====================#
    print( 'Loading Images...' )
    images = np.array( [ LoadImage( './smoke.png', True, (width, height) ) ] )

    #================== Extract feature vevtor from query image ====================#
    with tf.Session() as sess:
        sess.run( tf.global_variables_initializer() )
        query_feature = sess.run( feature_extractor, feed_dict={ x: images } )


    #===================== Extract Dataset features ===================#
    feature_path = pathlib.Path( './feature' )

    features = LoadFeatures( feature_path )
    mov_links = LoadLinks( feature_path / 'links.pkl' )


    
    info = [None] * len(features)
    dist = np.empty( len(features) )
    i=0
    for k, v in features.items():
        print( '    %s:'% k, v.shape )

        norm_a = np.linalg.norm( query_feature[0] )
        norm_b = np.linalg.norm( v, axis=-1 )
    
        video_frame_distances = np.dot( v, query_feature[0] ) / np.fmax( norm_a * norm_b, 1.0e-6 )

        nearest = np.argmax( video_frame_distances )

        info[i] = (k, nearest)
        dist[i] = video_frame_distances[ nearest ]
        i+=1

    sorted_idx = np.argsort( -dist )# 降順で受け取りたいので、distの正負反転させた

    for i in range(20):
        idx = sorted_idx[i]
        print( info[idx][0], info[idx][1], mov_links[info[idx][0]] )
