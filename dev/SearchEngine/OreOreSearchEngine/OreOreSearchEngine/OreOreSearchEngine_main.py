#import os

#from SearchEngine.FileCrawler import FileCrawler
#from SearchEngine.Snapshot import Snapshot


from VideoSearch.Crawler import *

from VideoSearch.Indexer import *


##=================== Crawl =====================# OK
#out, snapshot = ProcCrawl( './settings.json' )

## Output to file
#out_path = '%s_%s' % (out, snapshot.DateTime().strftime('%Y%m%d-%H%M%S') )
#snapshot.Export( out_path )


#=================== Indexing ==================# Testing

videoframes = ExtractImagesFrom( 'L:/Library/composite/readymade/movie/Gunstock_1/Clips/GS101.mov' )

#x = tf.placeholder( dtype=tf.float32, shape=[None, videoframes.shape[1], videoframes.shape[2], videoframes.shape[3]] )
g = tf.Graph()
with g.as_default():
    x, imgs = ImageAlign( [ videoframes.shape[1], videoframes.shape[2], videoframes.shape[3] ], [299, 299] )
    init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
g.finalize()


with tf.Session( graph=g ) as sess:
    sess.run( init_op )

    out = sess.run( imgs, feed_dict={ x: videoframes[0:50] } )
    print( out.shape )
    

import matplotlib.pyplot as plt


plt.imshow( out[25] )

plt.show()

#TODO: 解像度変わった画像が出力できているか確認する

#aligned_imgs = AlignImages( videoframes, 299, 299 )



