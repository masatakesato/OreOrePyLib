from Preview import Plt_Preview
import pathlib


npz_path = pathlib.Path( '../data/wrangled/10_waterfall-free-video8.npz' )


if __name__=='__main__':
    Plt_Preview( npz_path )