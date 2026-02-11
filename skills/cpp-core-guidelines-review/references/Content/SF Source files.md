# <a name="s-source"></a>SF: Source files

Distinguish between declarations (used as interfaces) and definitions (used as implementations).
Use header files to represent interfaces and to emphasize logical structure.

Source file rule summary:

* [SF.1: Use a `.cpp` suffix for code files and `.h` for interface files if your project doesn't already follow another convention](#rs-file-suffix)
* [SF.2: A header file must not contain object definitions or non-inline function definitions](#rs-inline)
* [SF.3: Use header files for all declarations used in multiple source files](#rs-declaration-header)
* [SF.4: Include header files before other declarations in a file](#rs-include-order)
* [SF.5: A `.cpp` file must include the header file(s) that defines its interface](#rs-consistency)
* [SF.6: Use `using namespace` directives for transition, for foundation libraries (such as `std`), or within a local scope (only)](#rs-using)
* [SF.7: Don't write `using namespace` at global scope in a header file](#rs-using-directive)
* [SF.8: Use `#include` guards for all header files](#rs-guards)
* [SF.9: Avoid cyclic dependencies among source files](#rs-cycles)
* [SF.10: Avoid dependencies on implicitly `#include`d names](#rs-implicit)
* [SF.11: Header files should be self-contained](#rs-contained)
* [SF.12: Prefer the quoted form of `#include` for files relative to the including file and the angle bracket form everywhere else](#rs-incform)
* [SF.13: Use portable header identifiers in `#include` statements](#rs-portable-header-id)

* [SF.20: Use `namespace`s to express logical structure](#rs-namespace)
* [SF.21: Don't use an unnamed (anonymous) namespace in a header](#rs-unnamed)
* [SF.22: Use an unnamed (anonymous) namespace for all internal/non-exported entities](#rs-unnamed2)

### <a name="rs-file-suffix"></a>SF.1: Use a `.cpp` suffix for code files and `.h` for interface files if your project doesn't already follow another convention

See [NL.27](#rl-file-suffix)

### <a name="rs-inline"></a>SF.2: A header file must not contain object definitions or non-inline function definitions

##### Reason

Including entities subject to the one-definition rule leads to linkage errors.

##### Example

    // file.h:
    namespace Foo {
        int x = 7;
        int xx() { return x+x; }
    }

    // file1.cpp:
    #include <file.h>
    // ... more ...

     // file2.cpp:
    #include <file.h>
    // ... more ...

Linking `file1.cpp` and `file2.cpp` will give two linker errors.

**Alternative formulation**: A header file must contain only:

* `#include`s of other header files (possibly with include guards)
* templates
* class definitions
* function declarations
* `extern` declarations
* `inline` function definitions
* `constexpr` definitions
* `const` definitions
* `using` alias definitions
* ???

##### Enforcement

Check the positive list above.

### <a name="rs-declaration-header"></a>SF.3: Use header files for all declarations used in multiple source files

##### Reason

Maintainability. Readability.

##### Example, bad

    // bar.cpp:
    void bar() { cout << "bar\n"; }

    // foo.cpp:
    extern void bar();
    void foo() { bar(); }

A maintainer of `bar` cannot find all declarations of `bar` if its type needs changing.
The user of `bar` cannot know if the interface used is complete and correct. At best, error messages come (late) from the linker.

##### Enforcement

* Flag declarations of entities in other source files not placed in a `.h`.

### <a name="rs-include-order"></a>SF.4: Include header files before other declarations in a file

##### Reason

Minimize context dependencies and increase readability.

##### Example

    #include <vector>
    #include <algorithm>
    #include <string>

    // ... my code here ...

##### Example, bad

    #include <vector>

    // ... my code here ...

    #include <algorithm>
    #include <string>

##### Note

This applies to both `.h` and `.cpp` files.

##### Note

There is an argument for insulating code from declarations and macros in header files by `#including` headers *after* the code we want to protect
(as in the example labeled "bad").
However

* that only works for one file (at one level): Use that technique in a header included with other headers and the vulnerability reappears.
* a namespace (an "implementation namespace") can protect against many context dependencies.
* full protection and flexibility require modules.

**See also**:

* [Working Draft, Extensions to C++ for Modules](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4592.pdf)
* [Modules, Componentization, and Transition](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0141r0.pdf)

##### Enforcement

Easy.

### <a name="rs-consistency"></a>SF.5: A `.cpp` file must include the header file(s) that defines its interface

##### Reason

This enables the compiler to do an early consistency check.

##### Example, bad

    // foo.h:
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp:
    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);

The errors will not be caught until link time for a program calling `bar` or `foobar`.

##### Example

    // foo.h:
    void foo(int);
    int bar(long);
    int foobar(int);

    // foo.cpp:
    #include "foo.h"

    void foo(int) { /* ... */ }
    int bar(double) { /* ... */ }
    double foobar(int);   // error: wrong return type

The return-type error for `foobar` is now caught immediately when `foo.cpp` is compiled.
The argument-type error for `bar` cannot be caught until link time because of the possibility of overloading, but systematic use of `.h` files increases the likelihood that it is caught earlier by the programmer.

##### Enforcement

???

### <a name="rs-using"></a>SF.6: Use `using namespace` directives for transition, for foundation libraries (such as `std`), or within a local scope (only)

##### Reason

 `using namespace` can lead to name clashes, so it should be used sparingly.
 However, it is not always possible to qualify every name from a namespace in user code (e.g., during transition)
 and sometimes a namespace is so fundamental and prevalent in a code base, that consistent qualification would be verbose and distracting.

##### Example

    #include <string>
    #include <vector>
    #include <iostream>
    #include <memory>
    #include <algorithm>

    using namespace std;

    // ...

Here (obviously), the standard library is used pervasively and apparently no other library is used, so requiring `std::` everywhere
could be distracting.

##### Example

The use of `using namespace std;` leaves the programmer open to a name clash with a name from the standard library

    #include <cmath>
    using namespace std;

    int g(int x)
    {
        int sqrt = 7;
        // ...
        return sqrt(x); // error
    }

However, this is not particularly likely to lead to a resolution that is not an error and
people who use `using namespace std` are supposed to know about `std` and about this risk.

##### Note

A `.cpp` file is a form of local scope.
There is little difference in the opportunities for name clashes in an N-line `.cpp` containing a `using namespace X`,
an N-line function containing a `using namespace X`,
and M functions each containing a `using namespace X` with N lines of code in total.

##### Note

[Don't write `using namespace` at global scope in a header file](#rs-using-directive).

### <a name="rs-using-directive"></a>SF.7: Don't write `using namespace` at global scope in a header file

##### Reason

Doing so takes away an `#include`r's ability to effectively disambiguate and to use alternatives. It also makes `#include`d headers order-dependent as they might have different meaning when included in different orders.

##### Example

    // bad.h
    #include <iostream>
    using namespace std; // bad

    // user.cpp
    #include "bad.h"

    bool copy(/*... some parameters ...*/);    // some function that happens to be named copy

    int main()
    {
        copy(/*...*/);    // now overloads local ::copy and std::copy, could be ambiguous
    }

##### Note

An exception is `using namespace std::literals;`. This is necessary to use string literals
in header files and given [the rules](https://eel.is/c++draft/over.literal) - users are required
to name their own UDLs `operator""_x` - they will not collide with the standard library.

##### Enforcement

Flag `using namespace` at global scope in a header file.

### <a name="rs-guards"></a>SF.8: Use `#include` guards for all header files

##### Reason

To avoid files being `#include`d several times.

In order to avoid include guard collisions, do not just name the guard after the filename.
Be sure to also include a key and good differentiator, such as the name of library or component
the header file is part of.

##### Example

    // file foobar.h:
    #ifndef LIBRARY_FOOBAR_H
    #define LIBRARY_FOOBAR_H
    // ... declarations ...
    #endif // LIBRARY_FOOBAR_H

##### Enforcement

Flag `.h` files without `#include` guards.

##### Note

Some implementations offer vendor extensions like `#pragma once` as alternative to include guards.
It is not standard and it is not portable.  It injects the hosting machine's filesystem semantics
into your program, in addition to locking you down to a vendor.
Our recommendation is to write in ISO C++: See [rule P.2](#rp-cplusplus).

### <a name="rs-cycles"></a>SF.9: Avoid cyclic dependencies among source files

##### Reason

Cycles complicate comprehension and slow down compilation. They also
complicate conversion to use language-supported modules (when they become
available).

##### Note

Eliminate cycles; don't just break them with `#include` guards.

##### Example, bad

    // file1.h:
    #include "file2.h"

    // file2.h:
    #include "file3.h"

    // file3.h:
    #include "file1.h"

##### Enforcement

Flag all cycles.


### <a name="rs-implicit"></a>SF.10: Avoid dependencies on implicitly `#include`d names

##### Reason

Avoid surprises.
Avoid having to change `#include`s if an `#include`d header changes.
Avoid accidentally becoming dependent on implementation details and logically separate entities included in a header.

##### Example, bad

    #include <iostream>
    using namespace std;

    void use()
    {
        string s;
        cin >> s;               // fine
        getline(cin, s);        // error: getline() not defined
        if (s == "surprise") {  // error == not defined
            // ...
        }
    }

`<iostream>` exposes the definition of `std::string` ("why?" makes for a fun trivia question),
but it is not required to do so by transitively including the entire `<string>` header,
resulting in the popular beginner question "why doesn't `getline(cin,s);` work?"
or even an occasional "`string`s cannot be compared with `==`").

The solution is to explicitly `#include <string>`:

##### Example, good

    #include <iostream>
    #include <string>
    using namespace std;

    void use()
    {
        string s;
        cin >> s;               // fine
        getline(cin, s);        // fine
        if (s == "surprise") {  // fine
            // ...
        }
    }

##### Note

Some headers exist exactly to collect a set of consistent declarations from a variety of headers.
For example:

    // basic_std_lib.h:

    #include <string>
    #include <map>
    #include <iostream>
    #include <random>
    #include <vector>

a user can now get that set of declarations with a single `#include`

    #include "basic_std_lib.h"

This rule against implicit inclusion is not meant to prevent such deliberate aggregation.

##### Enforcement

Enforcement would require some knowledge about what in a header is meant to be "exported" to users and what is there to enable implementation.
No really good solution is possible until we have modules.

### <a name="rs-contained"></a>SF.11: Header files should be self-contained

##### Reason

Usability, headers should be simple to use and work when included on their own.
Headers should encapsulate the functionality they provide.
Avoid clients of a header having to manage that header's dependencies.

##### Example

    #include "helpers.h"
    // helpers.h depends on std::string and includes <string>

##### Note

Failing to follow this results in difficult to diagnose errors for clients of a header.

##### Note

A header should include all its dependencies. Be careful about using relative paths because C++ implementations diverge on their meaning.

##### Enforcement

A test should verify that the header file itself compiles or that a cpp file which only includes the header file compiles.

### <a name="rs-incform"></a>SF.12: Prefer the quoted form of `#include` for files relative to the including file and the angle bracket form everywhere else

##### Reason

The [standard](https://eel.is/c++draft/cpp.include) provides flexibility for compilers to implement
the two forms of `#include` selected using the angle (`<>`) or quoted (`""`) syntax. Vendors take
advantage of this and use different search algorithms and methods for specifying the include path.

Nevertheless, the guidance is to use the quoted form for including files that exist at a relative path to the file containing the `#include` statement (from within the same component or project) and to use the angle bracket form everywhere else, where possible. This encourages being clear about the locality of the file relative to files that include it, or scenarios where the different search algorithm is required. It makes it easy to understand at a glance whether a header is being included from a local relative file versus a standard library header or a header from the alternate search path (e.g. a header from another library or a common set of includes).

##### Example

    // foo.cpp:
    #include <string>                // From the standard library, requires the <> form
    #include <some_library/common.h> // A file that is not locally relative, included from another library; use the <> form
    #include "foo.h"                 // A file locally relative to foo.cpp in the same project, use the "" form
    #include "util/util.h"           // A file locally relative to foo.cpp in the same project, use the "" form
    #include <component_b/bar.h>     // A file in the same project located via a search path, use the <> form

##### Note

Failing to follow this results in difficult to diagnose errors due to picking up the wrong file by incorrectly specifying the scope when it is included. For example, in a typical case where the `#include ""` search algorithm might search for a file existing at a local relative path first, then using this form to refer to a file that is not locally relative could mean that if a file ever comes into existence at the local relative path (e.g. the including file is moved to a new location), it will now be found ahead of the previous include file and the set of includes will have been changed in an unexpected way.

Library creators should put their headers in a folder and have clients include those files using the relative path `#include <some_library/common.h>`

##### Enforcement

A test should identify whether headers referenced via `""` could be referenced with `<>`.

### <a name="rs-portable-header-id"></a>SF.13: Use portable header identifiers in `#include` statements

##### Reason

The [standard](https://eel.is/c++draft/cpp.include) does not specify how compilers uniquely locate headers from an identifier in an `#include` directive, nor does it specify what constitutes uniqueness. For example, whether the implementation considers the identifiers to be case-sensitive, or whether the identifiers are file system paths to a header file, and if so, how a hierarchical file system path is delimited.

To maximize the portability of `#include` directives across compilers, guidance is to:

* use case-sensitivity for the header identifier, matching how the header is defined by the standard, specification, implementation, or file that provides the header.
* when the header identifier is a hierarchical file path, use forward-slash `/` to delimit path components as this is the most widely-accepted path-delimiting character.

##### Example

    // good examples
    #include <vector>
    #include <string>
    #include "util/util.h"

    // bad examples
    #include <VECTOR>        // bad: the standard library defines a header identified as <vector>, not <VECTOR>
    #include <String>        // bad: the standard library defines a header identified as <string>, not <String>
    #include "Util/Util.H"   // bad: the header file exists on the file system as "util/util.h"
    #include "util\util.h"   // bad: may not work if the implementation interprets `\u` as an escape sequence, or where '\' is not a valid path separator

##### Enforcement

It is only possible to enforce on implementations where header identifiers are case-sensitive and which only support `/` as a file path delimiter.

### <a name="rs-namespace"></a>SF.20: Use `namespace`s to express logical structure

##### Reason

 ???

##### Example

    ???

##### Enforcement

???

### <a name="rs-unnamed"></a>SF.21: Don't use an unnamed (anonymous) namespace in a header

##### Reason

It is almost always a bug to mention an unnamed namespace in a header file.

##### Example

    // file foo.h:
    namespace
    {
        const double x = 1.234;  // bad

        double foo(double y)     // bad
        {
            return y + x;
        }
    }

    namespace Foo
    {
        const double x = 1.234; // good

        inline double foo(double y)        // good
        {
            return y + x;
        }
    }

##### Enforcement

* Flag any use of an anonymous namespace in a header file.

### <a name="rs-unnamed2"></a>SF.22: Use an unnamed (anonymous) namespace for all internal/non-exported entities

##### Reason

Nothing external can depend on an entity in a nested unnamed namespace.
Consider putting every definition in an implementation source file in an unnamed namespace unless that is defining an "external/exported" entity.

##### Example; bad

    static int f();
    int g();
    static bool h();
    int k();

##### Example; good

    namespace {
        int f();
        bool h();
    }
    int g();
    int k();

##### Example

An API class and its members can't live in an unnamed namespace; but any "helper" class or function that is defined in an implementation source file should be at an unnamed namespace scope.

    ???

##### Enforcement

* ???

# <a name="s-stdlib"></a>SL: The Standard Library

Using only the bare language, every task is tedious (in any language).
Using a suitable library any task can be reasonably simple.

The standard library has steadily grown over the years.
Its description in the standard is now larger than that of the language features.
So, it is likely that this library section of the guidelines will eventually grow in size to equal or exceed all the rest.

<< ??? We need another level of rule numbering ??? >>

C++ Standard Library component summary:

* [SL.con: Containers](#ss-con)
* [SL.str: String](#ss-string)
* [SL.io: Iostream](#ss-io)
* [SL.regex: Regex](#ss-regex)
* [SL.chrono: Time](#ss-chrono)
* [SL.C: The C Standard Library](#ss-clib)

Standard-library rule summary:

* [SL.1: Use libraries wherever possible](#rsl-lib)
* [SL.2: Prefer the standard library to other libraries](#rsl-sl)
* [SL.3: Do not add non-standard entities to namespace `std`](#sl-std)
* [SL.4: Use the standard library in a type-safe manner](#sl-safe)
* ???

### <a name="rsl-lib"></a>SL.1:  Use libraries wherever possible

##### Reason

Save time. Don't re-invent the wheel.
Don't replicate the work of others.
Benefit from other people's work when they make improvements.
Help other people when you make improvements.

### <a name="rsl-sl"></a>SL.2: Prefer the standard library to other libraries

##### Reason

More people know the standard library.
It is more likely to be stable, well-maintained, and widely available than your own code or most other libraries.


### <a name="sl-std"></a>SL.3: Do not add non-standard entities to namespace `std`

##### Reason

Adding to `std` might change the meaning of otherwise standards conforming code.
Additions to `std` might clash with future versions of the standard.

##### Example

    namespace std { // BAD: violates standard

    class My_vector {
        //     . . .
    };

    }

    namespace Foo { // GOOD: user namespace is allowed

    class My_vector {
        //     . . .
    };

    }

##### Enforcement

Possible, but messy and likely to cause problems with platforms.

### <a name="sl-safe"></a>SL.4: Use the standard library in a type-safe manner

##### Reason

Because, obviously, breaking this rule can lead to undefined behavior, memory corruption, and all kinds of other bad errors.

##### Note

This is a semi-philosophical meta-rule, which needs many supporting concrete rules.
We need it as an umbrella for the more specific rules.

Summary of more specific rules:

* [SL.4: Use the standard library in a type-safe manner](#sl-safe)


## <a name="ss-con"></a>SL.con: Containers

???

Container rule summary:

* [SL.con.1: Prefer using STL `array` or `vector` instead of a C array](#rsl-arrays)
* [SL.con.2: Prefer using STL `vector` by default unless you have a reason to use a different container](#rsl-vector)
* [SL.con.3: Avoid bounds errors](#rsl-bounds)
* [SL.con.4: don't use `memset` or `memcpy` for arguments that are not trivially-copyable](#rsl-copy)

### <a name="rsl-arrays"></a>SL.con.1: Prefer using STL `array` or `vector` instead of a C array

##### Reason

C arrays are less safe, and have no advantages over `array` and `vector`.
For a fixed-length array, use `std::array`, which does not degenerate to a pointer when passed to a function and does know its size.
Also, like a built-in array, a stack-allocated `std::array` keeps its elements on the stack.
For a variable-length array, use `std::vector`, which additionally can change its size and handles memory allocation.

##### Example

    int v[SIZE];                        // BAD

    std::array<int, SIZE> w;            // ok

##### Example

    int* v = new int[initial_size];     // BAD, owning raw pointer
    delete[] v;                         // BAD, manual delete

    std::vector<int> w(initial_size);   // ok

##### Note

Use `gsl::span` for non-owning references into a container.

##### Note

Comparing the performance of a fixed-sized array allocated on the stack against a `vector` with its elements on the free store is bogus.
You could just as well compare a `std::array` on the stack against the result of a `malloc()` accessed through a pointer.
For most code, even the difference between stack allocation and free-store allocation doesn't matter, but the convenience and safety of `vector` does.
People working with code for which that difference matters are quite capable of choosing between `array` and `vector`.

##### Enforcement

* Flag declaration of a C array inside a function or class that also declares an STL container (to avoid excessive noisy warnings on legacy non-STL code). To fix: At least change the C array to a `std::array`.

### <a name="rsl-vector"></a>SL.con.2: Prefer using STL `vector` by default unless you have a reason to use a different container

##### Reason

`vector` and `array` are the only standard containers that offer the following advantages:

* the fastest general-purpose access (random access, including being vectorization-friendly);
* the fastest default access pattern (begin-to-end or end-to-begin is prefetcher-friendly);
* the lowest space overhead (contiguous layout has zero per-element overhead, which is cache-friendly).

Usually you need to add and remove elements from the container, so use `vector` by default; if you don't need to modify the container's size, use `array`.

Even when other containers seem more suited, such as `map` for O(log N) lookup performance or a `list` for efficient insertion in the middle, a `vector` will usually still perform better for containers up to a few KB in size.

##### Note

`string` should not be used as a container of individual characters. A `string` is a textual string; if you want a container of characters, use `vector</*char_type*/>` or `array</*char_type*/>` instead.

##### Exceptions

If you have a good reason to use another container, use that instead. For example:

* If `vector` suits your needs but you don't need the container to be variable size, use `array` instead.

* If you want a dictionary-style lookup container that guarantees O(K) or O(log N) lookups, the container will be larger (more than a few KB) and you perform frequent inserts so that the overhead of maintaining a sorted `vector` is infeasible, go ahead and use an `unordered_map` or `map` instead.

##### Note

To initialize a vector with a number of elements, use `()`-initialization.
To initialize a vector with a list of elements, use `{}`-initialization.

    vector<int> v1(20);  // v1 has 20 elements with the value 0 (vector<int>{})
    vector<int> v2 {20}; // v2 has 1 element with the value 20

[Prefer the {}-initializer syntax](#res-list).

##### Enforcement

* Flag a `vector` whose size never changes after construction (such as because it's `const` or because no non-`const` functions are called on it). To fix: Use an `array` instead.

### <a name="rsl-bounds"></a>SL.con.3: Avoid bounds errors

##### Reason

Read or write beyond an allocated range of elements typically leads to bad errors, wrong results, crashes, and security violations.

##### Note

The standard-library functions that apply to ranges of elements all have (or could have) bounds-safe overloads that take `span`.
Standard types such as `vector` can be modified to perform bounds-checks under the bounds profile (in a compatible way, such as by adding contracts), or used with `at()`.

Ideally, the in-bounds guarantee should be statically enforced.
For example:

* a range-`for` cannot loop beyond the range of the container to which it is applied
* a `v.begin(),v.end()` is easily determined to be bounds safe

Such loops are as fast as any unchecked/unsafe equivalent.

Often a simple pre-check can eliminate the need for checking of individual indices.
For example

* for `v.begin(),v.begin()+i` the `i` can easily be checked against `v.size()`

Such loops can be much faster than individually checked element accesses.

##### Example, bad

    void f()
    {
        array<int, 10> a, b;
        memset(a.data(), 0, 10);         // BAD, and contains a length error (length = 10 * sizeof(int))
        memcmp(a.data(), b.data(), 10);  // BAD, and contains a length error (length = 10 * sizeof(int))
    }

Also, `std::array<>::fill()` or `std::fill()` or even an empty initializer are better candidates than `memset()`.

##### Example, good

    void f()
    {
        array<int, 10> a, b, c{};       // c is initialized to zero
        a.fill(0);
        fill(b.begin(), b.end(), 0);    // std::fill()
        fill(b, 0);                     // std::ranges::fill()

        if ( a == b ) {
          // ...
        }
    }

##### Example

If code is using an unmodified standard library, then there are still workarounds that enable use of `std::array` and `std::vector` in a bounds-safe manner. Code can call the `.at()` member function on each class, which will result in an `std::out_of_range` exception being thrown. Alternatively, code can call the `at()` free function, which will result in fail-fast (or a customized action) on a bounds violation.

    void f(std::vector<int>& v, std::array<int, 12> a, int i)
    {
        v[0] = a[0];        // BAD
        v.at(0) = a[0];     // OK (alternative 1)
        at(v, 0) = a[0];    // OK (alternative 2)

        v.at(0) = a[i];     // BAD
        v.at(0) = a.at(i);  // OK (alternative 1)
        v.at(0) = at(a, i); // OK (alternative 2)
    }

##### Enforcement

* Issue a diagnostic for any call to a standard-library function that is not bounds-checked.
??? insert link to a list of banned functions

This rule is part of the [bounds profile](#ss-bounds).


### <a name="rsl-copy"></a>SL.con.4: don't use `memset` or `memcpy` for arguments that are not trivially-copyable

##### Reason

Doing so messes the semantics of the objects (e.g., by overwriting a `vptr`).

##### Note

Similarly for (w)memset, (w)memcpy, (w)memmove, and (w)memcmp

##### Example

    struct base {
        virtual void update() = 0;
    };

    struct derived : public base {
        void update() override {}
    };


    void f(derived& a, derived& b) // goodbye v-tables
    {
        memset(&a, 0, sizeof(derived));
        memcpy(&a, &b, sizeof(derived));
        memcmp(&a, &b, sizeof(derived));
    }

Instead, define proper default initialization, copy, and comparison functions

    void g(derived& a, derived& b)
    {
        a = {};    // default initialize
        b = a;     // copy
        if (a == b) do_something(a, b);
    }

##### Enforcement

* Flag the use of those functions for types that are not trivially copyable

**TODO Notes**:

* Impact on the standard library will require close coordination with WG21, if only to ensure compatibility even if never standardized.
* We are considering specifying bounds-safe overloads for stdlib (especially C stdlib) functions like `memcmp` and shipping them in the GSL.
* For existing stdlib functions and types like `vector` that are not fully bounds-checked, the goal is for these features to be bounds-checked when called from code with the bounds profile on, and unchecked when called from legacy code, possibly using contracts (concurrently being proposed by several WG21 members).



## <a name="ss-string"></a>SL.str: String

Text manipulation is a huge topic.
`std::string` doesn't cover all of it.
This section primarily tries to clarify `std::string`'s relation to `char*`, `zstring`, `string_view`, and `gsl::span<char>`.
The important issue of non-ASCII character sets and encodings (e.g., `wchar_t`, Unicode, and UTF-8) will be covered elsewhere.

**See also**: [regular expressions](#ss-regex)

Here, we use "sequence of characters" or "string" to refer to a sequence of characters meant to be read as text (somehow, eventually).
We don't consider ???

String summary:

* [SL.str.1: Use `std::string` to own character sequences](#rstr-string)
* [SL.str.2: Use `std::string_view` or `gsl::span<char>` to refer to character sequences](#rstr-view)
* [SL.str.3: Use `zstring` or `czstring` to refer to a C-style, zero-terminated, sequence of characters](#rstr-zstring)
* [SL.str.4: Use `char*` to refer to a single character](#rstr-charp)
* [SL.str.5: Use `std::byte` to refer to byte values that do not necessarily represent characters](#rstr-byte)

* [SL.str.10: Use `std::string` when you need to perform locale-sensitive string operations](#rstr-locale)
* [SL.str.11: Use `gsl::span<char>` rather than `std::string_view` when you need to mutate a string](#rstr-span)
* [SL.str.12: Use the `s` suffix for string literals meant to be standard-library `string`s](#rstr-s)

**See also**:

* [F.24 span](#rf-range)
* [F.25 zstring](#rf-zstring)


### <a name="rstr-string"></a>SL.str.1: Use `std::string` to own character sequences

##### Reason

`string` correctly handles allocation, ownership, copying, gradual expansion, and offers a variety of useful operations.

##### Example

    vector<string> read_until(const string& terminator)
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // read a word
            res.push_back(s);
        return res;
    }

Note how `>>` and `!=` are provided for `string` (as examples of useful operations) and there are no explicit
allocations, deallocations, or range checks (`string` takes care of those).

In C++17, we might use `string_view` as the argument, rather than `const string&` to allow more flexibility to callers:

    vector<string> read_until(string_view terminator)   // C++17
    {
        vector<string> res;
        for (string s; cin >> s && s != terminator; ) // read a word
            res.push_back(s);
        return res;
    }

##### Example, bad

Don't use C-style strings for operations that require non-trivial memory management

    char* cat(const char* s1, const char* s2)   // beware!
        // return s1 + '.' + s2
    {
        int l1 = strlen(s1);
        int l2 = strlen(s2);
        char* p = (char*) malloc(l1 + l2 + 2);
        strcpy(p, s1, l1);
        p[l1] = '.';
        strcpy(p + l1 + 1, s2, l2);
        p[l1 + l2 + 1] = 0;
        return p;
    }

Did we get that right?
Will the caller remember to `free()` the returned pointer?
Will this code pass a security review?

##### Note

Do not assume that `string` is slower than lower-level techniques without measurement and remember that not all code is performance critical.
[Don't optimize prematurely](#rper-knuth)

##### Enforcement

???

### <a name="rstr-view"></a>SL.str.2: Use `std::string_view` or `gsl::span<char>` to refer to character sequences

##### Reason

`std::string_view` or `gsl::span<char>` provides simple and (potentially) safe access to character sequences independently of how
those sequences are allocated and stored.

##### Example

    vector<string> read_until(string_view terminator);

    void user(zstring p, const string& s, string_view ss)
    {
        auto v1 = read_until(p);
        auto v2 = read_until(s);
        auto v3 = read_until(ss);
        // ...
    }

##### Note

`std::string_view` (C++17) is read-only.

##### Enforcement

???

### <a name="rstr-zstring"></a>SL.str.3: Use `zstring` or `czstring` to refer to a C-style, zero-terminated, sequence of characters

##### Reason

Readability.
Statement of intent.
A plain `char*` can be a pointer to a single character, a pointer to an array of characters, a pointer to a C-style (zero-terminated) string, or even to a small integer.
Distinguishing these alternatives prevents misunderstandings and bugs.

##### Example

    void f1(const char* s); // s is probably a string

All we know is that it is supposed to be the nullptr or point to at least one character

    void f1(zstring s);     // s is a C-style string or the nullptr
    void f1(czstring s);    // s is a C-style string constant or the nullptr
    void f1(std::byte* s);  // s is a pointer to a byte (C++17)

##### Note

Don't convert a C-style string to `string` unless there is a reason to.

##### Note

Like any other "plain pointer", a `zstring` should not represent ownership.

##### Note

There are billions of lines of C++ "out there", most use `char*` and `const char*` without documenting intent.
They are used in a wide variety of ways, including to represent ownership and as generic pointers to memory (instead of `void*`).
It is hard to separate these uses, so this guideline is hard to follow.
This is one of the major sources of bugs in C and C++ programs, so it is worthwhile to follow this guideline wherever feasible.

##### Enforcement

* Flag uses of `[]` on a `char*`
* Flag uses of `delete` on a `char*`
* Flag uses of `free()` on a `char*`

### <a name="rstr-charp"></a>SL.str.4: Use `char*` to refer to a single character

##### Reason

The variety of uses of `char*` in current code is a major source of errors.

##### Example, bad

    char arr[] = {'a', 'b', 'c'};

    void print(const char* p)
    {
        cout << p << '\n';
    }

    void use()
    {
        print(arr);   // run-time error; potentially very bad
    }

The array `arr` is not a C-style string because it is not zero-terminated.

##### Alternative

See [`zstring`](#rstr-zstring), [`string`](#rstr-string), and [`string_view`](#rstr-view).

##### Enforcement

* Flag uses of `[]` on a `char*`

### <a name="rstr-byte"></a>SL.str.5: Use `std::byte` to refer to byte values that do not necessarily represent characters

##### Reason

Use of `char*` to represent a pointer to something that is not necessarily a character causes confusion
and disables valuable optimizations.

##### Example

    ???

##### Note

C++17

##### Enforcement

???


### <a name="rstr-locale"></a>SL.str.10: Use `std::string` when you need to perform locale-sensitive string operations

##### Reason

`std::string` supports standard-library [`locale` facilities](#rstr-locale)

##### Example

    ???

##### Note

???

##### Enforcement

???

### <a name="rstr-span"></a>SL.str.11: Use `gsl::span<char>` rather than `std::string_view` when you need to mutate a string

##### Reason

`std::string_view` is read-only.

##### Example

???

##### Note

???

##### Enforcement

The compiler will flag attempts to write to a `string_view`.

### <a name="rstr-s"></a>SL.str.12: Use the `s` suffix for string literals meant to be standard-library `string`s

##### Reason

Direct expression of an idea minimizes mistakes.

##### Example

    auto pp1 = make_pair("Tokyo", 9.00);         // {C-style string,double} intended?
    pair<string, double> pp2 = {"Tokyo", 9.00};  // a bit verbose
    auto pp3 = make_pair("Tokyo"s, 9.00);        // {std::string,double}    // C++14
    pair pp4 = {"Tokyo"s, 9.00};                 // {std::string,double}    // C++17



##### Enforcement

???


## <a name="ss-io"></a>SL.io: Iostream

`iostream`s is a type safe, extensible, formatted and unformatted I/O library for streaming I/O.
It supports multiple (and user extensible) buffering strategies and multiple locales.
It can be used for conventional I/O, reading and writing to memory (string streams),
and user-defined extensions, such as streaming across networks (asio: not yet standardized).

Iostream rule summary:

* [SL.io.1: Use character-level input only when you have to](#rio-low)
* [SL.io.2: When reading, always consider ill-formed input](#rio-validate)
* [SL.io.3: Prefer iostreams for I/O](#rio-streams)
* [SL.io.10: Unless you use `printf`-family functions call `ios_base::sync_with_stdio(false)`](#rio-sync)
* [SL.io.50: Avoid `endl`](#rio-endl)
* [???](#???)

### <a name="rio-low"></a>SL.io.1: Use character-level input only when you have to

##### Reason

Unless you genuinely just deal with individual characters, using character-level input leads to the user code performing potentially error-prone
and potentially inefficient composition of tokens out of characters.

##### Example

    char c;
    char buf[128];
    int i = 0;
    while (cin.get(c) && !isspace(c) && i < 128)
        buf[i++] = c;
    if (i == 128) {
        // ... handle too long string ....
    }

Better (much simpler and probably faster):

    string s;
    s.reserve(128);
    cin >> s;

and the `reserve(128)` is probably not worthwhile.

##### Enforcement

???


### <a name="rio-validate"></a>SL.io.2: When reading, always consider ill-formed input

##### Reason

Errors are typically best handled as soon as possible.
If input isn't validated, every function must be written to cope with bad data (and that is not practical).

##### Example

    ???

##### Enforcement

???

### <a name="rio-streams"></a>SL.io.3: Prefer `iostream`s for I/O

##### Reason

`iostream`s are safe, flexible, and extensible.

##### Example

    // write a complex number:
    complex<double> z{ 3, 4 };
    cout << z << '\n';

`complex` is a user-defined type and its I/O is defined without modifying the `iostream` library.

##### Example

    // read a file of complex numbers:
    for (complex<double> z; cin >> z; )
        v.push_back(z);

##### Exception

??? performance ???

##### Discussion: `iostream`s vs. the `printf()` family

It is often (and often correctly) pointed out that the `printf()` family has two advantages compared to `iostream`s:
flexibility of formatting and performance.
This has to be weighed against `iostream`s advantages of extensibility to handle user-defined types, resilience against security violations,
implicit memory management, and `locale` handling.

If you need I/O performance, you can almost always do better than `printf()`.

`gets()`, `scanf()` using `%s`, and `printf()` using `%s` are security hazards (vulnerable to buffer overflow and generally error-prone).
C11 defines some "optional extensions" that do extra checking of their arguments.
If present in your C library, `gets_s()`, `scanf_s()`, and `printf_s()` might be safer alternatives, but they are still not type safe.

##### Enforcement

Optionally flag `<cstdio>` and `<stdio.h>`.

### <a name="rio-sync"></a>SL.io.10: Unless you use `printf`-family functions call `ios_base::sync_with_stdio(false)`

##### Reason

Synchronizing `iostreams` with `printf-style` I/O can be costly.
`cin` and `cout` are by default synchronized with `printf`.

##### Example

    int main()
    {
        ios_base::sync_with_stdio(false);
        // ... use iostreams ...
    }

##### Enforcement

???

### <a name="rio-endl"></a>SL.io.50: Avoid `endl`

##### Reason

The `endl` manipulator is mostly equivalent to `'\n'` and `"\n"`;
as most commonly used it simply slows down output by doing redundant `flush()`s.
This slowdown can be significant compared to `printf`-style output.

##### Example

    cout << "Hello, World!" << endl;    // two output operations and a flush
    cout << "Hello, World!\n";          // one output operation and no flush

##### Note

For `cin`/`cout` (and equivalent) interaction, there is no reason to flush; that's done automatically.
For writing to a file, there is rarely a need to `flush`.

##### Note

For string streams (specifically `ostringstream`), the insertion of an `endl` is entirely equivalent
to the insertion of a `'\n'` character, but also in this case, `endl` might be significantly slower.

`endl` does *not* take care of producing a platform specific end-of-line sequence (like `"\r\n"` on
Windows). So for a string stream, `s << endl` just inserts a *single* character, `'\n'`.

##### Note

Apart from the (occasionally important) issue of performance,
the choice between `'\n'` and `endl` is almost completely aesthetic.

## <a name="ss-regex"></a>SL.regex: Regex

`<regex>` is the standard C++ regular expression library.
It supports a variety of regular expression pattern conventions.

## <a name="ss-chrono"></a>SL.chrono: Time

`<chrono>` (defined in namespace `std::chrono`) provides the notions of `time_point` and `duration` together with functions for
outputting time in various units.
It provides clocks for registering `time_points`.

## <a name="ss-clib"></a>SL.C: The C Standard Library

???

C Standard Library rule summary:

* [SL.C.1: Don't use setjmp/longjmp](#rclib-jmp)
* [???](#???)
* [???](#???)

### <a name="rclib-jmp"></a>SL.C.1: Don't use setjmp/longjmp

##### Reason

a `longjmp` ignores destructors, thus invalidating all resource-management strategies relying on RAII

##### Enforcement

Flag all occurrences of `longjmp`and `setjmp`
