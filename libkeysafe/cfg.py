# Copyright (C) 2005 by Magnus Therning

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

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
