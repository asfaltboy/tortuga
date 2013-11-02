# Allow access to command-line arguments
import importlib
import logging
import os
import sys

# Import the core and GUI elements of Qt
from PySide.QtCore import *
from PySide.QtGui import *

from uiloader import loadUi

logger = logging.getLogger('plugins.{}'.format(__name__))
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

SCRIPT_DIRECTORY = os.path.join(os.path.dirname(__file__), 'forms')
PLUGINS_PACKAGE = os.path.join('plugins')
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

    def get_plugins(self, package):
        plugins = importlib.import_module(package)
        logger.debug("Found plugin package: %s", plugins)
        return plugins.available_plugins

    def get_plugin_names(self, plugins):
        names = [unicode(p) for p in plugins]
        logger.debug("Found these plugins: %s", names)
        return names

    def prepare_data(self):
        self.plugins = self.get_plugins(PLUGINS_PACKAGE)
        plugin_list = self.findChild(QListView, "plugins")
        plugin_list.addItems(self.get_plugin_names(self.plugins))

    def prepare_interface(self):
        self.statusBar.showMessage('To start, open or create a flow')
        aquit = self.findChild(QAction, "actionQuit")
        aquit.triggered.connect(self.close)


app = MainWindow()
