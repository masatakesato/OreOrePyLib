import oreorepylib.utils.environment

import oreorepylib.network as oreoreRPC


# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data


host = 'localhost'
port = 5007

if __name__=='__main__':
    
    client = oreoreRPC.Client( host, port, 60, 5 )
    #client = oreoreRPC.SSLClient( host, port, 60, 5 )

    print( client.call( u'add', 5, 5 ) )
    print( client.call( u'add', 5, 4, 3 ) )
    print( client.call( u'add', 5, 2 ) )
    
    #for i in range(5):
    #    print( client.call( 'Sum', i, 1 ) )
