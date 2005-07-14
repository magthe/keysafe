import os
import os.path
import gconf

__all__ = [ \
        'get_config'
        ]

_config = None

class _Config(object):
    __dir = '/apps/keysafe'
    __timeout_key = '/apps/keysafe/timeout'
    __keysafe_key = '/apps/keysafe/keyfile'

    def __init__(self):
        object.__init__(self)
        self.__timeout = 0
        self.__keysafe = ''
        self.client = gconf.client_get_default()
        self.client.add_dir(self.__dir, gconf.CLIENT_PRELOAD_NONE)
        self.client.notify_add(self.__timeout_key, self.__new_timeout)
        self.client.notify_add(self.__keysafe_key, self.__new_keysafe)
        self.__new_timeout(self.client)
        self.__new_keysafe(self.client)

    def __new_timeout(self, client, *args, **kwargs):
        self.__timeout = client.get_int(self.__timeout_key)

    def __new_keysafe(self, client, *args, **kwargs):
        self.__keysafe = client.get_string(self.__keysafe_key)

    def __getitem__(self, name):
        if name == 'keyfile':
            return self.__keysafe
        elif name == 'timeout':
            return self.__timeout
        else:
            raise IndexError('Index:', name)

    def __setitem__(self, name, value):
        if name == 'keyfile':
            self.client.set_string(self.__keysafe_key, value)
        elif name == 'timeout':
            self.client.set_int(self.__timeout_key, int(value))
        else:
            raise IndexError('Index: %s - %s' % (name, value))

    def save(self):
        pass

def get_config():
    global _config
    if not _config:
        _config = _Config()
    return _config
