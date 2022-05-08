from Snapshot import Snapshot
from FileInfo import FileInfo

from Wrangler import MovieWrangler
import pathlib
import pickle

import numpy as np



path_snapshot = pathlib.Path( '../data/snapshot' )
dst_root = pathlib.Path( '../data/wrangled' )




if __name__=='__main__':
    
    snapshot = Snapshot()
    snapshot.Import( path_snapshot / 'snapshot.pkl' )


    wrangler = MovieWrangler( 50 )
    
    filepath_log = dst_root / 'wrangling.log'
    log_strings = [ '[ Wrangling failed at... ]' ]

    
    for i, info in enumerate( snapshot.FileInfos() ):
        # wrangle video data
        np_data = wrangler.run( info.FilePath() )

        if( np_data is None ):
            log_strings.append( '%d: %s' % ( i, str(info.FilePath()) ) )
            continue

        #print( '%d_%s' % ( i, info.FileName() ) )

        # save as npz files
        file_name = '%d_%s.npz' % (i, info.FileName())
        np.savez_compressed( dst_root / file_name, np_data.astype( np.uint8 ) )
        print( '    Saved result to: %s' % file_name )


    filepath_log.touch()
    filepath_log.write_text( '\n'.join( log_strings ), encoding='utf-8' )