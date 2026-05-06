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

.. _Names, Declarations and Scopes:

Names, Declarations and Scopes
##############################

.. meta:
    frontend_status: Done

This chapter introduces the following three mutually-related notions:

-  Names,
-  Declarations, and
-  Scopes.

Each entity in an |LANG| program---a variable, a constant, a class,
a type, a function, a method, etc.---is introduced via a *declaration*.
An entity declaration defines a *name* of the entity. The name is used to
refer to the entity further in the program text. The declaration binds the
entity name with the *scope* (see :ref:`Scopes`). The scope affects the
accessibility of a new entity, and how it can be referred to by its qualified
or simple (unqualified) name.

.. index::
   variable
   constant
   class
   type
   function
   method
   scope
   accessibility
   declaration
   entity
   simple name
   unqualified name
   qualified name
   name

|

.. _Names:

Names
*****

.. meta:
    frontend_status: Done

A name is a sequence of one or more identifiers. A name allows referring to
any declared entity. Names can have two syntactical forms:

    - *Simple name* that consists of a single identifier;
    - *Qualified name* that consists of a sequence of identifiers with the
      token ``'.'`` as separator.

Both situations are covered by the below syntax rule:

.. code-block:: abnf

    qualifiedName:
      identifier ('.' identifier )*
      ;

In a qualified name *N.x* (where *N* is a simple name, and ``x`` is an
identifier that can follow a sequence of identifiers separated with ``'.'``
tokens), *N* can name the following:

-  Name of a module (see :ref:`Module Declarations`) that is introduced as a
   result of ``import * as N`` (see :ref:`Bind All with Qualified Access`)
   with ``x`` to name the exported entity;

-  A class or interface type (see :ref:`Classes`, :ref:`Interfaces`) with ``x``
   to name its static member;

-  A class or interface type variable with ``x`` to name its instance member.

.. index::
   name
   entity
   simple name
   qualified access
   exported entity
   interface type variable
   interface type
   interface
   class
   static member
   qualified name
   identifier
   reference type
   variable
   field
   method
   token
   separator
   instance member

|

.. _Declarations:

Declarations
************

.. meta:
    frontend_status: Done

A declaration introduces a named entity in an appropriate *declaration scope*
(see :ref:`Scopes`), see

.. index::
   named entity
   declared entity
   declaration scope

- :ref:`Namespace Declarations`;
- :ref:`Type Declarations`;
- :ref:`Variable and Constant Declarations`;
- :ref:`Function Declarations`;
- :ref:`Classes`;
- :ref:`Interfaces`;
- :ref:`Enumerations`;
- :ref:`Constant or Variable Declarations`;
- :ref:`Top-Level Declarations`;
- :ref:`Explicit Overload Declarations`;
- :ref:`Annotations`;
- :ref:`Ambient Declarations`;
- :ref:`Accessor Declarations`;
- :ref:`Functions with Receiver`.

Each declaration in the declaration scope (see :ref:`Scopes`)
must be *distinguishable*.

Declarations are *distinguishable* if they have:

-  Different names,
-  Different signatures (see :ref:`Declaration Distinguishable by Signatures`).

.. index::
   distinguishable declaration
   declaration scope
   name
   signature

Distinguishable declarations are represented by the examples below:

.. code-block:: typescript
   :linenos:

    const PI = 3.14
    const pi = 3
    function Pi() {}
    type IP = number[]
    class A {
        static method() {}
        method() {}
        field: number = PI
        static field: number = PI + pi
    }

If a declaration is not distinguishable by name, except a valid overload
(see :ref:`Declaration Distinguishable by Signatures`),
then a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    // Compile-time error, the constant and the function have the same name.
    const PI = 3.14
    function PI() { return 3.14 }

    // Compile-time error, the type and the variable have the same name.
    class Person {}
    let Person: Person

    // Compile-time error, the field and the method have the same name.
    class C {
        counter: number
        counter(): number {
          return this.counter
        }
    }

    /* compile-time error, name of the declaration clashes with the predefined
        type or standard library entity name. */
    let number: number = 1
    let String = true
    function Record () {}
    interface Object {}
    let Array = 42


    /* compile-time error, ambient and non-ambient declarations refer to the
       same entity in a single module
    */
    declare function foo()
    function foo() {}

.. index::
   declaration
   distinguishable functions

|

.. _Declaration Distinguishable by Signatures:

Declaration Distinguishable by Signatures
=========================================

.. meta:
    frontend_status: None

The following kinds of same-name declarations are distinguishable
by signatures if signatures are not overload-equivalent
(see :ref:`Overload-Equivalent Signatures`):

-  Functions of the same name in the same *declaration scope*
   (see :ref:`Implicit Function Overloading`);
-  Methods of the same class with the same name (see
   :ref:`Implicit Method Overloading`);
-  Constructors of the same class.

.. index::
   distinguishable declaration
   signature
   function
   overloading
   constructor

A :index:`compile-time error` occurs if two same-name functions
declared in different scopes are made accessible in one scope:

