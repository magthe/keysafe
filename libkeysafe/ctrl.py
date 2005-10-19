# Copyright (C) 2005 by Magnus Therning

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import safe

import gtk

# TODO: Add signal handling so that the password won't be left in the GNOME
# clipboard if a signal is sent before the application times out and exits.

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

    def copy_text_to_clipboard(self, t):
        gtk.clipboard_get('CLIPBOARD').set_text(t)
        gtk.clipboard_get('PRIMARY').set_text(t)

    def copy_pw_to_clipboard(self, s, k):
        entry = safe.get_entry(s)
        # let the caller handle any exception due to bad password
        self.copy_text_to_clipboard(safe.decrypt(entry[1], k))

    def clear_clipboard(self):
        # a bit of a shortcut, we don't care what is in the clipboard, just
        # clear it!
        gtk.clipboard_get('CLIPBOARD').clear()
        gtk.clipboard_get('PRIMARY').clear()
