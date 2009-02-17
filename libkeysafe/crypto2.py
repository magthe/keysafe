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

from libkeysafe.safe import BadPwdException
from libkeysafe.cryptobotan import Crypto

_KNOWN_STR = "keysafe2"

def encrypt(plain_text, passwd):
    c = Crypto(passwd)
    s, ct = c.encrypt(plain_text + _KNOWN_STR)
    return (s + ct).encode('base64')

def decrypt(b64cipher_text, passwd):
    def _good_decipher(fpt):
        return fpt[-len(_KNOWN_STR):] == _KNOWN_STR

    ct0 = b64cipher_text.decode('base64')
    s, ct = ct0[:8], ct0[8:]
    c = Crypto(passwd)
    fpt = c.decrypt(s, ct)
    if not _good_decipher(fpt): raise BadPwdException()
    return fpt[:-len(_KNOWN_STR)]