.. code-block:: typescript
   :linenos:

    import {foo, goo as bar} from "some module"

    function foo() {} // Compile-time error, duplicate declaration
    function bar() {} // Compile-time error, duplicate declaration

Functions distinguishable by signatures are represented in the example below:

.. code-block:: typescript
   :linenos:

      function foo() {}
      function foo(x: number) {}
      function foo(x: number[]) {}
      function foo(x: string) {}

Functions with overload-equivalent signatures cause a
:index:`compile-time error` as represented in the following example:

.. code-block:: typescript
   :linenos:

      // Functions have overload-equivalent signatures
      function foo(x: number) {}
      function foo(y: number) {}

      // Functions have overload-equivalent signatures because of type erasure
      function bar(x: Array<number>) {}
      function bar(x: Array<string>) {}

.. index::
   distinguishable function
   function
   signature

|

.. _Scopes:

Scopes
******

.. meta:
    frontend_status: Done

Different entity declarations introduce new names in different *scopes*. Scope
is the region of program text where an entity is declared,
along with other regions it can be used in. The following entities are always
referred to by their qualified names only:

- Class and interface members (both static and instance ones);
- Entities imported via qualified import; and
- Entities declared in namespaces (see :ref:`Namespace Declarations`).

Other entities are referred to by their simple (unqualified) names.

Entities within the scope are accessible (see :ref:`Accessible`).

.. index::
   scope
   entity
   entity declaration
   class member
   interface member
   class
   member
   static member
   instance member
   qualified name
   qualified import
   namespace
   namespace declaration
   simple name
   access
   simple name
   unqualified name
   accessible scope
   variable
   constant
   function call
   accessibility

The scope level of an entity depends on the context the entity is
declared in:

.. _module-access:

.. meta:
    frontend_status: Partly

-  *Module level scope* is applicable to modules only. *Constants*
   and *variables* are accessible (see :ref:`Accessible`)
   from their respective points of declaration to the end of the module.
   Other entities are accessible through the entire scope level.
   If exported, a name can be accessed in other modules.

.. _namespace-access:

.. meta:
    frontend_status: Partly

-  *Namespace level scope* is applicable to namespaces only.
   *Constants*   and *variables* are accessible
   (see :ref:`Accessible`) from their respective points of declaration
   to the end of the namespace including all embedded namespaces.
   Other entities are accessible through the entire namespace scope level
   including embedded namespaces.
   If exported, a name can be accessed outside the namespace with mandatory
   namespace name qualification.

.. index::
   module level scope
   module
   access
   name
   declaration
   namespace
   namespace level scope

.. _class-access:

.. meta:
    frontend_status: Done

-  A name declared inside a class (*class level scope*) is accessible (see
   :ref:`Accessible`) in the class and sometimes, depending on the access
   modifier (see :ref:`Access Modifiers`), outside the class, or by means of a
   derived class.

   Access to names inside the class is qualified with one of the following:

   -  Keywords ``this`` or ``super``;
   -  Class instance expression for the names of instance entities; or
   -  Name of the class for static entities.

   Outside access is qualified with one of the following:

   -  The expression the value stores;
   -  A reference to the class instance for the names of instance entities; or
   -  Name of the class for static entities.

   |LANG| supports using the same identifier as names of a static entity and
   of an instance entity. The two names are *distinguishable* by the context,
   which is either a name of a class for static entities or an expression
   that denotes an instance.

.. index::
   class level scope
   accessibility
   access modifier
   keyword super
   keyword this
   expression
   value
   method
   name
   access
   modifier
   derived class
   declaration
   class instance
   instance entity
   static entity

.. _interface-access:

.. meta:
    frontend_status: Done

-  A name declared inside an interface (*interface level scope*) is accessible
   (see :ref:`Accessible`) inside and outside that interface (default
   ``public``).

.. index::
   name
   declaration
   class level scope
   interface level scope
   interface
   access

.. _class-or-interface-type-parameter-access:

.. meta:
    frontend_status: Done

-  *The scope of a type parameter* name in a class or interface declaration
   is that entire declaration, excluding static member declarations.

.. index::
   name
   declaration
   static member
   static member declaration
   scope
   type parameter

.. _function-type-parameter-access:

.. meta:
    frontend_status: Done

-  The scope of a type parameter name in a function declaration is that
   entire declaration (*function type parameter scope*).

.. index::
   parameter name
   function declaration
   function type parameter scope
   scope

.. _function-access:

.. meta:
    frontend_status: Done

-  The scope of a name declared inside the body of a function or a method
   declaration is the body of that declaration from the point of declaration
   and up to the end of the body (*method* or *function scope*). This scope is
   also applied to function or method parameter names.

.. index::
   scope
   function body declaration
   method body declaration
   method scope
   function scope
   method parameter name

.. _block-access:

.. meta:
    frontend_status: Done

-  The scope of a name declared inside a block is the body of the block from
   the point of the name declaration and up to the end of the block
   (*block scope*).

