# OpenHarmony C++ Review Checklist

Load this file for `review` mode.

## Output shape

- Report findings first, ordered by severity.
- Include file paths and line numbers when available.
- Explain the violated convention and the practical impact.
- Keep the overall summary to a short closing paragraph.
- Keep the focus on high-signal OpenHarmony issues, not formatting trivia that local tooling can already settle.
- Treat Hard No matches from `rules.md` as likely blockers unless the surrounding subsystem establishes a clear exception.

## Review categories

### File and naming

- Are new C++ files using `.h` and `.cpp`?
- Do file names match the main type in `snake_case`?
- Did the change introduce `CamelCase.hpp`, `CamelCase.cpp`, or `#pragma once` for new project files?
- Are globals prefixed with `g_`?
- Do class members use a trailing underscore?
- Are `struct` fields free of the trailing underscore?

### Header discipline

- Does each header use an include guard rather than `#pragma once`?
- Is any interface being exposed through `extern` instead of the proper header?
- Is any `#include` placed inside `extern "C"`?
- Does the header contain `using namespace`?
- Is `using namespace` placed before includes in a `.cpp` file?
- Are forward declarations hiding ownership, lifetime, or ABI expectations that should be visible through a real include?
- Are file-local helpers leaking into headers instead of staying in a `.cpp` anonymous namespace?

### Macros and templates

- Is a macro used where a constant, enum, or function should be used?
- Is any function-like macro introduced without a project-specific exception?
- Did the change add generic or template-heavy abstractions that the project does not need?
- Did the change add templates, traits, or helper frameworks for a local two-type problem better served by a concrete function or interface?

### API comments

- Do public functions have meaningful comments where behavior is not obvious from the signature?
- Are comments providing real information about constraints, return values, ownership, or threading?
- Do comments explain nullability, ownership transfer, callback lifetime, thread expectations, or failure semantics when those matter to callers?
- Are any comments just boilerplate paraphrases of the declaration?

### Object semantics

- Are copy and move operations explicitly deleted when not intended?
- Do polymorphic base classes have safe destructor and copy or move semantics?
- Is `final` used where inheritance is not intended?
- Are virtual functions free of default arguments?
- Is any inherited non-virtual function being shadowed?
- Did the change make a class inheritable accidentally, without a documented extension contract and virtual destructor?
- Could a non-virtual wrapper provide caller defaults instead of default arguments on a virtual function?

### Ownership and local correctness

- Is a `c_str()` pointer being stored beyond the immediate call?
- Is a `c_str()` pointer passed into asynchronous, stored, or deferred work where the string may not remain alive?
- Do non-owning interfaces avoid smart pointers unless surrounding code requires them?
- Did the change replace a raw pointer or reference non-owning interface with `std::shared_ptr` without changing the ownership contract?
- Are long-lived lambdas free of risky reference captures?
- Are default captures used where explicit captures would be safer?
- For returned, stored, posted, or cross-thread lambdas, are all captures explicit and are object lifetimes guaranteed?
