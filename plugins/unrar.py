"""
A Plugin to unarchive given rar file into destination.

depends on rarfile: http://rarfile.berlios.de/doc/
and unrar.exe file (provided)
"""
import logging
import os
import rarfile
import sys

from PySide import QtGui, QtCore

from base import BasePlugin

logger = logging.getLogger(__name__)


plugin_path = os.path.dirname(__file__)
rarfile.UNRAR_TOOL = os.path.join(plugin_path, 'unrar.exe')
logger.debug(u'unrar.exe should be found in path or at %s', rarfile.UNRAR_TOOL)


class UnRar(BasePlugin):
    dest_path = None

    def __init__(self, parent=None, settings=None):
        BasePlugin.__init__(self, parent)

        self.pathLabel = QtGui.QLabel(self.tr("Destination Path:"))
        self.pathComboBox = self.createComboBox()
        self.browseButton = self.createButton(self.tr("&Browse..."),
                                              self.browse)

        mainLayout = QtGui.QFormLayout()
        mainLayout.addWidget(self.pathLabel)
        mainLayout.addWidget(self.pathComboBox)
        mainLayout.addWidget(self.browseButton)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Select destination path to unrar surce files to"))

        self.set_settings(settings)

    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
            self, self.tr("Select File"),
            QtCore.QDir.currentPath()
        )
        self.pathComboBox.addItem(directory)
        # self.pathComboBox.setCurrentIndex(self.pathComboBox.currentIndex() + 1)
        self.validatePath(directory)

    def validatePath(self, text):
        logger.debug('Path selected: %s', text)
        if not os.path.exists(text):
            logger.warn('The selected path is invalid, please try again')
            self.pathComboBox.removeItem(self.pathComboBox.currentIndex())
            return
        if os.path.exists(text):
            self.dest_path = text

    # TODO
    def check_if_overwriting(self):
        """
        Check if extracting rar in destination would overwrite any files
        and prompt user if he wants to do so or abort.
        """
        return False

    def extract_rar(self, f):
        rf = rarfile.RarFile(f)
        rf.extractall(path=self.dest_path)

    def run(self, input_files):
        self.validatePath(self.pathComboBox.currentText())
        if not input_files:
            logger.warn("A rar source path is required as input_files")
            return
        if isinstance(input_files, list):
            for ifile in input_files:
                self.extract_rar(ifile)
        elif isinstance(input_files, basestring):
            self.extract_rar(ifile)

if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    window = UnRar()
    window.show()
    sys.exit(app.exec_())
