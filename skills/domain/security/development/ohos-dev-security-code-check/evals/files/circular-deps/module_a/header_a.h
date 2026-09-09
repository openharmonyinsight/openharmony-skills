// Fixture: circular dependency between two directory modules.
// module_a/header_a.h includes module_b/header_b.h
// module_b/header_b.h includes module_a/header_a.h
// => A depends on B, B depends on A => circular dependency.

#ifndef MODULE_A_HEADER_A_H
#define MODULE_A_HEADER_A_H

#include "module_b/header_b.h"

namespace module_a {
struct HeaderA {
    int a_value;
    module_b::HeaderB *b_ref;
};
} // namespace module_a

#endif // MODULE_A_HEADER_A_H
