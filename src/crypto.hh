#ifndef _CRYPTO_HH_
#define _CRYPTO_HH_

#include <boost/python.hpp>
#include <botan/botan.h>
#include <string>

class Crypto {
    public:
        Crypto(std::string pwd);
        ~Crypto();

        boost::python::tuple encrypt(std::string pt);
        std::string decrypt(std::string salt, std::string ct);

    private:
        static Botan::LibraryInitializer *libinit;
        std::string passphrase;
};

#endif
