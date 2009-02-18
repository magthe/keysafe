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
from libkeysafe import safe, cfg

class MainEdGui(object):
    __BADPWDTXT = 'Wrong master password'

    def __init__(self):
        object.__init__(self)
        self.__gui = gtk.glade.XML(os.path.join(libkeysafe.glade_path,'ksed.glade'))
        self.__gui.signal_autoconnect(self)
        self.__populate_list()
        self.__populate_cfg()
        self.__gui.get_widget('btnStore').set_sensitive(0)
        self.__gui.get_widget('winMain').show_all()
        gtk.main()

    def __populate_list(self):
        '''Populate the list store.
        '''
        self.store = gtk.ListStore(str)
        view = self.__gui.get_widget('treeSafe')
        view.set_model(self.store)
        column = gtk.TreeViewColumn(None)
        renderer = gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.set_attributes(renderer, text = 0)
        view.append_column(column)

        sel = view.get_selection()
        sel.connect("changed", self.on_treeSelection_changed)
        sel.set_mode(gtk.SELECTION_SINGLE)

        self.__update_list()

    def __update_list(self):
        _s = safe.get_safe()
        self.store.clear()
        for k in _s.keys():
            self.store.append([k])

    def __populate_cfg(self):
        c = cfg.get_config()
        self.__gui.get_widget('entrySafe').set_text(c['keyfile'])
        self.__gui.get_widget('entryTimeout').set_text(str(c['timeout']))

    def __save_cfg_values(self):
        c = cfg.get_config()
        c['keyfile'] = self.__gui.get_widget('entrySafe').get_text()
        c['timeout'] = self.__gui.get_widget('entryTimeout').get_text()
        c.save()

    def __populate_txt_entries(self, id):
        '''Put values in all the text entries based on the id.

        @type id: string
        @param id: The ID of the entry to use.
        '''
        entry = safe.get_entry(id)

        self.__gui.get_widget('entryID').set_text(id)
        self.__gui.get_widget('entryUserName').set_text(entry[0])
        self.__gui.get_widget('textNote').get_buffer().set_text(entry[2])
        try:
            self.__gui.get_widget('entryPasswd1').set_text(safe.decrypt(entry[1], self.__master_pwd))
            self.__gui.get_widget('entryPasswd2').set_text(safe.decrypt(entry[1], self.__master_pwd))
        except safe.BadPwdException, e:
            self.__gui.get_widget('entryPasswd1').set_text(self.__BADPWDTXT)
            self.__gui.get_widget('entryPasswd2').set_text(self.__BADPWDTXT)

    def __clear_txt_entries(self):
        self.__gui.get_widget('entryID').set_text('')
        self.__gui.get_widget('entryUserName').set_text('')
        self.__gui.get_widget('textNote').get_buffer().set_text('')
        self.__gui.get_widget('entryPasswd1').set_text('')
        self.__gui.get_widget('entryPasswd2').set_text('')

    def __collect_values(self):
        id = self.__gui.get_widget('entryID').get_text()
        un = self.__gui.get_widget('entryUserName').get_text()
        pwd1 = self.__gui.get_widget('entryPasswd1').get_text()
        pwd2 = self.__gui.get_widget('entryPasswd2').get_text()
        s, e = self.__gui.get_widget('textNote').get_buffer().get_bounds()
        note = self.__gui.get_widget('textNote').get_buffer().get_text(s, e)
        return id, un, pwd1, pwd2, note

    def on_dlgMainPwd_response(self, widget, response):
        if response == 1:
            mpwd = self.__gui.get_widget('entryMPwd').get_text()
            if len(safe.get_safe().keys()) > 0:
                e = safe.get_entry(safe.get_safe().keys()[0])
                if e:
                    try:
                        safe.decrypt(e[1], mpwd)
                    except:
                        self.__gui.get_widget('entryMPwd').set_text('')
                        return
            self.__master_pwd = mpwd
            self.__dlg.hide()
        else:
            gtk.main_quit()

    def on_entryMPwd_activate(self, widget):
        self.on_dlgMainPwd_response(None, 1)

    def on_winMain_show(self, widget, *args, **kwargs):
        self.__dlg = self.__gui.get_widget('dlgMainPwd')
        self.__dlg.show_all()

    def on_winMain_destroy(self, widget):
        gtk.main_quit()

    def on_btnCancel_clicked(self, widget):
        gtk.main_quit()

    def on_btnDone_clicked(self, widget):
        safe.save_safe()
        self.__save_cfg_values()
        gtk.main_quit()

    def on_treeSelection_changed(self, widget):
        '''@type widget: GtkTreeView
        @param widget: The widget'''
        model, iter = widget.get_selected()
        if iter:
            id = model.get_value(iter, 0)
            self.__populate_txt_entries(id)
        else:
            self.__clear_txt_entries()
    
    def on_btnStore_clicked(self, widget):
        id, un, pwd1, pwd2, note = self.__collect_values()
        safe.set_entry(id, un, pwd1, note, self.__master_pwd)
        self.__update_list()

    def on_btnDelete_clicked(self, widget):
        sel = self.__gui.get_widget('treeSafe').get_selection()
        model, iter = sel.get_selected()
        if iter:
            id = model.get_value(iter, 0)
            safe.delete_entry(id)
            self.__update_list()

    def on_entryPasswd1_changed(self, widget):
        l_text = widget.get_text()
        r_text = self.__gui.get_widget('entryPasswd2').get_text()
        if l_text == r_text and l_text != self.__BADPWDTXT:
            self.__gui.get_widget('btnStore').set_sensitive(1)
        else:
            self.__gui.get_widget('btnStore').set_sensitive(0)

    def on_entryPasswd2_changed(self, widget):
        l_text = widget.get_text()
        r_text = self.__gui.get_widget('entryPasswd1').get_text()
        if l_text == r_text and l_text != self.__BADPWDTXT:
            self.__gui.get_widget('btnStore').set_sensitive(1)
        else:
            self.__gui.get_widget('btnStore').set_sensitive(0)

def main():
    MainEdGui()
