#include "crypto.hh"

#include <memory>

const char *S2K_ALGO = "PBKDF2(SHA-1)";
const char *KDF_ALGO = "KDF2(SHA-1)";
const char *CIPHER_ALGO = "AES/CBC/PKCS7";

Botan::LibraryInitializer *Crypto::libinit = 0;

Crypto::Crypto(const char *pwd) : passphrase(pwd)
{
    if(!libinit)
        libinit = new Botan::LibraryInitializer();
}

Crypto::~Crypto() {}

std::pair<char *, char *> Crypto::encrypt(const char *pt)
{
    std::string _pt(pt);
    Botan::AutoSeeded_RNG rng;
    std::auto_ptr<Botan::S2K> s2k(Botan::get_s2k(S2K_ALGO));
    s2k->set_iterations(4096);
    s2k->new_random_salt(rng, 8);
    Botan::SecureVector<Botan::byte> the_salt = s2k->current_salt();

    Botan::SecureVector<Botan::byte> master_key = s2k->derive_key(48, passphrase).bits_of();

    std::auto_ptr<Botan::KDF> kdf(Botan::get_kdf(KDF_ALGO));

    Botan::SymmetricKey key = kdf->derive_key(32, master_key, "cipher key");
    //SymmetricKey mac_key = kdf->derive_key(20, masterkey, "hmac key");
    Botan::InitializationVector iv = kdf->derive_key(16, master_key, "cipher iv");

    Botan::Pipe pipe(get_cipher(CIPHER_ALGO, key, iv, Botan::ENCRYPTION));
    pipe.process_msg(_pt);

    std::string salt_string((const char *)the_salt.begin(), the_salt.size());
    char *ss = strdup(salt_string.c_str());
    std::string ct_string(pipe.read_all_as_string());
    char *ct = strdup(ct_string.c_str());
    return std::make_pair(ss, ct);
}

const char *Crypto::decrypt(const char *salt, const char *ct)
{
    std::string _salt(salt);
    std::string _ct(ct);
    std::auto_ptr<Botan::S2K> s2k(Botan::get_s2k(S2K_ALGO));
    s2k->set_iterations(4096);
    s2k->change_salt((const Botan::byte *)_salt.c_str(), _salt.size());

    Botan::SecureVector<Botan::byte> master_key = s2k->derive_key(48, passphrase).bits_of();

    std::auto_ptr<Botan::KDF> kdf(Botan::get_kdf(KDF_ALGO));

    Botan::SymmetricKey key = kdf->derive_key(32, master_key, "cipher key");
    //SymmetricKey mac_key = kdf->derive_key(20, masterkey, "hmac key");
    Botan::InitializationVector iv = kdf->derive_key(16, master_key, "cipher iv");

    Botan::Pipe pipe(get_cipher(CIPHER_ALGO, key, iv, Botan::DECRYPTION));
    pipe.process_msg(_ct);

    std::string pt_string(pipe.read_all_as_string());
    const char *pt = strdup(pt_string.c_str());
    return pt;
}
