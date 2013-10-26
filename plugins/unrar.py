"""
A Plugin to unarchive given rar file into destination.

depends on rarfile: http://rarfile.berlios.de/doc/
and unrar.exe file (provided)
"""

import rarfile


class Command(object):
    rar_path = None
    dest_path = None

    def __init__(self, rar_path, dest_path=None):
        self.rar_path = rar_path
        self.dest_path = dest_path

    # TODO
    def check_if_overwriting(self):
        """
        Check if extracting rar in destination would overwrite any files
        and prompt user if he wants to do so or abort.
        """
        return False

    def run(self):
        rf = rarfile.RarFile(self.rar_path)
        rf.extractall(path=self.dest_path)
