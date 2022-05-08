from .FileInfo import FileInfo

import os
from datetime import datetime
import time
import traceback
import pathlib
import pickle



class Snapshot:

    def __init__( self, roots=[], types=[], fileinfos=[] ):
        self.__m_Roots = roots
        self.__m_Types = types
        self.__m_FileInfos = fileinfos
        self.__m_DateTime = datetime.now()


    def Import( self, file_path ):
        with open( file_path, 'rb' ) as f:
            self.__m_Roots, self.__m_Types, self.__m_FileInfos, self.__m_DateTime = pickle.load(f)


    def Export( self, file_path ):
        with open( file_path, 'wb' ) as f:
            pickle.dump( (self.__m_Roots, self.__m_Types, self.__m_FileInfos, self.__m_DateTime), f )


    def DateTime( self ):
        return self.__m_DateTime


    def Compare( self, snapshot ):
        d = self.__m_DateTime - snapshot.__m_DateTime
        print( d.total_seconds() )
        invert = d.total_seconds()<0
        newer = snapshot if invert else self
        older = self if invert else snapshot
        
        #======= Detect ans warn root/types difference ======#        
        

        #============== Detect difference ==================#
        # TODO: Added files = newerは持ってるけどolderにはない
        # TODO: Removed files = olderは持ってるけどnewerから消えてる
        # TODO: Updated files = newerにもolderにもあって更新日時が変わっている





    def Info( self ):

        print( '//========== Snapshot... ==========//')
        print( 'RootDirs:' )
        for root in self.__m_Roots:
            print( '  %s' % str(root) )

        print( 'Types:' )
        for type in self.__m_Types:
            print( '  %s' % type )

        print( 'Files:' )
        for file in self.__m_FileInfos:
            print( '  %s:\n    %s' % (file.FileName(), file.CreationTime()) )
