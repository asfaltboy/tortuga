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
MAIN_FORM_UI = os.path.join(SCRIPT_DIRECTORY, 'mainwindow.ui')
PLUGINS_PACKAGE = 'plugins'


class MainWindow(QMainWindow):
    plugins_list = None
    plugins = {}
    flow = None
    flow_steps = []
    tabs = None

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
        self.plugins_list.itemDoubleClicked.connect(self.add_plugin)

    def get_current_flow(self):
        return self.flow or self.findChild(QListWidget, "flow_list")

    def flow_step_selected(self, index):
        print("Selected item: %s" % index)
        if index != -1:
            current_step = self.flow_steps[index]()
            settings = self.tabs_widget.findChild(
                QVBoxLayout, "settings_container")
            settings.addWidget(current_step, parent=settings)
            self.tabs_widget.setCurrentIndex(0)

    def add_plugin(self):
        selected = self.plugins_list.selectedItems()
        flow = self.get_current_flow()
        if len(selected):
            for plugin in selected:
                logger.debug("Adding plugin %s to list %s", plugin, flow)
                plugin_widget = self.plugins.get(plugin.text())
                if not plugin_widget:
                    raise Exception("Invalid widget key in plugins")
                self.flow_steps.append(plugin_widget)
                flow.addItem(plugin.text())

    def prepare_interface(self):
        self.tabs_widget = self.findChild(QTabWidget, 'tabWidget')
        self.flow = self.get_current_flow()
        aquit = self.findChild(QAction, "actionQuit")
        aadd = self.findChild(QToolButton, "flowPluginAdd")

        # connect handlers
        self.flow.currentRowChanged.connect(self.flow_step_selected)
        aquit.triggered.connect(self.close)
        aadd.clicked.connect(self.add_plugin)

        self.statusBar.showMessage('To start, open or create a flow')


app = MainWindow()
