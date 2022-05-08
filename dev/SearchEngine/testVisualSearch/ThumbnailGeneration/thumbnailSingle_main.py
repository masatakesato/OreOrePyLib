import traceback
import pathlib
import numpy as np
from PIL import Image



path_wrangled = pathlib.Path( '../data/wrangled' )
path_features = pathlib.Path( '../data/features' )
path_thumbnails = pathlib.Path('../data/thumbnails' )

window_size = 2



if __name__=='__main__':
    
    path = path_features / '1089_Sparks_08.npz'
    feature_batch = np.load( path )['arr_0']

# 0_Explosion_05
# 1892_SC107T
# 1089_Sparks_08
# 1091_Welding_Out-of-Focus_01
# 1088_FireCracker_02
# 93_FireCracker_02


    #print( feature_batch )
    #print( feature_batch[:,1] )# これで列成分だけ取得できる

    #================= 移動平均を出す ================#

    vec_mvavg = []
    b = np.ones(window_size) / window_size
    for dim in range(feature_batch.shape[1]):
        vec_mvavg.append( np.convolve( feature_batch[:,dim], b, 'same' ) )

    vv = np.array( vec_mvavg ).transpose()
    #print( vv )


    #========= 隣接特徴量間の距離順にソートする =======#
    norms = np.linalg.norm( vv, axis=-1 )
    
    ds = []
    for i in range( vv.shape[0] ):
        i_next = min( i+1, vv.shape[0]-1 )
        i_prev = max( i-1, 0 )
        forward = np.dot( vv[i], vv[i_next]) / np.fmax( norms[i] * norms[i_next], 1e-6 )
        backward = np.dot( vv[i], vv[i_prev]) / np.fmax( norms[i] * norms[i_prev], 1e-6 )
        
        ds.append( np.fmin(forward, backward) )
    dists = np.array( ds )

    order = np.argsort( dists )
    print( order)
    #print( np.argmin( dists ) )
    frame_idx = max( order[0]-window_size, 0 )

    
    #============== フレームを抜き出す ================#
    imgarray = np.load( path_wrangled / path.name )['arr_0']
    
    thumbnail_name = path.stem + '.gif'
    print( path_thumbnails / thumbnail_name )

    imgs = []
    for i in range(15):
        frame_num = frame_idx + i
        if( frame_num>=imgarray.shape[0] ): break
        img = Image.fromarray( imgarray[frame_num] ).resize( (256, 256), Image.BILINEAR )
        imgs.append( img )

    imgs[0].save( path_thumbnails / thumbnail_name, save_all=True, append_images=imgs[1:], duration=100, loop=0 ) 
