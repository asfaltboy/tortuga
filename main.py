# Allow access to command-line arguments
import importlib
import logging
import os
import sys

# Import the core and GUI elements of Qt
from PySide.QtCore import *
from PySide.QtGui import *

from uiloader import loadUi

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)
plogger = logging.getLogger('plugins')
plogger.addHandler(ch)
plogger.setLevel(logging.DEBUG)

SCRIPT_DIRECTORY = os.path.join(os.path.dirname(__file__), 'forms')
MAIN_FORM_UI = os.path.join(SCRIPT_DIRECTORY, 'mainwindow.ui')
PLUGINS_PACKAGE = 'plugins'


class FlowStep(object):
    """ An interface for passing stored flow step settings to the widget. """

    def __init__(self, widget_class, settings=None):
        self.widget_class = widget_class
        self.settings = settings
        self.widget_instance = self.widget_class(self.settings)

    @property
    def widget(self):
        """
        Always returns the widget, creating one if no current instance exists
        """
        if self.widget_instance is None:
            self.widget_instance = self.widget_class(settings=self.settings)
        return self.widget_instance

    def run(self, input):
        return self.widget.run(input)

    def deselect_widget(self, settings):
        """
        Store the widget settings in this flow and remove it from the passed
        settings layout.
        """
        if self.widget_instance:
            self.settings = self.widget_instance.get_settings()
            self.widget_instance = None
        current_setting_item = settings.takeAt(0)
        if current_setting_item:
            current_setting_item.widget().deleteLater()
            del current_setting_item


class MainWindow(QMainWindow):
    plugins_list = None
    plugins = {}
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

    @property
    def flow(self):
        if not getattr(self, '_flow', None):
            self._flow = self.findChild(QListWidget, "flow_list")
        return self._flow

    def flow_step_selected(self, new_item, prev_item):
        settings = self.tabs_widget.findChild(
            QVBoxLayout, "settings_container")

        prev_index = self.flow.indexFromItem(prev_item).row()
        logger.debug("Deselected item: %s" % prev_index)
        if prev_index != -1:
            prev_step = self.flow_steps[prev_index]
            prev_step.deselect_widget(settings)

        new_index = self.flow.indexFromItem(new_item).row()
        logger.debug("Selected item: %s" % new_index)
        if new_index != -1:
            current_step = self.flow_steps[new_index]
            settings.addWidget(current_step.widget, parent=settings)
            self.tabs_widget.setCurrentIndex(0)

    def add_plugin(self):
        selected = self.plugins_list.selectedItems()
        if len(selected):
            for plugin in selected:
                logger.debug("Adding plugin %s to list %s", plugin, self.flow)
                plugin_widget = self.plugins.get(plugin.text())
                if not plugin_widget:
                    raise Exception("Invalid widget key in plugins")
                self.flow_steps.append(FlowStep(plugin_widget))
                self.flow.addItem(plugin.text())

    def run_flow(self):
        logger.debug("Running flow")
        input = None
        all_output = ""
        for i, step in enumerate(self.flow_steps):
            output = step.run(input)
            logger.debug("ran flow step %i, input: %s, output: %s", i, input, output)
            if output:
                # use output as next step's input
                input = output

                # combine all output in a single
                if isinstance(output, (list, tuple)):
                    all_output += ", ".join(output) + "\n"
                else:
                    all_output += output + "\n"
        self.flow_output.setPlainText(all_output)

    def prepare_interface(self):
        self.tabs_widget = self.findChild(QTabWidget, 'tabWidget')
        aquit = self.findChild(QAction, "actionQuit")
        aadd = self.findChild(QToolButton, "flowPluginAdd")
        arun = self.findChild(QAction, "runFlow")
        self.flow_output = self.findChild(QTextEdit, "flow_output")

        # connect handlers
        self.flow.currentItemChanged.connect(self.flow_step_selected)
        aquit.triggered.connect(self.close)
        aadd.clicked.connect(self.add_plugin)
        arun.triggered.connect(self.run_flow)

        self.statusBar.showMessage('To start, open or create a flow')


app = MainWindow()
