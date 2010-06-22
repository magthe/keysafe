APPNAME = 'keysafe'
VERSION = '0.4.1'

top = '.'
out = '_build'


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
    conf.check_python_headers()
    conf.check_cfg(package='botan-1.8', args='--cflags --libs', uselib_store='botan')
    conf.env.KEYSAFE_PY_PATH = '/usr/lib/keysafe'
    conf.env.KEYSAFE_GLADE_PATH = '/usr/lib/keysafe/gui'
    conf.env.KEYSAFE_BIN_PATH = '/usr/bin'

def build(bld):
    bld.add_subdirs('src gnome libkeysafe tools')

    for fil in ['keysafe', 'ksed']:
        bld(
                features='subst',
                source=fil+'.in',
                target=fil,
                chmod=0755,
                dict={
                    'KEYSAFE_PY_PATH' : bld.env.KEYSAFE_PY_PATH,
                    'KEYSAFE_GLADE_PATH' : bld.env.KEYSAFE_GLADE_PATH,
                    'KEYSAFE_BIN_PATH' : bld.env.KEYSAFE_BIN_PATH,
                    },
                )

# vim: set ft=python :
