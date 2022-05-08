from SearchEngine.FileCrawler import FileCrawler

import json

#types = []
#root_paths = []
#snapshot_path = []



def ProcCrawl( path ):

    #=========== Load Crawl config from json ===============#
    # https://qiita.com/Yuu94/items/9ffdfcb2c26d6b33792e windowsだとエンコードで引っかかる
    with open( path, 'r', encoding='utf-8_sig' ) as f:
        settings = json.load(f)

    root = settings['crawl']['root_path']
    types = settings['crawl']['types']
    out = settings['crawl']['out_path']

    print( root )
    print( types )
    print( out )


    #========= Crawl directory and gather fileinfo ========#
    crawler = FileCrawler( root=root, types=types )
    snapshot = crawler.Run()
    #snapshot.Info()

    return out, snapshot