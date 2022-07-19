# syntax.py

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



# referred implementation: https://blog.csdn.net/xiaoyangyang20/article/details/68923133
# style: https://github.com/highlightjs/highlight.js/blob/master/src/styles/agate.css


class PythonHighlighter(QSyntaxHighlighter):

    Rules = []
    Formats = {}
    StartStr = ()

    Styles = (
       ( "normal", QColor(200, 200, 200) ),
       ( "keyword", QColor(252, 194, 140) ),
       ( "builtin", QColor(255, 255, 170) ),
       ( "constant", QColor(252, 194, 140) ),
       ( "decorator", QColor(252, 155, 155) ),
       ( "comment", QColor(96, 72,64) ),
       ( "string", QColor(162, 252, 162) ),
       ( "number", QColor(211, 99, 99) ),
       ( "error", Qt.darkRed) )



    def __init__( self, parent=None ):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        KEYWORDS = ["and", "as", "assert", "break", "class",
                "continue", "def", "del", "elif", "else", "except",
                "exec", "finally", "for", "from", "global", "if",
                "import", "in", "is", "lambda", "not", "or", "pass",
                "print", "raise", "return", "try", "while", "with",
                "yield"]
        BUILTINS = ["abs", "all", "any", "basestring", "bool",
                "callable", "chr", "classmethod", "cmp", "compile",
                "complex", "delattr", "dict", "dir", "divmod",
                "enumerate", "eval", "execfile", "exit", "file",
                "filter", "float", "frozenset", "getattr", "globals",
                "hasattr", "hex", "id", "int", "isinstance",
                "issubclass", "iter", "len", "list", "locals", "map",
                "max", "min", "object", "oct", "open", "ord", "pow",
                "property", "range", "reduce", "repr", "reversed",
                "round", "set", "setattr", "slice", "sorted",
                "staticmethod", "str", "sum", "super", "tuple", "type",
                "vars", "zip"] 
        CONSTANTS = ["False", "True", "None", "NotImplemented",
                     "Ellipsis"]

        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])),
                "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % constant
                for constant in CONSTANTS])), "constant"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\b[+-]?[0-9]+[lL]?\b"
                r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
                r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                "number"))

        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"),
                "decorator"))
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')

        start_str = ["#"]
        if( getattr(sys, 'ps1', sys.flags.interactive) ): start_str.append( sys.ps1 )
        if( getattr(sys, 'ps2', sys.flags.interactive) ): start_str.append( sys.ps2 )
        PythonHighlighter.StartStr = tuple( start_str )



    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        for name, color in PythonHighlighter.Styles:
            format = QTextCharFormat(baseFormat)
            format.setForeground(QColor(color))
            if( name in ("keyword", "decorator") ):
                format.setFontWeight(QFont.Bold)
            if( name == "comment" ):
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format


    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)

        textLength = len(text)
        prevState = self.previousBlockState()

        self.setFormat( 0, textLength, PythonHighlighter.Formats["normal"] )

        # for interactiva console
        if( text.startswith("Traceback") or text.startswith("Error: ") ):
            self.setCurrentBlockState(ERROR)
            self.setFormat( 0, textLength, PythonHighlighter.Formats["error"] )
            return

        if( prevState == ERROR and not text.startswith(tuple(PythonHighlighter.StartStr)) ):#(text.startswith(sys.ps1) or text.startswith("#")) ):# modified to check interacive mode. 2019.08.10
            self.setCurrentBlockState(ERROR)
            self.setFormat( 0, textLength, PythonHighlighter.Formats["error"] )
            return

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while( i >= 0 ):
                length = regex.matchedLength()
                self.setFormat( i, length, PythonHighlighter.Formats[format] )
                i = regex.indexIn(text, i + length)

        # Slow but good quality highlighting for comments. For more
        # speed, comment this out and add the following to __init__:
        # PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))
        if( not text ):
            pass
        elif( text[0] == "#" ):
            self.setFormat( 0, len(text), PythonHighlighter.Formats["comment"] )
        else:
            stack = []
            for i, c in enumerate(text):
                if( c in ('"', "'") ):
                    if stack and stack[-1] == c:
                        stack.pop()
                    else:
                        stack.append(c)
                elif( c == "#" and len(stack) == 0 ):
                    self.setFormat( i, len(text), PythonHighlighter.Formats["comment"] )
                    break

        self.setCurrentBlockState(NORMAL)

        if( self.stringRe.indexIn(text) != -1 ):
            return
        # This is fooled by triple quotes inside single quoted strings
        for i, state in ((self.tripleSingleRe.indexIn(text),
                          TRIPLESINGLE),
                         (self.tripleDoubleRe.indexIn(text),
                          TRIPLEDOUBLE)):
            if( self.previousBlockState() == state ):
                if( i == -1 ):
                    i = len(text)
                    self.setCurrentBlockState(state)
                self.setFormat( 0, i+3, PythonHighlighter.Formats["string"] )
            elif( i > -1 ):
                self.setCurrentBlockState(state)
                self.setFormat( i, len(text), PythonHighlighter.Formats["string"] )


    def rehighlight(self):
        QApplication.setOverrideCursor( QCursor(Qt.WaitCursor) )
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
