# Allow access to command-line arguments
import os
import sys

# Import the core and GUI elements of Qt
from PySide.QtCore import *
from PySide.QtGui import *

from uiloader import loadUi

SCRIPT_DIRECTORY = os.path.join(os.path.dirname(__file__), 'forms')
PLUGINS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'plugins')
MAIN_FORM_UI = os.path.join(SCRIPT_DIRECTORY, 'mainwindow.ui')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        QMainWindow.__init__(self, parent=None)
        loadUi(MAIN_FORM_UI, self)
        self.prepare_interface()
        self.prepare_data()
        self.show()
        self.app.exec_()

    def prepare_data(self):
        model = QFileSystemModel()
        model.setRootPath(PLUGINS_DIRECTORY)
        tview = self.findChild(QTreeView)
        tview.setModel(model)
        tview.setRootIndex(model.index(PLUGINS_DIRECTORY))

    def prepare_interface(self):
        self.statusBar.showMessage('To start, open or create a flow')
        aquit = self.findChild(QAction, "actionQuit")
        aquit.triggered.connect(self.close)


app = MainWindow()
