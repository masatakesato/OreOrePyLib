from oreorepylib.utils import environment
import oreorepylib.network as oreoreRPC

import io
import pathlib
from PIL import Image



# https://teratail.com/questions/71426
# https://stackoverflow.com/questions/39603978/reading-a-tarfile-into-bytesio


class ImageLoadServer:

    def Load( self, path ):
        path_img = pathlib.Path( path )

        if( not path_img.is_file() ):
            return None
        
        print( str(path_img) )

        with open( path_img, 'rb' ) as f:
            img_read = f.read()
        
        return img_read


    def LoadMultiple( self, paths ):
        return None





#https://stackoverflow.com/questions/15189888/python-socket-accept-in-the-main-thread-prevents-quitting



if __name__=='__main__':

    #server = oreoreRPC.Server( ImageLoadServer() )
    #server = oreoreRPC.SSLServer( ImageLoadServer() )
    #server = oreoreRPC.ServerThreading( ImageLoadServer() )
    server = oreoreRPC.ServerPrethreading( ImageLoadServer() )

    try:
        server.listen( host='localhost', port=5007, backlog=10 )
        server.run()
    except KeyboardInterrupt:
        server.close()
