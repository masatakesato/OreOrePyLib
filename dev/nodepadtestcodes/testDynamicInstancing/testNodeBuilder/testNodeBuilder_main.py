import NodeManager




code_foo = '''

def Initialize( self ):
    print( 'FOO Initialize()...' )


def Compute( self ):
    print( 'FOO Compute()...' )
    result = 1111111111
    return result

'''


code_bar = '''

def Initialize( self ):
    print( 'BAR Initialize()...' )


def Compute( self ):
    print( 'BAR Compute()...' )
    result = 5555555555555
    return result

'''


code_baz = '''

def Initialize( self ):
    print( 'BAR Initialize()...' )


def Compute( self ):
    print( 'BAR Compute()...' )
    result = 5555555555555
    return result

'''



if __name__=='__main__':

    print( '//=========== build class1 =============//' )
    NodeManager.Build( 'class1', code_foo )


    print( '//=========== create instance foo =============//' )
    foo = NodeManager.class1()
    foo.Compute()

    print( '//=========== modify foo implementation to bar =============//' )
    NodeManager.Modify( foo, code_bar )
    foo.Compute()


    print( '//=========== create instance baz =============//' )
    baz = NodeManager.class1()
    baz.Compute()

    print( '//=========== execute foo =============//' )
    foo.Initialize()
    foo.Compute()

    print( '//=======================//' )
    foo.Compute()
    NodeManager.Delete( foo, 'Compute' )
    
    foo.Compute()
    NodeManager.Delete( foo, 'Compute' )


    print('end')
