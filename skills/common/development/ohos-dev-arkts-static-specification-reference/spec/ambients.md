Ambient Declarations
####################

.. meta:

*Ambient declaration* specifies an entity declared elsewhere but usable in the
current context.

Ambient declarations:

-  Provide type information for entities declared elsewhere.
-  Introduce no new entities like regular declarations do.
-  Cannot include executable code, and thus 

   - Ambient variables, constants, and enumerations have no initializers;
   - Ambient functions, methods, and constructors have no bodies.

The syntax of *ambient declaration* is presented below:

.. code-block:: abnf

    ambientDeclaration:
        'declare'
        ( ambientConstantOrVariableDeclaration
        | ambientFunctionDeclaration
    ...

A :index:`compile-time error` occurs if the modifier ``declare`` is used in a
context that is already ambient:

.. code-block:: typescript
   :linenos:

    declare namespace A{
        declare function foo(): void // Compile-time error
    }

*Ambient declaration* by itself does not guarantee that non-ambient declartion
declared elsewhere for the same name entity is identical to the ambient one. 
By its nature, any *ambient declaration* is a requirement only that the build
system (see :ref:`Build System`) provides a proper non-ambient declaration.

Ambient Constant or Variable Declarations
*****************************************

.. meta:

The syntax of *ambient* constant or variable declarations is presented below:

.. code-block:: abnf

    ambientConstantOrVariableDeclaration:
        'const'|'let' ambientConstantOrVariableList ';'
        ;

    ...

An *ambient constant* and *variable declaration* must have an explicit type
annotation, and must have no initializer. Otherwise,
a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    declare let v1: number // OK
    declare let v2 = 1     // Compile-time error, ambient variable must have no initializer

    declare const c1: number // OK
    declare const c2 = 1     // Compile-time error, ambient constant must have no initializer

Ambient Function Declarations
*****************************

.. meta:

The syntax of *ambient function declaration* is presented below:

.. code-block:: abnf

    ambientFunctionDeclaration:
        'function' identifier typeParameters? signature
        ;

A :index:`compile-time error` occurs if an ambient function declaration has the
following:

- No explicit return type specified;
- A parameter with the default value;
- A function body, or;
- Modifier ``async`` specified.

Examples below illustrate that:

.. code-block:: typescript
   :linenos:

    declare function ok1(x: number): void // OK
    declare function bad1(x: number) // Compile-time error, no return specified

    declare function ok2(x?: string): void // OK, optional parameters can be used
    declare function bad2(y: number = 1): void // Compile-time error, parameter
                                               // has default value

    declare function bad3(): void {} // Compile-time error, function body provided

    declare async function bad4(): void // Compile-time error, async modifier is used 

Ambient Overload Function Declarations
**************************************

.. meta:

The syntax of *ambient overload function declaration* is identical to that of
:ref:`Explicit Function Overload`. The semantics of such declarations is
defined by the same rules.

.. code-block:: typescript
   :linenos:

   // Top-level functions are overloaded
   declare function foo1(p: string): void
   declare function foo2(p: number): void
   declare overload foo {foo1, foo2}

   // Namespace functions are overloaded
   declare namespace N {
      function foo1(p: string): void
      function foo2(p: number): void
      overload foo {foo1, foo2}
   }

   // All calls are valid
   foo("a string")
   foo(5)
   N.foo("a string")
   N.foo(5)

Ambient Class Declarations
**************************

.. meta:

The syntax of *ambient class declaration* is presented below:

.. code-block:: abnf

    ambientClassDeclaration:
        'class'|'struct' identifier typeParameters?
        classExtendsClause? implementsClause?
        '{' ambientClassMember* '}'
    ...

Ambient field declarations have no initializers.

The syntax of *ambient field declaration* is presented below:

.. code-block:: abnf

    ambientFieldDeclaration:
        ambientFieldModifier* identifier ':' type
        ;

    ...

Ambient constructor, method, and accessor declarations have no bodies.

Their syntax is presented below:

.. code-block:: abnf

    ambientConstructorDeclaration:
        'constructor' parameters
        ;

    ...

Ambient methods can be overloaded similarly to non-ambient methods with the
same syntax and semantics (see :ref:`Explicit Class Method Overload`).

.. code-block:: typescript
   :linenos:

   // Class methods are overloaded
   declare class A {
      foo1(p: string): void
      foo2(p: number): void
      overload foo {foo1, foo2}
   }

   // All methods calls are valid
   function demo (a: A) {
      a.foo("a string")
      a.foo(5)
   }

Ambient Indexer
===============

.. meta:

*Ambient indexer declarations* specify the indexing of a class instance
in an ambient context. The feature is provided for |TS| compatibility:

The syntax of *ambient indexer declaration* is presented below:

.. code-block:: abnf

    ambientIndexerDeclaration:
        'readonly'? '[' identifier ':' type ']' returnType
        ;

The use of *ambient indexer declarations* is represented in the example below:

.. code-block:: typescript
   :linenos:

    declare class C {
        [index: number]: number
    }
    declare class D {
        [index: int]: C
    }
    declare class E {
        [index: string]: string
    }

The following restrictions apply:

- Only one *ambient indexer declaration* is allowed in an ambient class declaration.

- *Ambient indexer declaration* is supported in ambient contexts only.
  If written in ArkTS, ambient class implementation must conform to
  :ref:`Indexable Types`.

Ambient Call Signature
======================

.. meta:

*Ambient call signature* declarations are used to specify *callable types*
in an ambient context. The feature is provided for |TS| compatibility:

The syntax of *ambient call signature declaration* is presented below:

.. code-block:: abnf

    ambientCallSignatureDeclaration:
        signature
        ;

.. code-block:: typescript
   :linenos:

    declare class C {
        (someArg: number): boolean
        (someArg: string): boolean
        ...
    }

*Ambient class signature declaration* is supported in ambient contexts
only. If written in ArkTS, ambient class implementation must conform to
:ref:`Callable Types with $_invoke Method`.
   
Multiple *ambient call signatures* are allowed in an ambient class declaration
provided that they are distinct (see :ref:`Declaration Distinguishable by Signatures`).
Multiple distinct ambient call signatures are represented in the following
example:

.. code-block:: typescript
   :linenos:

   // sdk_file.d.ets, declaration file
   export declare class C {
      (x: string): void
      (x: number): void
   }

   // sdk_file.ets, implementation file
   export class C {
      static $_invoke(x: string): void {
         console.log('string')
      }
      static $_invoke(x: number): void {
         console.log('number')
      }
   }

   // app.ets
   import { C } from './sdk_file'

   C(123)    // log: number
   C('abc')  // log: string

Ambient Iterable
================

.. meta:

*Ambient iterable declaration* indicates that a class instance is iterable
in an ambient context. The feature is provided for |TS| compatibility:

The syntax of *ambient iterable declaration* is presented below:

.. code-block:: abnf

    ambientIterableDeclaration:
        '[Symbol.iterator]' '(' ')' returnType
        ;

The following restrictions apply:

- *returnType* must be a type that implements ``Iterator`` interface defined
  in :ref:`Standard Library`.
- Only one *ambient iterable declaration* is allowed in an ambient class
  declaration.

.. code-block:: typescript
   :linenos:

    declare class C {
        [Symbol.iterator] (): CIterator
    }

.. note::
   *Ambient iterable declaration* is supported in ambient contexts only.
   If written in ArkTS, ambient class implementation must conform to
   :ref:`Iterable Types`.

Ambient Interface Declarations
******************************

.. meta:

The syntax of *ambient interface declaration* is presented below:

.. code-block:: abnf

    ambientInterfaceDeclaration:
        'interface' identifier typeParameters?
        interfaceExtendsClause?
        '{' ambientInterfaceMember* '}'
    ...

*Ambient interface* can contain additional members in the same manner as
an ambient class (see :ref:`Ambient Indexer`, and :ref:`Ambient Iterable`).

If an interface method declaration is marked with the keyword ``default``, then
a non-ambient interface must contain the default implementation for the method
as follows:

.. code-block:: typescript
   :linenos:

    declare interface I1 {
        default foo (): void // method foo will have the default implementation
    }
    class C1 implements I1 {} // Class C1 is valid as foo() has the default implementation

    interface I1 {
        // If such interface is used as I1 it will be runtime error as there is
        // no default implementation for foo()
        foo (): void 
    }

    declare interface I2 {
        foo (): void // method foo has no default implementation
    }
    class C2 implements I2 {} // Class C2 is invalid as foo() has no implementation
    class C3 implements I2 { foo() {} } // Class C3 is valid as foo() has implementation

Ambient Enumeration Declarations
********************************

.. meta:

The syntax of *ambient enumeration declaration* is presented below:

.. code-block:: abnf

    ambientEnumDeclaration
        : 'const'? 'enum' identifier enumBaseType? '{' ambientEnumMemberList? '}'
        ;

    ...

If an *enumeration declaration* is prefixed with the keyword
``const``, then a :index:`compile-time error` occurs. This restriction
is temporary, and the semantics of ``const enum`` is to be made
available in the future versions of ArkTS.

No member of an enum declaration can have an initializer.
Otherwise, a :index:`compile-time error` occurs as represented
in the example below: 

.. code-block:: typescript
   :linenos:

    declare enum RGB {Red, Green, Blue} // OK
    
    declare enum Err1 { A = 5 }      // Compile-time error, initializer is present

Ambient Namespace Declarations
******************************

.. meta:

Namespaces are used to logically group multiple entities. ArkTS supports
*ambient namespaces* for better |TS| compatibility. |TS| often uses ambient
namespaces to specify the platform API or a third-party library API.

The syntax of *ambient namespace declaration* is presented below:

.. code-block:: abnf

    ambientNamespaceDeclaration:
        'namespace' identifier '{' ambientNamespaceElement* '}'
        ;

    ...

An *enumeration type declaration* can be prefixed with the keyword ``const``
for |TS| compatibility. The prefix has no influence on the declared type.
Only exported entities can be accessed outside a namespace.

Namespaces can be nested:

.. code-block:: typescript
   :linenos:

    declare namespace A {
        export namespace B {
            export function foo(): void;
        }
    }

A namespace is not an object but merely a scope for entities that can be
accessed by using qualified names only.

If an ambient namespace is imported from a module, then all ambient
namespace declarations are accessible (see :ref:`Accessible`) across
all declarations and top-level statements of the current module.

.. code-block:: typescript
   :linenos:

    // File1.d.ets
    export declare namespace A { // namespace itself must be exported
        function foo(): void
        type X = Array<number>
    }

    // File2.ets
    import {A} from 'File1.d.ets'

    A.foo() // Valid function call, as 'foo' is accessible for top-level statements
    function foo () {
        A.foo() // Valid function call, as 'foo' is accessible here as well
    }
    class C {
        method () {
            A.foo() // Valid function call, as 'foo' is accessible here too
            let x: A.X = [] // Type A.X can be used
        }
    }

A :index:`compile-time error` occurs if an *ambient namespace* declaration
contains an *exportDirective* that refers to a declaration which is not a part
of the namespace.

.. code-block:: typescript
   :linenos:

    export declare namespace A {
         export {foo} // Compile-time error, no 'foo' in namespace 'A'
    }
    function foo() {}

Implementing Ambient Namespace Declaration
==========================================

.. meta:

If an *ambient namespace* is implemented in ArkTS, a namespace with the
same name must be declared (see :ref:`Namespace Declarations`) as the
top-level declaration of a module. All namespace names of a nested
namespace (i.e. a namespace embedded into another namespace) must be the same
as in ambient context.

Ambient Accessor Declarations
*****************************

.. meta:
    
*Ambient accessor declaration* is an ambient version of 
:ref:`Accessor Declarations`. The syntax of an *ambient accessor declaration*
is presented below:

.. code-block:: abnf

    ambientAccessorDeclaration:
        ( 'get' identifier '(' receiverParameter? ')' returnType
        | 'set' identifier '(' (receiverParameter ',')? requiredParameter ')'
        )
        ;

A compile-time error occurs if explicit return type for an ambient getter
declaration is not specified.

.. code-block:: typescript
   :linenos:

    declare get name(): string // OK
    declare get age() // Compile-time error, return type must be specified

See :ref:`Accessor Declarations` for details.

.. raw:: pdf

   PageBreak
