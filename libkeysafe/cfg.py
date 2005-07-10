import os
import os.path
from ConfigParser import SafeConfigParser as CfgParser

__all__ = [ \
        'get_config'
        ]

_config = None

class _Config(object):
    __defaults = { \
            'safe' : os.path.join(os.getenv('HOME'), '.keysafe'),
            'timeout' : '15000',
            }

    def __init__(self, cfg_file = None):
        object.__init__(self)
        self.__cfgfile = cfg_file
        if not self.__cfgfile:
            self.__cfg_file = os.path.join(os.getenv('HOME'), '.keysaferc')
        self.__cfg = CfgParser(self.__defaults)
        self.__cfg.add_section('keysafe')
        try:
            cfg_file = open(self.__cfg_file, 'r')
            self.__cfg.readfp(cfg_file)
            cfg_file.close()
        except IOError, e:
            pass # don't care at the moment

    def __getitem__(self, name):
        if name == 'timeout':
            return self.__cfg.getint('keysafe', name)
        else:
            try:
                return self.__cfg.get('keysafe', name)
            except:
                raise AttributeError

    def __setitem__(self, name, value):
        self.__cfg.set('keysafe', name, str(value))

    def save(self):
        cfg_file = open(self.__cfg_file, 'w+')
        self.__cfg.write(cfg_file)
        cfg_file.close()

def get_config():
    global _config
    if not _config:
        _config = _Config()
    return _config
