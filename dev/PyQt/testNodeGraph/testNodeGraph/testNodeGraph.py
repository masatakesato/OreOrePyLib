import sys
import graphics.stylesheet as StyleSheet

from oreorepylib.utils import environment

from nodegraph.NENodeGraph import *
from graphics.NodeEditorUI import *
#from graphics.AttributeEditorUI import *
#from graphics.PythonInterpreter import PyInterp
from NESceneManager import NESceneManager




class MainWidget(QMainWindow):

    def __init__( self ):
        super(MainWidget,self).__init__()

       



        self.__m_SceneManager = NESceneManager()

        #=============== NodeGraph ===============#
        self.__m_NodeGraph = NENodeGraph()
        self.__m_SceneManager.BindNodeGraph( self.__m_NodeGraph )

        #========== Graphic Components ===========#
        self.__m_NodeEditorUI = NodeEditorUI()
        self.__m_NodeEditorUI.setSceneRect(-400, -400, 800, 800)

        # create view(graphics)
        view = GraphicsView()
        view.setScene( self.__m_NodeEditorUI )

        # bind graphicsscene
        self.__m_SceneManager.BindNodeEditorUI( self.__m_NodeEditorUI )


        #============ Attribute Editor ============#
        # create attribute editor
#        attribEditor = AttributeEditorUI()

#        qtab = QTabWidget()
#        qtab.addTab( attribEditor, 'Attribute Editor')
#        qtab.setStyleSheet( StyleSheet.TabWidgetStyleSheet )
        
        # bind attribute editor
#        self.__m_SceneManager.BindAttributeEditorUI( attribEditor )


        vsplitter = QSplitter(Qt.Vertical)
        vsplitter.addWidget(view)


        hsplitter = QSplitter(Qt.Horizontal)
        hsplitter.addWidget(vsplitter)
#        hsplitter.addWidget( qtab )
        #hsplitter.setStyleSheet(StyleSheet.BackGround)
        #hsplitter.setSizes( [100, 100] )

        Pal = QPalette()
        Pal.setColor( QPalette.Background, QColor(80,80,80) )
        hsplitter.setAutoFillBackground(True)
        hsplitter.setPalette(Pal)
        


        #
        self.setCentralWidget(hsplitter)


        self.setGeometry( 300, 50, 1280, 768 )
        

    def SceneManager( self ):
        return self.__m_SceneManager



if __name__ == "__main__":

    app = QApplication(sys.argv)

    mainWindow = MainWidget()
    mainWindow.setWindowTitle('Node Editor Test')
    mainWindow.show()
        
    sys.exit(app.exec_())