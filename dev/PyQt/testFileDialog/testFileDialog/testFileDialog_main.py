import sys

from oreorepylib.utils import environment

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *




g_TreeViewStyleSheet = """

/* http://stackoverflow.com/questions/26162387/qtableview-qtablewidget-grid-stylesheet-grid-line-width */
QHeaderView
{
    background: transparent;
    show-decoration-selected: 1;
}

QHeaderView::section
{
    background: transparent;
}



QTreeView::item
{
    
    border: 1px solid #d9d9d9;
    border-top-color: transparent;
    border-bottom-color: transparent;
}

QTreeView::item:hover
{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
    border: 1px solid #bfcde4;
}

QTreeView::item:selected
{
    border: 1px solid #567dbc;
}

QTreeView::item:selected:active
{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
}

QTreeView::item:selected:!active
{
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
}
"""


ComboBoxStyleSheet = """
QComboBox
{
    color: rgb(235, 235, 235);
    border: 1px solid gray;
    border-radius: 3px;
    padding: 1px 18px 1px 3px;
    min-width: 6em;
}
/*
QComboBox:editable {
    background: white;
}
*/
QComboBox:!editable, QComboBox::drop-down:editable
{
    
/*
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
*/
}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);
}

QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
}

"""

g_ListViewStyleSheet = """
QListView
{
    background-color: transparent;
}
"""



g_DialogStyleSheet = """
QWidget
{
    color: rgb(235, 235, 235);
    background-color: rgb(60, 60, 60);
}

/* Left part: ListView*/


/* Right part: TreeView */

QDialog, QFileDialog
{
    color: rgb(100,100,100);
    /*background-color: rgb(0,0,0);*/
}

QLineEdit
{
    color: rgb(235,235,235);
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

QScrollBar
{
    /*border: 2px solid green;*/
    color: rgb(196,196,196);
    background: rgb(42,42,42);
}

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



class filedialogdemo(QWidget):
   def __init__(self, parent=None):
      super(filedialogdemo, self).__init__(parent)

      layout = QVBoxLayout()

      self.le = QLabel("Hello")

      layout.addWidget(self.le)
      self.btn1 = QPushButton("QFileDialog object")
      self.btn1.clicked.connect(self.getfiles)
      layout.addWidget(self.btn1)

      self.contents = QTextEdit()
      layout.addWidget(self.contents)
      self.setLayout(layout)
      self.setWindowTitle("File Dialog demo")

      
   def getfiles(self):
      dlg = QFileDialog(self)
      dlg.setFileMode(QFileDialog.AnyFile)
      dlg.setOption( QFileDialog.DontUseNativeDialog, True)
      dlg.setStyleSheet(g_DialogStyleSheet + ComboBoxStyleSheet + g_ListViewStyleSheet + g_TreeViewStyleSheet )

      dlg.setNameFilter("Images (*.jpg *.png)")
      filenames = []#QStringList()

      if dlg.exec_():
         filenames = dlg.selectedFiles()
         f = open(filenames[0], 'r')

         with f:
            data = f.read()
            self.contents.setText(data)




def main():
   app = QApplication(sys.argv)
   ex = filedialogdemo()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()