﻿from INode import INode

import traceback
import types



TODO: INodeを継承したクラスを生成したい. 2019.10.13
TODO: クラス生成時に関数定義(InitializeとCompute)を生成したい. 2019.10.13
TODO: ClassTemplateで頑張ってる部分をmetaclass使ってうまく解決できるか？？？. 2019.10.13




# Declare new class
ClassTemplate = '''
class %s( INode ):
    def __init__( self ):
        super(%s, self).__init__( '%s' )

    #def Initialize( self ):
    #    print( 'CLASS::Initialize()...' )

    #def Compute( self, dataBlock ):
    #    print( 'CLASS::Compute()...' )
'''



def Build( class_name, custom_code ):

    exec( ClassTemplate % ( (class_name,) * ClassTemplate.count('%s') ), globals() )
    ClassType = eval( class_name )#getattr( sys.modules[__name__], class_name )

    # Modify class methods
    exec_local = { 'Initialize': None, 'Compute': None }
    exec( custom_code, globals(), exec_local )

    for name, func in exec_local.items():
        if( func ): setattr( ClassType, name, func )



def Modify( obj, custom_code ):

    # Modify class methods
    exec_local = { 'Initialize': None, 'Compute': None }
    exec( custom_code, globals(), exec_local )

    #obj.Initialize = types.MethodType( exec_local['Initialize'], obj )
    #obj.Compute = types.MethodType( exec_local['Compute'], obj )

    for name, func in exec_local.items():
        if( func ): exec( 'obj.%s = types.MethodType( func, obj )' % name )



# Clear all member functions
def Delete( obj, func_name ):
    print( 'Deleting method "%s" from "%s" instance...' % ( func_name, obj.__class__.__name__ ) )
    try:
        delattr( obj, func_name )
    except AttributeError as e:
        traceback.print_exc()
