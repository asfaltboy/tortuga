from pprint import pformat
import logging
import os
import sys

from PySide import QtCore, QtGui

from base import BasePlugin, WrongInput

logger = logging.getLogger('plugins.{}'.format(__name__))


class FindFiles(BasePlugin):
    setting_attributes = ['fileComboBox', 'textComboBox']

    def __init__(self, parent=None, settings=None):
        BasePlugin.__init__(self, parent)

        self.fileComboBox = self.createComboBox()
        self.textComboBox = self.createComboBox()
        self.sourcePath = QtGui.QLabel('')

        self.fileLabel = QtGui.QLabel(self.tr('Named:'))
        self.textLabel = QtGui.QLabel(self.tr('Containing text:'))

        mainLayout = QtGui.QFormLayout()
        mainLayout.addWidget(self.fileLabel)
        mainLayout.addWidget(self.fileComboBox)
        mainLayout.addWidget(self.textLabel)
        mainLayout.addWidget(self.textComboBox)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Find Files"))

        if settings is None:
            # by default show a * in file combobox
            settings = {'fileComboBox': [self.tr("*")]}

        self.set_settings(settings)

    def validate(self):
        if not self.input:
            raise WrongInput('No input provided')

        if not os.path.exists(self.input):
            raise WrongInput('Input path does not exist')

    def run(self, input):
        self.validate()
        directory = QtCore.QDir(self.input)
        self.output = self.find(directory)
        logger.debug("Found files: %s", pformat(self.output))
        return self.output

    def find(self, directory):
        fileName = self.fileComboBox.currentText()
        text = self.textComboBox.currentText()

        files = []
        if len(fileName) == 0:
            fileName = "*"
        files = directory.entryList([fileName],
                                    QtCore.QDir.Files | QtCore.QDir.NoSymLinks)

        if len(text):
            files = self.findFiles(directory, files, text)
        return files

    def findFiles(self, directory, files, text):
        progressDialog = QtGui.QProgressDialog(self)

        progressDialog.setCancelButtonText(self.tr("&Cancel"))
        progressDialog.setRange(0, len(files))
        progressDialog.setWindowTitle(self.tr("Find Files"))

        foundFiles = []

        for i in range(len(files)):
            progressDialog.setValue(i)
            progressDialog.setLabelText(self.tr(
                "Searching file number {0} of {1}...").format(i, len(files)))
            QtGui.qApp.processEvents()

            if progressDialog.wasCanceled():
                break

            inFile = QtCore.QFile(directory.absoluteFilePath(files[i]))

            if inFile.open(QtCore.QIODevice.ReadOnly):
                line = ""
                stream = QtCore.QTextStream(inFile)
                while not stream.atEnd():
                    if progressDialog.wasCanceled():
                        break
                    line = stream.readLine()
                    if line.contains(text):
                        foundFiles.append(files[i])
                        break

        progressDialog.close()

        return foundFiles


if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    window = FindFiles()
    window.show()
    sys.exit(app.exec_())
