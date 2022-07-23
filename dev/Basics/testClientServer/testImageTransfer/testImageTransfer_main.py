from oreorepylib.utils import environment
import oreorepylib.network.socket as oreoreRPC

#import numpy as np
import io
from PIL import Image


# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

# https://teratail.com/questions/71426

host = 'localhost'
port = 5007


if __name__=='__main__':
    
    client = oreoreRPC.Client( host, port, 60, 5 )
    #client = oreoreRPC.SSLClient( host, port, 60, 5 )
    
    data_bin = client.call( 'Load', './0_Explosion_05.gif' )

    data_io = io.BytesIO( data_bin )
    img_pil = Image.open( data_io )

    print(img_pil.is_animated)
    print(img_pil.n_frames)
