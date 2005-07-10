import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, gobject

from libkeysafe import safe, cfg

class MainEdGui(object):
    def __init__(self):
        object.__init__(self)
        self.__gui = gtk.glade.XML('gui/ksed.glade')
        self.__gui.signal_autoconnect(self)
        self.__populate_list()
        self.__populate_cfg()
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
        self.__gui.get_widget('entrySafe').set_text(c['safe'])
        self.__gui.get_widget('entryTimeout').set_text(str(c['timeout']))

    def __save_cfg_values(self):
        c = cfg.get_config()
        c['safe'] = self.__gui.get_widget('entrySafe').get_text()
        c['timeout'] = self.__gui.get_widget('entryTimeout').get_text()
        c.save()

    def __populate_txt_entries(self, id):
        '''Put values in all the text entries based on the id.

        @type id: string
        @param id: The ID of the entry to use.
        '''
        entry = safe.get_entry(id)
        master_pwd = self.__gui.get_widget('entryMasterPwd').get_text()

        self.__gui.get_widget('entryID').set_text(id)
        self.__gui.get_widget('entryUserName').set_text(entry[0])
        self.__gui.get_widget('textNote').get_buffer().set_text(entry[2])
        try:
            self.__gui.get_widget('entryPasswd1').set_text(safe.decrypt(entry[1], master_pwd))
            self.__gui.get_widget('entryPasswd2').set_text(safe.decrypt(entry[1], master_pwd))
        except safe.BadPwdException, e:
            self.__gui.get_widget('entryPasswd1').set_text('Wrong master password')
            self.__gui.get_widget('entryPasswd2').set_text('Wrong master password')

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
        mpwd = self.__gui.get_widget('entryMasterPwd').get_text()
        return id, un, pwd1, pwd2, note, mpwd

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
        id, un, pwd1, pwd2, note, mpw = self.__collect_values()
        # TODO: sanity checks on values
        safe.set_entry(id, un, pwd1, note, mpw)
        self.__update_list()

    def on_btnDelete_clicked(self, widget):
        sel = self.__gui.get_widget('treeSafe').get_selection()
        model, iter = sel.get_selected()
        if iter:
            id = model.get_value(iter, 0)
            safe.delete_entry(id)
            self.__update_list()

    def on_entryMasterPwd_changed(self, widget):
        '''@type widget: GtkEntry
        @param widget: The widget
        '''
        model, iter = self.__gui.get_widget('treeSafe').get_selection().get_selected()
        if iter:
            id = model.get_value(iter, 0)
            self.__populate_txt_entries(id)

def main():
    MainEdGui()
