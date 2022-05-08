#http://testpy.hatenablog.com/entry/2017/07/13/003000


import pickle
import pathlib
import subprocess
import concurrent.futures



#TODO: Opencv は3.3.1使うこと. matplotlib.pyplotのバージョン

#def video_2_frames( video_file='./IMG_2140.MOV', image_dir='./image_dir/', image_file='img_%s.png' ):
#    # Delete the entire directory tree if it exists.
#    if os.path.exists(image_dir):
#        shutil.rmtree(image_dir)  

#    # Make the directory if it doesn't exist.
#    if not os.path.exists(image_dir):
#        os.makedirs(image_dir)

#    # Video to frames
#    i = 0
#    cap = cv2.VideoCapture(video_file)
#    while(cap.isOpened()):
#        flag, frame = cap.read()  # Capture frame-by-frame
#        if flag == False:  # Is a frame left?
#            break
#        cv2.imwrite(image_dir+image_file % str(i).zfill(6), frame)  # Save a frame
#        print('Save', image_dir+image_file % str(i).zfill(6))
#        i += 1

#    cap.release()  # When everything done, release the capture



video_types = [ '**/*.mp4', '**/*.mov', '**/*.avi' ]


if __name__ == '__main__':

    srcdir = pathlib.Path( 'L:/Library/composite/readymade/movie' )
    frames_root = pathlib.Path('./frames')
    tgtdir = pathlib.Path('./features')


    #===================== Output Links to actual mov file ===================#
    movie_paths = []
    for type in video_types:
        movie_paths.extend( list( srcdir.glob( type ) ) )

    movie_dict = {}# key: unique_media_name, value: fullpath
    for i in range(len(movie_paths)):
        movie_dict[ str(i) + '_' + movie_paths[i].name ] = movie_paths[i]

    f = open( (frames_root / 'links.pkl').absolute(), 'wb' )
    pickle.dump( movie_dict, f )
    f.close()


    #====================== Load movie files and save frame ================#

    if( frames_root.exists()==False ):
        frames_root.mkdir()
    

    executor = concurrent.futures.ThreadPoolExecutor( max_workers=4 )

    #i = 0

    for key, movie_path in movie_dict.items():
        frame_path = frames_root / key

        if( frame_path.exists()==False ):
            frame_path.mkdir()
        
        #print( movie_path )
        #print( frame_path )

        #cmd = 'ffmpeg.exe -i %s -f image2 ./img/%s/img_%%06d.png' % ( data[ empty_dir ], empty_dir )
        img_name = './frames/%s/img_%%06d.png' % key
        #print( img_name )
        args = [ 'ffmpeg.exe', '-i', str(movie_path), '-f', 'image2', img_name ]
        
        executor.submit( subprocess.call, args, shell=False )#executor.submit( subprocess.Popen, args, shell=False )

        #p = subprocess.Popen( [ 'ffmpeg.exe', '-i', str(movie_path), '-f', 'image2', img_name ], shell=False )
        #p.wait()

        #if( i==30): break
        #i+=1


    executor.shutdown( wait=True )