.. index::
   block
   body
   point of declaration
   block scope

.. code-block:: typescript
   :linenos:

    function foo() {
        let x = y // Compile-time error - y is not accessible yet
        let y = 1
    }

Scopes of two names can overlap (e.g., when statements are nested). If scopes
of two names overlap, then:

-  The innermost declaration takes precedence; and
-  Access to the outer name is not possible.

Class, interface, and enumeration members can only be accessed by applying
the dot operator ``'.'`` to an instance or to a type.
Accessing them otherwise is not possible.

.. index::
   name
   scope
   overlap
   nested statement
   innermost declaration
   precedence
   access
   class member
   interface member
   enum member
   instance
   dot operator

|

.. _Accessible:

Accessible
**********

.. meta:
    frontend_status: Done

Entity is considered accessible if it belongs to the current scope (see
:ref:`Scopes`) and means that its name can be used for different purposes as
follows:

- Type name is used to declare variables, constants, parameters, class fields,
  or interface properties;
- Function or method name is used to call the function or method;
- Variable name is used to read or change the value of the variable;
- Name of a module introduced as a result of import with Bind All with
  Qualified Access (see :ref:`Bind All with Qualified Access`) is used to deal
  with exported entities.

.. index::
   accessible entity
   accessibility
   scope
   function name
   method name
   value
   module
   qualified access
   import
   bind all
   entity
   export
   exported entity

|

.. _Type Declarations:

Type Declarations
*****************

.. meta:
    frontend_status: Done

An interface declaration (see :ref:`Interfaces`), a class declaration (see
:ref:`Classes`), an enum declaration (see :ref:`Enumerations`), or a type alias
(see :ref:`Type Alias Declaration`) are type declarations.

The syntax of *type declaration* is presented below:

.. code-block:: abnf

    typeDeclaration:
        classDeclaration
        | interfaceDeclaration
        | enumDeclaration
        | constEnumDeclaration
        | typeAlias
        ;

.. index::
   type declaration
   interface declaration
   class declaration
   enum declaration
   alias
   type alias
   type declaration

|

.. _Type Alias Declaration:

Type Alias Declaration
======================

.. meta:
    frontend_status: Done

Type aliases enable using meaningful and concise notations by providing the
following:

-  Names for anonymous types (array, function, and union types); or
-  Alternative names for existing types.

Scopes of type aliases are module or namespace level scopes. Names of all type
aliases must follow the uniqueness rules of :ref:`Declarations` in the current
context.

.. index::
   type alias
   anonymous type
   array
   declaration
   function
   union type
   scope
   context
   alias
   name

The syntax of *type alias* is presented below:

.. code-block:: abnf

    typeAlias:
        'type' identifier typeParameters? '=' type
        ;

Meaningful names can be provided for anonymous types as follows:

.. code-block:: typescript
   :linenos:

    type Matrix = number[][]
    type Handler = (s: string, no: number) => string
    type Predicate<T> = (x: T) => boolean
    type NullishNumber = number | undefined

If the existing type name is too long, then a shorter new name can be
introduced by using type alias (particularly for a generic type).

.. code-block:: typescript
   :linenos:

    type Dictionary = Map<string, string>
    type MapOfString<T> = Map<T, string>

A type alias acts as a new name only. It neither changes the original type
meaning nor introduces a new type.

.. code-block:: typescript
   :linenos:

    type Vector = number[]
    function max(x: Vector): number {
        let m = x[0]
        for (let v of x)
            if (v > m) m = v
        return m
    }

    let x: Vector = [2, 3, 1]
    console.log(max(x)) // output: 3

.. index::
   alias
   anonymous type
   name
   type alias
   name
   generic type

Type aliases can be recursively referenced inside the right-hand side of a type
alias declaration.

In a type alias defined as ``type A = something``, *A* can be used recursively
if it is one of the following:

-  Array element type: ``type A = A[]``; or
-  Type argument of a generic type: ``type A = C<A>``.

.. code-block:: typescript
   :linenos:

    type A = A[] // OK, used as element type

    class C<T> { /*body*/}
    type B = C<B> // OK, used as a type argument

    type D = string | Array<D> // OK

Any other use including unresolvable circular references causes a
:index:`compile-time error`, because the compiler does not have enough
information about the defined alias:

.. code-block:: typescript
   :linenos:

    type E = E          // Compile-time error
    type F = string | F // Compile-time error
    type C<T> = T
    type A = C<A>       // Compile-time error


.. index::
   type alias
   alias
   recursive reference
   type alias declaration
   array element
   type argument
   generic type
   compiler

The same rules apply to a generic type alias defined as
``type A<T> = something``:

.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

    type A<T> = Array<A<T>> // OK, A<T> is used as a type argument
    type A<T> = string | Array<A<T>> // OK

    type A<T> = A<T> // Compile-time error

A :index:`compile-time error` occurs if a generic type alias is used without
a type argument:

