from SearchEngine.Snapshot import Snapshot

import numpy as np
import skvideo.io
import tensorflow as tf



#================== まずは単体動画ファイルで動かす ====================#

def ExtractImagesFrom( path ):
    videodata = skvideo.io.vread( path ).astype( np.float32 ) / 255.0
    
    return videodata



def ImageAlign( in_size, out_size ):
    
    # define placeholder for image input
    x = tf.placeholder( dtype=tf.float32, shape=[None, in_size[0], in_size[1], in_size[2]] )

    # crop to square
    crop_size = max( in_size[0], in_size[1] )
    tf_images = tf.image.resize_image_with_crop_or_pad( x, crop_size, crop_size )

    # resize to target resolution
    tf_images = tf.image.resize_images( tf_images, out_size, method = tf.image.ResizeMethod.BILINEAR, align_corners=True )
    
    return x, tf_images









#import skvideo.io  
#videodata = skvideo.io.vread('L:/Library/composite/readymade/movie/Gunstock_1/Clips/GS101.mov')  
#print(videodata.shape)



def ProcIndex( snapshot ):



    pass

#    TODO: Snapshotのファイルを使って動画ファイルを画像に分解する: video2Frame

#    TODO:  calcFeatureする


# TODO: ディレクトリ違いで同一名称のファイルはどうやって管理する？



##http://testpy.hatenablog.com/entry/2017/07/13/003000


#import pickle
#import pathlib
#import subprocess
#import concurrent.futures


#video_types = [ '**/*.mp4', '**/*.mov', '**/*.avi' ]


#if __name__ == '__main__':

#    srcdir = pathlib.Path( 'L:/Library/composite/readymade/movie' )
#    frames_root = pathlib.Path('./frames')
#    tgtdir = pathlib.Path('./features')


#    #===================== Output Links to actual mov file ===================#
#    movie_paths = []
#    for type in video_types:
#        movie_paths.extend( list( srcdir.glob( type ) ) )

#    movie_dict = {}# key: unique_media_name, value: fullpath
#    for i in range(len(movie_paths)):
#        movie_dict[ str(i) + '_' + movie_paths[i].name ] = movie_paths[i]

#    f = open( (frames_root / 'links.pkl').absolute(), 'wb' )
#    pickle.dump( movie_dict, f )
#    f.close()


#    #====================== Load movie files and save frame ================#

#    if( frames_root.exists()==False ):
#        frames_root.mkdir()
    

#    executor = concurrent.futures.ThreadPoolExecutor( max_workers=4 )

#    #i = 0

#    for key, movie_path in movie_dict.items():
#        frame_path = frames_root / key

#        if( frame_path.exists()==False ):
#            frame_path.mkdir()
        
#        #print( movie_path )
#        #print( frame_path )

#        #cmd = 'ffmpeg.exe -i %s -f image2 ./img/%s/img_%%06d.png' % ( data[ empty_dir ], empty_dir )
#        img_name = './frames/%s/img_%%06d.png' % key
#        #print( img_name )
#        args = [ 'ffmpeg.exe', '-i', str(movie_path), '-f', 'image2', img_name ]
        
#        executor.submit( subprocess.call, args, shell=False )#executor.submit( subprocess.Popen, args, shell=False )

#        #p = subprocess.Popen( [ 'ffmpeg.exe', '-i', str(movie_path), '-f', 'image2', img_name ], shell=False )
#        #p.wait()

#        #if( i==30): break
#        #i+=1


#    executor.shutdown( wait=True )