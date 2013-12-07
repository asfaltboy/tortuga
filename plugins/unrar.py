"""
A Plugin to unarchive given rar file into destination.

depends on rarfile: http://rarfile.berlios.de/doc/
and unrar.exe file (provided)
"""
import logging
import rarfile
import sys

from PySide import QtGui

from base import BasePlugin

logger = logging.getLogger('plugins.{}'.format(__name__))


class UnRar(BasePlugin):
    def __init__(self, parent=None, settings=None):
        BasePlugin.__init__(self, parent)

    # TODO
    def check_if_overwriting(self):
        """
        Check if extracting rar in destination would overwrite any files
        and prompt user if he wants to do so or abort.
        """
        return False

    def run(self):
        if not self.input:
            logger.warn("A rar source path is required as input")
            return
        rf = rarfile.RarFile(self.rar_path)
        rf.extractall(path=self.dest_path)

if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    window = UnRar()
    window.show()
    sys.exit(app.exec_())
