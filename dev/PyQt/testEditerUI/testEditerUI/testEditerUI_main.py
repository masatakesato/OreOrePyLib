import sys

from oreorepylib.utils import environment

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class TestFrame(QWidget):

    def __init__(self, parent):
        super(TestFrame, self).__init__(parent)

        self.button = QPushButton('button', self)

        self.button.clicked.connect( parent.changeSomething )


    def changeText(self):
        print( 'changeText' )



# http://blog.csdn.net/Artprog/article/details/50651209
# このへん見てやってみる



g_LabelWidth = 80

g_MarginLeft = 0
g_MarginTop  = 0
g_MarginRight = 0
g_MartginBottom = 0

#self.__m_SingleStep = 0.01
#self.__m_Decimals = 2
#self.__m_RangeMin = 0
#self.__m_RangeMax = 100


class AttributeEditor_ScalarDouble(QWidget):

    def __init__( self, minval, maxval, decimals, singlestep ):
        super(AttributeEditor_ScalarDouble, self).__init__()
        
        # range/precision settings
        self.__m_RangeMin = minval
        self.__m_RangeMax = maxval
        self.__m_Decimals = decimals
        self.__m_SingleStep = singlestep        

        # initialize label
        self.label = QLabel('Double')
        self.label.setFixedWidth( g_LabelWidth )
        self.label.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize spinbox 
        self.spinBox = QDoubleSpinBox()
        self.spinBox.setDecimals( self.__m_Decimals )
        self.spinBox.setSingleStep( self.__m_SingleStep )
        self.spinBox.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.spinBox.setRange( self.__m_RangeMin, self.__m_RangeMax )

        # initialize slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.slider.setRange(0,1e+6)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1e+5)

        # connect signal and slot
        self.spinBox.valueChanged.connect( self.changeValue_Spin2Slider )
        self.spinBox.editingFinished.connect( self.editingFinished_SpinBox )
        self.slider.valueChanged.connect( self.changeValue_Slider2Splin )

        self.slider.setValue( 1 )
        self.spinBox.setValue( 0.0 )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.label )
        layout.addWidget( self.spinBox )
        layout.addWidget( self.slider )
        layout.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        self.setLayout( layout )

        # GUIコンポーネントの整列 http://puarts.com/?pid=922


    # slots 
    def changeValue_Spin2Slider( self, value ):
        val = (value - self.spinBox.minimum()) / (self.spinBox.maximum() - self.spinBox.minimum()) * self.slider.maximum()
        self.slider.setValue( int(val) )


    def changeValue_Slider2Splin( self, value ):
        val = value / self.slider.maximum() * (self.spinBox.maximum() - self.spinBox.minimum()) + self.spinBox.minimum()
        self.spinBox.setValue( val )


    def editingFinished_SpinBox( self ):
        self.spinBox.clearFocus()

#self.__m_SingleStep = 1
#self.__m_PageStep = 10
#self.__m_RangeMin = 0
#self.__m_RangeMax = 100


class AttributeEditor_ScalarInt(QWidget):

    def __init__( self, minval, maxval, singlestep, pagestep ):
        super(AttributeEditor_ScalarInt, self).__init__()
        
        # range/step settings
        self.__m_RangeMin = minval
        self.__m_RangeMax = maxval
        self.__m_SingleStep = singlestep
        self.__m_PageStep = pagestep

        # initialize label
        self.label = QLabel('Int')
        self.label.setFixedWidth( g_LabelWidth )
        self.label.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize spinbox 
        self.spinBox = QSpinBox()
        self.spinBox.setSingleStep( self.__m_SingleStep )
        self.spinBox.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.spinBox.setRange( self.__m_RangeMin, self.__m_RangeMax )

        # initialize slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.slider.setRange( self.__m_RangeMin, self.__m_RangeMax )
        self.slider.setSingleStep( self.__m_SingleStep )
        self.slider.setPageStep( self.__m_PageStep )

        # connect signal and slot
        self.spinBox.valueChanged.connect( self.slider.setValue )
        self.spinBox.editingFinished.connect( self.editingFinished_SpinBox )
        self.slider.valueChanged.connect( self.spinBox.setValue )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.label )
        layout.addWidget( self.spinBox )
        layout.addWidget( self.slider )
        layout.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        self.setLayout( layout )

    # slots 
    def editingFinished_SpinBox( self ):
        self.spinBox.clearFocus()



class AttributeEditor_String(QWidget):

    def __init__(self):
        super(AttributeEditor_String, self).__init__()

        # initialize label
        self.label = QLabel('String')
        self.label.setFixedWidth( g_LabelWidth )
        self.label.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize lineEdit
        self.lineEdit = QLineEdit()
        self.lineEdit.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        
        # connect signal and slot
        #self.lineEdit.returnPressed.connect( self.myReturnPressed )
        self.lineEdit.editingFinished.connect( self.myEditingFinished )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.label )
        layout.addWidget( self.lineEdit )
        layout.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        self.setLayout( layout )


    #def myReturnPressed( self ):
    #    self.lineEdit.clearFocus()
    #    print( 'myReturnPressed' )

    def myEditingFinished( self ):
        self.lineEdit.clearFocus()



