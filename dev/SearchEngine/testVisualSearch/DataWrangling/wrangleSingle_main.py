from Preview import Plt_Preview
from Wrangler import MovieWrangler
import pathlib
import numpy as np


src_path = pathlib.Path( 'V:/testVideoDataset/waterfall-free-video2.mp4' )#'L:/Library/composite/readymade/movie/ActionEssentials2/Video_Thumbnails/08. Explosions/Fireball_Day_07.mp4' )
npz_path = pathlib.Path( './test_out.npz' )



#'L:/Library/composite/readymade/movie/ReelFire2_3/EXTRAS/TRANSITS/COLOR/ARCPLA_X/ARCPLAX_.MOV'

if __name__=='__main__':
    
    wrangler = MovieWrangler( 50 )
        
    np_data = wrangler.run( str(src_path) )
        
    if( np_data.any() ):
        # save as npz files
        np.savez_compressed( npz_path, np_data.astype( np.uint8 ) )
        print( '    Saved result to: %s' % npz_path.name )
        
        Plt_Preview( npz_path )