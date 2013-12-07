import re

from PySide import QtGui


class WrongInput(Exception):
    pass


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
    setting_attributes = []

    def __init__(self, parent=None, settings=None):
        QtGui.QWidget.__init__(self, parent)
        self.input = None
        self.output = None

    def get_settings(self):
        """
        Plugins should override this method to return a dict of the settings
        that should be stored or None if no settings should be stored.

        By default stores a set of pre-defined input widget values
        (setting_attributes) into a settings dict and returns it.
        """
        ret = {}
        for atr in self.setting_attributes:
            s = getattr(self, atr, None)
            if isinstance(s, QtGui.QComboBox):
                ret[atr] = [s.itemText(i) for i in range(s.count())
                            if s.itemText(i) != '']
                ret['%s_index' % atr] = s.currentIndex()
        return ret

    def set_settings(self, settings=None):
        """
        Plugins should override this method to set sub_widget properties
        and data per the given settings.

        By default retreives a set of values from the passed settings dict
        using attribute names as key bases and sets them to the sub-widgets
        (setting_attributes) values by type.
        """
        if settings is None:
            return
        for atr in self.setting_attributes:
            s = getattr(self, atr, None)
            if not s:
                continue
            if isinstance(s, QtGui.QComboBox):
                s.addItems(settings.get(atr, []))
                s.setCurrentIndex(settings.get('%s_index' % atr, 0))

    # helper methods
    def createComboBox(self, text=None):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        if text:
            comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                               QtGui.QSizePolicy.Preferred)
        return comboBox

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button
