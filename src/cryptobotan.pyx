from libcpp.pair cimport pair

cdef extern from "crypto.hh":
    cdef cppclass Crypto:
        Crypto(char *)
        pair[char *, char *] encrypt(char *)
        char *decrypt(char *, char *)

cdef class PyCrypto:
    cdef Crypto *thisptr

    def __init__(self, pwd):
        self.thisptr = new Crypto(pwd)

    def __dealloc__(self):
        del self.thisptr

    def encrypt(self, pt):
        r = self.thisptr.encrypt(pt)
        return (r.first, r.second)

    def decrypt(self, salt, ct):
        return self.thisptr.decrypt(salt, ct)