.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

    type A<T> = Array<A> // Compile-time error

.. note::
   There is no restriction on using a type parameter *T* in the right side of
   a type alias declaration. The following code is valid:

.. code-block:: typescript
   :linenos:

    type NodeValue<T> = T | Array<T> | Array<NodeValue<T>>;

.. index::
   alias
   generic type
   type argument
   type alias
   type parameter

A type parameter of a type alias can *depend* on another type parameter
of the same generic.

.. index::
   type parameter
   generic

.. code-block:: typescript
   :linenos:

    type X<T, S extends T> = T | S

A :index:`compile-time error` occurs if a type parameter in the type parameter
section depends on itself directly or indirectly:

.. code-block:: typescript
   :linenos:

   type X<T extends T> = T // circular dependency
   type Y<T extends R, R extends T>  = T // circular dependency
   type Z<T extends R, R extends T | undefined> = T // circular dependency

|

.. _Variable and Constant Declarations:

Variable and Constant Declarations
**********************************

.. meta:
    frontend_status: Done

.. _Variable Declarations:

Variable Declarations
=====================

.. meta:
    frontend_status: Partly
    todo: arrays never have default values
    todo: raise error for non initialized arrays: let x: number[];console.log(x)
    todo: fix grammar change - ident '?' is not allowed, readonly is not here

A non-ambient *variable declaration* introduces a new variable which is in fact
a named storage location. A declared variable must be assigned an initial value
before the first usage. The initial value is assigned either as a part of the
declaration or in various forms via initialization.

The syntax of *variable declarations* is presented below:

.. code-block:: abnf

    variableDeclarations:
        'let' variableDeclarationList
        ;

    variableDeclarationList:
        variableDeclaration (',' variableDeclaration)*
        ;

    variableDeclaration:
        identifier ':' type initializer?
        | identifier initializer
        ;

    initializer:
        '=' expression
        ;

When a variable is introduced by a variable declaration, type ``T`` of the
variable is determined as follows:

-  ``T`` is the type specified in a type annotation (if any) of the declaration.

   - If the declaration also has an initializer, then the initializer expression
     type must be assignable to ``T`` (see :ref:`Assignability with Initializer`).

-  If no type annotation is available, then ``T`` is inferred from the
   initializer expression (see :ref:`Type Inference from Initializer`).

An ambient variable declaration (see 
:ref:`Ambient Constant or Variable Declarations`) must have *type*
but no *initializer*. Otherwise, a :index:`compile-time error` occurs.

.. index::
   variable declaration
   declaration
   name
   named store location
   variable
   type annotation
   initialization
   initializer expression
   assignability
   inference
   annotation
   inference
   variable declaration
   value
   declaration

.. code-block:: typescript
   :linenos:

    let a: number // OK
    let b = 1 // OK, type 'int' is inferred
    let c: number = 6, d = 1, e = "hello" // OK

    // OK, type of lambda and type of 'f' can be inferred
    let f = (p: number) => b + p
    let x // Compile-time error, either type or initializer

Every variable in a program must have an initial value before it can be used:

- If the *initializer* of a variable is specified explicitly, then its
  execution produces the initial value for this variable.

- Otherwise, the following situations are possible:

   + If the type of a variable is ``T``, and ``T`` has a *default value*
     (see :ref:`Default Values for Types`), then the variable is initialized
     with the default value.
   + If a variable has no default value, then its value must be set by the
     :ref:`Simple Assignment Operator` before any use of the variable.

.. index::
   value
   method parameter
   function parameter
   method
   default value
   assignment operator
   assignment
   function
   initializer
   initialization
   cyclic dependency
   variable
   initializer expression
   non-initialized variable

|

.. _Constant Declarations:

Constant Declarations
=====================

.. meta:
    frontend_status: Done

A *constant declaration* introduces a named variable with a mandatory
explicit value. The value of a constant cannot be changed by an assignment
expression (see :ref:`Assignment`). If the constant is an object or array, then
object fields or array elements can be modified.

The syntax of *constant declarations* is presented below:

.. code-block:: abnf

    constantDeclarations:
        'const' constantDeclarationList
        ;

    constantDeclarationList:
        constantDeclaration (',' constantDeclaration)*
        ;

    constantDeclaration:
        identifier (':' type)? initializer
        ;

The type ``T`` of a constant declaration is determined as follows:

-  If ``T`` is the type specified in a type annotation (if any) of the
   declaration, then the initializer expression must be assignable to
   ``T`` (see :ref:`Assignability with Initializer`).
-  If no type annotation is available, then ``T`` is inferred from the
   initializer expression (see :ref:`Type Inference from Initializer`).

.. index::
   constant declaration
   variable
   constant
   value
   assignment expression
   object
   array
   type
   constant declaration
   type annotation
   inferred type
   initializer expression
   type inference

.. code-block:: typescript
   :linenos:

    const a: number = 1 // OK
    const b = 1 // OK, int type is inferred
    const c: number = 1, d = 2, e = "hello" // OK
    const x // Compile-time error, initializer is mandatory
    const y: number // Compile-time error, initializer is mandatory

