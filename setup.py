from distutils.core import setup

# The following setup will install in the following locations:
#  keysafe -> <prefix>/bin
#  ksed -> <prefix>/bin
#  libkeysafe/*.py -> <prefix>/lib/python<version>/site-packages/libkeysafe
#  gui/*.glade -> <prefix>/lib/keysafe/gui
setup(name = 'keysafe',
        version = '0.3a',
        author = 'Magnus Therning',
        author_email = 'magnus@therning.org',
        scripts = ['keysafe', 'ksed'],
        packages = ['libkeysafe'],
        data_files = [\
                ('lib/keysafe/gui', ['gui/keysafe.glade', 'gui/ksed.glade']),
                ('share/gconf/schemas', ['gnome/keysafe.schemas']),
                ],
        )
