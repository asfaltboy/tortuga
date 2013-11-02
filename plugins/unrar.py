"""
A Plugin to unarchive given rar file into destination.

depends on rarfile: http://rarfile.berlios.de/doc/
and unrar.exe file (provided)
"""
import logging
import rarfile

logger = logging.getLogger('plugins.{}'.format(__name__))


class Command(object):
    rar_path = None
    dest_path = None

    def __init__(self, dest_path=None):
        self.dest_path = dest_path

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
