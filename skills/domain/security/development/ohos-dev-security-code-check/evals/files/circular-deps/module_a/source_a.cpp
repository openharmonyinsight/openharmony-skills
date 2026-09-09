// Source file for module_a — makes the directory recognized as a module by the scanner.
#include "module_a/header_a.h"

namespace module_a {

HeaderA *CreateHeaderA(int value) {
    HeaderA *h = new HeaderA();
    h->a_value = value;
    h->b_ref = nullptr;
    return h;
}

} // namespace module_a
