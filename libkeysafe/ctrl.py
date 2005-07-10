import safe

import gtk

class MainWinCtrl(object):
    def __init__(self, gui):
        object.__init__(self)
        self.gui = gui
        _s = safe.get_safe()
        for k in _s.keys():
            gui.liststore.append([k])

    def get_from_entry(self, s):
        entry = safe.get_entry(s)
        if entry != None:
            return entry[0], entry[2]
        else:
            return None, None

    def copy_to_clipb(self, s, k):
        entry = safe.get_entry(s)
        cb = gtk.clipboard_get("CLIPBOARD")
        # let the caller handle any exception due to bad password
        cb.set_text(safe.decrypt(entry[1], k))