|

.. _Validity of Initializer:

Validity of Initializer
=======================

.. meta:
    frontend_status: None

If a variable or constant initializer expression refers to a variable or to a
constant, and the declaration of that variable or constant is textually located
after the current declaration, then a :index:`compile-time error` occurs.


.. code-block:: typescript
   :linenos:

    const a: number = b // Compile-time error
    let   b = 1
    let   c: number = d // Compile-time error
    const d = 123


|

.. _Assignability with Initializer:

Assignability with Initializer
==============================

.. meta:
    frontend_status: Done

If a variable or constant declaration contains type annotation ``T`` and
initializer expression *E*, then the type of *E* must be assignable to ``T``
(see :ref:`Assignability`).

.. index::
   initializer expression
   assignment-like contexts
   annotation
   constant declaration
   type
   assignability
   type annotation

|

.. _Type Inference from Initializer:

Type Inference from Initializer
===============================

.. meta:
    frontend_status: Done

The type of a declaration that contains no explicit type annotation is inferred
from the initializer expression as follows:

-  In a variable declaration (not in a constant declaration, though), if the
   initializer expression is of a literal type, then the literal type is
   replaced with its supertype, if any (see :ref:`Subtyping for Literal Types`).
   If the initializer expression is of a union type that contains literal types,
   then each literal type is replaced with its supertype (see
   :ref:`Subtyping for Literal Types`), and then normalized (see
   :ref:`Union Types Normalization`).

-  Otherwise, type of a declaration is inferred from its initializer
   expression.

-  Type of an expression with ternary operator ``condition ? expr1 : expr2``
   (see :ref:`Ternary Conditional Expressions`) is inferred as follows:   

   - If ``condition`` can be evaluated at compile time, then the type of the
     entire expression is inferred from ``expr1`` (where ``condition`` is
     ``true``) or ``expr2`` (where ``condition`` is ``false``) in accordance
     with the rules above.

   - Otherwise, type of the ternary expression is a normalized union of
     the inferred types of ``expr1`` and ``expr2``.

If type of an initializer expression cannot be inferred, then a
:index:`compile-time error` occurs.

.. index::
   type
   declaration
   annotation
   type inference
   initializer
   subtyping
   supertype
   type inference
   inferred type
   type annotation
   initializer expression
   literal type

.. code-block:: typescript
   :linenos:

    // Get boolean value unknown at compile time
    function cond(): boolean { return Math.random() < 0.5 ? true : false; }

    let a = null                // Type of 'a' is null
    let aa = undefined          // Type of 'aa' is undefined
    let arr = [null, undefined] // Type of 'arr' is (null | undefined)[]

    let b = cond() ? 1 : 2    // Type of 'b' is int

    let c = cond() ? 3 : 3.14 // Type of 'c' is int | double
    let c1 = true ? 3 : 3.14  // Type of 'c1' is int
    let c2 = false ? 3 : 3.14 // Type of 'c1' is double

    let d = cond() ? "one" : "two" // Type of 'd' is string

    let e = cond() ? 1 : "one" // Type of 'e' is int | string
    let e1 = true ? 1 : "one"  // Type of 'e1' is int
    let e2 = false ? 1 : "one" // Type of 'e2' is string

    const bb  = cond() ? 1 : 2     // Type of 'bb' is int

    const cc  = cond() ? 1 : 3.14  // Type of 'cc' is int | double
    const cc1 = true   ? 1 : 3.14  // Type of 'cc1' is int
    const cc2 = false  ? 1 : 3.14  // Type of 'cc2' is double

    const dd  = cond() ? "one" : "two" // Type of 'dd'  is "one" | "two"
    const dd1 = true   ? "one" : "two" // Type of 'dd1' is "one"
    const dd2 = cond() ? "one" : "two" // Type of 'dd2' is "two"

    const ee = cond() ? 1 : "one" // Type of 'ee' is int | "one"

    let f = {name: "aa"} // Compile-time error, type of object literal is not inferred

    let   x1 = 1 // Type of 'x1' is int
    const x2 = 1 // Type of 'x2' is int

    let   s1 = "1" // Type of 's1' is string
    const s2 = "1" // Type of 's2' is "1"

.. note::

    The presence of an initializer for 
    :ref:`Ambient Constant or Variable Declarations`
    causes a :index:`compile-time error`.

|

.. _Function Declarations:

Function Declarations
*********************

.. meta:
    frontend_status: Done

*Function declarations* specify names, signatures, and bodies when
introducing *named functions*. An optional function body is a block
(see :ref:`Block`).

The syntax of *function declarations* is presented below:

.. code-block:: abnf

    functionDeclaration:
        modifiers? 'function' identifier
        typeParameters? signature block?
        ;

    modifiers:
        'native' | 'async'
        ;

Functions must be declared on the top level (see :ref:`Top-Level Statements`).

