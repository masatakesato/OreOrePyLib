import Snapshot

import pathlib


snapshot_path = pathlib.Path( '../data/snapshot/snapshot.pkl' )


if __name__=='__main__':

    snapshot = Snapshot.Snapshot()
    snapshot.Import( snapshot_path )

    snapshot.Info()