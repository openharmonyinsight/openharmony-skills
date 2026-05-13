Execution model
***************

.. meta:

A program in ArkTS defines one or more |C_JOBS| that are executed by the
runtime environment. A |C_JOB| is a piece of code that can be executed
concurrently (that is, either asynchronously or in parallel with other |C_JOBS|)
and communicate its return value via the language provided mechanism. 

Given that the target platform allows for parallel code execution, a |C_WORKER|
is an abstraction over platform provided unit of parallelism. Typically, it will
map 1:1 with OS threads. That means:

-  every |C_JOB| is hosted by a |C_WORKER| with only one |C_JOB| per |C_WORKER|
   being executed at once
-  if two or more |C_JOBS| run on different |C_WORKERS| then their code is able
   to run in parallel (this execution mode will be referred to as
   :term:`parallel execution`)
-  if several |C_JOBS| share the same |C_WORKER| then their code can never run
   in parallel (this execution mode will be referred to as :term:`asynchronous
   execution`).

A |C_JOB|'s body has the starting point (the beginning of the corresponding
piece of code) and the completion point (the end of the corresponding piece of
code). A |C_JOB|'s body can (but is not obliged to) map 1:1 to such language
entities as functions, methods or lambdas.

A |C_JOB| can have zero or more suspension points. Execution of a |C_JOB| can be
paused at a suspension point and resumed at a later moment in time. Once
suspended, a |C_JOB| allows another |C_JOB| to be executed on the same
|C_WORKER|.

Any ArkTS program implicitly defines one **main** |C_JOB|, which corresponds to
the :ref:`Program Entry Point`. The execution starts from it, and its completion
initiates the program termination sequence.

The exact language features and standard library APIs that are used for defining
|C_JOBS| and their respective suspension points are described in the subsequent
sections.

The program memory is shared between all |C_JOBS| , which allows for efficient
data sharing but implies that the developer should use the provided means of
synchronization to avoid race conditions and guarantee thread safety.

Overview of concurrency features
********************************

ArkTS allows for both asynchronous and parallel programming and provides the
following:

- :ref:`Asynchronous execution` primitives: ``async`` / ``await`` / ``Promise``;
- :ref:`Parallel execution` API: ``EAWorker API`` / ``Taskpool API``,
  including the structured concurrency support;
- :ref:`Synchronization` API: locks API, atomics API and other means of
  synchronization;

The :ref:`API details and restrictions` section provides the detailed API
description and the restrictions on its usage.
Asynchronous execution
**********************

.. meta:

The :term:`asynchronous execution` capability addresses the situation when
developer's code regularly needs to wait for external (e.g network, timers or
user input) or internal (e.g. status updates from a |C_JOB| that is running on
another |C_WORKER|) events. For such cases, ArkTS provides a way to suspend
execution of a |C_JOB|, mark the |C_JOB| as blocked on a wait for certain event
and resume its execution later, once the event happens.

The ArkTS features that provide the asynchronous execution support are:

- the ``async`` and ``await`` keywords that mark suspendable (``asynchronous``)
  functions and suspension points inside such functions, respectively
- the ``Promise`` class in the Standard Library, which is an abstraction of the
  unfinished computation result that will get its value at some time in future.

Asynchronous Functions
======================

.. meta:

An *asynchronous function* is a function that can define suspension points inside
its body. A non-asynchronous function can not have suspension points.

.. note::
  A *suspension point* is the point in the function code where function
  execution can be paused (so the function becomes *suspended*) and, at some
  time in future, *resumed*.
  The suspension implies that control is transferred elsewhere, but all the
  local function state (e.g. the argument and local variable values)
  is preserved until the resumption.

Asynchronous functions should be marked with the ``async`` modifier and return
an instance of the generic :ref:`Concurrency Promise Class` class, which wraps
the return value. The ``async`` modifier is not a part of the function type: a
``non-async`` function that returns ``Promise`` and an ``async`` function with
the same return type and arguments are no different from the type system
perspective. The function that serves as the :ref:`Program Entry Point` can be
asynchronous, too.

Execution of an ``async`` function can be paused at suspension points, which are
defined with the :ref:`await Expression`. If suspension happens, the ``async``
function immediately returns a *pending* ``Promise`` instance. In case of the
first (by the control flow) suspension point, the control is transferred to the
caller of the asynchronous function, and the runtime environment creates a new
|C_CORO| that corresponds to the suspended function. Eventually, in accordance
with the :ref:`Scheduling rules`, the ``async`` function resumes its execution
from the suspension point where the execution was paused. In case of second and
further suspension points, after the suspension happens, the runtime environment
schedules another |C_JOB| for execution. The |C_JOB| to be scheduled is chosen
in accordance with the :ref:`Scheduling rules`.

