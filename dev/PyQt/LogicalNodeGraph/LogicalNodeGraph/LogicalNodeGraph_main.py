from NEConnectionObject import *
from NEAttributeObject import *
from NENodeObject import *

from INENodeUpdater import *
from NodeTypeManager import *


#from NEScene import *
from NESceneManager import *




#if __name__ == '__main__':

#    print( 'Test Logical Node Graph Connection' )

#    scene = NEScene()
#    sceneManager = NESceneManager()

#    sceneManager.BindScene( scene )

#    # Test Node Creation
#    sceneManager.CreateNode( 'TestNode' )
#    sceneManager.CreateNode( 'TestNode' )
#    sceneManager.CreateNode( 'TestNode' )

#    #sceneManager.DeleteNode( 'TestNode001' )

#    sceneManager.CreateNode( 'TestNode' )
#    sceneManager.Rename( 'TestNode003', 'OreOre' )
#    #sceneManager.Rename( 'TestNode001', 'TestNode004' )

#    # Test Attribute Connection
#    conn = sceneManager.ConnectAttribute( 'TestNode004.Output', 'OreOre.Input1' )
#    sceneManager.ConnectAttribute( 'TestNode004.Output', 'OreOre.Input1' ) # Avoid duplication
#    sceneManager.ConnectAttribute( 'TestNode000.Output', 'TestNode002.Output' ) # Wrong Case: Out to Out connection
#    sceneManager.ConnectAttribute( 'TestNode000.Output', 'TestNode001.Input2' ) # Wrong Case: Datatype mismatching


#    # Change Source/Destination of Connection
#    if( conn ):
#        sceneManager.ReconnectAttribute( conn.Name(), 'OreOre.Output', 'TestNode002.Input1' )
#    #sceneManager.DisconnectAttribute( 'TestNode000.Output', 'TestNode001.Input1' ) # Remove Connection
#    #sceneManager.ConnectAttribute( 'TestNode000.Output', 'TestNode002.Input1' )# Create New Connection


#    # TODO Delete Connection
#    sceneManager.DisconnectAttribute( 'TestNode003.Output', 'TestNode002.Input1' )

#    # Detele Node
#    sceneManager.DeleteNode( 'OreOre' )
    
#    pass




if __name__ == '__main__':

    print( 'Test Logical Node Graph Connection' )

    scene = NEScene()
    sceneManager = NESceneManager()

    sceneManager.BindScene( scene )

    sceneManager.CreateNode( 'TestNode' )
    sceneManager.CreateNode( 'TestNode' )
    sceneManager.CreateNode( 'TestNode' )
    sceneManager.CreateNode( 'TestNode' )
    sceneManager.CreateNode( 'TestNode' )

    sceneManager.ConnectAttribute( 'TestNode001.Output', 'TestNode002.Input1' )
    sceneManager.ConnectAttribute( 'TestNode001.Output', 'TestNode003.Input1' ) # Avoid duplication
    sceneManager.ConnectAttribute( 'TestNode001.Output', 'TestNode004.Input1' ) # Wrong Case: Out to Out connection
    sceneManager.ConnectAttribute( 'TestNode001.Output', 'TestNode005.Input1' ) # Wrong Case: Datatype mismatching

    #sceneManager.DeleteNode( 'TestNode003' )
    #sceneManager.DeleteNode( 'TestNode005' )
    sceneManager.Rename( 'TestNode001', 'TestNode995' )

    sceneManager.DeleteNode( 'TestNode995' )
    #sceneManager.DisconnectAttribute( 'TestNode001.Output', 'TestNode002.Input1' )
    
    sceneManager.CreateNode( 'TestNode2' )
    sceneManager.CreateNode( 'TestNode' )

    pass