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
    plugin_list = None
    plugins = []

    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        QMainWindow.__init__(self, parent=None)
        loadUi(MAIN_FORM_UI, self)
        self.prepare_interface()
        self.prepare_data()
        self.show()
        self.app.exec_()

    def load_plugins(self):
        plugins = self.get_plugins(PLUGINS_PACKAGE)
        if not plugins:
            logger.debug("No plugins found")
        self.plugins = self.get_plugin_dict(plugins)
        logger.debug("Found these plugins: %s", self.plugins)

    def get_plugins(self, package):
        plugins = importlib.import_module(package)
        logger.debug("Found plugin package: %s", plugins)
        return plugins.available_plugins

    def get_plugin_dict(self, plugins):
        return dict([(unicode(p), p) for p in plugins])

    def prepare_data(self):
        self.load_plugins()
        self.plugins_list = self.findChild(QListWidget, "plugins")
        self.plugins_list.addItems(self.plugins.keys())

    def get_current_flow(self):
        return self.flow

    def add_plugin(self):
        selected = self.plugin_list.selectedItems()
        flow = self.get_current_flow()
        if len(selected):
            for plugin in selected:
                flow.add_step(plugin)

    def prepare_interface(self):
        self.flow = self.findChild(QVBoxLayout, "flow_container")
        self.statusBar.showMessage('To start, open or create a flow')
        aquit = self.findChild(QAction, "actionQuit")
        aquit.triggered.connect(self.close)
        aadd = self.findChild(QToolButton, "flowPluginAdd")
        aadd.clicked.connect(self.add_plugin)


app = MainWindow()
