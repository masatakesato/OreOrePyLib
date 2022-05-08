import traceback
import math
import pathlib
import numpy as np
import skvideo.io
import tensorflow as tf



# in_size = [ batch_size, height, width, channels ]
def TF_ImageAlign( out_size, data_type ):# in_size
    
    # define placeholder for image input
    x = tf.placeholder( dtype=data_type, shape=[None, None, None, None] )
    crop_size = tf.placeholder( dtype=tf.int32, shape=[] )
    
    # crop to square
    #crop_size = max( tf.shape(x)[1], tf.shape(x)[2] )
    tf_images = tf.image.resize_image_with_crop_or_pad( x, crop_size, crop_size )

    # resize to target resolution
    tf_images = tf.image.resize_images( tf_images, out_size, method = tf.image.ResizeMethod.BILINEAR, align_corners=True )
    
    return { 'in': x, 'out': tf_images, 'crop_size': crop_size }




# ram version. unused(2019.04.11).
def TF_ResizeAndCrop( sess, model, batch_size, img_array ):

    num_batches = int( math.ceil( img_array.shape[0] / batch_size ) )
    crop_size = max( img_array.shape[1], img_array.shape[2] )
    img_batches = []

    for batch_i in range( num_batches ):
        start_idx = batch_i * batch_size
        end_idx = min( start_idx + batch_size, img_array.shape[0] )
            
        print( 'TF_ResizeAndCrop... processing image batch[%d : %d]' % (start_idx, end_idx) )

        # scale and crop
        out = sess.run( model['out'], feed_dict = { model['in']: img_array[start_idx:end_idx], model['crop_size']: crop_size } )
        
        img_batches.append( out )

    return np.concatenate( img_batches )



# generator version. avoiding out-of-memory.
def TF_ResizeAndCrop_gen( sess, model, batch_size, img_gen ):

    def procImageBatch( sess, model, img_array ):
        crop_size = max( img_array.shape[1], img_array.shape[2] )
        return sess.run( model['out'], feed_dict = { model['in']: img_array, model['crop_size']: crop_size } )
        
    img_array = []
    img_batches = []

    try:
        for i, frame in enumerate(img_gen):
            img_array.append( frame )
        
            if( len(img_array) % batch_size == 0 ):
                print( 'TF_ResizeAndCrop_gen...Processing videoframe batch: %d' % len(img_array) )
                img_batches.append( procImageBatch( sess, model, np.stack( img_array, axis=0 ) ) )
                img_array.clear()
    except:
        traceback.print_exc()
        

    if( img_array ):
       print( 'TF_ResizeAndCrop_gen...Processing videoframe batch: %d' % len(img_array) )
       img_batches.append( procImageBatch( sess, model, np.stack( img_array, axis=0 ) ) )
       img_array.clear()

    return np.concatenate( img_batches )




# TODO: ファイルのpathlib.Pathオブジェクトを与えてデータラングリングしたnpzを返す関数がほしい

class MovieWrangler:

    def __init__( self, batch_size ):
        
        g = tf.Graph()
        with g.as_default():
            init_op = tf.group( [tf.global_variables_initializer(), tf.tables_initializer()] )
            self.cleaner = TF_ImageAlign( (299, 299), tf.uint8 )# video_frames.shape[1:], 
        
        g.finalize()
    
        config = tf.ConfigProto()
        config.gpu_options.allow_growth=True

        self.sess = tf.Session( config=config, graph=g )
        self.sess.run( init_op )

        self.batch_size = batch_size



    def run( self, file_path ):
        
        try:
            print( '//========= Processing file: %s =========//' % file_path )

            # scale/crop video frames ( generator version )
            video_gen = skvideo.io.vreader( file_path ) # 一括で読み込むとメモリ足りなくなる場合あり
            img_processed = TF_ResizeAndCrop_gen( self.sess, self.cleaner, self.batch_size, video_gen )

            # scale/crop video frames ( memory version. unused )
            #video_frames = skvideo.io.vread( str(file_path) ).astype( np.uint8 )
            #img_processed = TF_ResizeAndCrop( sess, self.cleaner, batch_size, video_frames )

            return img_processed

        except:
            traceback.print_exc()
            return None



















# load video to numpy
#video_path = 'L:/Library/composite/readymade/movie/DVM03_1/DATA1/WEB/M03_039.mov'#'L:/Library/composite/readymade/movie/PyromaniaHD/HD_2/MUSH009_HD.mov'

#dst_root = pathlib.Path( './npz' )
#src_root = pathlib.Path( 'L:/Library/composite/readymade/movie/PyromaniaHD/HD_2' )



#if __name__=='__main__':

#    try:

#        #==================== Initialize tensorflow ====================#
#        g = tf.Graph()
#        with g.as_default():
#            init_op = tf.group( [tf.global_variables_initializer(), tf.tables_initializer()] )
#            cleaner = TF_ImageAlign( (299, 299), tf.uint8 )# video_frames.shape[1:], 
        
#        g.finalize()
    
#        config = tf.ConfigProto()
#        config.gpu_options.allow_growth=True

#        sess = tf.Session( config=config, graph=g )
#        sess.run( init_op )

#        batch_size = 100


#        #===================== process video data ======================#
#        filepath_log = dst_root / 'wrangling.log'
#        log_strings = []

#        video_paths = src_root.glob( '**/*.mov' )#[ pathlib.Path( video_path ) ]#

#        for path in video_paths:

#            try:
#                print( '//========= Processing file: %s =========//' % path.name )

#                # scale/crop video frames ( generator version )
#                video_gen = skvideo.io.vreader( str(path) ) # 一括で読み込むとメモリ足りなくなる場合あり
#                img_processed = TF_ResizeAndCrop_gen( sess, cleaner, batch_size, video_gen )

#                # scale/crop video frames ( memory version. unused )
#                #video_frames = skvideo.io.vread( str(path) ).astype( np.uint8 )
#                #img_processed = TF_ResizeAndCrop( sess, cleaner, batch_size, video_frames )

#                # save as npz files
#                npz_name = path.name.replace( path.suffix, '.npz' )
#                dst_filepath = dst_root / npz_name
        
#                np.savez_compressed( dst_filepath, img_processed.astype( np.uint8 ) )
#                print( '    Saved result to: %s' % dst_filepath.name )

#            except:
#                traceback.print_exc()
#                log_strings.append( path )
#                log_strings.append( traceback.format_exc() )
#                log_strings.append( '\n' )
#                continue

#            # preview numpy image.
#            #import matplotlib.pyplot as plt
#            #plt.imshow( cleaned_data[0]/255.0 )
#            #plt.show()
#            #break

#        filepath_log.touch()
#        filepath_log.write_text( '\n'.join( log_strings ), encoding='utf-8' )


#        #========================= quit program ========================#
#        sess.close()

#    except:
        
#        traceback.print_exc()