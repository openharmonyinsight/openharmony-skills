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

.. _Build System:

Build System
############

.. meta:
    frontend_status: Partly


The Build System of the |LANG| language defines the following:

- :ref:`Package Definition` that introduces the concept of a package as a
  distributable unit composed of one or more modules.
- :ref:`Module Visibility` that determines whether a module is accessible from
  other packages based on the presence of the modifier ``export`` in the module
  header (e.g.: ``export module "name"``). Modules with no modifier ``export``
  are internal to the package.
- :ref:`Runtime Name Formation` that defines the fully qualified name (see
  :ref:`RT Fully Qualified Name`) for each entity. This name is used for
  runtime identification and access control.
- :ref:`ImportPath Resolution Rules` that defines how an *importPath* (see
  :ref:`Import Path`) is resolved to an actual module.

.. index::
    build system
    module
    module visibility
    export modifier
    internal module
    entity
    qualified name
    runtime
    access control

|

.. _Package Definition:

Package Definition
******************

.. meta:
    frontend_status: Done

*Package* is defined as an entity that groups together one or more modules.
*Package* is a unit of distribution. Each module (see
:ref:`Module Declarations`) belongs to exactly one package.

A package is described by a configuration file that provides the build
system with all information necessary to compile, link, and distribute
the package. The file specifies the following:

- *Package name*, i.e., a string that uniquely identifies the package in the
  build. The name is used as a prefix when forming runtime names (see
  :ref:`Runtime Name Formation`).
- *Source files*, i.e., the set of the |LANG| files that constitute the
  package. The build system compiles these files and combines them into the
  binary file (see :ref:`RT Binary File Format`).
- *Dependencies*, i.e., a set of other packages on which the package depends.
  The build system uses this information to locate those packages during
  compilation, and to ensure that their exported declarations are available for
  *importPath* (see :ref:`Import Path`).
- *ImportPath resolution rules*, i.e., the rules affecting how *importPath*
  (see :ref:`Import Path`) is resolved to modules within the package
  or in external packages. The rules are applied by the build system
  during compilation to locate imported modules.

.. index::
    package
    module

|

.. _Module Visibility:

Module Visibility
*****************

.. meta:
    frontend_status: Done

*Module visibility* determines whether a module can be accessed from modules
residing in other packages. The visibility of a module is determined by the
modifier ``export`` in the module header (see :ref:`Module Header`). If the
module has no module header (see :ref:`Module Header`), then the visibility
of the module is determined similarly to that of a module without the modifier
``export``.

A module can be *exported* or *internal*:

- *Exported* is a module declared with the modifier ``export``. An exported
  module is accessible from modules of other packages.
- *Internal* is a module declared without the modifier ``export``. An internal
  module is accessible only from other modules belonging to the same package.

Attempting to import an *internal* module from another package causes a
:index:`compile-time error`.

An *exported* module with a *module header* is represented in the example
below:

.. code-block:: typescript
   :linenos:

    export module "x"
    // module contents

An *internal* module with a *module header* is represented in the example
below:

.. code-block:: typescript
   :linenos:

    module "y"
    // module contents

An *internal* module with no *module header* is represented in the example
below:

.. code-block:: typescript
   :linenos:

    // module contents

A *public API of a package* in the build system is any declaration exported
from an exported module. If a signature of an exported function, method, class,
or interface specifically includes a unexported type (e.g., a type defined in
an internal module), then a :index:`compile-time error` occurs. This rule is
consistent with the general requirement for exported declarations as discussed
in detail in :ref:`Exported Declarations`. The build system verifies this
property at compile time to ensure that the public interface of the package
remains self-contained, and that runtime visibility checks (see
:ref:`RT Verification`) never fail due to leaks.

*Internal* type protection from package leaks is represented in the example
below:

.. code-block:: typescript
   :linenos:

    // file1.ets
    module "y"          // Internal module "y" (not exported)
    export class InternalClass1 {}

    // file2.ets        // Internal module (not exported)
    export class InternalClass2 {}

    // file3.ets
    export module "x"   // Exported module "x"
    import { InternalClass1 } from "./file1"        // OK, import is allowed
    import { InternalClass2 } from "./file2"        // OK, import is allowed

    export function foo(x: InternalClass1): void {} // Compile-time error, exported function signature contains reference to an unexported type
    export function foo(x: InternalClass2): void {} // Compile-time error, exported function signature contains reference to an unexported type

.. index::
    internal module

|

.. _Runtime Name Formation:

Runtime Name Formation
**********************

.. meta:
    frontend_status: Done

The build system is responsible for constructing the runtime name (see
:ref:`RT Runtime Name`) of each entity.

Forming a runtime name (see :ref:`RT Runtime Name`) from the package name, the
module name (see :ref:`Module Header`), and the qualified name of an entity
is defined by the following rules:

.. code-block:: text
   :linenos:

    if M is not set:
        M = F

    if M is an empty string, and Q is not set:
        R = P
    if M is an empty string:
        R = P + ":" + Q
    else:
        R = P + ":" + M + "." + Q

    R = R.replace("/", ".")

