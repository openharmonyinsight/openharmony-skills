// Source file for module_b — makes the directory recognized as a module by the scanner.
#include "module_b/header_b.h"

namespace module_b {

HeaderB *CreateHeaderB(int value) {
    HeaderB *h = new HeaderB();
    h->b_value = value;
    h->a_ref = nullptr;
    return h;
}

} // namespace module_b