Execution of an asynchronous function completes either by a normal return or by
throwing an error. In both cases, the resulting value or error is
wrapped into a ``Promise`` class instance, *resolving* or *rejecting* it
respectively (see :ref:`Concurrency Promise Class` for details).

An asynchronous function with the return type ``Promise<T>`` can explicitly
return a ``Promise<T>`` instance (in this case, the returned value  is returned
"as is") or a value of type ``T``, which is then automatically boxed in an
instance of ``Promise<T>``. Both options are allowed to be the ``expression`` of
the ``return`` statement inside the ``async`` function body (see :ref:`return
Statements` and :ref:`Return Type Inference`). ``T`` here is a subtype of
:ref:`Type Any`. If ``T`` has ``void`` or ``undefined`` type (see
:ref:`Type void or undefined`) then, like in non-asynchronous functions, an
argumentless ``return`` statement is allowed.

.. note::
   Summarizing: an asynchronous function with one or more suspension points
   defines a new |C_CORO| in an ArkTS program, which starts from the first
   suspension and ends with the asynchronous function completion. An
   asynchronous function with zero suspension points does not define any
   additional |C_JOBS|.

A :index:`compile-time error` occurs if:

- ``async`` function is called in a static initialization;
- ``async`` function has an ``abstract`` or a ``native`` modifier;
- return type of an ``async`` function is other than ``Promise``.
- a ``non-async`` function defines any suspension points

Asynchronous Lambdas
====================

.. meta:

A lambda can have the ``async`` modifier (see :ref:`Lambda Expressions` and
:ref:`Trailing Lambdas`).

With regard to concurrency, ``async`` lambdas have the same semantics and
follow the same rules as :ref:`Async Functions`.

Asynchronous Methods
====================

.. meta:

A static or instance class method can have the ``async`` modifier
(see :ref:`Method Declarations`).

With regard to concurrency, ``async`` methods have the same semantics and
follow the same rules as :ref:`Async Functions`.

``await`` expression
====================

.. meta:

An *await expression* defines a suspension point within the asynchronous
function body. The syntax of the *await expression* is as follows:

.. code-block:: abnf

    awaitExpression:
        'await' expression
        ;

The ``expression`` argument here can be of any type (:ref:`Type Any`). The type
of an *await expression* is ``Awaited<type(expression)>`` (see :ref:`Awaited
Utility Type`), but the value and the semantics of the *await expression*
depend on the type of its ``expression`` argument.

If the type of an ``expression`` is a subtype of :ref:`Concurrency Promise
Class`, then:

- Execution of the enclosing asynchronous function is paused until the awaited
  ``Promise`` instance is *resolved* or *rejected*;
- If the awaited ``Promise`` instance is *resolved*, then the value with which
  the ``Promise`` is resolved becomes the value of the *await expression*;
- If the awaited ``Promise`` instance is *rejected*, then the
  *await expression* throws the error with which the ``Promise`` instance is
  rejected;

If the ``expression`` type is not a subtype of :ref:`Concurrency Promise Class`,
then the *await expression* returns the value of the ``expression`` argument,
and the enclosing asynchronous function is not suspended:

.. code-block:: typescript
   :linenos:

   class SomeClass {
     method(): SomeClass | undefined { /* body */ }
     async asyncMethod(): Promise<string> { /* body */ }
   }

   async function g(): Promise<Object> { /* returns Promise */ }

   async function f() { // await is allowed in async context only
     // ...

     // v1 is Awaited<Promise<Object>>, which is effectively Object
     // g returns Promise, hence f can be suspended potentially
     let v1 = await g()

     // v2 is Awaited<Int>, which is effectively Int
     // await argument is an Int, hence no suspension occurs
     let v2 = await new Int(5)

     // v3 is Awaited<Promise<string> | undefined>, which is (string | undefined)
     // - if method() returned an object: suspension can occur, v3 is the await result
     // - if method() returned undefined: no suspension, v3 is undefined
     let v3 = await (new SomeClass).method()?.asyncMethod()

     // ...
   }

Under certain circumstances, the |C_CORO| that has been suspended on ``await``
can be moved to another |C_WORKER| upon resumption, i.e. rescheduled (see
:ref:`Scheduling rules`).

