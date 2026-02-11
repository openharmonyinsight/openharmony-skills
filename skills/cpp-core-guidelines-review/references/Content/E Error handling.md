# <a name="s-errors"></a>E: Error handling

Error handling involves:

* Detecting an error
* Transmitting information about an error to some handler code
* Preserving a valid state of the program
* Avoiding resource leaks

It is not possible to recover from all errors. If recovery from an error is not possible, it is important to quickly "get out" in a well-defined way. A strategy for error handling must be simple, or it becomes a source of even worse errors.  Untested and rarely executed error-handling code is itself the source of many bugs.

The rules are designed to help avoid several kinds of errors:

* Type violations (e.g., misuse of `union`s and casts)
* Resource leaks (including memory leaks)
* Bounds errors
* Lifetime errors (e.g., accessing an object after it has been `delete`d)
* Complexity errors (logical errors made likely by overly complex expression of ideas)
* Interface errors (e.g., an unexpected value is passed through an interface)

Error-handling rule summary:

* [E.1: Develop an error-handling strategy early in a design](#re-design)
* [E.2: Throw an exception to signal that a function can't perform its assigned task](#re-throw)
* [E.3: Use exceptions for error handling only](#re-errors)
* [E.4: Design your error-handling strategy around invariants](#re-design-invariants)
* [E.5: Let a constructor establish an invariant, and throw if it cannot](#re-invariant)
* [E.6: Use RAII to prevent leaks](#re-raii)
* [E.7: State your preconditions](#re-precondition)
* [E.8: State your postconditions](#re-postcondition)

* [E.12: Use `noexcept` when exiting a function because of a `throw` is impossible or unacceptable](#re-noexcept)
* [E.13: Never throw while being the direct owner of an object](#re-never-throw)
* [E.14: Use purpose-designed user-defined types as exceptions (not built-in types)](#re-exception-types)
* [E.15: Throw by value, catch exceptions from a hierarchy by reference](#re-exception-ref)
* [E.16: Destructors, deallocation, `swap`, and exception type copy/move construction must never fail](#re-never-fail)
* [E.17: Don't try to catch every exception in every function](#re-not-always)
* [E.18: Minimize the use of explicit `try`/`catch`](#re-catch)
* [E.19: Use a `final_action` object to express cleanup if no suitable resource handle is available](#re-finally)

* [E.25: If you can't throw exceptions, simulate RAII for resource management](#re-no-throw-raii)
* [E.26: If you can't throw exceptions, consider failing fast](#re-no-throw-crash)
* [E.27: If you can't throw exceptions, use error codes systematically](#re-no-throw-codes)
* [E.28: Avoid error handling based on global state (e.g. `errno`)](#re-no-throw)

* [E.30: Don't use exception specifications](#re-specifications)
* [E.31: Properly order your `catch`-clauses](#re_catch)

### <a name="re-design"></a>E.1: Develop an error-handling strategy early in a design

##### Reason

A consistent and complete strategy for handling errors and resource leaks is hard to retrofit into a system.

### <a name="re-throw"></a>E.2: Throw an exception to signal that a function can't perform its assigned task

##### Reason

To make error handling systematic, robust, and non-repetitive.

##### Example

    struct Foo {
        vector<Thing> v;
        File_handle f;
        string s;
    };

    void use()
    {
        Foo bar { {Thing{1}, Thing{2}, Thing{monkey} }, {"my_file", "r"}, "Here we go!"};
        // ...
    }

Here, `vector` and `string`s constructors might not be able to allocate sufficient memory for their elements, `vector`s constructor might not be able to copy the `Thing`s in its initializer list, and `File_handle` might not be able to open the required file.
In each case, they throw an exception for `use()`'s caller to handle.
If `use()` could handle the failure to construct `bar` it can take control using `try`/`catch`.
In either case, `Foo`'s constructor correctly destroys constructed members before passing control to whatever tried to create a `Foo`.
Note that there is no return value that could contain an error code.

The `File_handle` constructor might be defined like this:

    File_handle::File_handle(const string& name, const string& mode)
        : f{fopen(name.c_str(), mode.c_str())}
    {
        if (!f)
            throw runtime_error{"File_handle: could not open " + name + " as " + mode};
    }

##### Note

It is often said that exceptions are meant to signal exceptional events and failures.
However, that's a bit circular because "what is exceptional?"
Examples:

* A precondition that cannot be met
* A constructor that cannot construct an object (failure to establish its class's [invariant](#rc-struct))
* An out-of-range error (e.g., `v[v.size()] = 7`)
* Inability to acquire a resource (e.g., the network is down)

In contrast, termination of an ordinary loop is not exceptional.
Unless the loop was meant to be infinite, termination is normal and expected.

##### Note

Don't use a `throw` as simply an alternative way of returning a value from a function.

##### Exception

Some systems, such as hard-real-time systems require a guarantee that an action is taken in a (typically short) constant maximum time known before execution starts. Such systems can use exceptions only if there is tool support for accurately predicting the maximum time to recover from a `throw`.

**See also**: [RAII](#re-raii)

**See also**: [discussion](#sd-noexcept)

##### Note

Before deciding that you cannot afford or don't like exception-based error handling, have a look at the [alternatives](#re-no-throw-raii);
they have their own complexities and problems.
Also, as far as possible, measure before making claims about efficiency.

### <a name="re-errors"></a>E.3: Use exceptions for error handling only

##### Reason

To keep error handling separated from "ordinary code."
C++ implementations tend to be optimized based on the assumption that exceptions are rare.

##### Example, don't

    // don't: exception not used for error handling
    int find_index(vector<string>& vec, const string& x)
    {
        try {
            for (gsl::index i = 0; i < vec.size(); ++i)
                if (vec[i] == x) throw i;  // found x
        }
        catch (int i) {
            return i;
        }
        return -1;   // not found
    }

This is more complicated and most likely runs much slower than the obvious alternative.
There is nothing exceptional about finding a value in a `vector`.

##### Enforcement

Would need to be heuristic.
Look for exception values "leaked" out of `catch` clauses.

### <a name="re-design-invariants"></a>E.4: Design your error-handling strategy around invariants

##### Reason

To use an object it must be in a valid state (defined formally or informally by an invariant) and to recover from an error every object not destroyed must be in a valid state.

##### Note

An [invariant](#rc-struct) is a logical condition for the members of an object that a constructor must establish for the public member functions to assume.

##### Enforcement

???

### <a name="re-invariant"></a>E.5: Let a constructor establish an invariant, and throw if it cannot

##### Reason

Leaving an object without its invariant established is asking for trouble.
Not all member functions can be called.

##### Example

    class Vector {  // very simplified vector of doubles
        // if elem != nullptr then elem points to sz doubles
    public:
        Vector() : elem{nullptr}, sz{0}{}
        Vector(int s) : elem{new double[s]}, sz{s} { /* initialize elements */ }
        ~Vector() { delete [] elem; }
        double& operator[](int s) { return elem[s]; }
        // ...
    private:
        owner<double*> elem;
        int sz;
    };

The class invariant - here stated as a comment - is established by the constructors.
`new` throws if it cannot allocate the required memory.
The operators, notably the subscript operator, rely on the invariant.

**See also**: [If a constructor cannot construct a valid object, throw an exception](#rc-throw)

##### Enforcement

Flag classes with `private` state without a constructor (public, protected, or private).

### <a name="re-raii"></a>E.6: Use RAII to prevent leaks

##### Reason

Leaks are typically unacceptable.
Manual resource release is error-prone.
RAII ("Resource Acquisition Is Initialization") is the simplest, most systematic way of preventing leaks.

##### Example

    void f1(int i)   // Bad: possible leak
    {
        int* p = new int[12];
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

We could carefully release the resource before the throw:

    void f2(int i)   // Clumsy and error-prone: explicit release
    {
        int* p = new int[12];
        // ...
        if (i < 17) {
            delete[] p;
            throw Bad{"in f()", i};
        }
        // ...
    }

This is verbose. In larger code with multiple possible `throw`s explicit releases become repetitive and error-prone.

    void f3(int i)   // OK: resource management done by a handle (but see below)
    {
        auto p = make_unique<int[]>(12);
        // ...
        if (i < 17) throw Bad{"in f()", i};
        // ...
    }

Note that this works even when the `throw` is implicit because it happened in a called function:

    void f4(int i)   // OK: resource management done by a handle (but see below)
    {
        auto p = make_unique<int[]>(12);
        // ...
        helper(i);   // might throw
        // ...
    }

Unless you really need pointer semantics, use a local resource object:

    void f5(int i)   // OK: resource management done by local object
    {
        vector<int> v(12);
        // ...
        helper(i);   // might throw
        // ...
    }

That's even simpler and safer, and often more efficient.

##### Note

If there is no obvious resource handle and for some reason defining a proper RAII object/handle is infeasible,
as a last resort, cleanup actions can be represented by a [`final_action`](#re-finally) object.

##### Note

But what do we do if we are writing a program where exceptions cannot be used?
First challenge that assumption; there are many anti-exceptions myths around.
We know of only a few good reasons:

* We are on a system so small that the exception support would eat up most of our 2K memory.
* We are in a hard-real-time system and we don't have tools that guarantee us that an exception is handled within the required time.
* We are in a system with tons of legacy code using lots of pointers in difficult-to-understand ways
  (in particular without a recognizable ownership strategy) so that exceptions could cause leaks.
* Our implementation of the C++ exception mechanisms is unreasonably poor
(slow, memory consuming, failing to work correctly for dynamically linked libraries, etc.).
Complain to your implementation purveyor; if no user complains, no improvement will happen.
* We get fired if we challenge our manager's ancient wisdom.

Only the first of these reasons is fundamental, so whenever possible, use exceptions to implement RAII, or design your RAII objects to never fail.
When exceptions cannot be used, simulate RAII.
That is, systematically check that objects are valid after construction and still release all resources in the destructor.
One strategy is to add a `valid()` operation to every resource handle:

    void f()
    {
        vector<string> vs(100);   // not std::vector: valid() added
        if (!vs.valid()) {
            // handle error or exit
        }

        ifstream fs("foo");   // not std::ifstream: valid() added
        if (!fs.valid()) {
            // handle error or exit
        }

        // ...
    } // destructors clean up as usual

Obviously, this increases the size of the code, doesn't allow for implicit propagation of "exceptions" (`valid()` checks), and `valid()` checks can be forgotten.
Prefer to use exceptions.

**See also**: [Use of `noexcept`](#re-noexcept)

##### Enforcement

???

### <a name="re-precondition"></a>E.7: State your preconditions

##### Reason

To avoid interface errors.

**See also**: [precondition rule](#ri-pre)

### <a name="re-postcondition"></a>E.8: State your postconditions

##### Reason

To avoid interface errors.

**See also**: [postcondition rule](#ri-post)

### <a name="re-noexcept"></a>E.12: Use `noexcept` when exiting a function because of a `throw` is impossible or unacceptable

##### Reason

To make error handling systematic, robust, and efficient.

##### Example

    double compute(double d) noexcept
    {
        return log(sqrt(d <= 0 ? 1 : d));
    }

Here, we know that `compute` will not throw because it is composed out of operations that don't throw.
By declaring `compute` to be `noexcept`, we give the compiler and human readers information that can make it easier for them to understand and manipulate `compute`.

##### Note

Many standard-library functions are `noexcept` including all the standard-library functions "inherited" from the C Standard Library.

##### Example

    vector<double> munge(const vector<double>& v) noexcept
    {
        vector<double> v2(v.size());
        // ... do something ...
    }

The `noexcept` here states that I am not willing or able to handle the situation where I cannot construct the local `vector`.
That is, I consider memory exhaustion a serious design error (on par with hardware failures) so that I'm willing to crash the program if it happens.

##### Note

Do not use traditional [exception-specifications](#re-specifications).

##### See also

[discussion](#sd-noexcept).

### <a name="re-never-throw"></a>E.13: Never throw while being the direct owner of an object

##### Reason

That would be a leak.

##### Example

    void leak(int x)   // don't: might leak
    {
        auto p = new int{7};
        if (x < 0) throw Get_me_out_of_here{};  // might leak *p
        // ...
        delete p;   // we might never get here
    }

One way of avoiding such problems is to use resource handles consistently:

    void no_leak(int x)
    {
        auto p = make_unique<int>(7);
        if (x < 0) throw Get_me_out_of_here{};  // will delete *p if necessary
        // ...
        // no need for delete p
    }

Another solution (often better) would be to use a local variable to eliminate explicit use of pointers:

    void no_leak_simplified(int x)
    {
        vector<int> v(7);
        // ...
    }

##### Note

If you have a local "thing" that requires cleanup, but is not represented by an object with a destructor, such cleanup must
also be done before a `throw`.
Sometimes, [`finally()`](#re-finally) can make such unsystematic cleanup a bit more manageable.

### <a name="re-exception-types"></a>E.14: Use purpose-designed user-defined types as exceptions (not built-in types)

##### Reason

A user-defined type can better transmit information about an error to a handler.  Information
can be encoded into the type itself and the type is unlikely to clash with other people's exceptions.

##### Example

    throw 7; // bad

    throw "something bad";  // bad

    throw std::exception{}; // bad - no info

Deriving from `std::exception` gives the flexibility to catch the specific exception or handle generally through `std::exception`:

    class MyException : public std::runtime_error
    {
    public:
        MyException(const string& msg) : std::runtime_error{msg} {}
        // ...
    };

    // ...

    throw MyException{"something bad"};  // good

Exceptions do not need to be derived from `std::exception`:

    class MyCustomError final {};  // not derived from std::exception

    // ...

    throw MyCustomError{};  // good - handlers must catch this type (or ...)

Library types derived from `std::exception` can be used as generic exceptions if
no useful information can be added at the point of detection:

    throw std::runtime_error("something bad"); // good

    // ...

    throw std::invalid_argument("i is not even"); // good

`enum` classes are also allowed:

    enum class alert {RED, YELLOW, GREEN};

    throw alert::RED; // good

##### Enforcement

Catch `throw` of built-in types and `std::exception`.

### <a name="re-exception-ref"></a>E.15: Throw by value, catch exceptions from a hierarchy by reference

##### Reason

Throwing by value (not by pointer) and catching by reference prevents copying, especially slicing base subobjects.

##### Example; bad

    void f()
    {
        try {
            // ...
            throw new widget{}; // don't: throw by value, not by raw pointer
            // ...
        }
        catch (base_class e) {  // don't: might slice
            // ...
        }
    }

Instead, use a reference:

    catch (base_class& e) { /* ... */ }

or - typically better still - a `const` reference:

    catch (const base_class& e) { /* ... */ }

Most handlers do not modify their exception and in general we [recommend use of `const`](#res-const).

##### Note

Catch by value can be appropriate for a small value type such as an `enum` value.

##### Note

To rethrow a caught exception use `throw;` not `throw e;`. Using `throw e;` would throw a new copy of `e` (sliced to the static type `std::exception`, when the exception is caught by `catch (const std::exception& e)`) instead of rethrowing the original exception of type `std::runtime_error`. (But keep [Don't try to catch every exception in every function](#re-not-always) and [Minimize the use of explicit `try`/`catch`](#re-catch) in mind.)

##### Enforcement

* Flag catching by value of a type that has a virtual function.
* Flag throwing raw pointers.

### <a name="re-never-fail"></a>E.16: Destructors, deallocation, `swap`, and exception type copy/move construction must never fail

##### Reason

We don't know how to write reliable programs if a destructor, a swap, a memory deallocation, or attempting to copy/move-construct an exception object fails; that is, if it exits by an exception or simply doesn't perform its required action.

##### Example, don't

    class Connection {
        // ...
    public:
        ~Connection()   // Don't: very bad destructor
        {
            if (cannot_disconnect()) throw I_give_up{information};
            // ...
        }
    };

##### Note

Many have tried to write reliable code violating this rule for examples, such as a network connection that "refuses to close".
To the best of our knowledge nobody has found a general way of doing this.
Occasionally, for very specific examples, you can get away with setting some state for future cleanup.
For example, we might put a socket that does not want to close on a "bad socket" list,
to be examined by a regular sweep of the system state.
Every example we have seen of this is error-prone, specialized, and often buggy.

##### Note

The standard library assumes that destructors, deallocation functions (e.g., `operator delete`), and `swap` do not throw. If they do, basic standard-library invariants are broken.

##### Note

* Deallocation functions, including `operator delete`, must be `noexcept`.
* `swap` functions must be `noexcept`.
* Most destructors are implicitly `noexcept` by default.
* Also, [make move operations `noexcept`](#rc-move-noexcept).
* If writing a type intended to be used as an exception type, ensure its copy constructor is `noexcept`. In general we cannot mechanically enforce this, because we do not know whether a type is intended to be used as an exception type.
* Try not to `throw` a type whose copy constructor is not `noexcept`. In general we cannot mechanically enforce this, because even `throw std::string(...)` could throw but does not in practice.

##### Enforcement

* Catch destructors, deallocation operations, and `swap`s that `throw`.
* Catch such operations that are not `noexcept`.

**See also**: [discussion](#sd-never-fail)

### <a name="re-not-always"></a>E.17: Don't try to catch every exception in every function

##### Reason

Catching an exception in a function that cannot take a meaningful recovery action leads to complexity and waste.
Let an exception propagate until it reaches a function that can handle it.
Let cleanup actions on the unwinding path be handled by [RAII](#re-raii).

##### Example, don't

    void f()   // bad
    {
        try {
            // ...
        }
        catch (...) {
            // no action
            throw;   // propagate exception
        }
    }

##### Enforcement

* Flag nested try-blocks.
* Flag source code files with a too high ratio of try-blocks to functions. (??? Problem: define "too high")

### <a name="re-catch"></a>E.18: Minimize the use of explicit `try`/`catch`

##### Reason

 `try`/`catch` is verbose and non-trivial uses are error-prone.
 `try`/`catch` can be a sign of unsystematic and/or low-level resource management or error handling.

##### Example, Bad

    void f(zstring s)
    {
        Gadget* p;
        try {
            p = new Gadget(s);
            // ...
            delete p;
        }
        catch (Gadget_construction_failure) {
            delete p;
            throw;
        }
    }

This code is messy.
There could be a leak from the naked pointer in the `try` block.
Not all exceptions are handled.
`deleting` an object that failed to construct is almost certainly a mistake.
Better:

    void f2(zstring s)
    {
        Gadget g {s};
    }

##### Alternatives

* proper resource handles and [RAII](#re-raii)
* [`finally`](#re-finally)

##### Enforcement

??? hard, needs a heuristic

### <a name="re-finally"></a>E.19: Use a `final_action` object to express cleanup if no suitable resource handle is available

##### Reason

`finally` from the [GSL](#gsl-guidelines-support-library) is less verbose and harder to get wrong than `try`/`catch`.

##### Example

    void f(int n)
    {
        void* p = malloc(n);
        auto _ = gsl::finally([p] { free(p); });
        // ...
    }

##### Note

`finally` is not as messy as `try`/`catch`, but it is still ad-hoc.
Prefer [proper resource management objects](#re-raii).
Consider `finally` a last resort.

##### Note

Use of `finally` is a systematic and reasonably clean alternative to the old [`goto exit;` technique](#re-no-throw-codes)
for dealing with cleanup where resource management is not systematic.

##### Enforcement

Heuristic: Detect `goto exit;`

### <a name="re-no-throw-raii"></a>E.25: If you can't throw exceptions, simulate RAII for resource management

##### Reason

Even without exceptions, [RAII](#re-raii) is usually the best and most systematic way of dealing with resources.

##### Note

Error handling using exceptions is the only complete and systematic way of handling non-local errors in C++.
In particular, non-intrusively signaling failure to construct an object requires an exception.
Signaling errors in a way that cannot be ignored requires exceptions.
If you can't use exceptions, simulate their use as best you can.

A lot of fear of exceptions is misguided.
When used for exceptional circumstances in code that is not littered with pointers and complicated control structures,
exception handling is almost always affordable (in time and space) and almost always leads to better code.
This, of course, assumes a good implementation of the exception handling mechanisms, which is not available on all systems.
There are also cases where the problems above do not apply, but exceptions cannot be used for other reasons.
Some hard-real-time systems are an example: An operation has to be completed within a fixed time with an error or a correct answer.
In the absence of appropriate time estimation tools, this is hard to guarantee for exceptions.
Such systems (e.g. flight control software) typically also ban the use of dynamic (heap) memory.

So, the primary guideline for error handling is "use exceptions and [RAII](#re-raii)."
This section deals with the cases where you either do not have an efficient implementation of exceptions,
or have such a rat's nest of old-style code
(e.g., lots of pointers, ill-defined ownership, and lots of unsystematic error handling based on tests of error codes)
that it is infeasible to introduce simple and systematic exception handling.

Before condemning exceptions or complaining too much about their cost, consider examples of the use of [error codes](#re-no-throw-codes).
Consider the cost and complexity of the use of error codes.
If performance is your worry, measure.

##### Example

Assume you wanted to write

    void func(zstring arg)
    {
        Gadget g {arg};
        // ...
    }

If the `gadget` isn't correctly constructed, `func` exits with an exception.
If we cannot throw an exception, we can simulate this RAII style of resource handling by adding a `valid()` member function to `Gadget`:

    error_indicator func(zstring arg)
    {
        Gadget g {arg};
        if (!g.valid()) return gadget_construction_error;
        // ...
        return 0;   // zero indicates "good"
    }

The problem is of course that the caller now has to remember to test the return value. To encourage doing so, consider adding a `[[nodiscard]]`.

**See also**: [Discussion](#sd-???)

##### Enforcement

Possible (only) for specific versions of this idea: e.g., test for systematic test of `valid()` after resource handle construction

### <a name="re-no-throw-crash"></a>E.26: If you can't throw exceptions, consider failing fast

##### Reason

If you can't do a good job at recovering, at least you can get out before too much consequential damage is done.

**See also**: [Simulating RAII](#re-no-throw-raii)

##### Note

If you cannot be systematic about error handling, consider "crashing" as a response to any error that cannot be handled locally.
That is, if you cannot recover from an error in the context of the function that detected it, call `abort()`, `quick_exit()`,
or a similar function that will trigger some sort of system restart.

In systems where you have lots of processes and/or lots of computers, you need to expect and handle fatal crashes anyway,
say from hardware failures.
In such cases, "crashing" is simply leaving error handling to the next level of the system.

##### Example

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) abort();     // abort if memory is exhausted
        // ...
    }

Most programs cannot handle memory exhaustion gracefully anyway. This is roughly equivalent to

    void f(int n)
    {
        // ...
        p = new X[n];    // throw if memory is exhausted (by default, terminate)
        // ...
    }

Typically, it is a good idea to log the reason for the "crash" before exiting.

##### Enforcement

Awkward

### <a name="re-no-throw-codes"></a>E.27: If you can't throw exceptions, use error codes systematically

##### Reason

Systematic use of any error-handling strategy minimizes the chance of forgetting to handle an error.

**See also**: [Simulating RAII](#re-no-throw-raii)

##### Note

There are several issues to be addressed:

* How do you transmit an error indicator from out of a function?
* How do you release all resources from a function before doing an error exit?
* What do you use as an error indicator?

In general, returning an error indicator implies returning two values: The result and an error indicator.
The error indicator can be part of the object, e.g. an object can have a `valid()` indicator
or a pair of values can be returned.

##### Example

    Gadget make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        Gadget g = make_gadget(17);
        if (!g.valid()) {
                // error handling
        }
        // ...
    }

This approach fits with [simulated RAII resource management](#re-no-throw-raii).
The `valid()` function could return an `error_indicator` (e.g. a member of an `error_indicator` enumeration).

##### Example

What if we cannot or do not want to modify the `Gadget` type?
In that case, we must return a pair of values.
For example:

    std::pair<Gadget, error_indicator> make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.second) {
                // error handling
        }
        Gadget& g = r.first;
        // ...
    }

As shown, `std::pair` is a possible return type.
Some people prefer a specific type.
For example:

    Gval make_gadget(int n)
    {
        // ...
    }

    void user()
    {
        auto r = make_gadget(17);
        if (!r.err) {
                // error handling
        }
        Gadget& g = r.val;
        // ...
    }

One reason to prefer a specific return type is to have names for its members, rather than the somewhat cryptic `first` and `second`
and to avoid confusion with other uses of `std::pair`.

##### Example

In general, you must clean up before an error exit.
This can be messy:

    std::pair<int, error_indicator> user()
    {
        Gadget g1 = make_gadget(17);
        if (!g1.valid()) {
            return {0, g1_error};
        }

        Gadget g2 = make_gadget(31);
        if (!g2.valid()) {
            cleanup(g1);
            return {0, g2_error};
        }

        // ...

        if (all_foobar(g1, g2)) {
            cleanup(g2);
            cleanup(g1);
            return {0, foobar_error};
        }

        // ...

        cleanup(g2);
        cleanup(g1);
        return {res, 0};
    }

Simulating RAII can be non-trivial, especially in functions with multiple resources and multiple possible errors.
A not uncommon technique is to gather cleanup at the end of the function to avoid repetition (note that the extra scope around `g2` is undesirable but necessary to make the `goto` version compile):

    std::pair<int, error_indicator> user()
    {
        error_indicator err = 0;
        int res = 0;

        Gadget g1 = make_gadget(17);
        if (!g1.valid()) {
            err = g1_error;
            goto g1_exit;
        }

        {
            Gadget g2 = make_gadget(31);
            if (!g2.valid()) {
                err = g2_error;
                goto g2_exit;
            }

            if (all_foobar(g1, g2)) {
                err = foobar_error;
                goto g2_exit;
            }

            // ...

        g2_exit:
            if (g2.valid()) cleanup(g2);
        }

    g1_exit:
        if (g1.valid()) cleanup(g1);
        return {res, err};
    }

The larger the function, the more tempting this technique becomes.
`finally` can [ease the pain a bit](#re-finally).
Also, the larger the program becomes the harder it is to apply an error-indicator-based error-handling strategy systematically.

We [prefer exception-based error handling](#re-throw) and recommend [keeping functions short](#rf-single).

**See also**: [Discussion](#sd-???)

**See also**: [Returning multiple values](#rf-out-multi)

##### Enforcement

Awkward.

### <a name="re-no-throw"></a>E.28: Avoid error handling based on global state (e.g. `errno`)

##### Reason

Global state is hard to manage and it is easy to forget to check it.
When did you last test the return value of `printf()`?

**See also**: [Simulating RAII](#re-no-throw-raii)

##### Example, bad

    int last_err;

    void f(int n)
    {
        // ...
        p = static_cast<X*>(malloc(n * sizeof(X)));
        if (!p) last_err = -1;     // error if memory is exhausted
        // ...
    }

##### Note

C-style error handling is based on the global variable `errno`, so it is essentially impossible to avoid this style completely.

##### Enforcement

Awkward.


### <a name="re-specifications"></a>E.30: Don't use exception specifications

##### Reason

Exception specifications make error handling brittle, impose a run-time cost, and have been removed from the C++ standard.

##### Example

    int use(int arg)
        throw(X, Y)
    {
        // ...
        auto x = f(arg);
        // ...
    }

If `f()` throws an exception different from `X` and `Y` the unexpected handler is invoked, which by default terminates.
That's OK, but say that we have checked that this cannot happen and `f` is changed to throw a new exception `Z`,
we now have a crash on our hands unless we change `use()` (and re-test everything).
The snag is that `f()` might be in a library we do not control and the new exception is not anything that `use()` can do
anything about or is in any way interested in.
We can change `use()` to pass `Z` through, but now `use()`'s callers probably need to be modified.
This quickly becomes unmanageable.
Alternatively, we can add a `try`-`catch` to `use()` to map `Z` into an acceptable exception.
This, too, quickly becomes unmanageable.
Note that changes to the set of exceptions often happen at the lowest level of a system
(e.g., because of changes to a network library or some middleware), so changes "bubble up" through long call chains.
In a large code base, this could mean that nobody could update to a new version of a library until the last user was modified.
If `use()` is part of a library, it might not be possible to update it because a change could affect unknown clients.

The policy of letting exceptions propagate until they reach a function that potentially can handle it has proven itself over the years.

##### Note

No. This would not be any better had exception specifications been statically enforced.
For example, see [Stroustrup94](#Stroustrup94).

##### Note

If no exception can be thrown, use [`noexcept`](#re-noexcept).

##### Enforcement

Flag every exception specification.

### <a name="re_catch"></a>E.31: Properly order your `catch`-clauses

##### Reason

`catch`-clauses are evaluated in the order they appear and one clause can hide another.

##### Example, bad

    void f()
    {
        // ...
        try {
                // ...
        }
        catch (Base& b) { /* ... */ }
        catch (Derived& d) { /* ... */ }
        catch (...) { /* ... */ }
        catch (std::exception& e) { /* ... */ }
    }

If `Derived`is derived from `Base` the `Derived`-handler will never be invoked.
The "catch everything" handler ensured that the `std::exception`-handler will never be invoked.

##### Enforcement

Flag all "hiding handlers".
