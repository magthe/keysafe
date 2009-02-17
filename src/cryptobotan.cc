#include <boost/python.hpp>

#include "crypto.hh"

using namespace boost::python;

BOOST_PYTHON_MODULE(cryptobotan)
{
    class_<Crypto>("Crypto", init<std::string>())
        .def("encrypt", &Crypto::encrypt)
        .def("decrypt", &Crypto::decrypt)
        ;
}
