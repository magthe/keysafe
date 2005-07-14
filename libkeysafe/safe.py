import os.path
import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.randpool import RandomPool
from base64 import b64encode, b64decode
import struct
import pickle

import cfg

_KNOWN_STR = "keysafe"

class BadPwdException(Exception):
    pass

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

def _load_safe():
    # This should use the configured filename for the safe, load it using
    # pickle and then return it. I need to come up with a good format for
    # it.
    s = get_safe()
    c = cfg.get_config()
    try:
        fd = file(os.path.expanduser(c['keyfile']), 'r')
        s.set_entries(pickle.load(fd))
        fd.close()
    except (IOError, EOFError), e:
        s.set_entries({})
        raise e
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
    except IOError, e:
        s.set_entries({})
        raise e
    except pickle.PickleError, e:
        s.set_entries({})
        fd.close()

def get_safe():
    if not _Safe.instance:
        _Safe.instance = _Safe()
        _load_safe()
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

def _derive_key(pwd, salt):
    '''Constructs a string of bytes from the provided password.

    The key is constructed from the password and the provided salt in the
    following way SHA256(salt + pwd).

    @type pwd: string
    @param pwd: password
    @type salt: byte string
    @param salt: salt
    @rtype: byte string
    @return: 32 byte long string, suitable for use as key in AES
    '''
    return SHA256.new(salt + pwd).digest()

def encrypt(plain_text, passwd):
    '''Encrypts C{plain_text} using a key derived from C{passwd}.

    A key is derived from C{passwd} using L{_derive_key} with a random 8 byte
    salt. This key is then used to encrypt the following string:

        <len(plain)> + plain + "keysafe" + <random bytes>

    Then the salt and the ciphertext is concatenated and the result is base64
    encoded before being returned.

    @type plain_text: string
    @param plain_text: password
    @type passwd: string
    @param passwd: key to use for encryption
    @rtype: string
    @return: base64 encoded encryption of C{plain_text} using C{passwd}
    '''
    # TODO: Change the string to be encrypted to
    #  <len(plain)> + <plain> + <sha256(plain)> + <random bytes>
    # This should be better than using "keysafe" in the string

    # create the salt, and derive the key
    rp = RandomPool()
    salt = rp.get_bytes(8)
    key = _derive_key(passwd, salt)

    # create the full plain text string, make sure it matches the block size
    # for AES
    pt = plain_text + "keysafe"
    rnd_pad_len = struct.unpack('B', rp.get_bytes(1))[0]
    rnd_pad_len += AES.block_size - \
            (1 + len(pt) + rnd_pad_len) % AES.block_size
    rnd_pad = rp.get_bytes(rnd_pad_len)
    full_plain_text = struct.pack('B', len(plain_text)) + pt + rnd_pad

    # encrypt, it seems I need to do it twice to get a predictable result
    cipher_block = AES.new(key, AES.MODE_PGP)
    cipher_text = cipher_block.encrypt(full_plain_text)
    cipher_text = cipher_block.encrypt(full_plain_text)

    return b64encode(salt + cipher_text)

def decrypt(b64cipher_text, passwd):
    '''Decrypt C{b64cipher_text} using C{passwd} as key.

    @type b64cipher_text: string
    @param b64cipher_text: See L{encrypt} for the format of C{b64cipher_text}.
    @type passwd: string
    @param passwd: The master password.
    '''

    def _good_decipher(full_plain_text):
        return full_plain_text[:len(_KNOWN_STR)] == _KNOWN_STR

    cipher_text = b64decode(b64cipher_text)

    # pick out the salt and derive the key
    salt = cipher_text[:8]
    key = _derive_key(passwd, salt)

    # decrypt, do it twice to get it correct!
    cipher_block = AES.new(key, AES.MODE_PGP)
    plain_text = cipher_block.decrypt(cipher_text[8:])
    plain_text = cipher_block.decrypt(cipher_text[8:])

    plain_len = struct.unpack('B', plain_text[0])[0]
    if plain_len < 0 or plain_len > len(plain_text[1:]):
        raise BadPwdException()
    if not _good_decipher(plain_text[1 + plain_len:]):
        raise BadPwdException()
    return plain_text[1:plain_len + 1]