A :index:`compile-time error` occurs if ``await`` is used outside of an
asynchronous function, method or lambda body.

``Promise`` class
=================

.. meta:

The ``Promise`` class represents a value that is to be defined at some time in
future, thus allowing for referencing a result of an unfinished calculation or
an incomplete task. All kinds of |C_JOBS| in ArkTS use promises to communicate
their results to the client code.

A ``Promise`` instance can have the following states:

- *pending*: this state means that the resulting value is not yet known;
- *resolved*: this state means that the ``Promise`` has been *fulfilled* and its
  value has been defined;
- *rejected*: this state means that the associated calculation completed
  abnormally, so the ``Promise`` instance contains the error instance that
  describes the reason of abnormal completion;

The only way to get the value that was used to resolve or reject the ``Promise``
is to apply the :ref:`await Expression` to the ``Promise`` instance.

.. note::
    The semantics of ``Promise`` is similar to the semantics of ``Promise`` in
    |JS|/|TS| if it was returned by an asynchronous function on the **main**
    |C_WORKER| or created manually on the **main** |C_WORKER|.
    It is to be defined if such statements should reside in ArkTS
    specification.

In general, the ``Promise`` instances are safe to be accessed concurrently.
The exceptions for this rule and the detailed API is described in the
:ref:`API details and restrictions` section.
Parallel Execution
******************

.. meta:

The :term:`parallel execution` capability addresses the situation when
developer's code executes either CPU-intensive tasks that can take advantage of
utilizing multiple CPU cores or long tasks that can take advantage of running in
a separate OS thread of execution to avoid blocking.

For such cases, ArkTS provides a standard library level API that allows for
running code in parallel at function/method granularity (that is, for defining
|C_JOBS| that can run on different |C_WORKERS|), with the ability to specify
dependencies between |C_JOBS| and balance the load across the available CPU
cores and/or OS threads. 

This capability is orthogonal to the :ref:`Asynchronous execution` capability,
i.e. asynchronous functions can also be run in parallel, and this in general
does not affect the way they are suspended/resumed. The only difference is that
under certain conditions a |C_CORO| can change its |C_WORKER| upon resumption
(see :ref:`Scheduling rules`).

Parallel execution API
======================

.. meta:

ArkTS standard library provides the following sets of API for parallel
execution:

- :ref:`EAWorker API`: the API that allows for creation of |C_WORKERS| that are
  used exclusively by a |C_JOB| and its children;
- :ref:`Taskpool API`: the framework that offers structured concurrency
  capabilities: task grouping, dependencies and cancellation

EAWorker API
============

The EAWorker API is designed for the use case when developer's code requires a
dedicated |C_WORKER| to run on (for example, such use case is relevant for UI
frameworks). 

This API creates a |C_WORKER| for the *exclusive* use of an initial |C_JOB|.
That means, the initial |C_JOB| and all the |C_JOBS| spawned by it will stay on
this newly created |C_WORKER|, and no other |C_JOB| can be scheduled to this
|C_WORKER|.

Please refer to the standard library documentation to find out more information.

Taskpool API
============

The ``taskpool`` is the structured concurrency framework. It allows to create
new |C_JOBS|, specify dependencies between them, cancel the spawned |C_JOBS|,
combine them in groups and choose a complex execution order.

.. note::
    The |C_COROS| created by the taskpool API can not be rescheduled to another 
    |C_WORKER| upon resumption.

Please refer to the standard library documentation to find out more information.
Synchronization
***************

.. meta:

The synchronization mechanisms that exist in ArkTS and its standard library
address the need for imposing certain order on the execution of the code that
belongs to the |C_JOBS| being executed asynchronously or in parallel. Such need
originates from the two facts:

- firstly, all the data in ArkTS are by default shared between all |C_JOBS| on
  all |C_WORKERS|, which may cause data races in case when the same data is
  accessed concurrently;
- secondly, certain code sequences expect the data they operate on to be
  accessed exclusively by their |C_JOB|. If this |C_JOB| is a |C_CORO| and it
  suspends its execution inbetween of such code sequence, then another |C_JOB|
  can violate the expected exclusivity even in case when it runs on the same
  |C_WORKER|.

The means of synchronization that ArkTS provides are:

- :ref:`AsyncLock`: the "fused" asynchronous locking API, which allows the
  provided callback to safe operate on some data;
