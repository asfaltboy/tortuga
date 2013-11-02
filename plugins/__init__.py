import logging

from find_files import FindFiles
from select_path import SelectPath
from unrar import UnRar

logger = logging.getLogger('plugins.{}'.format(__name__))

available_plugins = [FindFiles, SelectPath, UnRar]