If a function is declared *generic* (see :ref:`Generics`), then its type
parameters must be specified.

The modifier ``native`` indicates that the function is a *native function* (see
:ref:`Native Functions` in Experimental Features). If a *native function* has a
body, then a :index:`compile-time error` occurs.

Functions with the modifier ``async`` are discussed in :ref:`Async Functions`.

.. index::
   function declaration
   name
   signature
   named function
   function body
   block
   body
   function call
   native function
   generic function
   type parameter
   top-level statement

|

.. _Signatures:

Signatures
==========

.. meta:
    frontend_status: Done

A signature defines parameters and the return type (see :ref:`Return Type`)
of a function, method, or constructor.

The syntax of *signature* is presented below:

.. code-block:: abnf

    signature:
        '(' parameterList? ')' returnType?
        ;

.. index::
   signature
   parameter
   return type
   function
   method
   constructor

|

.. _Parameter List:

Parameter List
==============

.. meta:
    frontend_status: Partly
    todo: change parser as grammar rules, are changed - rest can be after optional, annotation for rest

A signature can contain a *parameter list* that specifies an identifier of
each parameter name, and the type of each parameter. The type of each
parameter must be defined explicitly. If the *parameter list* is omitted, then
the function or the method has no parameters.

The syntax of *parameter list* is presented below:

.. code-block:: abnf

    parameterList:
        parameter (',' parameter)* (',' restParameter)? ','?
        | restParameter ','?
        ;

    parameter:
        annotationUsage? (requiredParameter | optionalParameter)
        ;

    requiredParameter:
        identifier ':' type
        ;
    optionalParameter:
        identifier ':' type '=' expression
        | identifier '?' ':' type
        ;

If a parameter is *required*, then each function or method call must contain
an argument corresponding to that parameter. :ref:`Optional parameters` are
described in a separate section. The function below has *required parameters*:

.. code-block:: typescript
   :linenos:

    function power(base: number, exponent: number): number {
      return Math.pow(base, exponent)
    }
    power(2, 3) // both arguments are required in the call

Several parameters can be *optional*, allowing to omit
corresponding arguments in a call (see :ref:`Optional Parameters`).

A :index:`compile-time error` occurs if an *optional parameter* precedes a
*required parameter*.

The last parameter of a function or a method can be a single *rest parameter*
(see :ref:`Rest Parameter`).

.. index::
   signature
   parameter list
   identifier
   parameter name
   type
   function
   method
   method call
   parameter
   rest parameter
   argument
   required parameter
   optional parameter
   prefix readonly

If a parameter type is prefixed with ``readonly``, then there are additional
restrictions on the parameter as described in :ref:`Readonly Parameters`.

|

.. _Readonly Parameters:

Readonly Parameters
===================

.. meta:
    frontend_status: Done

If the parameter type is ``readonly`` array or tuple type, then
no assignment and no function or method call can modify
elements of this array or tuple.
Otherwise, a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    function foo(array: readonly number[], tuple: readonly [number, string]) {
        let element = array[0] // OK, one can get array element
        array[0] = element // Compile-time error, array is readonly

        element = tuple[0] // OK, one can get tuple element
        tuple[0] = element // Compile-time error, tuple is readonly
    }

Any assignment of readonly parameters and variables must follow the limitations
stated in :ref:`Type of Expression`.

.. index::
   readonly parameter
   parameter type
   prefix readonly
   array type
   tuple type
   array
   assignment
   conversion

|

.. _Optional Parameters:

Optional Parameters
===================

.. meta:
    frontend_status: Done

*Optional parameters* can be of two forms as follows:

.. code-block:: abnf

    optionalParameter:
        identifier ':' type '=' expression
        | identifier '?' ':' type
        ;

The first form contains an ``expression`` that specifies a *default value*.
It is called *parameter with default value*, and acts as an optional parameter
of the type of a function and of its call sites. If a corresponding argument
value is ``undefined`` (i.e., a parameter is omitted, or ``undefined`` is
passed explicitly), then the default value is used:

.. index::
   optional parameter
   expression
   default value
   parameter with default value
   argument
   function call
   method call

.. code-block:: typescript
   :linenos:

    function pair(x: number, y: number = 7)
    {
        console.log(x, y)
    }
    pair(1, 2) // prints: 1 2
    pair(1) // prints: 1 7
    pair(1, undefined) // prints: 1 7

.. note::
   *undefined* passed as an argument does not affect the *type* of the
   parameter in a function, a method, or a constructor body.

The second form is a short-cut notation and ``identifier '?' ':' type``
effectively means that ``identifier`` has type ``T | undefined`` with the
default value ``undefined``.

.. index::
   notation
   undefined
   default value
   identifier

For example, the following two functions can be used in the same way:

.. code-block:: typescript
   :linenos:

    function hello1(name: string | undefined = undefined) {}
    function hello2(name?: string) {}

    hello1() // 'name' has 'undefined' value
    hello1("John") // 'name' has a string value
    hello2() // 'name' has 'undefined' value
    hello2("John") // 'name' has a string value

    function foo1 (p?: number) {}
    function foo2 (p: number | undefined = undefined) {}

    foo1()  // 'p' has 'undefined' value
    foo1(5) // 'p' has a numeric value
    foo2()  // 'p' has 'undefined' value
    foo2(5) // 'p' has a numeric value

|

.. _Rest Parameter:

Rest Parameter
==============

.. meta:
    frontend_status: Done

*Rest parameters* allow functions, methods, constructors, or lambdas to take
arbitrary numbers of arguments. *Rest parameters* have the ``spread`` operator
``'...'`` as a prefix before the parameter name.

.. note::
   The ``spread`` operator ``'...'`` is also used as a prefix in *spread
   expressions* in |LANG|. The concepts *rest parameter* and *spread expression*
   are syntactically similar as a result. The difference between the two is
   clarified in :ref:`Spread Expression`.


The syntax of *rest parameter* is presented below:

.. code-block:: abnf

    restParameter:
        annotationUsage? '...' identifier ':' type
        ;

A :index:`compile-time error` occurs if a *rest parameter*:

-  Is followed by a parameter, which is not a *rest parameter* ;
-  Has a type that is not an array type, a tuple type, nor a type
   parameter constrained by an array or a tuple type.

A call of entity with a *rest parameter* of array type ``T[]``
(or ``FixedArray<T>``) can accept any number of arguments
of types that are assignable (see :ref:`Assignability`) to ``T``:

.. index::
   rest parameter
   function
   method
   constructor
   lambda
   spread operator
   prefix
   parameter name
   syntax
   parameter list
   array type
   tuple type
   assignability
   argument

.. code-block:: typescript
   :linenos:

    function sum(...numbers: number[]): number {
      let res = 0
      for (let n of numbers)
        res += n
      return res
    }

    sum() // returns 0
    sum(1) // returns 1
    sum(1, 2, 3) // returns 6

If an argument of array type ``T[]`` is to be passed to a call of entity
with the *rest parameter*, then the spread expression (see
:ref:`Spread Expression`) must be used with the ``spread`` operator ``'...'``
as a prefix before the array argument:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    function sum(...numbers: number[]): number {
      let res = 0
      for (let n of numbers)
        res += n
      return res
    }

    let x: number[] = [1, 2, 3]
    sum(...x) // spread an array 'x'
       // returns 6

.. index::
   argument
   prefix
   spread operator
   spread expression
   function
   array argument
   array type

A call of entity with a *rest parameter* of tuple type
[``T``:sub:`1` ``, ..., T``:sub:`n`] can accept only ``n`` arguments of types
that are assignable (see :ref:`Assignability`) to the corresponding
``T``:sub:`i`:

.. index::
   call
   rest parameter
   tuple type
   type
   argument
   assignability

.. code-block:: typescript
   :linenos:

    function sum(...numbers: [number, number, number]): number {
      return numbers[0] + numbers[1] + numbers[2]
    }

    sum()          // Compile-time error, wrong number of arguments, 0 instead of 3
    sum(1)         // Compile-time error, wrong number of arguments, 1 instead of 3
    sum(1, 2, "a") // Compile-time error, wrong type of the 3rd argument
    sum(1, 2, 3)   // returns 6

It is legal though meaningless to declare a function with an optional
parameter followed by a *rest parameter* of a tuple type.
However, using such a function without explicitly set optional and
*rest parameters* causes compile-time error:

.. code-block:: typescript
   :linenos:

    // optional tuple + rest tuple
    function g(opt?: [number, string], ...tail: [number,string]) { // OK
       // ...
    }

    g() // Compile-time error, no rest tuple
    g([1, "str"]) // Compile-time error, no rest tuple
    g([ 1, "str"], 1, "str") // OK

If an argument of tuple type [``T``:sub:`1` ``, ..., T``:sub:`n`]
is to be passed to a call of entity with the rest parameter,
then a spread expression (see :ref:`Spread Expression`)
must have the ``spread`` operator ``'...'`` as a
prefix before the tuple argument:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    function sum(...numbers: [number, number, number]): number {
      return numbers[0] + numbers[1] + numbers[2]
    }

    let x: [number, number, number] = [1, 2, 3]
    sum(...x) // spread tuple 'x'
       // returns 6

.. index::
   optional parameter
   tuple type
   entity
   argument
   prefix
   spread expression
   function
   rest parameter
   tuple argument
   spread operator

If an argument of fixed-size array type ``FixedArray<T>`` is to be passed to a
function or a method with the rest parameter, then the spread expression (see
:ref:`Spread Expression`) must be used with the ``spread`` operator ``'...'``
as a prefix before the fixed-size array argument:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    function sum(...numbers: Array<number>): number {
      let res = 0
      for (let n of numbers)
        res += n
      return res
    }

    let x: FixedArray<number> = [1, 2, 3]
    sum(...x) // spread an fixed-size array 'x'
       // returns 6