- :ref:`AsyncMutex`, :ref:`AsyncRWLock`, :ref:`AsyncCondVar`: the "decoupled"
  asynchronous locking API, which provides the asynchronous version of
  traditional decoupled ``lock()`` / ``unlock()`` operations and also an
  asynchronous condition variable equivalent;
- :ref:`Atomics`: the atomic operations support, which also allows for building
  efficient lock-free structures
- :ref:`Other synchronization`: a variety of other supplemental standard library
  classes and methods
  

Asynchronous lock
=================

.. meta:

The asynchronous lock (``AsyncLock`` class) allows to protect some shared data,
for example, a part of object state, from concurrent access. It is designed for
the use cases when the code sequence that accesses the protected state can be
conveniently isolated as a distinct function object (function, method or
lambda).

.. code-block:: typescript
   :linenos:

   // a shared (e.g. global) data that we would like to protect
   class SharedState {
     value: string = "nothing"
   }
   let whatIsInTheBag: SharedState = new SharedState

   // a function that reads and modifies the shared data
   function checkAndModify(data: SharedState, expected: string, updated: string) {
     if (data.value != expected) {
       // data race!
       console.log("race!")
     }
     data.value = updated
   }

   // a suspension point emulator
   async function delay() {
     return new Promise<void>((res, rej) => {
       setTimeout(res, 1, undefined)
     })
   }

   // create a lock somewhere, for example as a global variable
   let lock = new AsyncLock()

   async function f() {
    // request an operation under the specified lock
    let p1 = lock.lockAsync<void>(async () => {
        // once the request can be satisfied, this lambda will run on the same
        // worker thread with the lock acquired

        // execute a modification sequence on the protected data:
        // nothing -> paraglider -> nothing

        // nothing -> paraglider
        checkAndModify(whatIsInTheBag, "nothing", "paraglider")

        // a sample suspension point that simulates a real life situation when
        // the modification sequence gets paused and another async function on
        // the same worker thread gets control 
        await delay()
        
        // continue with the modification
        // paraglider -> nothing
        checkAndModify(whatIsInTheBag, "paraglider", "nothing")
    }, AsyncLockMode.EXCLUSIVE)

    // request another operation under the same lock: it will be executed not
    // earlier than the lock can be acquired
    let p2 = lock.lockAsync<void>(async () => {
        // another asynchronous modification sequence that suspends inbetween:
        // nothing -> apple -> nothing

        checkAndModify(whatIsInTheBag, "nothing", "apple")
        await delay()
        checkAndModify(whatIsInTheBag, "apple", "nothing")
    }) // AsyncLockMode.EXCLUSIVE is the default, so it can be skipped

    // wait for both operations to complete
    await p1
    await p2

    // Since both sequences have suspension points within them, they were
    // executed in an interleaved manner if there would no locks, which would 
    // cause a data race and thus an error.
    // However, the lock that we used for synchronization prevents this
    // situation and each modification sequence executes as a critical section,
    // which leads to the correct result.
   }

   function main() {
     f()
   }

A developer can request one of two levels of access exclusivity to the given
``AsyncLock``: exclusive or shared. The difference is as follows:

- if an exclusive access is requested (default behaviour), then no other request
  for callback execution under the same ``AsyncLock`` instance will be satisfied
  until the requester's callback is finished;
- if a shared access is requested then any other request for the callback
  execution under this lock can be concurrently satisfied, but all requests that
  demand exclusive access will wait their turn

  The callback execution under an ``AsyncLock`` can be safely requested
  concurrently both by the same and different |C_JOBS|.

``AsyncLock`` API provides a way to abort an existing request for callback
execution and to query the status of the existing locks. Additionally it
provides a way to limit the waiting time for an issued lock acquire request with
a timeout and also gives hints about the potential deadlocks.

Please refer to the standard library documentation to find out more information.

Asynchronous mutex
==================

.. meta:

The asynchronous mutex (``AsyncMutex``) allows to protect some shared data,
for example, a part of object state, from concurrent access. It is designed for
the following use cases:

- developer wants to use a condition variable (:ref:`AsyncCondVar`)
- the code sequence that accesses the protected state is hard to be conveniently
  isolated as a distinct function object (function, method or lambda), so the
  decoupled ``lock()`` and ``unlock()`` operations are required