class AttributeEditor_Double3(QWidget):

    def __init__(self):
        super(AttributeEditor_Double3, self).__init__()
        
        # numeric settings
        self.__m_SingleStep = 0.01
        self.__m_Decimals = 2

        # initialize label
        self.label = QLabel('Vector')
        self.label.setFixedWidth( g_LabelWidth )
        self.label.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize spinbox 
        self.spinBox_X = QDoubleSpinBox()
        self.spinBox_X.setDecimals( self.__m_Decimals )
        self.spinBox_X.setSingleStep( self.__m_SingleStep )
        self.spinBox_X.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        
        self.spinBox_Y = QDoubleSpinBox()
        self.spinBox_Y.setDecimals( self.__m_Decimals )
        self.spinBox_Y.setSingleStep( self.__m_SingleStep )
        self.spinBox_Y.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        self.spinBox_Z = QDoubleSpinBox()
        self.spinBox_Z.setDecimals( self.__m_Decimals )
        self.spinBox_Z.setSingleStep( self.__m_SingleStep )
        self.spinBox_Z.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        # connect signal and slot
        self.spinBox_X.editingFinished.connect( self.editingFinished_SpinBox_X )
        self.spinBox_Y.editingFinished.connect( self.editingFinished_SpinBox_Y )
        self.spinBox_Z.editingFinished.connect( self.editingFinished_SpinBox_Z )

        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.label )
        layout.addWidget( self.spinBox_X )
        layout.addWidget( self.spinBox_Y )
        layout.addWidget( self.spinBox_Z )
        layout.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        self.setLayout( layout )


    def editingFinished_SpinBox_X( self ):
        self.spinBox_X.clearFocus()

    def editingFinished_SpinBox_Y( self ):
        self.spinBox_Y.clearFocus()

    def editingFinished_SpinBox_Z( self ):
        self.spinBox_Z.clearFocus()


class AttributeEditor_CheckBox(QWidget):

    def __init__( self ):
        super(AttributeEditor_CheckBox, self).__init__()

        # initialize label
        self.label = QLabel('CheckBox')
        self.label.setFixedWidth( g_LabelWidth )
        self.label.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize checkbox
        self.checkBox = QCheckBox()

        # connect signal and slot
        
        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.label )
        layout.addWidget( self.checkBox )
        layout.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        self.setLayout( layout )



class AttributEditor_CombobBox(QWidget):

    def __init__( self, items ):
        super(AttributEditor_CombobBox, self).__init__()

        # initialize label
        self.label = QLabel('ComboBox')
        self.label.setFixedWidth( g_LabelWidth )
        self.label.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        self.label.setAlignment( Qt.AlignRight | Qt.AlignCenter )

        # initialize lineEdit
        self.comboBox = QComboBox()
        self.comboBox.addItems( items )
        self.comboBox.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )
        
        # connect signal and slot
        
        # setup layout
        layout = QHBoxLayout()
        layout.addWidget( self.label )
        layout.addWidget( self.comboBox )
        layout.setContentsMargins( g_MarginLeft, g_MarginTop, g_MarginRight, g_MartginBottom )

        self.setLayout( layout )




class AttributeEditor_MultipleWidgets(QWidget):

    def __init__(self):
        super(AttributeEditor_MultipleWidgets, self).__init__()

        layout = QVBoxLayout()

        layout.addWidget( AttributEditor_CombobBox( ['Option1','Option2','Option3','Option4'] ) )
        layout.addWidget( AttributeEditor_CheckBox() )
        layout.addWidget( AttributeEditor_ScalarDouble(-1000.0, 1000.0, 2, 0.01) )
        layout.addWidget( AttributeEditor_ScalarInt(-100, 100, 1, 10) )
        layout.addWidget( AttributeEditor_String() )
        layout.addWidget( AttributeEditor_Double3() )
        layout.addStretch() # place stretch under widgets

        self.setLayout( layout )


    def changeValue(self, value):
        self.label.setText(str(value))


# TODO: Create AttributeEditor using NodeTypeInfo instance



class MainWidget(QWidget):

    def __init__( self ):
        super(MainWidget,self).__init__()

        hbox = QVBoxLayout(self)

        frame = TestFrame(self)
        textedit = QTextEdit()


        self.pagesWidget = QStackedWidget()
        self.pagesWidget.addWidget( AttributeEditor_ScalarDouble(-1000.0,1000.0,2,0.01) )
        self.pagesWidget.addWidget( AttributeEditor_ScalarInt(-100,100,1,10) )
        self.pagesWidget.addWidget( AttributeEditor_String() )
        self.pagesWidget.addWidget( AttributeEditor_Double3() )
        self.pagesWidget.addWidget( AttributEditor_CombobBox( ['Option1','Option2','Option3','Option4'] ) )
        self.pagesWidget.addWidget( AttributeEditor_CheckBox() )
        self.pagesWidget.addWidget( AttributeEditor_MultipleWidgets() )


        vsplitter = QSplitter(Qt.Vertical)
        vsplitter.addWidget(frame)
        vsplitter.addWidget(textedit)


        hsplitter = QSplitter(Qt.Horizontal)
        hsplitter.addWidget( vsplitter )
        hsplitter.addWidget( self.pagesWidget )
        hsplitter.setSizes([400,100])



        hbox.addWidget(hsplitter)

        self.setLayout(hbox)

        self.setGeometry( 300, 300, 500, 500 )

        self.idx = 0


    def changeSomething(self):
        self.idx += 1
        self.idx %= self.pagesWidget.count()
        self.pagesWidget.setCurrentIndex( self.idx )





if __name__=='__main__':

    app = QApplication(sys.argv)

    mainWindow = MainWidget()
    mainWindow.show()
#    graphicsView = GraphicsView()
#    graphicsView.show()
    sys.exit(app.exec_())

    pass

