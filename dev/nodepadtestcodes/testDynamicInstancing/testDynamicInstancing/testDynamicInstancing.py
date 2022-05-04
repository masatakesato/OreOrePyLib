# https://www.slideshare.net/ssuser38b704/ll-lang-blackmagic



# https://stackoverflow.com/questions/24733831/using-a-function-defined-in-an-execed-string-in-python-3
# metaclass reference page

# https://stackoverflow.com/questions/19205608/exec-to-add-a-function-into-a-class
# add a function to class


#import numpy as np
# https://github.com/microsoft/PTVS/issues/4874 solution for dll load failure. 2019.08.13



import sys
import traceback
import types



custom_code = '''

def Initialize( self ):
    print(42)


def Compute( self ):
    result = %d
    print( result )
    return result

@staticmethod
def DDD( param ):
    print( 'param:', param )

'''

# 注意. staticmethodはインスタンスではなく一旦クラス定義に追加される.



# Base class
class IPlugin:

    def __init__( self ):
        print( 'IPlugin::__init__()...' )


    def Initialize( self ):
        print( 'IPlugin::Initialize()...' )


    def Compute( self ):
        print( 'IPlugin::Compute()...' )





def DefineBaseClass( class_name ):

    classdef = '''
class %s( IPlugin ):
    def __init__( self ):
        super(%s, self).__init__()

    def Initialize( self ):
        print( 'CLASS::Initialize()...' )

    def Compute( self ):
        print( 'CLASS::Compute()...' )
'''
    exec( classdef % ((class_name,)*classdef.count('%s')), globals() )



def DynamicClass_exec( class_name, custom_method_string ):

    #============ define class ===============#
    DefineBaseClass( class_name )

    #============ customize methods ==========#
    ClassType = eval( class_name )#getattr( sys.modules[__name__], class_name )

    exec_local = {}
    exec( custom_method_string, globals(), exec_local )

    for name, func in exec_local.items():
        if( type(func)==staticmethod ):
            setattr( ClassType, name, func )
        else:
            setattr( ClassType, name, types.MethodType( func, ClassType ) )

    exec_local.clear()



def CustomizeObjectMethod( obj, code_string ):
    try:
        exec_local = {}
        exec( code_string, globals(), exec_local )

        #for name, func in exec_local.items():
        #    if( getattr( obj, name, None ) ):# 既に定義済みの関数だけ登録する
        #        setattr( obj, name, types.MethodType( func, obj ) )

        for name, func in exec_local.items():
            if( type(func)==staticmethod ):
                setattr( type(obj), name, func )
            else:
                setattr( obj, name, types.MethodType( func, obj ) )

    except:
        traceback.print_exc()




def DynamicClass_type( class_name, custom_method_string ):

    exec_local = { 'Initialize': None, 'Compute': None }
    exec( custom_method_string, exec_local )

    return type( class_name,
             (IPlugin,),
             {
                 'Initialize': exec_local['Initialize'],
                 'Compute': exec_local['Compute'],
             }
            )




if __name__=='__main__':

    #A = type( 'A',
    #         (IPlugin,),
    #         {
    #             'sayHello': lambda self: print('ADSFSFS')
             
    #             }
    #         )
    #x = A()
    #print(type(x))
    #x.func()
    #x.sayHello()


    #exec( custom_code % 5, globals() )
    #Initialize()
    #result = Compute()


    #del Compute# 関数をメモリから削除できる


    #print( result )

    #print( Compute() )


    #Foo = DynamicClass_type( 'Foo',  custom_code % 1000 )
    #a = Foo()
    #a.Compute()



    # define CLASS0 base
    DefineBaseClass( 'CLASS0' )


    # create custom CLASS0
    c0 = CLASS0()
    #CustomizeObjectMethod( c0, custom_code % 0 )

    c0.Initialize()
    c0.Compute()
    #c0.DDD('c0 static method.')


    # create custom CLASS0
    c02 = CLASS0()
    CustomizeObjectMethod( c02, custom_code % -333 )# ここでstaticmethodがクラス定義に追加される
    
    c02.Initialize()
    c02.Compute()
    c02.DDD('c02 static method.')


    c0.DDD( 'c0 static method.' )# staticmethod追加前に生成したインスタンスからでも呼び出し可能!


    c0_base = CLASS0()
    c0_base.Initialize()
    c0_base.Compute()

    print( type(c0_base), type(c0),  type(c02) ) 


    DynamicClass_exec( 'CLASS', custom_code % -995.5 )
    c = CLASS()
    c.Compute()
    c.DDD(None)

    #Compute(None)

    #DynamicClass_exec( 'CLASS2', custom_code % 333333.5 )
    #c2 = CLASS2()
    #c2.Compute()