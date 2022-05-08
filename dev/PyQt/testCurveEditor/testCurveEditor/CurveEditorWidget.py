import functools

from qtwidget import *


class CurveEditorWidget( QWidget ):

    def __init__( self, parent=None ):
        super(CurveEditorWidget, self).__init__(parent)

        # Initialize View and Scene
        self.__m_Scene = CurveEditorScene()
        self.__m_View = CurveEditorView( self.__m_Scene )

        # Initialize Buttons
        self.__m_CurveImpulseButton = QPushButton( 'Impulse' )
        self.__m_CurveImpulseButton.released.connect( functools.partial(self.__m_View.SetCurveMode, mode=CurveMode.Impulse) )

        self.__m_CurveLinearButton = QPushButton( 'Linear' )
        self.__m_CurveLinearButton.released.connect( functools.partial(self.__m_View.SetCurveMode, mode=CurveMode.Linear) )

        self.__m_CurveCubicButton = QPushButton( 'Cubic' )
        self.__m_CurveCubicButton.released.connect( functools.partial(self.__m_View.SetCurveMode, mode=CurveMode.Cubic) )

        self.__m_RemovePointButton = QPushButton( 'RemovePoint' )
        self.__m_RemovePointButton.released.connect( self.__m_View.RemoveAnchor )

        # Initialize Layouts
        mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        editorLayout = QVBoxLayout()

        buttonLayout.addWidget( self.__m_CurveImpulseButton )
        buttonLayout.addWidget( self.__m_CurveLinearButton )
        buttonLayout.addWidget( self.__m_CurveCubicButton )
        buttonLayout.addWidget( self.__m_RemovePointButton )
        editorLayout.addWidget( self.__m_View )

        mainLayout.addLayout( buttonLayout )
        mainLayout.addLayout( editorLayout )
    
        # Initialize MainWidgets
        self.setLayout( mainLayout )
    
        self.setGeometry( 0, 0, 600, 600 )