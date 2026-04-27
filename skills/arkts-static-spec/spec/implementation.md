..
    Copyright (c) 2021-2026 Huawei Device Co., Ltd.
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

.. _Implementation Details:

Implementation Details
######################

.. meta:
    frontend_status: Partly
    todo: Implement Type.from in stdlib

Important implementation details are discussed in this section.

.. _Import Path Lookup:

Import Path Lookup
******************

.. meta:
    frontend_status: Done

If an import path ``<some path>/name`` is resolved to a path in the folder
'*name*', then  the compiler executes the following lookup sequence:

-   If the folder contains the file ``index.ets``, then this file is imported
    as a module written in |LANG|;

-   If the folder contains the file ``index.ts``, then this file is imported
    as a module written in |TS|.


.. index::
   implementation
   import path
   path
   folder
   file
   compiler
   lookup sequence
   module

|

.. _Modules in Host System:

Modules in Host System
**********************

.. meta:
    frontend_status: Done

Modules are created and stored in a manner that is determined by the host
system. The exact manner modules are stored in a file system is determined by
a particular implementation of the compiler and other tools.

A simple implementation stores every module in a single file.

.. index::
   host system
   storage
   storage management
   module
   file system
   implementation
   file
   folder
   source file

|

.. _Getting Runtime Type Via Reflection:

Getting Runtime Type Via Reflection
***********************************

.. meta:
    frontend_status: None

The |LANG| standard library (see :ref:`Standard Library`) provides a
pseudogeneric static method ``Class.from<T>()`` to be processed by the compiler
in a specific way during compilation. A call to this method allows getting a
value of type ``Class`` that represents type ``T`` at runtime.

.. code-block:: typescript
   :linenos:

    let type_of_int: Class = Class.from<int>()
    let type_of_string: Class = Class.from<string>()
    let type_of_number: Class = Class.from<number>()
    let type_of_Object: Class = Class.from<Object>()

    class UserClass {}
    let type_of_user_class: Class = Class.from<UserClass>()

    interface SomeInterface {}
    let type_of_interface: Class = Class.from<SomeInterface>()

.. index::
   pseudogeneric static method
   static method
   compiler
   method call
   call
   method
   compilation
   variable
   runtime
   value
   type

If type ``T`` used as type argument is affected by :ref:`Type Erasure`, then
the function returns value of type ``Class`` for *effective type* of ``T``
but not for ``T`` itself:

.. code-block:: typescript
   :linenos:

    let type_of_array1: Class = Class.from<int[]>() // value of Class for Array<> 
    let type_of_array2: Class = Class.from<Array<number>>() // the same Class value

.. index::
   type argument
   type erasure
   function
   array

|

.. _Ensuring Module Initialization:

Ensuring Module Initialization
******************************

.. meta:
    frontend_status: None

The |LANG| standard library (see :ref:`Standard Library`) provides a top-level
function ``initModule()`` with a single parameter of type ``string``. Its value
is resolved at compile time according to the rules of import path resolution
(see :ref:`ImportPath Resolution Rules`). A call to this function ensures that
the module referred by the argument is available, and that its initialization
(see :ref:`Static Initialization`) is performed. An argument must be a string
literal. Otherwise, a :index:`compile-time error` occurs.

The current module has no access to the exported declarations of the module
referred by the argument. If such module is not available or any other runtime
issue occurs then a proper exception is thrown.

.. code-block:: typescript
   :linenos:

    initModule ("@ohos/library/src/main/ets/pages/Index")

.. index::
   module initialization
   initialization
   top-level function
   parameter
   sting literal
   module
   argument
   function
   argument
   access
   declaration
   runtime
   exception

|

.. _Generic and Function Types Peculiarities:

Generic and Function Types Peculiarities
****************************************

The current compiler and runtime implementations use type erasure.
Type erasure affects the behavior of generics and function types. It is
expected to change in the future. A particular example is provided in the last
bullet point in the list of compile-time errors in :ref:`instanceof Expression`.

.. index::
   generic
   function type
   compiler
   runtime implementation
   type erasure
   instanceof expression

|

.. _Keyword struct and ArkUI:

Keyword ``struct`` and ArkUI
****************************

.. meta:
    frontend_status: Done

The current compiler reserves the keyword ``struct`` because it is used in
legacy ArkUI code. This keyword can be used as a replacement for the keyword
``class`` in :ref:`Class declarations`. Class declarations marked with the
keyword ``struct`` are processed by the ArkUI plugin and replaced with class
declarations that use specific ArkUI types.

.. index::
   compiler
   struct keyword
   class keyword
   class declaration
   ArkUI plugin
   ArkUI type
   ArkUI code

|

.. _Make a Bridge Method for Overriding Method:

Make a Bridge Method for Overriding Method
******************************************

.. meta:
    frontend_status: None

Situations are possible where the compiler must create an additional bridge
method to provide a type-safe call for the overriding method in a subclass of
a generic class. Overriding is based on *erased types* (see :ref:`Type Erasure`).
The situation is represented in the following example:

.. code-block:: typescript
   :linenos:

    class B<T extends Object> {
        foo(p: T) {}
    }
    class D extends B<string> {
        foo(p: string) {} // original overriding method
    }

In the example above, the compiler generates a *bridge* method with the name
``foo`` and signature ``(p: Object)``. The *bridge* method acts as follows:

.. index::
   bridge method
   overriding method
   erased type
   subclass
   compiler
   type-safe call
   generic class
   type erasure
   signature

-  Behaves as an ordinary method in most cases, but is not accessible from
   the source code, and does not participate in overloading;

-  Applies narrowing to argument types inside its body to match the parameter
   types of the original method, and invokes the original method.

The use of the *bridge* method is represented by the following code:

.. code-block:: typescript
   :linenos:

    let d = new D()
    d.foo("aa") // original method from 'D' is called
    let b: B<string> = d
    b.foo("aa") // bridge method with signature (p: Object) is called
    // its body calls original method, using (p as string) to check the type of the argument

More formally, a bridge method ``m(C``:sub:`1` ``, ..., C``:sub:`n` ``)``
is created in ``D``, in the following cases:

- Class ``B`` comprises type parameters
  ``B<T``:sub:`1` ``extends C``:sub:`1` ``, ..., T``:sub:`n` ``extends C``:sub:`n` ``>``;
- Subclass ``D`` is defined as ``class D extends B<X``:sub:`1` ``, ..., X``:sub:`n` ``>``;
- Method ``m`` of class ``D`` overrides ``m`` from ``B`` with type parameters in signature,
  e.g., ``(T``:sub:`1` ``, ..., T``:sub:`n` ``)``;
- Signature of the overridden method ``m`` is not ``(C``:sub:`1` ``, ..., C``:sub:`n` ``)``.

.. index::
   ordinary method
   access
   source code
   overloading
   argument type
   method
   bridge method
   type parameter
   subclass
   overriding
   signature
   overridden method

.. raw:: pdf

   PageBreak
