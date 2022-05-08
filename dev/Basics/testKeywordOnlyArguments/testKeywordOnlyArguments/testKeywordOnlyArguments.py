# CreateNodeの場合

# nodetype: 必須パラメータ。
# pos: オプションパラメータ。
# name: オプションパラメータ。ノード名称を指定できる
# parent: オプションパラメータ。親ノードを指定できる→NodeEditorUIから呼び出す際は、ウィジェット毎に基点ノードのObjectIDを渡す必要あり

# オプションパラメータを任意に指定したい
# パラメータ並び順で暗黙的に渡すのはやめたい

##################################################################################################################
#                     コマンドラインインターフェース用の関数は、キーワード引数形式強制にしておく                      #
##################################################################################################################
# Keyword-only arguments in Python2/3
# http://d.hatena.ne.jp/yohhoy/20150315/p1


# キーワード引数形式の強制方法...python3版
def createNode_py3( nodeType, *, name='', parent=None ):
    print( 'CreateNode_py3...' )
    print( '    nodeType=', nodeType )
    print( '    name=', name )
    print( '    parent=', parent )


createNode_py3('Transform')# OK
createNode_py3('Transform', name='OOO')# OK
createNode_py3('Transform', parent='Parent')# OK
createNode_py3('Transform', parent='Parent', name='Name')# OK
#createNode_py3('Transform', 'Name')# NG
#createNode_py3('Transform', 'Name', 'Parent')# NG



# キーワード引数形式の強制方法...python2版(kwargsを利用)
def createNode_py2_kwargs( nodeType, **kwargs ):
    print( 'createNode_py2_kwargs...' )
    print( '    nodeType=', nodeType )
    print( '    name=', kwargs.pop('name', None) )
    print( '    parent=', kwargs.pop('parent', None) )


createNode_py2_kwargs('Transform')# OK
createNode_py2_kwargs('Transform', name='OOO')# OK
createNode_py2_kwargs('Transform', parent='Parent')# OK
createNode_py2_kwargs('Transform', parent='Parent', name='Name')# OK
createNode_py2_kwargs('Transform', 'Name')# NG
#createNode_py2_kwargs('Transform', 'Name', 'Parent')# NG



# キーワード引数形式の強制方法...python2版(特殊マーカーオブジェクト利用)
_end_of_args = object()

def createNode_py2_eoa( nodeType, marker=_end_of_args, name='', parent=None ):
    print( 'createNode_py2_eoa...' )
    if( marker != _end_of_args ):
        raise TypeError
    print( '    nodeType=', nodeType )
    print( '    name=', name )
    print( '    parent=', parent )


createNode_py2_eoa('Transform')# OK
createNode_py2_eoa('Transform', name='OOO')# OK
createNode_py2_eoa('Transform', parent='Parent')# OK
createNode_py2_eoa('Transform', parent='Parent', name='Name')# OK
createNode_py2_eoa('Transform', 'Name')# NG
#createNode_py2_eoa('Transform', 'Name', 'Parent')# NG