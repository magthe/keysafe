APPNAME = 'keysafe'
VERSION = '0.4.1'

top = '.'
out = '_build'

import os.path

def set_options(opt):
    opt.tool_options('compiler_cxx')
    opt.tool_options('boost')
    opt.tool_options('python')
    opt.tool_options('misc')

def configure(conf):
    conf.check_tool('compiler_cxx')
    conf.check_tool('boost')
    conf.check_tool('python')
    conf.check_tool('misc')
    conf.check_tool('gnome')
    conf.check_python_headers()
    conf.check_cfg(package='botan-1.8', args='--cflags --libs', uselib_store='botan')
    conf.env.KEYSAFE_PATH = os.path.join(conf.env.PREFIX, 'lib', 'keysafe')
    conf.env.KEYSAFE_PY_PATH = os.path.join(conf.env.PREFIX, 'lib', 'keysafe', 'libkeysafe')
    conf.env.KEYSAFE_GLADE_PATH = os.path.join(conf.env.PREFIX, 'lib', 'keysafe', 'gui')
    conf.env.KEYSAFE_BIN_PATH = os.path.join(conf.env.PREFIX, 'bin')
    conf.env.KEYSAFE_GNOME_DATA_PATH = os.path.join(conf.env.PREFIX, 'share', 'applications')
    conf.env.KEYSAFE_GNOME_SCHEMA_PATH = os.path.join(conf.env.PREFIX, 'etc', 'gconf', 'schemas')

def build(bld):
    bld.add_subdirs('src gnome libkeysafe tools')

    for fil in ['keysafe', 'ksed']:
        bld(
                features='subst',
                source=fil+'.in',
                target=fil,
                chmod=0755,
                dict={
                    'KEYSAFE_PATH' : bld.env.KEYSAFE_PATH,
                    'KEYSAFE_GLADE_PATH' : bld.env.KEYSAFE_GLADE_PATH,
                    'KEYSAFE_BIN_PATH' : bld.env.KEYSAFE_BIN_PATH,
                    },
                install_path = '${KEYSAFE_BIN_PATH}',
                )

# vim: set ft=python :
