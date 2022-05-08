import FileCrawler

import pathlib
import json


path_settings = './settings.json'
path_output = pathlib.Path( '../data/snapshot' )



if __name__=='__main__':

    #=========== Load Crawl config from json ===============#
    # https://qiita.com/Yuu94/items/9ffdfcb2c26d6b33792e windowsだとエンコードで引っかかる
    with open( path_settings, 'r', encoding='utf-8_sig' ) as f:
        settings = json.load(f)

    root = settings['crawl']['root_path']
    types = settings['crawl']['types']

    print( root )
    print( types )


    #========= Crawl directory and gather fileinfo =========#
    crawler = FileCrawler.FileCrawler( root=root, types=types )
    snapshot = crawler.Run()
    #snapshot.Info()


    #==================== Output snapshot ==================#
    out_path = path_output / 'snapshot.pkl'#'%s/%s.pkl' % (path_output, snapshot.DateTime().strftime('%Y%m%d-%H%M%S') )
    snapshot.Export( out_path )







# depreated. 2019.04.19

#if __name__ == '__main__':

#    srcdir = pathlib.Path( 'L:/Library/composite/readymade/movie' )
#    video_types = [ '**/*.mp4', '**/*.mov', '**/*.avi' ]

#    #===================== Output Links to actual mov file ===================#
#    movie_paths = []
#    for type in video_types:
#        movie_paths.extend( list( srcdir.glob( type ) ) )
    
#    for i, path in enumerate(movie_paths):
#        print( '%d: %s' % ( i, path ) )