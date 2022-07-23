import oreorepylib.utils.environment

import oreorepylib.network.tcp as tcp#from oreorelib.network import server_threading
import time


class AddServer:
    def add( self, x, y ):
        time.sleep(5)
        return x + y



#https://stackoverflow.com/questions/15189888/python-socket-accept-in-the-main-thread-prevents-quitting



if __name__=='__main__':

    #server = tcp.Server( AddServer() )
    #server = tcp.SSLServer( AddServer() )
    #server = tcp.ServerThreading( AddServer() )# server_threading.ServerThreading( AddServer() )
    server = tcp.ServerPrethreading( AddServer(), 6 )

    try:
        server.listen( host='localhost', port=5007, backlog=10 )
        server.run()
    except KeyboardInterrupt:
        server.close()
