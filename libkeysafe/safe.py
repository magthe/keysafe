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

import os.path
import sys
import pickle

import cfg
from crypto1 import *


class _Safe(object):
    '''Class to hold the safe.

    It basically behaves like a dictionary with some added functions for
    storing and loading the entries.
    '''

    instance = None

    def __init__(self):
        object.__init__(self)
        self.__entries = {}

    def __getitem__(self, name):
        return self.__entries[name]

    def __setitem__(self, name, value):
        self.__entries[name] = value

    def keys(self):
        k = self.__entries.keys()
        k.sort()
        return k

    def set_entries(self, e):
        self.__entries = e

    def get_entries(self):
        return self.__entries
    
    def delete(self, id):
        self.__entries.pop(id)

def _load_safe(config):
    s = get_safe()
    try:
        fd = file(os.path.expanduser(config['keyfile']), 'r')
        s.set_entries(pickle.load(fd))
        fd.close()
    except (IOError, EOFError), e:
        s.set_entries({})
    except pickle.PickleError, e:
        s.set_entries({})
        fd.close()

def save_safe():
    s = get_safe()
    c = cfg.get_config()
    try:
        fd = file(os.path.expanduser(c['keyfile']), 'w+')
        pickle.dump(s.get_entries(), fd)
        fd.close()
    except pickle.PickleError, e:
        fd.close()
        raise e

def get_safe(config=None):
    if not config:
        config = cfg.get_config()
    if not _Safe.instance:
        _Safe.instance = _Safe()
        _load_safe(config=config)
    return _Safe.instance

def get_entry(id):
    '''Searches through the safe for the entry with the given C{id}.

    @type id: string
    @param id: the ID of the entry we are looking for
    @rtype: (string, string, string)
    @return: the entry with the given id C{(un, pw, text)}
    '''
    safe = get_safe()
    try:
        return safe[id]
    except:
        return None

def set_entry(id, un, pw, text, mpw):
    '''Add/modify an entry in the safe.

    An entry with ID of C{id} is added or modified in the safe. The password
    C{pw} is encrypted using C{mpw} before being put in.

    The ID of the entry has to be unique, adding an entry with the same ID as
    another will overwrite the first.

    @type id: string
    @param id: the ID of the entry
    @type un: string
    @param un: user name
    @type pw: string
    @param pw: clear text password
    @type text: string
    @param text: extra info
    @type mpw: string
    @param mpw: master password
    '''
    safe = get_safe()
    safe[id] = (un, encrypt(pw, mpw), text)

def delete_entry(id):
    safe = get_safe()
    safe.delete(id)
