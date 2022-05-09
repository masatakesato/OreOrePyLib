# reference http://www.yasinuludag.com/darkorange.stylesheet

TextFieldStyleSheet = """
QTextEdit, QPlainTextEdit
{
    color: rgb(225,180,64);
    background: rgb(42,42,42);
}

QScrollBar:vertical
{
    /*border: 2px solid green;*/
    color: rgb(196,196,196);
    background: rgb(42,42,42);
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
     background: none;
}
"""

LabelStyleSheet = """
QLabel
{
    color: rgb(200,200,200);
}
"""


LineEditStyleSheet = """
QLineEdit
{
    color: rgb(200,200,200);
    background: rgb(42,42,42);
    selection-background-color: darkgray;
    
    height: 18px;

    border-left: 1px solid rgb(32,32,32);
    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(100,100,100);
    border-bottom: 1px solid rgb(100,100,100);

    border-radius: 2px;
    padding: 0px 2px;
}

QLineEdit:focus
{
    border: 1px solid darkgray;
}

QLineEdit:read-only
{
    color: rgb(100,100,100);
}

"""


SliderStyleSheet = """

QSlider::groove:horizontal
{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(32,32,32), stop:1 rgb(100,100,100) );

    height: 6px;

    border-radius: 3px;
    margin: 2px 3px;
}

QSlider::handle:horizontal
{
    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgb(200,200,200), stop:1 rgb(32,32,32) );

    width: 16px;
    height: 18px;

    border-radius: 8px;
    margin: -5px -3px;
}
"""


SpinBoxStyleSheet = """
QSpinBox, QDoubleSpinBox
{
    color: rgb(200,200,200);
    background: rgb(42,42,42);
    selection-background-color: darkgray;

    height: 18px;

    border-left: 1px solid rgb(32,32,32);
    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(100,100,100);
    border-bottom: 1px solid rgb(100,100,100);

    border-radius: 2px;
    padding: 0px 2px;
}

QSpinBox:focus, QDoubleSpinBox:focus
{
    border: 1px solid darkgray;
}

"""


CheckBoxStyleSheet = """
QCheckBox:disabled
{
    color: #414141;
}

QCheckBox::indicator
{
    color: rgb(200,200,200);
    background: rgb(42,42,42);

    width: 12px;
    height: 12px;

    border-left: 1px solid rgb(32,32,32);
    border-top: 1px solid rgb(32,32,32);
    border-right: 1px solid rgb(100,100,100);
    border-bottom: 1px solid rgb(100,100,100);
}


QCheckBox::indicator:hover
{
    border: 1px solid darkgray;
}

QCheckBox::indicator:checked
{
    image: url(images/checkbox.png);
}

QCheckBox::indicator:disabled
{
    border: 1px solid #444;
}

"""



TabWidgetStyleSheet = """ 
QTabBar::tab
{
    color: rgb(200,200,200);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(96,96,96), stop:1 rgb(60,60,60) );

    height: 18px;

    border-top: 1px solid rgb(196,196,196);
    border-right: 1px solid rgb(32,32,32);

    border-top-left-radius: 4px;
    border-top-right-radius: 4px;

    min-width: 8ex;
    padding: 4px;
}

QTabWidget::pane
{
    background: rgb(60,60,60);

    border-top: 0px solid rgb(196,196,196);
    border-right: 2px solid rgb(32,32,32);
    border-bottom: 2px solid rgb(32,32,32);
    
    border-top-right-radius: 4px;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}
"""


NodeEditorStyleSheet = """
QGraphicsView
{
    background-color: rgb(42,42,42);
    selection-background-color: darkGray;
}

"""





#background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
#                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
#                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
#background: #606060;
#border: 2px solid #C4C4C3;
#border-bottom-color: #C2C7CB; /* same as the pane color */
#border-top-left-radius: 4px;
#border-top-right-radius: 4px;
#min-width: 8ex;
#padding: 8px;