import oreorepylib.utils.environment

import oreorepylib.network.tcp as tcp


# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data


host = 'localhost'
port = 5007

if __name__=='__main__':
    
    client = tcp.Client( host, port, 60, 5 )
    #client = tcp.SSLClient( host, port, 60, 5 )

    print( client.call( u'add', 5, 5 ) )
    print( client.call( u'add', 5, 4, 3 ) )
    print( client.call( u'add', 5, 2 ) )
    
    #for i in range(5):
    #    print( client.call( 'Sum', i, 1 ) )