.. code-block:: typescript
   :linenos:

   // a shared (e.g. global) data that we would like to protect
   class SharedState {
     value: string = "nothing"
   }
   let whatIsInTheBag: SharedState = new SharedState

   // a function that reads and modifies the shared data
   function checkAndModify(data: SharedState, expected: string, updated: string) {
     if (data.value != expected) {
       // data race!
       console.log("race!")
     }
     data.value = updated
   }

   // a suspension point emulator
   async function delay() {
     return new Promise<void>((res, rej) => {
       setTimeout(res, 1, undefined)
     })
   }

   // create a lock somewhere, for example as a global variable
   let lock = new AsyncMutex()

   async function f() {
    // here we execute a modification sequence on the protected data under the 
    // lock: nothing -> paraglider -> nothing

    // the await is mandatory! the promise returned by the lock() method will
    // get resolved not earlier than the lock is successfullly acquired
    await lock.lock();
    // the code between lock() and unlock() acts like a critical section:
    // no other job is able to acquire the "lock" till the "unlock()" is called

    // nothing -> paraglider
    checkAndModify(whatIsInTheBag, "nothing", "paraglider")

    // a sample suspension point that simulates a real life situation when
    // the modification sequence gets paused and another async function on
    // the same worker thread gets control 
    await delay()
    
    // continue with the modification
    // paraglider -> nothing
    checkAndModify(whatIsInTheBag, "paraglider", "nothing")

    // end of the critical section
    lock.unlock()
   }

   async function g() {
    // another asynchronous modification sequence that suspends inbetween:
    // nothing -> apple -> nothing
    await lock.lock()
    // start of the critical section

    checkAndModify(whatIsInTheBag, "nothing", "apple")
    await delay()
    checkAndModify(whatIsInTheBag, "apple", "nothing")

    // end of the critical section
    lock.unlock()
   }

   function main() {
    // Call both functions consequently without any waits.
    // Since both functions have suspension points within them, they were
    // executed in an interleaved manner if there would no locks, which would 
    // cause a data race and thus an error.
    // However, the mutex we used for synchronization prevents this
    // situation and each modification sequence executes as a critical section,
    // which leads to the correct result.
     f()
     g()
   }

The ``AsyncMutex`` can be safely used in both the |C_JOBS| that run on the same
|C_WORKER| and on different |C_WORKERS|.

The avoidance of double locking (happens if the `lock()` method is called from
the lock instance that is already acquired by the current |C_JOB|) and deadlocks
is the developer's responsibility. Please refer to the standard library
documentation to find out more information.

Asynchronous read/write lock
============================

.. meta:

The asynchronous read/write lock (``AsyncRWLock``) allows to protect some shared
data, for example, a part of object state, from concurrent access. It is
designed for the use case when both of the following statements are true:

- the code sequence that accesses the protected state is hard to be conveniently
  isolated as a distinct function object (function, method or lambda), so the
  decoupled ``lock()`` and ``unlock()`` operations are required
- access to the shared state must be mutually exclusive between a group of
  entities that can safely access the data concurrently ("readers") and any
  other entity that requires exclusive access to the data ("writer"/"writers")

Please refer to the standard library documentation to find out more information.

Asynchronous condition variable
===============================

.. meta:

The asynchronous condition variable (``AsyncCondVar``) is designed for the use
case when some shared data is used as a condition for a sequence of actions in
one |C_JOB| and is concurrently modified in another |C_JOB|.

The use of ``AsyncCondVar`` requires :ref:`AsyncMutex`:

.. code-block:: typescript
   :linenos:

   // create mutex and condition variable somewhere, e.g. in the global scope
   let m = new AsyncMutex();
   let cv = new AsyncCondVar();
   // the shared data, which is used as a condition
   let flag = false;

   async function f() {
    // the notification sequence (in job A): 
    // lock the mutex
    await m.lock()
    // start of the critical section

    // update the condition
    flag = true
    // notify the waiter(s):
    // the API requires that the same mutex is to be provided here
    cv.notifyOne(m)

    // end of the critical section: unlock the mutex
    m.unlock()
   }

   async function g() {
    // the wait-and-react sequence (in job B):
    // lock the same mutex that is used for condition update and notification
    await m.lock() // await is mandatory!
    // start of the critical section

    // check the shared condition
    while (flag == false) {
      // start waiting for the condition to change:
      // the API requires that the same mutex is to be provided here
      // wait() unlocks "m" and returns the Promise that is going to be resolved
      // once some other job calls notifyOne()/notifyAll()
      await cv.wait(m) // await is mandatory!

      // at this point, "m" is locked again, and the notification has been received
    }
    // here the condition is satisfied, and the mutex is locked:
    // any dependent actions (e.g. some state update) can happen here, and they
    // effectively happen in the same critical section with the verification of
    // the shared condition value

    // end of the critical section: unlock the mutex
    m.unlock()
   }

   function main() {
     f()
     g()
   }

