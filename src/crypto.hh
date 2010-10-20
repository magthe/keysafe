#ifndef _CRYPTO_HH_
#define _CRYPTO_HH_

#include <boost/python.hpp>
#include <botan/botan.h>
#include <string>
#include <utility>

class Crypto {
    public:
        Crypto(const char *);
        ~Crypto();

        std::pair<char *, char *> encrypt(const char *);
        const char * decrypt(const char *, const char *);

    private:
        static Botan::LibraryInitializer *libinit;
        std::string passphrase;
};

#endif
