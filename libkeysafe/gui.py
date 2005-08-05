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

import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, gobject
import os.path

import libkeysafe
import cfg
import ctrl

class MainWinGui(object):
    def __init__(self):
        object.__init__(self)
        self.gui = gtk.glade.XML(os.path.join(libkeysafe.glade_path, 'keysafe.glade'))
        self.gui.signal_autoconnect(self)
        completion = gtk.EntryCompletion()
        self.gui.liststore = gtk.ListStore(str)
        completion.set_model(self.gui.liststore)
        self.gui.get_widget('entryKeyId').set_completion(completion)
        completion.set_text_column(0)
        self.ctrl = ctrl.MainWinCtrl(self.gui)
        self.gui.get_widget('btnCopyUN').set_sensitive(0)
        self.gui.get_widget('btnCopyExit').set_sensitive(0)
        self.gui.get_widget('winMain').show_all()
        self.gui.get_widget('winMain').set_position(gtk.WIN_POS_MOUSE)
        gtk.main()

    # Main window callbacks
    def on_winMain_destroy(self, widget):
        gtk.main_quit()

    def timeout_quit(self):
        gtk.main_quit()

    def on_entryKeyId_changed(self, widget):
        un, info = self.ctrl.get_from_entry(widget.get_text())
        if un and info:
            self.gui.get_widget('lblUserName').set_text(un)
            self.gui.get_widget('lblInfo').set_text(info)
            self.gui.get_widget('btnCopyUN').set_sensitive(1)
            self.gui.get_widget('btnCopyUN').grab_focus()
            self.gui.get_widget('entryPwd').set_sensitive(1)
            self.gui.get_widget('btnCopyExit').set_sensitive(1)
        else:
            self.gui.get_widget('lblUserName').set_text('')
            self.gui.get_widget('lblInfo').set_text('')
            self.gui.get_widget('btnCopyUN').set_sensitive(0)
            self.gui.get_widget('entryPwd').set_sensitive(0)
            self.gui.get_widget('btnCopyExit').set_sensitive(0)

    def on_btnCopyUN_clicked(self, widget):
        self.gui.get_widget('entryPwd').grab_focus()
        self.ctrl.copy_text_to_clipboard(
                self.gui.get_widget('lblUserName').get_text())

    def on_btnCopyExit_clicked(self, widget):
        try:
            self.ctrl.copy_pw_to_clipboard(
                    self.gui.get_widget('entryKeyId').get_text(),
                    self.gui.get_widget('entryPwd').get_text())
            gobject.timeout_add(cfg.get_config()['timeout'], self.timeout_quit)
            self.gui.get_widget('winMain').hide_all()
        except Exception, e:
            print e

def main():
    MainWinGui()