Please refer to the standard library documentation to find out more information.

Atomic operations
=================

.. meta:

ArkTS standard library provides a set of classes that support atomic
operations. The intended use cases for them are lock free data structures and
algorithms: from simple compare-and-swap and spinlocks to complex containers.

Please refer to the standard library documentation to find out more information.

Additional entities and other notes
===================================

.. meta:

The ArkTS standard library provides various additional classes and APIs that
help developers to build safe and efficient concurrent programs. Such classes
include:

- thread safe concurrent containers
- APIs that operate on |C_WORKER|-local data
- other helpers

Please refer to the standard library documentation to find out more information
about them.
API details and restrictions
****************************

.. meta:

This section describes the noteworthy details and the notable restrictions for
the concurrency APIs described in the previous sections.

Using the asynchronous API
==========================

In certain cases, a call to an ``async`` function requires awaiting its result,
but the call site resides in the non-async function. In such cases, the caller
function should be converted to an asynchronous one, and in some cases this
chain of conversions has to be continued up to the program entry point. For this
case, ArkTS supports the ``async`` entry point function (see :ref:`Program Entry Point`).

.. note::
   Maybe, this section should be moved to the handbook.

Promise class API
=================

There are some important restrictions that limit the correct usage of the
``Promise`` class.

A ``Promise`` class instance is safe to be awaited within a |C_JOB| on some
|C_WORKER| while being resolved or rejected from another |C_JOB| on the same or 
different |C_WORKER|.

A ``Promise`` class allows to register callbacks that are to be called upon
``Promise`` resolution and/or rejection. This is done by calling the ``.then()``
/ ``.catch()`` / ``.finally()`` methods of the ``Promise`` class. However, these
methods have the following usage restrictions:

- the registered callback will be called as a separate |C_JOB| on the same
  |C_WORKER| where it was registered
- if multiple callbacks are registered from the |C_JOBS| that reside on the same
  |C_WORKER|, the order of their execution matches the order of their
  registration
- if multiple callbacks are registered from the |C_JOBS| that reside on
  different |C_WORKERS|, the order of their execution is defined only within
  each |C_WORKER|, and no order is guaranteed between the resulting |C_JOBS|
  that reside on different |C_WORKERS|

Please refer to the standard library documentation to find out more information
about the ``Promise`` methods.

Unhandled Rejected Promises
===========================

.. meta:

.. note::
   The semantics of unhandled rejections will be revisited later, once the
   design of ArkTS concurrency subsystem is complete.

A rejected ``Promise`` is considered unhandled if, at certain time, there is no
``await`` waiting for it and there are no callbacks registered for it with the
``.then()`` / ``.catch()`` methods.

This moment of time is defined separately on each |C_WORKER|, hence the
``Promise`` instance is considered an *unhandled rejection* only within a
context of some |C_WORKER|, while possibly being *handled* on other ones.

Error handling policy
=====================

In general, all errors thrown in an ArkTS program should either have an ability
to be handled by the developer or considered uncaught, and initiate a program
termination sequence. This applies to any |C_JOB| on any |C_WORKER|.

A |C_JOB| in an ArkTS program can complete abnormally, i.e., can throw an error.
Since |C_JOBS| communicate their return values using ``Promise`` class
instances, in case of |C_JOB|'s abnormal completion the corresponding promise
gets rejected and the original error is not considered uncaught.

However, there can exist some cases when such rejection cannot be handled by the
developer, for example:

- when the thrower |C_JOB| was created by the runtime environment, and no
  promise can be awaited or handled with a ``.then()`` / ``.catch()`` callback
- when the *main* |C_JOB| throws an error

In such cases, the original error thrown by the |C_JOB| will be considered
uncaught.
Runtime implementation details
******************************

.. meta:

Scheduling rules
================

.. meta:

The runtime environment schedules the |C_JOBS| that are defined by an ArkTS
program in accordance with the following rules:

- Every |C_JOB| has a priority, which depends solely on its type. The list of
  types, from highest to lowest priority:

  1. |C_COROS| and ``Promise`` callbacks (``.then()``, etc.);
  2. Other |C_JOBS|
  
- Within each |C_WORKER|, the |C_JOBS| with higher priority are scheduled
  before |C_JOBS| with lower priority;
- All |C_JOBS| with the same priority are scheduled in the FIFO order;

.. note::
   These rules are incomplete and will be updated.