-- where:

- ``M`` is the module name declared in the module header (see
  :ref:`Module Header`).
- ``F`` is the relative path to the file in the package (see
  :ref:`Package Definition`) with its extension deleted.
- ``R`` is the runtime name (see :ref:`RT Runtime Name`) of an entity.
- ``P`` is the name of the package that contains an entity (see
  :ref:`Package Definition`).
- ``Q`` is the qualified name of an entity within the module. The name consists
  of dot-separated identifiers (see :ref:`Names`) except functions, variables,
  methods, and static methods.

If the resulting ``R`` coincides with the runtime name (see
:ref:`RT Runtime Name`) of any other entity in the same package, then a
:index:`compile-time error` occurs.

Forming a runtime name is represented in the example below:

.. code-block:: typescript
   :linenos:

    // packageName: pkg1

    // src/file1.ets
    export module ""            // Runtime Name: "pkg1"

    export class A {}           // Runtime Name: "pkg1:A"
    export namespace ns1 {      // Runtime Name: "pkg1:ns1"
        export namespace ns2 {  // Runtime Name: "pkg1:ns1.ns2"
            exprot class B {}   // Runtime Name: "pkg1:ns1.ns2.B"
        }
        export class C {}       // Runtime Name: "pkg1:ns1.C"
    }

    // src/file2.ets
    export module "x"           // Runtime Name: "pkg1:x"

    export class A {}           // Runtime Name: "pkg1:x.A"
    export namespace ns1 {      // Runtime Name: "pkg1:x.ns1"
        export namespace ns2 {  // Runtime Name: "pkg1:x.ns1.ns2"
            exprot class B {}   // Runtime Name: "pkg1:x.ns1.ns2.B"
        }
        export class C {}       // Runtime Name: "pkg1:x.ns1.C"
    }

    // src/file3.ets
    export class A {}           // Runtime Name: "pkg1:src.file3.A"
    export namespace ns1 {      // Runtime Name: "pkg1:src.file3.ns1"
        export namespace ns2 {  // Runtime Name: "pkg1:src.file3.ns1.ns2"
            exprot class B {}   // Runtime Name: "pkg1:src.file3.ns1.ns2.B"
        }
        export class C {}       // Runtime Name: "pkg1:src.file3.ns1.C"
    }

|

.. _ImportPath Resolution Rules:

ImportPath Resolution Rules
***************************

.. meta:
    frontend_status: Done

The build system resolves importPath (see :ref:`Import Path`) according to the
rules below.

**Step 1**. The build system tries to resolve the *import path* inside its
package by using one of the following:

- *File-relative path*. If the *import path* (see :ref:`Import Path`) starts
  with the prefixes ``./`` or ``../``, then the *import path* points at the
  file path that resolves the relative path to the location of the importing
  file inside the package. If no file exists, then a
  :index:`compile-time error` occurs.
- *Module name*. If the *import path* starts with the prefix ``//``, then the
  *import path* refers to the *module name* declared in the *module header*
  (see :ref:`Module Header`) and located within the current package. If no
  module exists, then a :index:`compile-time error` occurs.
- *Full module name*. If the *import path* equals
  ``"package_name/module_name"``, where ``package_name`` is the name of the
  current  package, and ``module_name`` is the name of one of the modules of
  the current package declared in the *module header* (see
  :ref:`Module Header`), then the *import path* refers to the corresponding
  module.

**Step 2**. The build system tries to resolve the *import path* to the
external module by using one of the following:

- *Aliases section*. If the *import path* equals ``"alias_name/module_name"``,
  where ``alias_name`` is an alias of the name of an external package, and
  ``module_name`` is the name one of the modules of that package, then the
  *import path* refers to the corresponding module.
- *Dependencies section*. If the *import path* equals
  ``"package_name/module_name"``, where ``package_name`` is the name of an
  external package, and ``module_name`` is the name of one of the modules of
  that package, then the *import path* refers to the corresponding module.

If the *import path* fails to resolve, then a :index:`compile-time error`
occurs.

Resolving an import within a single package is represented in the example
below:

.. code-block:: typescript
   :linenos:

    // packageName: pkg1

    // src/file1.ets
    module "x"
    export function foo() {}

    // src/file2.ets
    export function foo() {}

    // src/file3.ets
    import {...} from "./file1"       // OK, importPath is resolved to "file1.ets" by the relative path
    import {...} from "./file2"       // OK, importPath is resolved to "file2.ets" by the relative path
    import {...} from "../src/file1"  // OK, importPath is resolved to "file1.ets" by the relative path
    import {...} from "../src/file2"  // OK, importPath is resolved to "file2.ets" by the relative path
    import {...} from "//x"           // OK, importPath is resolved to "x" by the module name
    import {...} from "//file2"       // Compile-time error, importPath refers to a non-existent module inside the package
    import {...} from "pkg1/x"        // OK, importPath is resolved to "x" by the full module name
    import {...} from "pkg1/file2"    // Compile-time error, importPath refers to a non-existent module inside the package

.. raw:: pdf

   PageBreak
