import sys
import pathlib

from VisualSearch_UI import *
from Searcher import Searcher



path_root = pathlib.Path('../data')
path_thumbnails = pathlib.Path( '../data/thumbnails' )# './frames' #'V:/Moa/management/datasets/fx_reference/img'#



if __name__=='__main__':

    searcher = Searcher()
    searcher.Init( path_root )

    app = QApplication(sys.argv)

    window = Window( searcher, path_thumbnails )
    window.show()

    sys.exit(app.exec_())
