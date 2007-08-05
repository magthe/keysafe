AUTOMAKE_OPTIONS = dist-bzip2 subdir-objects

# directories
pylibdir = $(pkglibdir)/libkeysafe
guidir = $(pkglibdir)/gui
schemadir = $(GCONF_SCHEMA_FILE_DIR)
desktopdir = $(datadir)/applications

bin_SCRIPTS = keysafe ksed
noinst_SCRIPTS = tools/ksdump

pylib_PYTHON = \
	libkeysafe/cfg.py \
	libkeysafe/ctrl.py \
	libkeysafe/edgui.py \
	libkeysafe/gui.py \
	libkeysafe/__init__.py \
	libkeysafe/safe.py

gui_DATA = gui/keysafe.glade gui/ksed.glade

schema_DATA = gnome/keysafe.schemas

desktop_DATA = gnome/keysafe.desktop gnome/ksed.desktop

# some manual builds
edit = sed \
       -e 's,@KEYSAFE_PY_PATH@,$(pkglibdir),g' \
       -e 's,@KEYSAFE_GLADE_PATH@,$(guidir),g' \
       -e 's,@KEYSAFE_BIN_PATH@,$(bindir),g'

keysafe: $(srcdir)/keysafe.in Makefile
	rm -f $(top_builddir)/keysafe $(top_builddir)/keysafe.tmp
	$(edit) $(srcdir)/keysafe.in > $(top_builddir)/keysafe.tmp
	chmod +x $(top_builddir)/keysafe.tmp
	mv $(top_builddir)/keysafe.tmp $(top_builddir)/keysafe

ksed: $(srcdir)/ksed.in Makefile
	rm -f $(top_builddir)/ksed $(top_builddir)/ksed.tmp
	$(edit) $(srcdir)/ksed.in > $(top_builddir)/ksed.tmp
	chmod +x $(top_builddir)/ksed.tmp
	mv $(top_builddir)/ksed.tmp $(top_builddir)/ksed

tools/ksdump: $(srcdir)/tools/ksdump.in Makefile
	[ -d $(top_builddir)/tools ] || mkdir tools
	rm -f $(top_builddir)/tools/ksdump $(top_builddir)/tools/ksdump.tmp
	$(edit) $(srcdir)/tools/ksdump.in > $(top_builddir)/tools/ksdump.tmp
	chmod +x $(top_builddir)/tools/ksdump.tmp
	mv $(top_builddir)/tools/ksdump.tmp $(top_builddir)/tools/ksdump

libkeysafe/__init__.py: $(srcdir)/libkeysafe/__init__.py.in Makefile
	[ -d $(top_builddir)/libkeysafe ] || mkdir libkeysafe
	rm -f $(top_builddir)/libkeysafe/__init__.py \
		$(top_builddir)/libkeysafe/__init__.py.tmp
	$(edit) $(srcdir)/libkeysafe/__init__.py.in > \
		$(top_builddir)/libkeysafe/__init__.py.tmp
	mv $(top_builddir)/libkeysafe/__init__.py.tmp \
		$(top_builddir)/libkeysafe/__init__.py

gnome/%.desktop : $(srcdir)/gnome/%.desktop.in Makefile
	[ -d $(top_builddir)/gnome ] || mkdir $(top_builddir)/gnome
	rm -f $(top_builddir)/$@ $(top_builddir)/$@.tmp
	$(edit) $(srcdir)/$@.in > $(top_builddir)/$@.tmp
	mv $(top_builddir)/$@.tmp $(top_builddir)/$@

# installation of schemas
if GCONF_SCHEMAS_INSTALL
install-data-hook:
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) \
		$(GCONFTOOL) --makefile-install-rule $(srcdir)/$(schema_DATA)
endif

# dist
EXTRA_DIST = \
	     autogen.sh \
	     gnome/keysafe.desktop.in \
	     gnome/keysafe.schemas \
	     gnome/ksed.desktop.in \
	     gui/keysafe.glade \
	     gui/ksed.glade \
	     keysafe.in \
	     ksed.in \
	     libkeysafe/__init__.py.in \
	     libkeysafe/cfg.py \
	     libkeysafe/ctrl.py \
	     libkeysafe/edgui.py \
	     libkeysafe/gui.py \
	     libkeysafe/safe.py \
	     tools/ksdump.in

# clean
CLEANFILES = \
	     keysafe ksed \
	     libkeysafe/__init__.py \
	     gnome/keysafe.desktop gnome/ksed.desktop \
	     tools/ksdump
