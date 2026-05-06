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

.. _Binary Compatibility:

Binary Compatibility
####################

.. meta:
    frontend_status: Partly

The |LANG| allows source code of a single runnable program to be compiled
piece by piece. Such property allows source code authors to develop and
distribute code independently. However, certain limitations have to be
met for the existing programs to remain runnable without the recompilation
of all the source code that constitutes them.

*Binary compatibility* is different from the *source compatibility*, which
allows the dependent source code to remain compilable without any *compile-time
errors*. Certain *source compatible* changes may be not *binary compatible*
and vice versa.

.. note::
   Certain *binary incompatible* changes may violate the type system invariants
   of the execution environment, making the execution of binary code impossible.
   In that case, the runtime verification system (see :ref:`Verification <RT Verification>`)
   is responsible for the detection and rejection of such binary code.

This chapter defines the *binary compatible* change of the source code as
a change that allows all the dependent programs with all the *types* and
*namespaces* *loadable* and *resolvable* to preserve this property.

*Type* or *namespace* is *loadable* if the code that depends on such entity
and none of its members can be executed within the running program, while the
*Static Initialization* of the entity *completes*. If the entity is not
*loadable*, the *Static Initialization* does not *complete* and throws
an error.

*Type* or *namespace* is *resolvable* if all of its members, such as
*namespace* variables and functions or *class* fields and *methods*, can
be accessed with no *resolution* errors, i.e., errors that do not appear
within the consistently compiled programs. *Resolvable* type is always
*loadable*.

.. code-block:: typescript
   :linenos:

    // source1.ets
    export interface I {
      m(): void
    }

    // source2.ets
    export namespace N {

      // The type I must be loadable, otherwise the f and the whole N is not loadable.
      //
      // Example case: the definition of I is removed during the change in
      // the source1.ets, while the code of function f was not recompiled.
      export function f(i: I) {

        // I.m must be resolvable for the actual type of I, otherwise an attempt
        // to call i.m will throw a runtime error.
        //
        // Example case: the class that was compiled with an older source code
        // of source1.ets, where I does not declare the method m, does not provide
        // an implementation of the method I.m.
        return i.m()
      }
    }

    // app.ets

    class A implements I {
      m() { }
    }

    try {
      N.f(new A())
    } catch (e) {
      // Some platform-specific errors may appear if the binary compatibility
      // was broken by changes in source1.ets or source2.ets
      //
      // While the recovery for the running program may be possible in some
      // circumstances, this is a detail of the platform whether such
      // program can run or not, and whether it will be terminated during
      // the execution or not.
    }

Source code changes may produce specific errors during the execution
that may not occur if the whole executed program was compiled without any
intermediate source code changes. The resulting errors and conditions may
cause some entity to remain *resolvable*, not *resolvable* but *loadable*, or
not *loadable*. For example,

- If a *public* or *exported* type is removed from the source code,
  the code that accesses the type becomes invalid, making some dependent code not *loadable*.

- *Dynamic Method Resolution* may fail if the method definition is missing or
  some method definitions are conflicting. The fail results in an error thrown
  during an invocation of the method, while the considered class remains
  *loadable*, yet not *resolvable*.

- Changes in the type hierarchy may cause a *type circularity*. Types
  which constitute the *circularity* are not *loadable*.

.. _Classification of Source Code Changes:

Classification of Source Code Changes
*************************************

For bodies of *Method Declarations* and *Function Declarations*, *Top-level Statements*,
initialization expressions of *Top-level Variables* and *static class fields*:

- If the *Effective Type* of the one *Method* or *Function* declaration, *field* or *variable*
  is not affected, the change does not affect *binary compatibility*.

- Otherwise, see other sections for the changes in the *Effective Type*.


For *Namespace Definitions*:

Changes that don't affect the binary compatibility:

- Renaming or removing of a *namespace* member which is not *exported*.

- Adding a new member *namespace*.

- Adding a new *function* or *variable*.

- Adding a new member type definition, such as *class*, *interface*, *enum* or *type alias*.

Some of the changes that break the binary compatibility:

- Changing the name or removing of an *exported* *namespace*.

- Changing the *Effective Type* of an *exported* *function* or *variable*.

- Changing the name or removing of an *exported* *function* or *variable*.

- Changing the name or removing of an *exported* *class*, *interface*, *enum*, *type alias* or *namespace*.


For *Class* and *Interface Declarations*:

Changes that don't affect the binary compatibility:

- Reordering the types in *extends* or *implements* clause.

- Inserting a previously nonexistent interface or class with no members to the type hierarchy.

- Reordering of members, such as *fields*, *methods*.

- Adding, removing or renaming a *private* member.

- Adding a new *field* to the *class*.


Some of the changes that can make some compiled code not *resolvable*:

- If some derived class contains several method definitions of the same name,
  the following conditions may cause a conflict during the method resolution:

  - Adding a new *public* method to an *exported* class.

  - Moving a method upwards in the class hierarchy.

  - Adding a new default method or an optional property to the interface may
    cause a conflict during the method resolution.

- Adding a *required property* or a *method* to an interface without supplying
  a *default implementation* for it.

- Adding an *abstract* method to an existing *exported* *abstract* class.

Some of the changes that can make some compiled code not *loadable*:

- Changing *Effective Type* of a *public* or *protected* *method* or *field*.

- Changing the name or removing a *public* or *protected* *method* or *field*.

- Adding a *final* modifier to an existing *exported* class.


For *enumeration declarations*:

Changes that do not affect binary compatibility:

- Adding new enum constants.

- Changing the value of enum constants while preserving its type.

.. raw:: pdf

   PageBreak
