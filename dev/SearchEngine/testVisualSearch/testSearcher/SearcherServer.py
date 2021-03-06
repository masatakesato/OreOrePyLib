import oreorepylib.utils.environment

import pathlib
import argparse

import oreorepylib.network.tcp as tcp

from Searcher import Searcher



path_root = pathlib.Path( '../data' )




class SearcherServer( Searcher ):

    def __init__( self, path_root=None ):
        super(SearcherServer, self).__init__(path_root)


    def echo(self):
        return 'echo'



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument( '--host', type=str, default='localhost' )
    parser.add_argument( '--port', type=int, default=5007 )

    args = parser.parse_args() 

    host = args.host
    port = args.port


    searcher = SearcherServer()
    searcher.Init( path_root )
    #server = tcp.Server( searcher )
    #server = tcp.SSLServer( searcher )
    server = tcp.ServerThreading( searcher )
    #server = tcp.ServerPrethreading( searcher )

    try:
        server.listen( host, port, backlog=10 )
        server.run()
    except KeyboardInterrupt:
        server.close()






    