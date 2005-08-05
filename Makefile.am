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
	rm -f keysafe keysafe.tmp
	$(edit) $(srcdir)/keysafe.in > keysafe.tmp
	chmod +x keysafe.tmp
	mv keysafe.tmp keysafe

ksed: $(srcdir)/ksed.in Makefile
	rm -f ksed ksed.tmp
	$(edit) $(srcdir)/ksed.in > ksed.tmp
	chmod +x ksed.tmp
	mv ksed.tmp ksed

libkeysafe/__init__.py: $(srcdir)/libkeysafe/__init__.py.in Makefile
	rm -rf libkeysafe
	mkdir libkeysafe
	rm -f libkeysafe/__init__.py libkeysafe/__init__.py.tmp
	$(edit) $(srcdir)/libkeysafe/__init__.py.in > libkeysafe/__init__.py.tmp
	mv libkeysafe/__init__.py.tmp libkeysafe/__init__.py

# dist
EXTRA_DIST = keysafe.in ksed.in \
	     libkeysafe/cfg.py \
	     libkeysafe/ctrl.py \
	     libkeysafe/edgui.py \
	     libkeysafe/gui.py \
	     libkeysafe/__init__.py.in \
	     libkeysafe/safe.py \
	     gui/keysafe.glade gui/ksed.glade \
	     gnome/keysafe.schemas

# clean
CLEANFILES = keysafe ksed libkeysafe/__init__.py
