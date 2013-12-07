#!/usr/bin/env python

"""PySide port of the dialogs/findfiles example from Qt v4.x"""

import logging
import os
import sys

from PySide import QtCore, QtGui

from base import BasePlugin

logger = logging.getLogger(__name__)


class SelectPath(BasePlugin):
    setting_attributes = ['fileComboBox']

    def __init__(self, parent=None, settings=None):
        BasePlugin.__init__(self, parent)

        self.output = None

        self.fileLabel = QtGui.QLabel(self.tr("Select Path:"))
        self.fileComboBox = self.createComboBox()
        # self.fileComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.fileComboBox.setFixedHeight(self.fileComboBox.minimumSizeHint().height())
        self.fileComboBox.activated[str].connect(self.validatePath)
        self.browseButton = self.createButton(self.tr("&Browse..."),
                                              self.browse)

        mainLayout = QtGui.QFormLayout()
        mainLayout.addWidget(self.fileLabel)
        mainLayout.addWidget(self.fileComboBox)
        mainLayout.addWidget(self.browseButton)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Select path"))

        self.set_settings(settings)

    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
            self, self.tr("Select File"),
            QtCore.QDir.currentPath()
        )
        self.fileComboBox.addItem(directory)
        # self.fileComboBox.setCurrentIndex(self.fileComboBox.currentIndex() + 1)
        self.validatePath(directory)

    def validatePath(self, text):
        logger.debug('Path selected: %s', text)
        if not os.path.exists(text):
            logger.warn('The selected path is invalid, please try again')
            self.fileComboBox.removeItem(self.fileComboBox.currentIndex())
            return
        if os.path.exists(text):
            self.output = text

    def run(self, input=None):
        self.validatePath(self.fileComboBox.currentText())
        return self.output


if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    window = SelectPath()
    window.show()
    sys.exit(app.exec_())
