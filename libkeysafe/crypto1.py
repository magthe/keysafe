# Copyright (C) 2009 by Magnus Therning

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

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.randpool import RandomPool
from base64 import b64encode, b64decode
import struct

import oldsafe

_KNOWN_STR = "keysafe"

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
    pt = plain_text + _KNOWN_STR
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
        raise oldsafe.BadPwdException()
    if not _good_decipher(plain_text[1 + plain_len:]):
        raise oldsafe.BadPwdException()
    return plain_text[1:plain_len + 1]
