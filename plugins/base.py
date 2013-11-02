import re

from PySide import QtGui


class Meta(type):
    def split_on_caps(meta, str):
        rs = re.findall('[A-Z][^A-Z]*', str)
        fs = ""
        for word in rs:
            fs += " "+word
        return fs.strip()

    def __unicode__(meta, *args, **kwargs):
        return meta.split_on_caps(meta.__name__)

    def __new__(cls, name, bases, members):
        #collect up the metaclasses
        metas = [type(base) for base in bases]

        # prune repeated or conflicting entries
        metas = [meta for index, meta in enumerate(metas)
                 if not [later for later in metas[index+1:]
                 if issubclass(later, meta)]]

        # whip up the actual combined meta class derive off all of these
        meta = type(name, tuple(metas + [cls]), dict(combined_metas=metas))

        # make the actual object
        return meta(name, bases, members)

    def __init__(self, name, bases, members):
        for meta in self.combined_metas:
            meta.__init__(self, name, bases, members)


class BasePlugin(QtGui.QWidget):
    # TODO: to remove the ugly mess above, make the plugins return an
    #       instance of a generator that handles creation and naming and such
    __metaclass__ = Meta

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.input = None
        self.output = None

    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                               QtGui.QSizePolicy.Preferred)
        return comboBox
