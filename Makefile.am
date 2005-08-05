AUTOMAKE_OPTIONS = check-news dist-bzip2 subdir-objects

# directories
pylibdir = $(pkglibdir)/libkeysafe
guidir = $(pkglibdir)/gui
schemadir = $(GCONF_SCHEMA_FILE_DIR)
#desktopdir = $(datadir)/applications

bin_SCRIPTS = keysafe ksed

pylib_PYTHON = \
	libkeysafe/cfg.py \
	libkeysafe/ctrl.py \
	libkeysafe/edgui.py \
	libkeysafe/gui.py \
	libkeysafe/__init__.py \
	libkeysafe/safe.py

gui_DATA = gui/keysafe.glade gui/ksed.glade

schema_DATA = gnome/keysafe.schemas

# some manual builds
edit = sed \
       -e 's,@KEYSAFE_PY_PATH@,$(pkglibdir),g' \
       -e 's,@KEYSAFE_GLADE_PATH@,$(guidir),g'

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

libkeysafe/__init__.py: $(srcdir)/libkeysafe/__init__.py.in Makefile
	[ -d $(top_builddir)/libkeysafe ] || mkdir libkeysafe
	rm -f $(top_builddir)/libkeysafe/__init__.py \
		$(top_builddir)/libkeysafe/__init__.py.tmp
	$(edit) $(srcdir)/libkeysafe/__init__.py.in > \
		$(top_builddir)/libkeysafe/__init__.py.tmp
	mv $(top_builddir)/libkeysafe/__init__.py.tmp \
		$(top_builddir)/libkeysafe/__init__.py

# dist
EXTRA_DIST = keysafe.in \
	     ksed.in \
	     libkeysafe/cfg.py \
	     libkeysafe/ctrl.py \
	     libkeysafe/edgui.py \
	     libkeysafe/gui.py \
	     libkeysafe/__init__.py.in \
	     libkeysafe/safe.py \
	     gui/keysafe.glade \
	     gui/ksed.glade \
	     gnome/keysafe.schemas \
	     autogen.sh

# clean
CLEANFILES = keysafe ksed libkeysafe/__init__.py
