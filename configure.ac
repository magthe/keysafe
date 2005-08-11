AC_INIT(keysafe, 0.3.2, [Magnus Therning <magnus@therning.org>])
AC_CONFIG_SRCDIR(libkeysafe/safe.py)
AM_INIT_AUTOMAKE

AM_MAINTAINER_MODE

dnl Test for GConf
AC_PATH_PROG(GCONFTOOL, gconftool-2)
AM_GCONF_SOURCE_2

AM_PATH_PYTHON(2.4)

PKG_CHECK_MODULES(PYGTK, pygtk-2.0 gnome-python-2.0)
AC_SUBST(PYGTK_CFLAGS)
AC_SUBST(PYGTK_LIBS)

AC_SUBST(VERSION)

AC_OUTPUT([Makefile])
