# OpenHarmony C++ Rules

Load this file before making OpenHarmony-specific style decisions.

## Core Rules

### File and naming rules

- Use `.h` for headers and `.cpp` for C++ implementation files.
- Match the main type and file name. Convert type names to `snake_case`.
  Example: `DatabaseConnection` -> `database_connection.h` and `database_connection.cpp`.
- Use `CamelCase` for classes, structs, unions, enums, namespaces, and functions.
- Use `camelBack` for parameters, local variables, and non-static globals.
- Prefix globals with `g_`.
- Name class member variables as `camelBack_`.
- Keep `struct` and `union` fields in `camelBack` without a trailing underscore.
- Use `UPPER_CASE` for enum values and supported constant names.

Expert judgment:

- Treat naming as an integration contract, not cosmetic cleanup. OpenHarmony reviews often read file names, class names, and member names as signals that code belongs in the tree.
- When editing existing code, preserve a strong local convention inside the touched subsystem unless the task is explicitly to migrate it.
- Do not rename broadly just to satisfy this file. Rename new files and changed symbols when the blast radius is local and clear.

### Header and file organization

- Add the Apache 2.0 copyright header when creating new project files.
- Use include guards, not `#pragma once`.
- Do not declare external interfaces or variables through stray `extern` declarations when a header should own the declaration.
- Do not place `#include` directives inside `extern "C"`.
- Prefer including the real dependency over piling up forward declarations when designing normal OpenHarmony code.
- Keep file-local symbols inside anonymous namespaces in `.cpp` files, not headers.
- Do not place `using namespace` in headers. Avoid putting it before includes anywhere.
- Prefer namespaces for global helpers and global constants instead of utility classes with static methods.

Expert judgment:

- Header choices affect downstream users. A shortcut in a header spreads into every translation unit that includes it.
- Prefer real includes over forward declarations when the type is part of the interface contract or when a forward declaration would hide ownership, lifetime, or ABI expectations.
- Use forward declarations only when they clearly reduce coupling without making the public API harder to understand.
- Keep `extern "C"` wrappers tight around declarations. Includes inside the block can silently change linkage assumptions for declarations owned by other headers.

### Macros and comments

- Avoid macros by default.
- Do not use macros for constants.
- Do not introduce function-like macros except for established project exceptions such as logging or include guards.
- Comment public APIs when the signature alone does not convey behavior, ownership, lifecycle, threading, return semantics, or constraints.
- Do not add template-style comments that only restate the declaration.

Expert judgment:

- A useful API comment answers what a caller cannot infer safely from the declaration: who owns returned data, which thread may call it, what failures mean, and whether null is accepted.
- Do not generate comment blocks just to satisfy a visible style requirement. Boilerplate comments train reviewers to ignore the comments that matter.
- Macros are acceptable for include guards and established project logging or tracing hooks. New constants, helpers, and type-like abstractions should use language constructs.

### Object semantics and inheritance

- If copy or move is not needed, explicitly delete it.
- For polymorphic base classes, do not expose unsafe public copy or move operations.
- Give inheritable base classes virtual destructors.
- Mark classes `final` when they are not intended for inheritance.
- Do not put default arguments on virtual functions.
- Do not shadow inherited non-virtual functions to simulate polymorphism.

Expert judgment:

- Decide class semantics before writing the first public method. If a type manages a service handle, thread callback, registration, or resource lifetime, copying is usually wrong and should be deleted immediately.
- Use `final` as a design statement for leaf classes. Omit it only when extension is expected by callers or tests and the base-class contract is intentionally documented.
- Default arguments on virtual functions create split behavior between static and dynamic types. Move defaults into non-virtual wrappers if callers need convenience.
- Do not create inheritance just to share helpers. Prefer free functions in a namespace or composition unless polymorphism is part of the external contract.

### OpenHarmony-specific design preferences

- Do not retain pointers returned by `std::string::c_str()`. Use them only at the call site.
- Avoid custom generic programming by default. Do not introduce template-heavy abstractions unless the project already allows them.
- In OpenHarmony-style code, non-owning parameters should usually be raw pointers or references rather than smart pointers.
- For member-owned resources or singleton-style ownership, follow the surrounding OpenHarmony convention instead of defaulting to modern smart-pointer evangelism.
- For lambdas that outlive the local scope, cross threads, or are stored, avoid reference capture of local variables.
- Avoid default captures like `[=]` or `[&]`. When capturing `this`, list the other captures explicitly.

Expert judgment:

- Do not reflexively modernize OpenHarmony interfaces into `std::shared_ptr` or templates. In this codebase, ownership clarity and subsystem convention matter more than generic modern C++ style.
- Use `T&` when the parameter is required and cannot be null. Use `T*` when null is a meaningful state or the surrounding API already uses pointer-style optionality. Use smart pointers in parameters only when the call transfers or shares ownership.
- For member-owned resources, follow the surrounding subsystem's lifetime pattern. A raw pointer member can be correct when ownership is external, framework-managed, singleton-like, or explicitly released elsewhere.
- Stored, returned, posted, or cross-thread lambdas must make lifetime visible. Capture values explicitly, and capture `this` only when the object's lifetime is guaranteed by the surrounding mechanism.
- Templates need a clear local payoff. Do not add a generic abstraction for one or two call sites, or to avoid writing a concrete interface.

## Hard No Patterns

These patterns are common model mistakes in OpenHarmony C++ work. Treat them as review blockers unless the surrounding project already establishes a clear exception.

- Do not create `CamelCase.hpp`, `CamelCase.cpp`, or `#pragma once` for new project files. Use `.h/.cpp`, `snake_case` file names, and include guards.
- Do not add `using namespace` to a header or before includes. It leaks names across every includer and makes later integration failures look unrelated to the changed file.
- Do not expose cross-file interfaces by adding stray `extern` declarations in `.cpp` files. Put the declaration in the owning header and include it.
- Do not wrap `#include` directives in `extern "C"`. Wrap only the C declarations that require C linkage.
- Do not replace a simple OpenHarmony-style raw pointer or reference parameter with `std::shared_ptr` just because it looks safer. That changes the ownership contract.
- Do not store `name.c_str()` or pass that pointer into asynchronous work. Keep the `std::string` alive or copy the string data into the long-lived context.
- Do not return, store, post, or dispatch lambdas that capture locals by reference. Default captures are especially risky because later edits can silently add unsafe captures.
- Do not add templates, traits, or generic helper frameworks to solve a local two-type problem. Prefer a concrete function or interface unless the subsystem already uses generic infrastructure.
- Do not write public API comments that only repeat the function name, parameter names, or return type. Replace them with behavior, ownership, threading, constraints, and failure semantics, or omit them when the API is internal and obvious.
- Do not make a class inheritable by accident. If it is a base class, give it a virtual destructor and safe copy or move semantics; if it is not a base class, mark it `final`.

## Exceptions

- When editing third-party or imported upstream code, preserve the existing local style instead of forcing OpenHarmony naming or layout into that file.
- When a surrounding subsystem has a strong established convention, follow it unless the task is explicitly to migrate the code toward OpenHarmony style.
