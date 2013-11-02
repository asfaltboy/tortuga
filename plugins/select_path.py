#!/usr/bin/env python

"""PySide port of the dialogs/findfiles example from Qt v4.x"""

import logging
import os
import sys

from PySide import QtCore, QtGui

logger = logging.getLogger('plugins.{}'.format(__name__))


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # initialize input/output
        self.input = None
        self.output = None

        self.fileLabel = QtGui.QLabel(self.tr("Select Path:"))
        self.fileComboBox = self.createComboBox(self.getLastPaths())
        # self.fileComboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.fileComboBox.setFixedHeight(self.fileComboBox.minimumSizeHint().height())
        self.fileComboBox.activated[str].connect(self.pathSelected)
        self.browseButton = self.createButton(self.tr("&Browse..."),
                                              self.browse)

        mainLayout = QtGui.QFormLayout()
        mainLayout.addWidget(self.fileLabel)
        mainLayout.addWidget(self.fileComboBox)
        mainLayout.addWidget(self.browseButton)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Select path"))

    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
            self, self.tr("Select File"),
            QtCore.QDir.currentPath()
        )
        self.fileComboBox.addItem(directory)
        self.fileComboBox.setCurrentIndex(self.fileComboBox.currentIndex() + 1)
        self.pathSelected(directory)

    def pathSelected(self, text):
        logger.debug('Path selected: %s', text)
        if not os.path.exists(text):
            logger.warn('The selected path is invalid, please try again')
            self.fileComboBox.removeItem(self.fileComboBox.currentIndex())
            return
        self.output = os.path.exists(text)

    def getLastPaths(self):
        # TODO: get latest stored paths from db
        return

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                               QtGui.QSizePolicy.Preferred)
        return comboBox


if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
