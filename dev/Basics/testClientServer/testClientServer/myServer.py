import oreorepylib.utils.environment

import oreorepylib.network.socket as oreoreRPC#from oreorelib.network import server_threading
import time


class AddServer:
    def add( self, x, y ):
        time.sleep(5)
        return x + y



#https://stackoverflow.com/questions/15189888/python-socket-accept-in-the-main-thread-prevents-quitting



if __name__=='__main__':

    #server = oreoreRPC.Server( AddServer() )
    #server = oreoreRPC.SSLServer( AddServer() )
    #server = oreoreRPC.ServerThreading( AddServer() )# server_threading.ServerThreading( AddServer() )
    server = oreoreRPC.ServerPrethreading( AddServer(), 6 )

    try:
        server.listen( host='localhost', port=5007, backlog=10 )
        server.run()
    except KeyboardInterrupt:
        server.close()
