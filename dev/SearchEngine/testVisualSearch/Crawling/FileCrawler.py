from Crawler import Crawler
from FileInfo import FileInfo
from Snapshot import Snapshot


import traceback
import pathlib
import pickle



class FileCrawler( Crawler ):

    def __init__( self, root=[], types=[] ):
        super( FileCrawler, self ).__init__()

        self.__m_Roots = [ pathlib.Path(r) for r in root ]
        self.__m_Types = types
    

    #============= Register/Unregister search directories ==============#
    def AddRootDir( self, root ):
        self.__m_Types.append( root )
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def AddRootDirs( self, roots ):
        self.__m_Types += roots
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def RemoveRootDir( self, dir ):
        try:
            self.__m_Roots.remove( dir )
        except:
            traceback.print_exc()

    
    def RemoveRootDirs( self, roots ):
        try:
            self.__m_Roots = [ r for r in self.__m_Roots if not r in roots ]
        except:
            traceback.print_exc()


    def ClearRootDirs( self ):
        self.__m_Roots.clear()


    #============= Register/Unregister file types ==============#
    def AddType( self, type ):
        self.__m_Types.append( type )
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def AddTypes( self, types ):
        self.__m_Types += types
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def RemoveType( self, type ):
        try:
            self.__m_Types.remove( type )
        except:
            traceback.print_exc()


    def RemoveTypes( self, types ):
        try:
            self.__m_Types = [ r for r in self.__m_Types if not r in types ]
        except:
            traceback.print_exc()


    def ClearTypes( self ):
        self.__m_Types.clear()


    #============= Crawl ==============#
    def Run( self ):
        
        def unique(sequence):# remove duplications while preserving order http://www.martinbroadhurst.com/removing-duplicates-from-a-list-while-preserving-order-in-python.html
            seen = set()
            return [x for x in sequence if not (x in seen or seen.add(x))]

        fileInfos = []# FileInfo object array
        
        # Gether filepathes
        paths = []
        for root in self.__m_Roots:
            for type in self.__m_Types:
                paths.extend( list( root.glob( type ) ) )

        paths = unique(paths)
        #for i, path in enumerate(paths): print( '%d: %s' % ( i, path ) )

        # Gather FileInfo
        fileInfos = [ FileInfo(p) for p in paths ]

        
        return Snapshot( [str(p) for p in self.__m_Roots], self.__m_Types, fileInfos )


    #================ Info ==============#
    def Info( self ):

        print( '//========== FileCrawler Info... ==========//')
        print( 'Registered Root Dirs:' )
        for root in self.__m_Roots:
            print( '  %s' % root )

        print( 'Scan data types:' )
        for type in self.__m_Types:
            print( '  %s' % type )



#======================= test code ===========================#

#if __name__=='__main__':

    
#    types = [ '**/*.*' ]
#    root = [ './' ]

#    crawler = FileCrawler( root=root, types=types )

#    snapshot = crawler.Run()

#    #snapshot.Info()

#    snapshot.Export( './snapshot.pkl' )
    
#    snapshot_copy = Snapshot()
#    snapshot_copy.Import( './snapshot.pkl' )
#    snapshot_copy.Info()


#    snapshot2 = crawler.Run()
#    snapshot2.Export( './snapshot2.pkl' )
#    snapshot2.Compare( snapshot )