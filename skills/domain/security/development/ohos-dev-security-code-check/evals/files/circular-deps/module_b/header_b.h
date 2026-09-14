// Fixture: circular dependency between two directory modules.
// module_b/header_b.h includes module_a/header_a.h
// => completes the cycle module_a -> module_b -> module_a.

#ifndef MODULE_B_HEADER_B_H
#define MODULE_B_HEADER_B_H

#include "module_a/header_a.h"

namespace module_b {
struct HeaderB {
    int b_value;
    module_a::HeaderA *a_ref;
};
} // namespace module_b

#endif // MODULE_B_HEADER_B_H
