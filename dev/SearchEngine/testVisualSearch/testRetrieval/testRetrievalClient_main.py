﻿import oreorelib.network as oreoreRPC

import argparse
import pathlib
from PIL import Image




def AlignImage( pil_img, img_size, background_color ):

    # Crop to square
    width, height = pil_img.size
    img_cropped = None

    if width == height:
        img_cropped = pil_img
    elif width > height:
        img_cropped = Image.new( pil_img.mode, (width, width), background_color )
        img_cropped.paste( pil_img, (0, (width - height) // 2) )
    else:
        img_cropped = Image.new( pil_img.mode, (height, height), background_color )
        img_cropped.paste( pil_img, ((height - width) // 2, 0) )
    
    # Resize
    return img_cropped.resize( img_size, Image.BILINEAR )# resize image



path_root = pathlib.Path( '../data' )
path_query = pathlib.Path( './testimage.JPG' )




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument( '--host', type=str, default='localhost' )
    parser.add_argument( '--port', type=int, default=5007 )

    args = parser.parse_args() 

    host = args.host
    port = args.port


    client = oreoreRPC.Client( host, port, 60, 5 )

    input_shape = client.call( 'InputShape' )# input_shape = searcher.InputShape()
    img_size = ( input_shape[2], input_shape[1] )

    query_img = Image.open( str(path_query) ).convert('RGB')
    query_img = AlignImage( query_img, img_size, (0,0,0) )
 
    pixel_data = list( query_img.getdata() )

    results = client.call( 'Search', [ pixel_data ] )

    p = pathlib.Path( results[0][2] )
    print( p.as_posix() )

    thumbnail_ids = [ result[3] for result in results ]
    
    thumbnail_streams = client.call( 'GetThumbnailStreams', thumbnail_ids[0:10] )
    for stream in thumbnail_streams:
        print( len(stream) )