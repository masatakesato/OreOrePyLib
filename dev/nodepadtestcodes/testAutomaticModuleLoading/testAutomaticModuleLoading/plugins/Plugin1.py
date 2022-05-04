from IPlugin import IPlugin


class Plugin1(IPlugin):

    def InitializePlugin(self):
        print( 'Plugin1::InitializePlugin' )


    def UninitializePlugin(self):
        print( 'Plugin1::UninitializePlugin' )


    def Update(self, node):
        print( 'Plugin1::Update...' + node.name )