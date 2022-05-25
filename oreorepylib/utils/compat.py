import sys

Python3x = sys.version_info.major == 3
Python2x = sys.version_info.major == 2



if( Python3x ):

    def ToUnicode( string ):
        return string



    def Input( prompt=None ):

        return input( prompt )



else:

    def ToUnicode( string ):
        return unicode( string )



    def Input( prompt=None ):
        return raw_input( prompt )
