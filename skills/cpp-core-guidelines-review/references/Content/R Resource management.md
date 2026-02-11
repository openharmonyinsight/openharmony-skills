# <a name="s-resource"></a>R: Resource management

This section contains rules related to resources.
A resource is anything that must be acquired and (explicitly or implicitly) released, such as memory, file handles, sockets, and locks.
The reason it must be released is typically that it can be in short supply, so even delayed release might do harm.
The fundamental aim is to ensure that we don't leak any resources and that we don't hold a resource longer than we need to.
An entity that is responsible for releasing a resource is called an owner.

There are a few cases where leaks can be acceptable or even optimal:
If you are writing a program that simply produces an output based on an input and the amount of memory needed is proportional to the size of the input, the optimal strategy (for performance and ease of programming) is sometimes simply never to delete anything.
If you have enough memory to handle your largest input, leak away, but be sure to give a good error message if you are wrong.
Here, we ignore such cases.

* Resource management rule summary:

  * [R.1: Manage resources automatically using resource handles and RAII (Resource Acquisition Is Initialization)](#rr-raii)
  * [R.2: In interfaces, use raw pointers to denote individual objects (only)](#rr-use-ptr)
  * [R.3: A raw pointer (a `T*`) is non-owning](#rr-ptr)
  * [R.4: A raw reference (a `T&`) is non-owning](#rr-ref)
  * [R.5: Prefer scoped objects, don't heap-allocate unnecessarily](#rr-scoped)
  * [R.6: Avoid non-`const` global variables](#rr-global)

* Allocation and deallocation rule summary:

  * [R.10: Avoid `malloc()` and `free()`](#rr-mallocfree)
  * [R.11: Avoid calling `new` and `delete` explicitly](#rr-newdelete)
  * [R.12: Immediately give the result of an explicit resource allocation to a manager object](#rr-immediate-alloc)
  * [R.13: Perform at most one explicit resource allocation in a single expression statement](#rr-single-alloc)
  * [R.14: Avoid `[]` parameters, prefer `span`](#rr-ap)
  * [R.15: Always overload matched allocation/deallocation pairs](#rr-pair)

* <a name="rr-summary-smartptrs"></a>Smart pointer rule summary:

  * [R.20: Use `unique_ptr` or `shared_ptr` to represent ownership](#rr-owner)
  * [R.21: Prefer `unique_ptr` over `shared_ptr` unless you need to share ownership](#rr-unique)
  * [R.22: Use `make_shared()` to make `shared_ptr`s](#rr-make_shared)
  * [R.23: Use `make_unique()` to make `unique_ptr`s](#rr-make_unique)
  * [R.24: Use `std::weak_ptr` to break cycles of `shared_ptr`s](#rr-weak_ptr)
  * [R.30: Take smart pointers as parameters only to explicitly express lifetime semantics](#rr-smartptrparam)
  * [R.31: If you have non-`std` smart pointers, follow the basic pattern from `std`](#rr-smart)
  * [R.32: Take a `unique_ptr<widget>` parameter to express that a function assumes ownership of a `widget`](#rr-uniqueptrparam)
  * [R.33: Take a `unique_ptr<widget>&` parameter to express that a function reseats the `widget`](#rr-reseat)
  * [R.34: Take a `shared_ptr<widget>` parameter to express shared ownership](#rr-sharedptrparam-owner)
  * [R.35: Take a `shared_ptr<widget>&` parameter to express that a function might reseat the shared pointer](#rr-sharedptrparam)
  * [R.36: Take a `const shared_ptr<widget>&` parameter to express that it might retain a reference count to the object ???](#rr-sharedptrparam-const)
  * [R.37: Do not pass a pointer or reference obtained from an aliased smart pointer](#rr-smartptrget)

### <a name="rr-raii"></a>R.1: Manage resources automatically using resource handles and RAII (Resource Acquisition Is Initialization)

##### Reason

To avoid leaks and the complexity of manual resource management.
C++'s language-enforced constructor/destructor symmetry mirrors the symmetry inherent in resource acquire/release function pairs such as `fopen`/`fclose`, `lock`/`unlock`, and `new`/`delete`.
Whenever you deal with a resource that needs paired acquire/release function calls, encapsulate that resource in an object that enforces pairing for you -- acquire the resource in its constructor, and release it in its destructor.

##### Example, bad

Consider:

    void send(X* x, string_view destination)
    {
        auto port = open_port(destination);
        my_mutex.lock();
        // ...
        send(port, x);
        // ...
        my_mutex.unlock();
        close_port(port);
        delete x;
    }

In this code, you have to remember to `unlock`, `close_port`, and `delete` on all paths, and do each exactly once.
Further, if any of the code marked `...` throws an exception, then `x` is leaked and `my_mutex` remains locked.

##### Example

Consider:

    void send(unique_ptr<X> x, string_view destination)  // x owns the X
    {
        Port port{destination};            // port owns the PortHandle
        lock_guard<mutex> guard{my_mutex}; // guard owns the lock
        // ...
        send(port, x);
        // ...
    } // automatically unlocks my_mutex and deletes the pointer in x

Now all resource cleanup is automatic, performed once on all paths whether or not there is an exception. As a bonus, the function now advertises that it takes over ownership of the pointer.

What is `Port`? A handy wrapper that encapsulates the resource:

    class Port {
        PortHandle port;
    public:
        Port(string_view destination) : port{open_port(destination)} { }
        ~Port() { close_port(port); }
        operator PortHandle() { return port; }

        // port handles can't usually be cloned, so disable copying and assignment if necessary
        Port(const Port&) = delete;
        Port& operator=(const Port&) = delete;
    };

##### Note

Where a resource is "ill-behaved" in that it isn't represented as a class with a destructor, wrap it in a class or use [`finally`](#re-finally)

**See also**: [RAII](#re-raii)

### <a name="rr-use-ptr"></a>R.2: In interfaces, use raw pointers to denote individual objects (only)

##### Reason

Arrays are best represented by a container type (e.g., `vector` (owning)) or a `span` (non-owning).
Such containers and views hold sufficient information to do range checking.

##### Example, bad

    void f(int* p, int n)   // n is the number of elements in p[]
    {
        // ...
        p[2] = 7;   // bad: subscript raw pointer
        // ...
    }

The compiler does not read comments, and without reading other code you do not know whether `p` really points to `n` elements.
Use a `span` instead.

##### Example

    void g(int* p, int fmt)   // print *p using format #fmt
    {
        // ... uses *p and p[0] only ...
    }

##### Exception

C-style strings are passed as single pointers to a zero-terminated sequence of characters.
Use `zstring` rather than `char*` to indicate that you rely on that convention.

##### Note

Many current uses of pointers to a single element could be references.
However, where `nullptr` is a possible value, a reference might not be a reasonable alternative.

##### Enforcement

* Flag pointer arithmetic (including `++`) on a pointer that is not part of a container, view, or iterator.
  This rule would generate a huge number of false positives if applied to an older code base.
* Flag array names passed as simple pointers

### <a name="rr-ptr"></a>R.3: A raw pointer (a `T*`) is non-owning

##### Reason

There is nothing (in the C++ standard or in most code) to say otherwise and most raw pointers are non-owning.
We want owning pointers identified so that we can reliably and efficiently delete the objects pointed to by owning pointers.

##### Example

    void f()
    {
        int* p1 = new int{7};           // bad: raw owning pointer
        auto p2 = make_unique<int>(7);  // OK: the int is owned by a unique pointer
        // ...
    }

The `unique_ptr` protects against leaks by guaranteeing the deletion of its object (even in the presence of exceptions). The `T*` does not.

##### Example

    template<typename T>
    class X {
    public:
        T* p;   // bad: it is unclear whether p is owning or not
        T* q;   // bad: it is unclear whether q is owning or not
        // ...
    };

We can fix that problem by making ownership explicit:

    template<typename T>
    class X2 {
    public:
        owner<T*> p;  // OK: p is owning
        T* q;         // OK: q is not owning
        // ...
    };

##### Exception

A major class of exception is legacy code, especially code that must remain compilable as C or interface with C and C-style C++ through ABIs.
The fact that there are billions of lines of code that violate this rule against owning `T*`s cannot be ignored.
We'd love to see program transformation tools turning 20-year-old "legacy" code into shiny modern code,
we encourage the development, deployment and use of such tools,
we hope the guidelines will help the development of such tools,
and we even contributed (and contribute) to the research and development in this area.
However, it will take time: "legacy code" is generated faster than we can renovate old code, and so it will be for a few years.

This code cannot all be rewritten (even assuming good code transformation software), especially not soon.
This problem cannot be solved (at scale) by transforming all owning pointers to `unique_ptr`s and `shared_ptr`s,
partly because we need/use owning "raw pointers" as well as simple pointers in the implementation of our fundamental resource handles.
For example, common `vector` implementations have one owning pointer and two non-owning pointers.
Many ABIs (and essentially all interfaces to C code) use `T*`s, some of them owning.
Some interfaces cannot be simply annotated with `owner` because they need to remain compilable as C
(although this would be a rare good use for a macro, that expands to `owner` in C++ mode only).

##### Note

`owner<T*>` has no default semantics beyond `T*`. It can be used without changing any code using it and without affecting ABIs.
It is simply an indicator to programmers and analysis tools.
For example, if an `owner<T*>` is a member of a class, that class better have a destructor that `delete`s it.

##### Example, bad

Returning a (raw) pointer imposes a lifetime management uncertainty on the caller; that is, who deletes the pointed-to object?

    Gadget* make_gadget(int n)
    {
        auto p = new Gadget{n};
        // ...
        return p;
    }

    void caller(int n)
    {
        auto p = make_gadget(n);   // remember to delete p
        // ...
        delete p;
    }

In addition to suffering from the problem of [leak](#rp-leak), this adds a spurious allocation and deallocation operation, and is needlessly verbose. If Gadget is cheap to move out of a function (i.e., is small or has an efficient move operation), just return it "by value" (see ["out" return values](#rf-out)):

    Gadget make_gadget(int n)
    {
        Gadget g{n};
        // ...
        return g;
    }

##### Note

This rule applies to factory functions.

##### Note

If pointer semantics are required (e.g., because the return type needs to refer to a base class of a class hierarchy (an interface)), return a "smart pointer."

##### Enforcement

* (Simple) Warn on `delete` of a raw pointer that is not an `owner<T>`.
* (Moderate) Warn on failure to either `reset` or explicitly `delete` an `owner<T>` pointer on every code path.
* (Simple) Warn if the return value of `new` is assigned to a raw pointer.
* (Simple) Warn if a function returns an object that was allocated within the function but has a move constructor.
  Suggest considering returning it by value instead.

### <a name="rr-ref"></a>R.4: A raw reference (a `T&`) is non-owning

##### Reason

There is nothing (in the C++ standard or in most code) to say otherwise and most raw references are non-owning.
We want owners identified so that we can reliably and efficiently delete the objects pointed to by owning pointers.

##### Example

    void f()
    {
        int& r = *new int{7};  // bad: raw owning reference
        // ...
        delete &r;             // bad: violated the rule against deleting raw pointers
    }

**See also**: [The raw pointer rule](#rr-ptr)

##### Enforcement

See [the raw pointer rule](#rr-ptr)

### <a name="rr-scoped"></a>R.5: Prefer scoped objects, don't heap-allocate unnecessarily

##### Reason

A scoped object is a local object, a global object, or a member.
This implies that there is no separate allocation and deallocation cost in excess of that already used for the containing scope or object.
The members of a scoped object are themselves scoped and the scoped object's constructor and destructor manage the members' lifetimes.

##### Example

The following example is inefficient (because it has unnecessary allocation and deallocation), vulnerable to exception throws and returns in the `...` part (leading to leaks), and verbose:

    void f(int n)
    {
        auto p = new Gadget{n};
        // ...
        delete p;
    }

Instead, use a local variable:

    void f(int n)
    {
        Gadget g{n};
        // ...
    }

##### Enforcement

* (Moderate) Warn if an object is allocated and then deallocated on all paths within a function. Suggest it should be a local stack object instead.
* (Simple) Warn if a local `Unique_pointer` or `Shared_pointer` that is not moved, copied, reassigned or `reset` before its lifetime ends is not declared `const`.
Exception: Do not produce such a warning on a local `Unique_pointer` to an unbounded array. (See below.)

##### Exception

If your stack space is limited, it is OK to create a local `const unique_ptr<BigObject>` to store the object on the heap instead of the stack.

### <a name="rr-global"></a>R.6: Avoid non-`const` global variables

See [I.2](#ri-global)

## <a name="ss-alloc"></a>R.alloc: Allocation and deallocation

### <a name="rr-mallocfree"></a>R.10: Avoid `malloc()` and `free()`

##### Reason

 `malloc()` and `free()` do not support construction and destruction, and do not mix well with `new` and `delete`.

##### Example

    class Record {
        int id;
        string name;
        // ...
    };

    void use()
    {
        // p1 might be nullptr
        // *p1 is not initialized; in particular,
        // that string isn't a string, but a string-sized bag of bits
        Record* p1 = static_cast<Record*>(malloc(sizeof(Record)));

        auto p2 = new Record;

        // unless an exception is thrown, *p2 is default initialized
        auto p3 = new(nothrow) Record;
        // p3 might be nullptr; if not, *p3 is default initialized

        // ...

        delete p1;    // error: cannot delete object allocated by malloc()
        free(p2);    // error: cannot free() object allocated by new
    }

In some implementations that `delete` and that `free()` might work, or maybe they will cause run-time errors.

##### Exception

There are applications and sections of code where exceptions are not acceptable.
Some of the best such examples are in life-critical hard-real-time code.
Beware that many bans on exception use are based on superstition (bad)
or by concerns for older code bases with unsystematic resource management (unfortunately, but sometimes necessary).
In such cases, consider the `nothrow` versions of `new`.

##### Enforcement

Flag explicit use of `malloc` and `free`.

### <a name="rr-newdelete"></a>R.11: Avoid calling `new` and `delete` explicitly

##### Reason

The pointer returned by `new` should belong to a resource handle (that can call `delete`).
If the pointer returned by `new` is assigned to a plain/naked pointer, the object can be leaked.

##### Note

In a large program, a naked `delete` (that is a `delete` in application code, rather than part of code devoted to resource management)
is a likely bug: if you have N `delete`s, how can you be certain that you don't need N+1 or N-1?
The bug might be latent: it might emerge only during maintenance.
If you have a naked `new`, you probably need a naked `delete` somewhere, so you probably have a bug.

##### Enforcement

(Simple) Warn on any explicit use of `new` and `delete`. Suggest using `make_unique` instead.

### <a name="rr-immediate-alloc"></a>R.12: Immediately give the result of an explicit resource allocation to a manager object

##### Reason

If you don't, an exception or a return might lead to a leak.

##### Example, bad

    void func(const string& name)
    {
        FILE* f = fopen(name, "r");            // open the file
        vector<char> buf(1024);
        auto _ = finally([f] { fclose(f); });  // remember to close the file
        // ...
    }

The allocation of `buf` might fail and leak the file handle.

##### Example

    void func(const string& name)
    {
        ifstream f{name};   // open the file
        vector<char> buf(1024);
        // ...
    }

The use of the file handle (in `ifstream`) is simple, efficient, and safe.

##### Enforcement

* Flag explicit allocations used to initialize pointers (problem: how many direct resource allocations can we recognize?)

### <a name="rr-single-alloc"></a>R.13: Perform at most one explicit resource allocation in a single expression statement

##### Reason

If you perform two explicit resource allocations in one statement, you could leak resources because the order of evaluation of many subexpressions, including function arguments, is unspecified.

##### Example

    void fun(shared_ptr<Widget> sp1, shared_ptr<Widget> sp2);

This `fun` can be called like this:

    // BAD: potential leak
    fun(shared_ptr<Widget>(new Widget(a, b)), shared_ptr<Widget>(new Widget(c, d)));

This is exception-unsafe because the compiler might reorder the two expressions building the function's two arguments.
In particular, the compiler can interleave execution of the two expressions:
Memory allocation (by calling `operator new`) could be done first for both objects, followed by attempts to call the two `Widget` constructors.
If one of the constructor calls throws an exception, then the other object's memory will never be released!

This subtle problem has a simple solution: Never perform more than one explicit resource allocation in a single expression statement.
For example:

    shared_ptr<Widget> sp1(new Widget(a, b)); // Better, but messy
    fun(sp1, new Widget(c, d));

The best solution is to avoid explicit allocation entirely, use factory functions that return owning objects:

    fun(make_shared<Widget>(a, b), make_shared<Widget>(c, d)); // Best

Write your own factory wrapper if there is not one already.

##### Enforcement

* Flag expressions with multiple explicit resource allocations (problem: how many direct resource allocations can we recognize?)

### <a name="rr-ap"></a>R.14: Avoid `[]` parameters, prefer `span`

##### Reason

An array decays to a pointer, thereby losing its size, opening the opportunity for range errors.
Use `span` to preserve size information.

##### Example

    void f(int[]);          // not recommended

    void f(int*);           // not recommended for multiple objects
                            // (a pointer should point to a single object, do not subscript)

    void f(gsl::span<int>); // good, recommended

##### Enforcement

Flag `[]` parameters. Use `span` instead.

### <a name="rr-pair"></a>R.15: Always overload matched allocation/deallocation pairs

##### Reason

Otherwise you get mismatched operations and chaos.

##### Example

    class X {
        // ...
        void* operator new(size_t s);
        void operator delete(void*);
        // ...
    };

##### Note

If you want memory that cannot be deallocated, `=delete` the deallocation operation.
Don't leave it undeclared.

##### Enforcement

Flag incomplete pairs.

## <a name="ss-smart"></a>R.smart: Smart pointers

### <a name="rr-owner"></a>R.20: Use `unique_ptr` or `shared_ptr` to represent ownership

##### Reason

They can prevent resource leaks.

##### Example

Consider:

    void f()
    {
        X* p1 { new X };              // bad, p1 will leak
        auto p2 = make_unique<X>();   // good, unique ownership
        auto p3 = make_shared<X>();   // good, shared ownership
    }

This will leak the object used to initialize `p1` (only).

##### Enforcement

* (Simple) Warn if the return value of `new` is assigned to a raw pointer.
* (Simple) Warn if the result of a function returning a raw owning pointer is assigned to a raw pointer.

### <a name="rr-unique"></a>R.21: Prefer `unique_ptr` over `shared_ptr` unless you need to share ownership

##### Reason

A `unique_ptr` is conceptually simpler and more predictable (you know when destruction happens) and faster (you don't implicitly maintain a use count).

##### Example, bad

This needlessly adds and maintains a reference count.

    void f()
    {
        shared_ptr<Base> base = make_shared<Derived>();
        // use base locally, without copying it -- refcount never exceeds 1
    } // destroy base

##### Example

This is more efficient:

    void f()
    {
        unique_ptr<Base> base = make_unique<Derived>();
        // use base locally
    } // destroy base

##### Enforcement

(Simple) Warn if a function uses a `Shared_pointer` with an object allocated within the function, but never returns the `Shared_pointer` or passes it to a function requiring a `Shared_pointer`. Suggest using `unique_ptr` instead.

### <a name="rr-make_shared"></a>R.22: Use `make_shared()` to make `shared_ptr`s

##### Reason

`make_shared` gives a more concise statement of the construction.
It also gives an opportunity to eliminate a separate allocation for the reference counts, by placing the `shared_ptr`'s use counts next to its object.
It also ensures exception safety in complex expressions (in pre-C++17 code).

##### Example

Consider:

    shared_ptr<X> p1 { new X{2} }; // bad
    auto p = make_shared<X>(2);    // good

The `make_shared()` version mentions `X` only once, so it is usually shorter (as well as faster) than the version with the explicit `new`.

##### Enforcement

(Simple) Warn if a `shared_ptr` is constructed from the result of `new` rather than `make_shared`.

### <a name="rr-make_unique"></a>R.23: Use `make_unique()` to make `unique_ptr`s

##### Reason

`make_unique` gives a more concise statement of the construction.
It also ensures exception safety in complex expressions (in pre-C++17 code).

##### Example

    unique_ptr<Foo> p {new Foo{7}};    // OK: but repetitive

    auto q = make_unique<Foo>(7);      // Better: no repetition of Foo

##### Enforcement

(Simple) Warn if a `unique_ptr` is constructed from the result of `new` rather than `make_unique`.

### <a name="rr-weak_ptr"></a>R.24: Use `std::weak_ptr` to break cycles of `shared_ptr`s

##### Reason

 `shared_ptr`s rely on use counting and the use count for a cyclic structure never goes to zero, so we need a mechanism to
be able to destroy a cyclic structure.

##### Example

    #include <memory>

    class bar;

    class foo {
    public:
      explicit foo(const std::shared_ptr<bar>& forward_reference)
        : forward_reference_(forward_reference)
      { }
    private:
      std::shared_ptr<bar> forward_reference_;
    };

    class bar {
    public:
      explicit bar(const std::weak_ptr<foo>& back_reference)
        : back_reference_(back_reference)
      { }
      void do_something()
      {
        if (auto shared_back_reference = back_reference_.lock()) {
          // Use *shared_back_reference
        }
      }
    private:
      std::weak_ptr<foo> back_reference_;
    };

##### Note

 ??? (HS: A lot of people say "to break cycles", while I think "temporary shared ownership" is more to the point.)
???(BS: breaking cycles is what you must do; temporarily sharing ownership is how you do it.
You could "temporarily share ownership" simply by using another `shared_ptr`.)

##### Enforcement

??? probably impossible. If we could statically detect cycles, we wouldn't need `weak_ptr`

### <a name="rr-smartptrparam"></a>R.30: Take smart pointers as parameters only to explicitly express lifetime semantics

See [F.7](#rf-smart).

### <a name="rr-smart"></a>R.31: If you have non-`std` smart pointers, follow the basic pattern from `std`

##### Reason

The rules in the following section also work for other kinds of third-party and custom smart pointers and are very useful for diagnosing common smart pointer errors that cause performance and correctness problems.
You want the rules to work on all the smart pointers you use.

Any type (including primary template or specialization) that overloads unary `*` and `->` is considered a smart pointer:

* If it is copyable, it is recognized as a reference-counted `shared_ptr`.
* If it is not copyable, it is recognized as a unique `unique_ptr`.

##### Example, bad

    // use Boost's intrusive_ptr
    #include <boost/intrusive_ptr.hpp>
    void f(boost::intrusive_ptr<widget> p)  // error under rule 'sharedptrparam'
    {
        p->foo();
    }

    // use Microsoft's CComPtr
    #include <atlbase.h>
    void f(CComPtr<widget> p)               // error under rule 'sharedptrparam'
    {
        p->foo();
    }

Both cases are an error under the [`sharedptrparam` guideline](#rr-smartptrparam):
`p` is a `Shared_pointer`, but nothing about its sharedness is used here and passing it by value is a silent pessimization;
these functions should accept a smart pointer only if they need to participate in the widget's lifetime management. Otherwise they should accept a `widget*`, if it can be `nullptr`. Otherwise, and ideally, the function should accept a `widget&`.
These smart pointers match the `Shared_pointer` concept, so these guideline enforcement rules work on them out of the box and expose this common pessimization.

### <a name="rr-uniqueptrparam"></a>R.32: Take a `unique_ptr<widget>` parameter to express that a function assumes ownership of a `widget`

##### Reason

Using `unique_ptr` in this way both documents and enforces the function call's ownership transfer.

##### Example

    void sink(unique_ptr<widget>); // takes ownership of the widget

    void uses(widget*);            // just uses the widget

##### Enforcement

* (Simple) Warn if a function takes a `Unique_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.

### <a name="rr-reseat"></a>R.33: Take a `unique_ptr<widget>&` parameter to express that a function reseats the `widget`

##### Reason

Using `unique_ptr` in this way both documents and enforces the function call's reseating semantics.

##### Note

"reseat" means "making a pointer or a smart pointer refer to a different object."

##### Example

    void reseat(unique_ptr<widget>&); // "will" or "might" reseat pointer

##### Enforcement

* (Simple) Warn if a function takes a `Unique_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.

### <a name="rr-sharedptrparam-owner"></a>R.34: Take a `shared_ptr<widget>` parameter to express shared ownership

##### Reason

This makes the function's ownership sharing explicit.

##### Example, good

    class WidgetUser
    {
    public:
        // WidgetUser will share ownership of the widget
        explicit WidgetUser(std::shared_ptr<widget> w) noexcept:
            m_widget{std::move(w)} {}
        // ...
    private:
        std::shared_ptr<widget> m_widget;
    };

##### Enforcement

* (Simple) Warn if a function takes a `Shared_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by value or by reference to `const` and does not copy or move it to another `Shared_pointer` on at least one code path. Suggest taking a `T*` or `T&` instead.
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by rvalue reference. Suggesting taking it by value instead.

### <a name="rr-sharedptrparam"></a>R.35: Take a `shared_ptr<widget>&` parameter to express that a function might reseat the shared pointer

##### Reason

This makes the function's reseating explicit.

##### Note

"reseat" means "making a reference or a smart pointer refer to a different object."

##### Example, good

    void ChangeWidget(std::shared_ptr<widget>& w)
    {
        // This will change the callers widget
        w = std::make_shared<widget>(widget{});
    }

##### Enforcement

* (Simple) Warn if a function takes a `Shared_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by value or by reference to `const` and does not copy or move it to another `Shared_pointer` on at least one code path. Suggest taking a `T*` or `T&` instead.
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by rvalue reference. Suggesting taking it by value instead.

### <a name="rr-sharedptrparam-const"></a>R.36: Take a `const shared_ptr<widget>&` parameter to express that it might retain a reference count to the object ???

##### Reason

This makes the function's ??? explicit.

##### Example, good

    void share(shared_ptr<widget>);            // share -- "will" retain refcount

    void reseat(shared_ptr<widget>&);          // "might" reseat ptr

    void may_share(const shared_ptr<widget>&); // "might" retain refcount

##### Enforcement

* (Simple) Warn if a function takes a `Shared_pointer<T>` parameter by lvalue reference and does not either assign to it or call `reset()` on it on at least one code path. Suggest taking a `T*` or `T&` instead.
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by value or by reference to `const` and does not copy or move it to another `Shared_pointer` on at least one code path. Suggest taking a `T*` or `T&` instead.
* (Simple) ((Foundation)) Warn if a function takes a `Shared_pointer<T>` by rvalue reference. Suggesting taking it by value instead.

### <a name="rr-smartptrget"></a>R.37: Do not pass a pointer or reference obtained from an aliased smart pointer

##### Reason

Violating this rule is the number one cause of losing reference counts and finding yourself with a dangling pointer.
Functions should prefer to pass raw pointers and references down call chains.
At the top of the call tree where you obtain the raw pointer or reference from a smart pointer that keeps the object alive.
You need to be sure that the smart pointer cannot inadvertently be reset or reassigned from within the call tree below.

##### Note

To do this, sometimes you need to take a local copy of a smart pointer, which firmly keeps the object alive for the duration of the function and the call tree.

##### Example

Consider this code:

    // global (static or heap), or aliased local ...
    shared_ptr<widget> g_p = ...;

    void f(widget& w)
    {
        g();
        use(w);  // A
    }

    void g()
    {
        g_p = ...; // oops, if this was the last shared_ptr to that widget, destroys the widget
    }

The following should not pass code review:

    void my_code()
    {
        // BAD: passing pointer or reference obtained from a non-local smart pointer
        //      that could be inadvertently reset somewhere inside f or its callees
        f(*g_p);

        // BAD: same reason, just passing it as a "this" pointer
        g_p->func();
    }

The fix is simple -- take a local copy of the pointer to "keep a ref count" for your call tree:

    void my_code()
    {
        // cheap: 1 increment covers this entire function and all the call trees below us
        auto pin = g_p;

        // GOOD: passing pointer or reference obtained from a local unaliased smart pointer
        f(*pin);

        // GOOD: same reason
        pin->func();
    }

##### Enforcement

* (Simple) Warn if a pointer or reference obtained from a smart pointer variable (`Unique_pointer` or `Shared_pointer`) that is non-local, or that is local but potentially aliased, is used in a function call. If the smart pointer is a `Shared_pointer` then suggest taking a local copy of the smart pointer and obtain a pointer or reference from that instead.