If constrained by an array or a tuple type, a type parameter can be used with
generics as a *rest parameter*.

.. code-block:: typescript
   :linenos:

    function sum<T extends Array<number>>(...numbers: T): number {
      let res = 0
      for (let n of numbers)
        res += n
      return res
    }

.. note::
   Any call to a function, method, constructor, or lambda with a rest
   parameter implies that a new array or tuple is created from the arguments
   provided.

.. code-block:: typescript
   :linenos:

    function rest_array(...array_parameter: number[]) {
       // array_parameter is a new array created from the arguments passed
       array_parameter[0] = 1234
       console.log (array_parameter[0]) // 1234 is the output
    }
    function rest_tuple(...tuple_parameter: [number, string]) {
       // tuple_parameter is a new tuple created from the arguments passed
       tuple_parameter[0] = 1234
       console.log (tuple_parameter[0]) // 1234 is the output
    }

    const array_argument: number[] =  [1,2,3,4]
    const tuple_argument: [number, string] =  [1,"234"]

    console.log (array_argument[0], tuple_argument[0]) // 1 1 is the output

    rest_array (...array_argument)
         // array_argument is spread into a sequence of its elements

    rest_tuple (...tuple_argument)
         // tuple_argument is spread into a sequence of its elements

    console.log (array_argument[0], tuple_argument[0]) // 1 1 is the output


.. index::
   argument
   fixed-size array type
   rest parameter
   prefix
   spread operator
   spread expression
   function
   method
   fixed-size array argument


|

.. _Shadowing by Parameter:

Shadowing by Parameter
======================

.. meta:
    frontend_status: Done

If the name of a parameter is identical to the name of a top-level variable
accessible (see :ref:`Accessible`) within the body of a function or a method
with that parameter, then the name of the parameter shadows the name of the
top-level variable within the body of that function or method:

.. code-block:: typescript
   :linenos:

    let x: number = 1
    function foo (x: string) {
        // 'x' refers to the parameter and has type string
    }
    class SomeClass {
      method (x: boolean) {
        // 'x' refers to the method parameter and has type boolean
      }
    }
    x++ // 'x' refers to the global variable

.. index::
   shadowing
   parameter
   accessibility
   access
   top-level variable
   access
   function body
   method body
   name
   function
   method
   function parameter
   method parameter
   boolean type

|

.. _Return Type:

Return Type
===========

.. meta:
    frontend_status: Done

A function, a method, or a lambda return type defines the resultant type of the
function, method, or lambda execution (see :ref:`Function Call Expression`,
:ref:`Method Call Expression`, and :ref:`Lambda Expressions`). During the
execution, the function, method, or lambda can produce a value of a type
that is assignable to the return type (see :ref:`Assignability`).

The syntax of *return type* is presented below:

.. code-block:: abnf

    returnType:
        ':' (type | 'this')
        ;

If a function, a method, or a lambda return type is other than ``void`` or 
``undefined`` (see :ref:`Type void or undefined`), or than a union type
containing ``void`` or ``undefined``, and the execution path in the function,
method, or lambda body has neither a ``return`` statement (see
:ref:`Return Statements`) nor a ``throw`` statement (see
:ref:`Throw Statements`), then a :index:`compile-time error` occurs. 

If a function, a method, or a lambda return type is ``never`` (see
:ref:`Type never`), and there is an execution path in which all statements
execute normally (see :ref:`Normal and Abrupt Statement Execution`), then a
:index:`compile-time error` occurs.

A special form of return type with the keyword ``this`` as type annotation can
be used in class instance methods only (see :ref:`Methods Returning this`).

If a function, a method, or a lambda return type is not specified, then it is
inferred from its body (see :ref:`Return Type Inference`). If there is no body,
then the function, method, or lambda return type is ``void`` (see
:ref:`Type void or undefined`).


.. code-block:: typescript
   :linenos:

    function foo1 (): number {}  // Compile-time error, return or throw missing
    let foo2 =  (): number => {} // Compile-time error, return or throw missing

    function foo3 (): undefined {}  // OK, it returns 'undefined' value
    let foo4 =  (): undefined => {} // OK, it returns 'undefined' value

    function foo5 (): never {}  // Compile-time error, no throw or return never type function call
    let foo6 =  (): never => {} // Compile-time error, no throw or return never type function call

    function foo7 (): void {}  // OK, it returns undefined value
    let foo8 =  (): void => {} // OK, it returns undefined value

    function foo9 () {}   // OK, return type is void and return value is 'undefined'
    let foo10 =  () => {} // OK, return type is void and return value is 'undefined'


.. index::
   return type
   function
   method
   lambda
   function call
   function call expression
   method call expression
   lambda expression
   static type
   assignable type
   assignability
   return statement
   syntax
   method body
   type void
   execution path
   return statement
   inferred type
   type inference
   void type
   never type
   this keyword
   type annotation
   class instance method


|

.. raw:: pdf

   PageBreak
