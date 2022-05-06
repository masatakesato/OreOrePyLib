import umsgpack
import traceback


#class PackError(Exception): pass
#class UnpackError(Exception): pass



class Serializer:

    def __init__( self, pack_encoding, unpack_encoding ):
        print( "Serializer umsgpack ver..." )



    def Pack( self, data ):
        try:
            return umsgpack.packb( data )

        except:
            print( 'Exception occured at Serializer::Pack ')
            traceback.print_exc()
            #raise PackError( traceback.format_exc() )
            return None



    def Unpack( self, data ):
        try:
            return umsgpack.unpackb( data[:len(data)] )

        except:
            print( 'Exception occured at Serializer::Unpack ')
            traceback.print_exc()
            #raise UnpackError( traceback.format_exc() )
            return None