import math
import pathlib
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub



# 画像を正方形に成型しなおす
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



def LoadImage( path, bSquare=True, img_size=None, bg_color=(0,0,0) ):
    # load image
    img = Image.open( str(path) ).convert('RGB')
    if( bSquare ):  img = Expand2Square( img, bg_color )# alignt to square shape
    if( img_size ): img = img.resize( img_size, Image.LANCZOS )# resize image
    # construct numpy array
    img_np = np.array( img ).astype(np.float32) / 255.0 # normalize to [0, 1]
    while( img_np.shape[-1]>3): img_np = np.delete(img_np, -1, axis=-1)# align to 3 channel

    return img_np



# ディレクトリ内の全画像ファイルを読み込んでnumpy配列に変換する
def ExtractImages( path, img_size, bgcolor ):

    print( '    Extracting images...' )
    img_paths = list( path.glob('**/*.png') )  

    img_list = []
    for img_path in img_paths:    
        img_list.append( LoadImage( img_path, True, img_size, bgcolor ) )

    return np.array( img_list )




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
    src_dir = pathlib.Path( './frames' )
    out_dir = pathlib.Path( './features' )
    if( out_dir.exists()==False ):
        out_dir.mkdir()

    log_data = pathlib.Path( './features/failed.log' )
    invalid_dirs = []    


    config = tf.ConfigProto()
    config.gpu_options.allow_growth=True
    sess = tf.Session( config=config, graph=g )
    sess.run( init_op )

    for p in src_dir.iterdir():
        if( p.is_dir()==False ): continue
                
        print( '//================ processing', str(p),'================//' )
        # Extract images from path p
        images = ExtractImages( p, (width, height), (0, 0, 0) )
                
        if( images.shape[0]==0 ):
            invalid_dirs.append( str(p) )
            print( '   invalid folder. ignoring...' )
            continue

        # Extract feature vectors
        features = ExtractFeatures( images, feature_extractor, x, batch_size, sess )

        #sess.close()

        # Save features
        dst_filepath = pathlib.Path( './features/' + p.name + '.npz' )
        print( '    saving feature: %s' % dst_filepath, features.shape )

        np.savez_compressed( dst_filepath, features )
        

    log_data.touch()
    log_data.write_text( '\n'.join( invalid_dirs ), encoding='utf-8' )


#動画ディレクトリを一つ読む
#ディレクトリ内の全画像ファイルを読み込む
#ミニバッチ単位で特徴ベクトルを計算する
#全ミニバッチ分の特徴ベクトルを１つのdictionaryにまとめる feature_vec = { 'img_xxxx.png': np.array(2048) }# こんな感じ
#dictionaryをファイル保存する