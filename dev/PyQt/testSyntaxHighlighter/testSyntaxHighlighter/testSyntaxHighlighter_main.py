import sys
import functools
import traceback

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from SyntaxHighlighter import PythonHighlighter

from oreorepylib.ui.pyqt5.frame import Frame
import oreorepylib.ui.pyqt5.stylesheet as StyleUI





g_PythonSyntaxHighlightStyleSheet = """
QTextEdit, QPlainTextEdit
{
    color: rgb(200,200,200);
    background-color: rgb(24,24,24);
    selection-background-color: rgb(125,75,50);

    margin: 0px 0px 0px 0px;
    border: 1px solid rgb(60,60,60);
    padding: 0px 0px 0px 0px;
}

QTextEdit:focus, QPlainTextEdit:focus
{
    border: 1px solid rgb(96,96,96);
}

"""




g_String = ''



class PlainTextEdit( QPlainTextEdit ):

    def __init__( self, *args, **kwargs ):
        super(PlainTextEdit, self).__init__(*args, **kwargs)


    def keyPressEvent( self, event ):

        if( event.key()==Qt.Key_Tab ):
            self.insertPlainText( '    ' )
            #print( self.document().toPlainText() )
            return

        return super(PlainTextEdit, self).keyPressEvent(event)







class TextEditor( Frame ):

    closeSignal = pyqtSignal()

    def __init__( self, *args, **kwargs ):
        super(TextEditor, self).__init__( *args, **kwargs )

        self.textEdit = PlainTextEdit()
        tab_width = QFontMetrics( self.textEdit.font() ).width( ' ' ) * 4
        self.textEdit.setTabStopWidth( tab_width )
        self.textEdit.setStyleSheet( g_PythonSyntaxHighlightStyleSheet )
        self.textEdit.setFont( QFont('MS Gothic', 10) )

        self.heighlighter = PythonHighlighter( self.textEdit.document() )

        self.__m_Button = QPushButton( 'Update' )
        self.__m_Button.clicked.connect( self.Update )

        self.__m_refUpdateFunc = None


        self.setGeometry( 300, 200, 800, 600 )
        self.setLayout( QVBoxLayout() )
        self.layout().addWidget( self.textEdit )
        self.layout().addWidget( self.__m_Button )


    def BindUpdateFunc( self, func ):
        self.__m_refUpdateFunc = func


    def SetText( self, text ):
        self.textEdit.setPlainText( text )


    def Update( self ):
        try:
            self.__m_refUpdateFunc( self.textEdit.toPlainText() )
        except:
            traceback.print_exc()


    def Release( self ):
        self.__m_refUpdateFunc = None


    def closeEvent( self, event ):
        print( 'TextEditor::closeEvent()...' )
        super(TextEditor, self).closeEvent( event )
        self.closeSignal.emit()






class MainWindow(Frame):

    def __init__( self, *args, **kwargs ):
        super(MainWindow, self).__init__( *args, **kwargs )

        self.__m_PushButton = QPushButton( 'Button' )
        self.setLayout( QVBoxLayout() )
        self.layout().addWidget( self.__m_PushButton )

        self.__m_PushButton.clicked.connect( self.onPush )

        self.textEditor = None

        self.__m_Action = QAction( 'Update', self )
        self.__m_Action.triggered.connect( self.UpdateCustomNode )



    def onPush( self ):

        if( self.textEditor is None ):
            print( 'Open new child window' )
            self.textEditor = TextEditor()
            self.textEditor.closeSignal.connect( self.__RemoveEditorViewCallback )
            self.textEditor.BindUpdateFunc( self.UpdateCustomNode )
            self.textEditor.SetText( g_String )

            self.textEditor.show()

        else:
            print( 'Close current child window' )
            self.textEditor.Update()
            self.textEditor.close()



    def __RemoveEditorViewCallback( self ):
        print( '__RemoveEditorViewCallback' )
        try:
            self.textEditor.Release()
            del self.textEditor
            self.textEditor = None
        except:
            traceback.print_exc()



    def UpdateCustomNode( self, code_string ):
        print( 'MainWindow::UpdateCustomNode()...' )
        print( code_string )
        global g_String
        g_String= code_string




if __name__ == '__main__':
    app = QApplication( sys.argv )

    w = MainWindow()
    w.show()


    sys.exit( app.exec_() )





#if __name__=='__main__':

#    app = QApplication( sys.argv )

#    textEdit = PlainTextEdit()

#    tab_width = QFontMetrics( textEdit.font() ).width( ' ' ) * 4
#    textEdit.setTabStopWidth( tab_width )
#    textEdit.setStyleSheet( g_PythonSyntaxHighlightStyleSheet )
#    textEdit.setFont( QFont('MS Gothic', 10) )

#    heighlighter = PythonHighlighter( textEdit.document() )
    

#    frame = Frame()#QFrame()
#    frame.setWindowTitle( 'testSyntaxHighlighter' )
#    frame.setGeometry( 300, 200, 800, 600 )
#    frame.setLayout( QVBoxLayout() )
#    frame.layout().addWidget( textEdit )

#    frame.show()


#    sys.exit( app.exec_() )