import sys
import argparse
import pathlib

from VisualSearch_UI import *
import oreorepylib.network.socket as oreoreRPC



path_root = pathlib.Path('../data')
path_thumbnails = pathlib.Path( '../data/thumbnails' )# './frames' #'V:/Moa/management/datasets/fx_reference/img'#



class SearcherClient( oreoreRPC.Client ):

    def __init__( self, host, port ):
        super(SearcherClient, self).__init__( host, port, 60, 5 )
        #self.client = oreoreRPC.Client( host, port, 60, 5 )
    
    #def IsReady( self ):
    #    print('hshgsfd')
    #    return oreoreRPC.Client.IsReady()


    def InputShape( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( 'InputShape' )
        #return (0, 0, 0)


    def GetThumbnailStream( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( 'GetThumbnailStream', *argc, **argv )
        #return None


    def GetThumbnailStreams( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( 'GetThumbnailStreams', *argc, **argv )
        #return None


    def Search( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( 'Search', *argc, **argv )
        #return [], []




#host = '10.1.25.187'
#port = 5007


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument( '--host', type=str, default='10.1.27.12' )
    parser.add_argument( '--port', type=int, default=5007 )

    args = parser.parse_args() 

    host = args.host
    port = args.port


    searcher = SearcherClient( host, port )
    #searcher.Init( path_root )

    app = QApplication(sys.argv)

    window = Window( searcher, path_thumbnails )
    window.show()

    sys.exit(app.exec_())
