from IPlugin import IPlugin


class Plugin2(IPlugin):

    def InitializePlugin(self):
        print( 'Plugin2::InitializePlugin' )


    def UninitializePlugin(self):
        print( 'Plugin2::UninitializePlugin' )


    def Update(self, node):
        print( 'Plugin2::Update...' + node.name )