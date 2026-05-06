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

.. _Classes:

Classes
#######

.. meta:
    frontend_status: Done

Class declarations introduce new reference types and describe the manner
of their implementation.

A class body contains declarations and initializer blocks.

Declarations can introduce class members (see :ref:`Class Members`) or class
constructors (see :ref:`Constructor Declaration`).

The body of the declaration of a member comprises the scope of a
declaration (see :ref:`Scopes`).

Class members include:

-  Fields,
-  Methods, and
-  Accessors.

.. index::
   class declaration
   class constructor
   reference type
   implementation
   class body
   field
   method
   accessor
   constructor
   class member
   initializer block
   scope
   declaration scope

Class members can be *declared* or *inherited*.

Every member is associated with the class declaration it is declared in.

Field, method, accessor and constructor declarations can have the following
access modifiers (see :ref:`Access Modifiers`):

-  ``Public``,
-  ``Protected``,
-  ``Private``.

Every class defines two class-level scopes (see :ref:`Scopes`): one for
instance members, and the other for static members. It means that two members
of a class can have the same name if one is static while the other is not.


.. index::
   class declaration
   declared class member
   inherited class member
   access modifier
   accessor
   method
   field
   implementing
   overriding
   superclass
   superinterface
   class-level scope
   instance member
   static member

|

.. _Class Declarations:

Class Declarations
******************

.. meta:
    frontend_status: Done

Every class declaration defines a *class type*, i.e., a new named
reference type.

The class name is specified by an *identifier* inside a class declaration.

If ``typeParameters`` are defined in a class declaration, then that class
is a *generic class* (see :ref:`Generics`).

The syntax of *class declaration* is presented below:

.. code-block:: abnf

    classDeclaration:
        classModifier? 'class' identifier typeParameters?
        classExtendsClause? implementsClause?
        classMembers
        ;

    classModifier:
        'abstract' | 'final'
        ;

.. index::
   class declaration
   class type
   identifier
   class name
   generic class

Classes with the ``final`` modifier are an experimental feature
discussed in :ref:`Final Classes`.

.. Classes with the ``sealed`` modifier are an experimental feature
   discussed in :ref:`Sealed Classes`.

The scope of a class declaration is specified in :ref:`Scopes`.

An example of a class is presented below:

.. code-block:: typescript
   :linenos:

    class Point {
      public x: number
      public y: number
      public constructor(x : number, y : number) {
        this.x = x
        this.y = y
      }
      public distanceBetween(other: Point): number {
        return Math.sqrt(
          (this.x - other.x) * (this.x - other.x) +
          (this.y - other.y) * (this.y - other.y)
        )
      }
      static origin = new Point(0, 0)
    }

.. index::
   class
   final modifier
   modifier
   final class
   class declaration
   class type
   reference type
   class name
   identifier
   generic class
   scope

|

.. _Abstract Classes:

Abstract Classes
================

.. meta:
    frontend_status: Done

A class with the modifier ``abstract`` is known as abstract class. An abstract
class is a class that cannot be instantiated, i.e., no objects of this type
can be created. It serves as a blueprint for other classes by defining common
fields and methods that subclasses must implement. Abstract classes can contain
both abstract and concrete methods.

A :index:`compile-time error` occurs if an attempt is made to create an
instance of an abstract class:

.. code-block:: typescript
   :linenos:

   abstract class X {
      field: number
      constructor (p: number) { this.field = p }
   }
   let x = new X(42)
     // Compile-time error, Cannot create an instance of an abstract class.

Subclasses of an abstract class can be abstract or non-abstract.
A non-abstract subclass of an abstract superclass can be instantiated. As a
result, a constructor for the abstract class, and field initializers
for non-static fields of that class are executed:

.. index::
   abstract class
   abstract modifier
   subclass
   superclass
   instantiation
   non-abstract class
   field initializer
   constructor
   non-static field
   class

.. code-block:: typescript
   :linenos:

   abstract class Base {
      field: number
      constructor (p: number) { this.field = p }
   }

   class Derived extends Base {
      constructor (p: number) { super(p) }
   }

A method with the modifier ``abstract`` is considered an *abstract method*
(see :ref:`Abstract Methods`). Abstract methods have no bodies, i.e., they can
be declared but not implemented.


Only abstract classes can have abstract methods. A :index:`compile-time error`
occurs if a non-abstract class has an abstract method:

.. code-block:: typescript
   :linenos:

   class Y {
     abstract method (p: string)
     /* compile-time error, Abstract methods can only
        be within an abstract class. */
   }

A :index:`compile-time error` occurs if an abstract method declaration
contains the modifiers ``final`` or ``override``.

.. code-block:: typescript
   :linenos:

   abstract class Y {
     final abstract method (p: string)
     // Compile-time error, Abstract methods cannot be final
   }


.. index::
   abstract modifier
   modifier
   abstract method
   method body
   non-abstract class
   class
   method declaration
   implementation
   abstract class
   final modifier
   override modifier

|

.. _Class Extension Clause:

Class Extension Clause
**********************

.. meta:
    frontend_status: Done

All classes except class ``Object`` can contain the ``extends`` clause that
specifies the *base class*, or the *direct superclass* of the current class.
In this situation, the current class is a *derived class*, or a
*direct subclass*. Any class, except class ``Object`` that has no ``extends``
clause, is assumed to have the ``extends Object`` clause.

.. index::
   class
   Object
   extends clause
   extends Object clause
   base class
   derived class
   direct subclass
   clause
   direct superclass
   superclass

The syntax of *class extension clause* is presented below:

.. code-block:: abnf

    classExtendsClause:
        'extends' typeReference
        ;

A :index:`compile-time error` occurs if:

-  ``typeReference`` refers directly to, or is an alias of any
   non-class type, e.g., of interface, enumeration, union, function,
   utility type, or any instantiation of ``FixedArray``.

-  ``typeReference`` names a class type that is not accessible (see
   :ref:`Accessible`).

-  ``extends`` clause appears in the declaration of the class ``Object``.

-  ``extends`` graph has a cycle.

*Class extension* implies that a class inherits all members of the direct
superclass.

.. index::
   syntax
   class
   class extension clause
   alias
   non-class type
   interface
   enumeration
   union
   function
   utility type
   accessibility
   Object
   class extension
   superclass
   direct superclass
   subclass
   superclass
   type
   class type
   class extension
   extends clause
   extends graph
   accessibility
   private member

.. note::
   Private members are inherited from superclasses, but are not accessible (see
   :ref:`Accessible`) within subclasses:

   .. code-block:: typescript
      :linenos:

       class Base {
         /* All methods are accessible in the class where
             they were declared */
         public publicMethod () {
           this.protectedMethod()
           this.privateMethod()
         }
         protected protectedMethod () {
           this.publicMethod()
           this.privateMethod()
         }
         private privateMethod () {
           this.publicMethod();
           this.protectedMethod()
         }
       }
       class Derived extends Base {
         foo () {
           this.publicMethod()    // OK
           this.protectedMethod() // OK
           this.privateMethod()   // Compile-time error,
                                  // the private method is inaccessible
         }
       }


The transitive closure of a *direct subclass* relationship is the *subclass*
relationship. Class ``A`` can be a subclass of class ``C`` if:

-  Class ``A`` is the direct subclass of ``C``; or

-  Class ``A`` is a subclass of some class ``B``,  which is in turn a subclass
   of ``C`` (i.e., the definition applies recursively).

Class ``C`` is a *superclass* of class ``A`` if ``A`` is its subclass.

.. index::
   private method
   transitive closure
   direct subclass
   subclass
   class

|

.. _Class Implementation Clause:

Class Implementation Clause
***************************

.. meta:
    frontend_status: Done

A class can implement one or more interfaces. Interfaces to be implemented by
a class are listed in the ``implements`` clause. Interfaces listed in this
clause are *direct superinterfaces* of the class.

The syntax of *class implementation clause* is presented below:

.. code-block:: abnf

    implementsClause:
        'implements' interfaceTypeList
        ;

    interfaceTypeList:
        typeReference (',' typeReference)*
        ;

If ``typeReference`` fails to name an accessible interface type (see
:ref:`Accessible`), then a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    // File1
    interface I { } // Not exported

    // File2
    class C implements I {} // Compile-time error I is not accessible

If some interface is repeated as a direct superinterface in a single
``implements`` clause (even if that interface is named differently), then all
repetitions are ignored.

.. index::
   class declaration
   class implementation clause
   implements clause
   accessible interface type
   accessibility
   interface type
   type argument
   interface
   syntax
   direct superinterface

For the class declaration ``C`` <``F``:sub:`1` ``,..., F``:sub:`n`> (:math:`n\geq{}0`,
:math:`C\neq{}Object`):

- *Direct superinterfaces* of class type ``C`` <``F``:sub:`1` ``,..., F``:sub:`n`>
  are the types specified in the ``implements`` clause of the declaration of
  ``C`` (if there is an ``implements`` clause).

For the generic class declaration ``C`` <``F``:sub:`1` ``,..., F``:sub:`n`> (*n* > *0*):

-  *Direct superinterfaces* of the parameterized class type ``C``
   < ``T``:sub:`1` ``,..., T``:sub:`n`> are all types ``I``
   < ``U``:sub:`1`:math:`\theta{}` ``,..., U``:sub:`k`:math:`\theta{}`> if:

    - ``T``:sub:`i` (:math:`1\leq{}i\leq{}n`) is a type;
    - ``I`` <``U``:sub:`1` ``,..., U``:sub:`k`> is the direct superinterface of
      ``C`` <``F``:sub:`1` ``,..., F``:sub:`n`>; and
    - :math:`\theta{}` is the substitution [``F``:sub:`1` ``:= T``:sub:`1` ``,..., F``:sub:`n` ``:= T``:sub:`n`].

.. index::
   class declaration
   direct superinterface
   type
   declaration
   implements clause
   substitution
   generic class declaration
   parameterized class type

Interface type ``I`` is a superinterface of class type ``C`` if ``I`` is one of
the following:

-  Direct superinterface of ``C``;
-  Superinterface of ``J`` which is in turn a direct superinterface of ``C``
   (see :ref:`Superinterfaces and Subinterfaces` that defines superinterface
   of an interface); or
-  Superinterface of the direct superclass of ``C``.

A class *implements* all its superinterfaces.

A :index:`compile-time error` occurs if:

- Class implements two interface types
  that represent different instantiations of the same
  generic interface (see :ref:`Generics`);

- Class field and a method inherited from one of
  its superinterfaces have the same name, except
  where either is static and the other is not.

.. index::
   class type
   direct superinterface
   superinterface
   subinterface
   interface
   superclass
   class
   interface type
   instantiation
   generic interface

If a class is not *abstract*, then the following conditions must be met:

- Methods of a superinterface have implementation bodies
  that can be defined either in the class itself, or in its superclass
  or superinterface (see :ref:`Overriding in Classes` for detail);

- Required properties of superinterfaces are implemented
  (see :ref:`Implementing Required Interface Properties`).

- Otherwise, a :index:`compile-time error` occurs.

An optional property from a superinterface can be implemented or implicitly
defined (see :ref:`Implementing Optional Interface Properties`).

|

.. _Implementing Required Interface Properties:

Implementing Required Interface Properties
==========================================

.. meta:
    frontend_status: Partly
    todo: process last changes (see table) class field is always a field

A class must implement all required properties from all superinterfaces (see
:ref:`Interface Properties`) that can be defined as one of the following:

- Field,
- Readonly field,
- Getter,
- Setter, or
- Both a getter and a setter.

The following table summarizes all valid variants of implementation, and
a :index:`compile-time error` occurs for any other combinations:

   =========================== ======================================================
   Form of Interface Property  Implementation in a Class
   =========================== ======================================================
   field                       field, or getter and setter
   readonly field              readonly field, field, getter, or getter and setter
   getter only                 readonly field, field, getter, or getter and setter
   setter only                 field, setter, or setter and getter
   getter and setter           field, or getter and setter
   =========================== ======================================================

If a class field is used to implement an interface property in any form, then:

- The field is represented as an instance data member
  (see :ref:`Field Declarations`);

- Accessing the field via a class instance always means accessing
  an ordinary class field;

- Accessing a property via a reference of an interface type always means calling
  a getter or a setter;

- If an interface property is defined in a field form, then a getter and
  a setter (if the property is not ``readonly``) are generated implicitly
  in the class by the compiler.

This is represented in the following example:

.. code-block:: typescript
   :linenos:

    interface I {
        n: number
    }
    class C implements I {
        n: number = 1 // property is implemented as a field
    }
    let c = new C()
    console.log(c.n) // class field read
    c.n = 1 // class field write

    let i: I = c
    console.log(c.n) // implicitly generated getter is called
    i.n = 2          // implicitly generated setter is called

Getter and setter generated implicitly look as follows:

.. code-block:: typescript

    get n(): number  { return this.n }
    set n(x: number) { this.n = x }

.. note::

    - ``this.n`` in the pseudocode above is generated to provide
      access to the class field but not as a call to a getter or a
      setter;

    - Attempting to explicitly declare a getter or a setter with the same name
      as a field causes a :index:`compile-time error` because class members
      must be *distinguishable* (see :ref:`Declarations`).

An interface property implemented as an accessor or accessors is represented in
the example below:

.. code-block:: typescript
   :linenos:

    interface I {
        n: number
        readonly r: string
    }
    class C implements I {
        // 'n' is explicitly implemented as getter and setter
        get n(): number  { return 1 }
        set n(x: number) { /*some body*/ }
        // 'r' is explicitly implemented as getter
        get r(): string { return "abc" }
        // a setter can be defined for 'r', but it is not mandatory
        set r(x: string) { /*some body*/ }
    }

A :index:`compile-time error` occurs if:

    - Interface property is ``readonly``, and the getter is not defined;
    - Interface property is not ``readonly``, and either a getter or a setter
      is not defined.

The errors are represented in the example below:

.. code-block:: typescript
   :linenos:

    interface I {
        n: number
    }
    class A implements I { // Compile-time error, setter is not defined
        get n(): number  { return 1 }
    }
    class B implements I { // Compile-time error, getter is not defined
        set n(x: number)  {}
    }
    class C implements I {
        get n(): string { return "aa" } // Compile-time error, wrong type
    }

    interface J {
        readonly r: string
    }
    class D implements J { // Compile-time error, getter is not defined
        set r(x: string) {}
    }

If an interface property is defined in the form of an accessor
(a getter, a setter, or both) and implemented by a class field, then
implicit accessor bodies are generated in the class but only for accessors
defined in the interface. The situation is represented below:

.. code-block:: typescript
   :linenos:

    interface I {
      get n(): number
    }
    class C implements I {
        n: number = 1 // property is implemented as a field
        // getter body is implicitly generated
        // setter is not defined and not generated
    }

    function foo(i: I) {
      console.log(i.n) // OK, getter is used
      i.n = 1 // Compile-time error, setter is not defined
    }

    interface J {
      get n(): number
      set n(x: number)
    }
    class D implements J {
        n: number = 1 // property is implemented as a field
        // getter body is implicitly generated
        // setter body is implicitly generated
    }

    function bar(j: J) {
      console.log(j.n) // OK, getter is used
      j.n = 1          // OK, setter is used
    }

A :index:`compile-time error` occurs if **all** of the following conditions
are fulfilled:

    - Interface defines both a getter and a setter that have the same name;
    - Class implements a property by a field;
    - Return type of a getter and parameter type of a setter are not of the
      same type.

This situation is represented by the example below:

.. code-block:: typescript
   :linenos:

    interface J {
      get n(): number
      set n(x: string)
    }
    class D implements J {
        n: number = 1 // Compile-time error, types mismatch
    }

If a property defines both a getter and a setter of different types,
then the property can be implemented by accessors:

.. code-block:: typescript
   :linenos:

    interface J {
      get n(): number
      set n(x: string)
    }

    class E implements J {
      value: string = ""
      get n(): number  { return Number.parseFloat(this.value) }
      set n(x: string) { this.value = x }
    }

    let e = new E
    e.n = "123"
    console.log(e.n)

If a superclass implements an interface property, then all derived classes
inherit the property in the same form. A :index:`compile-time error` occurs
on an attempt to do one of the following:

    - Overriding a superclass field by an accessor or accessors;
    - Overriding a superclass accessor by a field.

Such error situations are represented by the example below:

.. code-block:: typescript
   :linenos:

    interface I {
        n: number
    }
    class C implements I {
        n: number = 1
    }
    class C1 extends C {
        get n(): number { return 1 } // Compile-time error, 'n' cannot be overridden by an accessor
    }

    class D implements I {
        get n(): number { return 1 }
        set n(x: number) {}
    }
    class D1 extends D {
        n: number = 2 // Compile-time error, 'n' cannot be overridden by a field
    }

A field that implements an interface property can override a field of the same
type defined in a superclass:

.. code-block:: typescript
   :linenos:

    interface I {
        n: number
    }
    class A {
        n: number = 1
    }
    class C extends A implements I {
        n: number = 2 // OK, 'n' overrides 'n' from A and implements 'n' from I
    }

If types mismatch as represented in the example below, then a
:index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    interface I {
        n: number
    }
    interface J {
        n: string
    }
    class A implements I, J { // Compile-time error, types mismatch
    }

    class B {
        n: string = "aa"
    }
    class C extends B implements I { // Compile-time error, types mismatch
    }

    class C implements I {
        get n(): string { return "aa" } // Compile-time error, types mismatch
    }

If a property is defined as ``readonly``, then the implementation of
the property can be ``readonly`` or not ``readonly`` as follows:

.. code-block:: typescript
   :linenos:

    interface I {
        readonly r: number
    }
    class A implements I {
        r: number = 0 // OK, the field is writeable
    }
    class B implements I {
        readonly r: number = 1  // OK, the field is readonly
    }

    function foo(i: I) {
        i.r = 42 // Compile-time error, 'r' is readonly
        if (i instanceof A) {
            i.r = 42 // OK, here 'i' is of type A, and 'r' is writeable
        }
        if (i instanceof B) {
         i.r = 42 // Compile-time error, here 'i' is of type B, and 'r' is readonly
        }
    }

If a writeable interface property is implemented as ``readonly`` as represented
in the example below, then a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    interface I {
        r: number
    }
    class C implements I {
        readonly r: number = 1 // Compile-time error
    }

    interface J {
        readonly r: number
    }
    class D implements I, J {
        readonly r: number = 1 // Compile-time error
    }
    class E implements I, J {
        r: number = 1 // OK
    }

If no implementation for the property is provided, then a
:index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    interface I {
        property: number
    }
    class C implements I { // Compile-time error, no implementation at all
    }


.. index::
   property
   readonly
   implementation

|

.. _Implementing Optional Interface Properties:

Implementing Optional Interface Properties
==========================================

.. meta:
    frontend_status: None

A class can implement :ref:`Optional Interface Properties`)
from superinterfaces or use implicitly defined accessors from an interface.

The use of accessors implicitly defined in the interface is represented in
the example below:

.. code-block:: typescript
   :linenos:

    interface I {
      n?: number
    }
    class C implements I {}

    let c = new C()
    console.log(c.n) // Output: undefined
    c.n = 1 // runtime error is thrown

.. index::
   property
   interface
   implementation
   class
   superinterface
   accessor

The implementation of an optional interface property as a field is represented
in the example below:

.. code-block:: typescript
   :linenos:

    interface I {
      num?: number
    }
    class C implements I {
      num?: number = 42
    }

For the example above, the private hidden field and the required accessors
are defined implicitly for the class ``C`` overriding accessors from
the interface:

.. code-block:: typescript
   :linenos:

    class C implements I {
      private $$_num: number = 42 // the exact name of the field is implementation specific
      get num(): number | undefined { return this.$$_num }
      set num(n: number | undefined) { this.$$_num = n }
    }


If a property is implemented by accessors (see
:ref:`Class Accessor Declarations`), then it is acceptable to implement only one
accessor for an optional field, and use default implementation for another
accessor as represented in the following example:

.. index::
   interface
   implementation
   property
   field
   private field
   hidden field
   accessor
   class
   class accessor declaration

.. code-block:: typescript
   :linenos:

    interface I {
      num?: number
    }

    class C1 implements I { // OK, both default implementations
    }

    class C2 implements I { // OK, default implementation used for get
      set num(n: number | undefined) { this.$$_num = n }
    }

    class C3 implements I { // OK, both explicit implementations
      get num(): number | undefined { return this.$$_num }
      set num(n: number | undefined) { this.$$_num = n }
    }

A  :index:`compile-time error` occurs, if an optional property in an interface
is implemented as non-optional field:

.. code-block:: typescript
   :linenos:

    interface I {
      num?: number
    }
    class C implements I {
      num: number = 42 // Compile-time error, must be optional
    }

.. index::
   interface
   implementation
   property
   non-optional field
   optional field

|

.. _Class Members:

Class Members
*************

.. meta:
    frontend_status: Done

A class can contain declarations of the following members:

-  Fields,
-  Methods,
-  Accessors,
-  Constructors,
-  Method overloads (see :ref:`Explicit Class Method Overload`), and
-  Single static initialization block (see :ref:`Static Initialization`).

The syntax is presented below:

.. index::
   class member
   declaration
   field
   method
   accessor
   constructor
   method overload
   class method
   static block
   initialization
   syntax

.. code-block:: abnf

    classMembers:
        '{'
           classMember* staticBlock? classMember*
        '}'
        ;

    classMember:
        annotationUsage?
        accessModifier?
        ( constructorDeclaration
        | explicitConstructorOverload
        | classFieldDeclaration
        | classMethodDeclaration
        | explicitClassMethodOverload
        | classAccessorDeclaration
        )
        ;

    staticBlock: 'static' Block;

Declarations can be inherited or immediately declared in a class. Any
declaration within a class has a class scope. The class scope is fully
defined in :ref:`Scopes`.

Members can be static or non-static as follows:

-  Static members that are not part of class instances, and can be accessed
   by using a qualified name notation (see :ref:`Names`) anywhere the class
   name is accessible (see :ref:`Accessible`); and
-  Non-static, or instance members that belong to any instance of the class.

.. note::
    Static members of a superclass are not inherited. A subclass that is to use
    static members of its superclass must use explicit qualification by the the
    name of the superclass. It applies to any kind of static members:

    - static fields;
    - static methods;
    - static accessors. 

Names of all *accessible* static and non-static entities in a class declaration
scope (see :ref:`Scopes`) must be unique, i.e., fields, methods, and overloads
with the same static or non-static status cannot have the same name.

The use of annotations is discussed in :ref:`Using Annotations`.

.. index::
   annotation
   static block
   class body
   class
   static member
   non-static member
   static entity
   non-static entity
   declaration
   member
   class instance
   access
   accessibility
   qualified name
   field
   method
   accessor
   type
   class
   class declaration
   interface
   constructor
   initializer block
   inheritance
   declaration scope
   overload
   scope


Class members are as follows:

-  Members inherited from their direct superclass (see :ref:`Inheritance`),
   except class ``Object`` that cannot have a direct superclass.
-  Members declared in a direct superinterface (see
   :ref:`Superinterfaces and Subinterfaces`).
-  Members declared in the class body (see :ref:`Class Members`).

Class members declared ``private`` are not accessible (see :ref:`Accessible`)
to all subclasses of the current class.

.. index::
   inheritance
   class member
   class body
   inherited member
   direct superclass
   superinstance
   subinterface
   Object
   direct superinstance
   private
   subclass
   access
   accessibility
   class

Class members declared ``protected`` or ``public`` are inherited by all
subclasses of the class and accessible (see :ref:`Accessible`) for all
subclasses.

Constructors and static block are not members, and are not inherited.

Members can be as follows:

.. index::
   class
   class member
   protected
   public
   subclass
   access
   constructor
   initializer block
   inheritance
   access
   accessibility
   static block

-  Class fields (see :ref:`Field Declarations`),
-  Methods (see :ref:`Method Declarations`), and
-  Accessors (see :ref:`Class Accessor Declarations`).

.. index::
   class field
   field declaration
   method
   method declaration
   accessor
   accessor declaration
   type parameter
   argument type
   return type
   declaration
   method member
   static member
   class instance
   qualified name
   notation
   class declaration scope
   field
   non-static class

|

.. _Access Modifiers:

Access Modifiers
****************

.. meta:
    frontend_status: Done

Access modifiers define how a class member or a constructor can be accessed.
Accessibility in |LANG| can be of the following kinds:

-  ``Private``,
-  ``Protected``,
-  ``Public``.

The desired accessibility of class members and constructors can be explicitly
specified by the corresponding *access modifiers*.

The syntax of *class members or constructors modifiers* is presented below:

.. code-block:: abnf

    accessModifier:
        'private'
        | 'protected'
        | 'public'
        ;

If no explicit modifier is provided, then a class member or a constructor
is implicitly considered ``public`` by default.


.. index::
   access modifier
   class member
   access
   member
   constructor
   private
   public
   protected
   access modifier
   accessibility

|

.. _Private Access Modifier:

Private Access Modifier
=======================

.. meta:
    frontend_status: Done
    todo: only parsing is implemented, but checking isn't implemented yet, need libarkfile support too

The modifier ``private`` indicates that a class member or a constructor is
accessible (see :ref:`Accessible`) within its declaring class only, i.e.,
a private member or constructor *m* declared in some class ``C`` can be accessed
only within the class body of ``C``. The usage of ``private`` is represented in
the following example:

.. code-block:: typescript
   :linenos:

    class C {
      private count: number = 1
      private hello() {}
      getCount(): number {
        return this.count // OK
      }
      sayHello() {
        this.hello()  // OK
      }
    }

    function increment(c: C) {
      c.sayHello()  // OK
      c.hello()     // Compile-time error - 'hello()' is private
      c.count++     // Compile-time error - 'count' is private
    }

    class D1 extends C {
      foo() {
         this.getCount() // OK
         this.sayHello() // OK
         this.hello()    // Compile-time error, private base method
         this.count++    // Compile-time error, private base field
      }
    }

    class D2 extends C {
      count = 1  // OK to reuse name since `count` in base inaccessible
      hello() {} // OK to reuse name since `hello` in base inaccessible
      foo() {
         this.count++    // OK
         this.hello()    // OK
      }
    }

    function bar(p: D2) {
      p.count++ // OK
      p.hello() // OK
   }


.. index::
   access modifier
   private
   private member
   class member
   constructor
   access
   accessibility
   declaring class
   class body

|

.. _Protected Access Modifier:

Protected Access Modifier
=========================

.. meta:
    frontend_status: Done

The modifier ``protected`` indicates that a class member or a constructor is
accessible (see :ref:`Accessible`) only within its declaring class and the
classes derived from that declaring class. A protected member ``M`` declared in
some class ``C`` can be accessed only within the class body of ``C`` or of a
class derived from ``C``:

.. code-block:: typescript
   :linenos:

    class C {
      protected count: number
       getCount(): number {
         return this.count // OK
       }
    }

    class D extends C {
      increment() {
        this.count++ // OK, D is derived from C
      }
    }

    function increment(c: C) {
      c.count++ // Compile-time error - 'count' is not accessible
    }


.. index::
   protected modifier
   access modifier
   accessible constructor
   method
   protected
   constructor
   accessibility
   class
   class body
   function increment
   class member
   derived class
   declaring class

|

.. _Public Access Modifier:

Public Access Modifier
======================

.. meta:
    frontend_status: Done
    todo: spec needs to be clarified - "The only exception and panic here is that the type the member or constructor belongs to must also be accessible"

The modifier ``public`` indicates that a class member or a constructor can be
accessed everywhere, provided that the member or the constructor belongs to
a type that is also accessible (see :ref:`Accessible`).

.. index::
   access modifier
   public modifier
   public
   class member
   constructor type
   access modifier
   protected
   access
   constructor
   accessibility
   accessible type

|

.. _Field Declarations:

Field Declarations
******************

.. meta:
    frontend_status: Partly
    todo: syntax for definite assignment

*Field declarations* represent data members in class instances or static data
members (see :ref:`Static and Instance Fields`). Class instance
*field declarations* are its *own fields* in contrast to the inherited ones.
Syntactically, a field declaration is similar to a variable declaration.

.. code-block:: abnf

    classFieldDeclaration:
        fieldModifier*
        identifier
        ( '?'? ':' type initializer?
        | '?'? initializer
        | '!' ':' type
        )
        ;

    fieldModifier:
        'static' | 'readonly' | 'override'
        ;

.. index::
   field declaration
   data member
   class instance
   static data member
   instance field
   own field
   inheritance
   syntax
   variable declaration

A field with an identifier marked with ``'?'`` is called *optional field*
(see :ref:`Optional Fields`).
A field with an identifier marked with ``'!'`` is called
*field with late initialization*
(see :ref:`Fields with Late Initialization`).

A :index:`compile-time error` occurs if:

-  Some field modifier is used more than once in a field declaration.
-  Name of a field declared in the body of a class declaration is also
   used for a method of this class with the same static or
   non-static status.
-  Name of a field declared in the body of a class declaration is also
   used for another field in the same declaration with the same static or
   non-static status.

.. index::
   field
   identifier
   optional field
   field with late initialization
   field modifier
   field declaration
   method
   class
   class declaration
   static field
   non-static field

Any static field can be accessed only with the qualification of a class name,
while an instance field can be accessed with the object reference qualification
(see :ref:`Field Access Expression`).


If a field declaration is an implementation of one or more properties inherited
from superinterfaces (see :ref:`Interface Inheritance`) then the types of the
field and all properties must be the same.
Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    // Two unrelated interfaces
    interface B1 {}
    interface B2 {}
    // Interface which extends both of them
    interface B3 extends B1, B2 {}
    // Class which implements B3
    class BB3 implements B3 {}

    interface II1 { f: B1 }
    interface II2 { f: B2 } // Different property 'f' type as in II1
    interface II3 { f: B1 } // The same property 'f' type as in II1

    class CC1 implements II1, II2 {
        f: B1  = new BB3 /* compile-time error, field and all inherited properties
                            must be of the same type */
    }
    class CC2 implements II1, II3 {
        f: B3 = new BB3 /* compile-time error, field and all inherited properties
                           must be of the same type */
    }
    class CC3 implements II1, II3 {
        f: B1 = new BB3 // OK, correct properties implementation
    }



.. index::
   static field
   qualified name
   qualification
   access
   superinterface
   superclass
   field
   property
   class body
   field declaration
   inheritance
   property

|

.. _Static and Instance Fields:

Static and Instance Fields
==========================

.. meta:
    frontend_status: Done

There are two categories of class fields as follows:

- Static fields

  Static fields are declared with the modifier ``static``. A static field
  is not part of a class instance. There is one copy of a static field
  irrespective of how many instances of the class (even if zero) are
  eventually created.

  Static fields are always accessed by using a qualified name notation
  wherever the class name is accessible (see :ref:`Accessible`).

  A :index:`compile-time error` occurs if the name of a type parameter of the
  surrounding declaration is used as the type of a static field.

- Instance, or non-static fields

  Instance fields belong to each instance of the class. An instance field
  is created for, and associated with a newly-created instance of a class,
  or of its superclass. An instance field is accessible (see :ref:`Accessible`)
  via the instance name.

.. index::
   class fields
   modifier static
   static
   static field
   instantiation
   instance
   initialization
   class
   class instance
   superclass
   non-static field
   accessibility
   access
   instance field
   qualified name
   notation
   instance name

|

.. _Readonly Constant Fields:

Readonly (Constant) Fields
==========================

.. meta:
    frontend_status: Done

A field with the modifier ``readonly`` is a *readonly field*. Changing
the value of a readonly field after initialization is not allowed. Both static
and non-static fields can be declared *readonly fields*.

.. index::
   readonly field
   readonly modifier
   readonly
   constant field
   initialization
   modifier
   static field
   non-static field

|

.. _Optional Fields:

Optional Fields
===============

.. meta:
    frontend_status: Partly

*Optional field* ``f?: T = expr`` effectively means that the type of ``f``is
``T | undefined``. If an *initializer* is absent in a *field declaration*,
then the default value ``undefined`` (see :ref:`Default Values for Types`) is
used as the initial value of the field.

.. index::
   undefined
   initializer
   field declaration
   undefined
   value
   default value
   optional field

For example, the following two fields are actually defined the same way:

.. code-block:: typescript
   :linenos:

    class C {
        f?: string
        g: string | undefined = undefined
    }

|

.. _Field Initialization:

Field Initialization
====================

.. meta:
    frontend_status: Done

All fields except :ref:`Fields with Late Initialization` are initialized by
using the default value (see :ref:`Default Values for Types`) or a field
initializer (see below) if present. Otherwise, a field must be initialized as
follows:

- Static field, by a static initialization block (see
  :ref:`Static Initialization`), or
- Instance field, by a class constructor (see
  :ref:`Constructor Declaration`).

.. index::
   field initialization
   initialization
   default value
   evaluation
   field initializer
   field access
   expression
   field access expression
   field initializer
   initializer block
   static field
   class constructor
   non-static field

*Field initializer* is an expression that is evaluated at compile time or
runtime. The result of successful evaluation is assigned into the field. The
semantics of field initializers is therefore similar to that of assignments
(see :ref:`Assignment`). Each initializer expression evaluation and the
subsequent assignment are only performed once.

.. index::
   field initializer
   evaluation
   expression
   compile time
   runtime
   access
   field
   semantics
   assignment
   this keyword
   super keyword
   method

The initializer of a non-static field declaration is evaluated at runtime.
The assignment is performed each time an instance of the class is created (see
:ref:`New Expressions`).

If the initializer expression uses ``super`` or ``this`` in any form, then a
:index:`compile-time warning` occurs.

If such use occurs then runtime error can occur as shown in the following examples:

.. index::
   non-static field declaration
   initializer
   initializer expression
   uninitialized field
   evaluation
   runtime
   assignment
   instance
   class
   instance field initializer
   call method
   this
   super
   restriction
   class instance

.. code-block:: typescript
   :linenos:

    class C {
        f0 = this // Compile-time warning as 'this' is used

        f1 = this.init_f1() // Compile-time warning as method of 'this' method is invoked

        init_f1 (): string {
           console.log (this.f1) // this.f1 was not yet initialized, a runtime error occurs
           return "a string field"
        }
    }

    class B {}
    function foo (f: () => B) { return f() }
    class A {
        field1 = foo(() => this.field2) 
            // Compile-time warning as 'this' is used in the initializer code
            // At runtime the lambda call will lead to a runtime error as
            // this.field2 was not yet initialized

        field2 = new B
    }


.. index::
   compiler
   field initializer
   this method
   access
   non-static field
   initialization
   circular dependency
   initializer
   initializer expression

|

.. _Fields with Late Initialization:

Fields with Late Initialization
===============================

.. meta:
    frontend_status: Done

*Field with late initialization* ``f!: T = expr`` effectively means that the
type of the field ``f`` is ``T | undefined``. However, the field behaves like a
field of type ``T`` with any form of access.

*Field with late initialization* must be an *instance field*. Otherwise,
a :index:`compile-time error` occurs.

*Field with late initialization* cannot be of a *nullish type* (see
:ref:`Nullish Types`). Otherwise, a :index:`compile-time error` occurs.

As all other fields, a *field with late initialization* must be initialized
before it is used for the first time. However, this field can be initialized
*later* and not within a class declaration.
Initialization of this field can be performed in a constructor
(see :ref:`Constructor Declaration`), although it is not mandatory.

.. index::
   field with late initialization
   field initializer
   instance field
   initialization
   nullish type
   class declaration
   field
   constructor
   constructor declaration

*Field with late initialization* cannot have *field initializers*, and can be
neither ``readonly`` (see :ref:`Readonly Constant Fields`) nor ``optional``
(see :ref:`Optional Fields`). Otherwise, a :index:`compile-time error` occurs.
*Field with late initialization* must be initialized explicitly, even though
its type has a *default value* which is ignored at the point of declaration.

Each time a *field with late initialization* is read, a field initialization
check is performed. If the compiler identifies that a field is not
initialized, then a :index:`compile-time error` occurs. Otherwise, a check
is performed at runtime, and if a non-initialized field is encountered, then
a :index:`runtime error` occurs:

.. code-block:: typescript
   :linenos:

    class C {
        f!: string
    }

    let x = new C()
    x.f = "aa"
    console.log(x.f) // OK

    let y = new C()
    console.log(y.f) // runtime or compile-time error

.. note::
   An initialization check on read slows down the access to a *field with late
   initialization*.

   |TS| uses the term *definite assignment assertion* for a notion similar to
   *late initialization*. However, |LANG| has a stricter read-check policy.

.. index::
   field with late initialization
   field initializer
   optional field
   initialization
   default value
   check
   runtime
   field value
   compiler
   error
   access
   field
   assignment
   definite assignment assertion
   notion
   late initialization

|

.. _Override Fields:

Override Fields
===============

.. meta:
    frontend_status: None
    todo: initialization must be explicit

When extending a class, an instance field declared in a superclass can be
overridden by a same-name, same-type field. The new declaration adds no new
field to the class type but allows changing field initialization. Using the
keyword ``override`` is not required.

.. note::

    Implementing interface properties by fields is discussed in detail
    in :ref:`Implementing Required Interface Properties` and
    :ref:`Implementing Optional Interface Properties`.

A :index:`compile-time error` occurs if:

-  Field marked with the modifier ``override`` does not override a field from
   a superclass.
-  Field declaration contains the modifier ``static`` along with the modifier
   ``override``.
-  Types of the overriding field and of the overridden field are different.
-  :ref:`Access Modifiers` of the overriding field and of the overridden field are
   different.

.. index::
   overriding field
   class
   interface
   field
   declaration
   superclass
   superinterface
   overriding
   static modifier
   non-static modifier
   override keyword
   modifier
   type

.. code-block:: typescript
   :linenos:

    class C {
        field: number = 1
        protected ff = 25
    }
    class D extends C {
        field: string = "aa"     // Compile-time error, type is not the same
        override no_field = 1224 // Compile-time error, no overridden field in the base class
        static override field: string = "aa" // Compile-time error, static cannot override
        ff = 66                  // Compile-time error, as access modifers are different 
    }

An overridden field must be initialized explicitly either by using an
initializer or in a constructor. Otherwise, :index:`compile-time error` occurs.
Implicit initialization is not used, even though the type of the field has
a default value (see :ref:`Default Values for Types`):

.. code-block:: typescript
   :linenos:

    class C {
        f1: number = 1
        f2: Object = 2
    }
    class D extends C {
        f1: number = 7 // OK
        f2: Object     // OK, initialized in the constructor
        constructor () {
            super()
            this.f2 = "abc"
        }
    }
    class E extends C {
        f1: number  // Compile-time error, must be initialized explicitly
        f2: Object  // Compile-time error, must be initialized explicitly
    }

Initializers of overridden fields are preserved for execution, and the
initialization is normally performed in the context of *superclass* constructors.

.. code-block:: typescript
   :linenos:

    class C {
        field: number = C.init()
        private static init() {
           console.log ("Field initialization in C")
           return 123
        }
    }
    class D1 extends C {
        override field: number = 321 // field can be explicitly marked as overridden
    }

    class D2 extends D1 {
        field: number = D2.init_in_derived()
        private static init_in_derived() {
           console.log ("Field initialization in Derived")
           return 42
        }
    }
    console.log ((new D2()).field)
    /* Output:
        Field initialization in C
        Field initialization in Derived
        42
    */

.. index::
   overriding
   field overriding
   overridden field
   base class
   static override field
   initialization
   initializer
   instance field
   context
   superclass constructor
   superclass
   superinterface
   interface
   field initialization
   implementation
   overriding
   field

The term *same-type* in case of generic classes means that the type of a field
in a derived class must be the same as in the base class instantiated with a
parameter of the same type as the type of the field in the derived class.

The situation is represented in the example below:

.. code-block:: typescript
   :linenos:

    class B<T> {
       f1: T
       f2: T
       constructor (v: T) { this.f1 = v; this.f2 = v }
    }
    class D<U, V> extends B<U>  {
       f1: U // Valid overriding as D extends B<U>, and type of f1 in B<U> is U
       f2: V // Compile-time error, wrong overriding
       constructor (v: U) {
           super (v)
       }
    }


A :index:`compile-time error` occurs if a field is not declared as ``readonly``
in a superclass, while an overriding field is marked as ``readonly``:

.. code-block:: typescript
   :linenos:

    class C {
        field = 1
    }
    class D extends C {
        readonly field = 2 // Compile-time error, wrong overriding
    }

A :index:`compile-time error` occurs if a field overrides a getter, a setter, or
both in a superclass:

.. code-block:: typescript
   :linenos:

    class C {
        get num(): number { return 42 }
        set num(x: number) {}
    }
    class D extends C {
        num: number = 2 // Compile-time error, wrong overriding
    }

Overriding a field by a single accessor or by both accessors causes a
:index:`compile-time error` as follows:

.. code-block:: typescript
   :linenos:

    class C {
        num: number = 1
    }
    class D extends C {
        get num(): number  { return this.shadow } // Compile-time error, wrong overriding
        set num(x: number) { this.shadow = p }    // Compile-time error, wrong overriding
        private shadow: number = 123
    }

.. index::
   field
   override
   overriding field
   superclass
   implementation
   superinterface
   inheritance
   accessor
   inherited field
   accessor declaration
   class accessor

|

.. _Method Declarations:

Method Declarations
*******************

.. meta:
    frontend_status: Done

*Methods* declare executable code that can be called.

A *method* is defined by the following:

#. *Type parameter*, i.e., the declaration of any type parameter of the
   method member.
#. *Argument type*, i.e., the list of types of arguments applicable to the
   method member.
#. *Return type*, i.e., the return type of the method member.

The syntax of *class method declarations* is presented below:

.. code-block:: abnf

    classMethodDeclaration:
        methodModifier* identifier typeParameters? signature block?
        ;

    methodModifier:
        'abstract'
        | 'static'
        | 'final'
        | 'override'
        | 'native'
        | 'async'
        ;

.. index::
   method declaration
   method
   executable code
   call
   syntax
   class method
   class method declaration

The identifier in a *class method declaration* defines the method name that can
be used to refer to a method (see :ref:`Method Call Expression`).

Methods with the ``final`` modifier is an experimental feature discussed in
detail in :ref:`Final Methods`.

A :index:`compile-time error` occurs if:

-  Method modifier appears more than once in a method declaration;
-  Body of a class declaration declares a method but the name of that
   method is already used for a field in the same declaration.

A non-static method declared in a class can do the following:

- Implement a method inherited from a superinterface or superinterfaces;
- Override a method inherited from a superclass (see :ref:`Overriding in Classes`);
- Act as method declaration of a new method.


Class static methods never implement or override superclass or superinterface
methods.


.. index::
   method declaration
   class method declaration
   method name
   method
   declaration
   executable code
   overriding
   inheritance
   superclass
   class
   static method
   overloading signature
   identifier
   method call
   method call expression
   expression
   method modifier
   final modifier
   method declaration
   class declaration
   class declaration body

|

.. _Static Methods:

Static Methods
==============

.. meta:
    frontend_status: Done

A method declared in a class with the modifier ``static`` is a *static method*.

A :index:`compile-time error` occurs if:

-  The method declaration contains another modifier (``abstract``, ``final``,
   or ``override``) along with the modifier ``static``.
-  The header or body of a class method includes the name of a type parameter
   of the surrounding declaration.

Static methods are always called without reference to a particular object. As
a result, a :index:`compile-time error` occurs if the keywords ``this`` or
``super`` are used inside a static method.

Static methods are not inherited from superclasses:

.. code-block:: typescript
   :linenos:

    class Base {
        static foo() { console.log ("static foo() from Base") }
        static bar() { console.log ("static foo() from Base") }
    }

    class Derived extends Base {
        static foo(p: string) { console.log ("static foo() from Derived") }
    }

    Base.foo() // Output: static foo() from Base
    Base.bar() // Output: static foo() from Base
    Derived.bar()           // Compile-time error, there is no bar() in Derived
    Derived.foo("a string") // Output: static foo() from Derived
    Derived.foo()           // Compile-time error, there is no foo(p:string) in Derived


.. note::
   Class static methods may access protected or private members of the same
   class type or derived one represented as parameters or local variables:

   .. code-block:: typescript
      :linenos:

       class C {
         protected count1: number
         private   count2: number
         static getCount(c: C): number {
           const local_c = new C
           return c.count1 + c.count2 + local_c.count1 + local_c.count2 // OK
         }
         static handleDerived (b: B) {
             b.count1 + b.count2 // OK
         }
       }
       class B extends C {
         static dealWithProtected (b: B) {
             b.count1 // OK
             b.count2 // Compile-time error
         }
       }

       C.getCount (new C)      // will return the sum of counts
       C.handleDerived (new B) // will work with protected and private fields



.. index::
   static method
   method
   method declaration
   modifier
   declaration
   class
   abstract modifier
   final modifier
   override modifier
   static modifier
   static method
   this keyword
   super keyword
   header
   body
   inheritance

|

.. _Instance Methods:

Instance Methods
================

.. meta:
    frontend_status: Done

A method that is not declared static is called *non-static method*, or
*instance method*.

An instance method is always called with respect to an object that becomes
the current object which the keyword ``this`` refers to during the execution
of the method body.

.. index::
   static method
   instance method
   non-static method
   declaration
   this keyword
   object
   method body
   execution
   instance

|

.. _Abstract Methods:

Abstract Methods
================

.. meta:
    frontend_status: Done

An *abstract* method declaration introduces the method as a member along
with its signature but without implementation. An abstract method is
declared with the modifier ``abstract`` in the declaration.

Non-abstract methods can be referred to as *concrete methods*.

A :index:`compile-time error` occurs if:

.. index::
   abstract method
   method declaration
   declaration
   abstract modifier
   non-abstract method
   concrete method
   method
   member
   signature
   implementation
   abstract

-  An abstract method is declared private.
-  The method declaration contains another modifier (``static``, ``final``,
   ``native``, or ``async``) along with the modifier ``abstract``.
-  The declaration of an abstract method *m* does not appear directly within
   abstract class ``A``.
-  Any non-abstract subclass of ``A`` (see :ref:`Abstract Classes`) does not
   provide implementation for *m*.

An abstract method declaration provided by an abstract subclass can override
another abstract method. An abstract method can also override non-abstract
methods inherited from base classes or base interfaces as follows:

.. code-block:: typescript
   :linenos:

    class C {
        foo() {}
    }
    interface I {
        foo() {} // default implementation
    }
    abstract class X extends C implements I {
        abstract foo(): void /* Here abstract foo() overrides both foo()
                                coming from class C and interface I */
    }


.. index::
   method declaration
   abstract method
   private modifier
   static modifier
   final modifier
   native modifier
   async modifier
   declaration
   abstract class
   non-abstract subclass
   implementation
   non-abstract instance method
   non-abstract method
   method signature
   abstract method
   overriding
   abstract modifier
   inheritance
   interface

|

.. _Async Methods:

Async Methods
=============

.. meta:
    frontend_status: Done

Async methods are discussed in :ref:`Concurrency Async Methods`.

.. index::
   async method

|

.. _Overriding Methods:

Overriding Methods
==================

.. meta:
    frontend_status: Done

The ``override`` modifier indicates that an instance method in a superclass is
overridden by the corresponding instance method from a subclass (see
:ref:`Overriding`).

The usage of the modifier ``override`` is optional but strongly recommended as
it makes the overriding explicit.

A :index:`compile-time error` occurs if:

-  Method marked with the modifier ``override`` overrides no method
   from a superclass.
-  Method declaration contains modifier ``static`` along with the modifier
   ``override``.

If the signature of an overridden method contains parameters with default
values (see :ref:`Optional Parameters`), then the overriding method must
always use the same default parameter values for the overridden method.
Otherwise, a :index:`compile-time error` occurs.

More details on overriding are provided in :ref:`Overriding in Classes` and
:ref:`Overriding in Interfaces`.


.. index::
   override modifier
   abstract modifier
   static modifier
   final method
   modifier
   signature
   overriding
   method
   superclass
   class
   instance
   interface
   subclass
   default value
   overriding method

|

.. _Native Methods:

Native Methods
==============

.. meta:
    frontend_status: Done

Native methods are discussed in :ref:`Native Methods Experimental`.

.. index::
   native method

|

.. _Method Body:

Method Body
===========

.. meta:
    frontend_status: Done

*Method body* is a block of code that implements a method. A semicolon or
an empty body (i.e., no body at all) indicate the absence of implementation.

An abstract or native method must have an empty body.

In particular, a :index:`compile-time error` occurs if:

-  The body of an abstract or native method declaration is a block.
-  The method declaration is neither abstract nor native, but its body
   is either empty or a semicolon.

The rules that apply to return statements in a method body are discussed in
:ref:`Return Statements`.

A :index:`compile-time error` occurs if a method:

-  Is declared to have a return type other than *void*, and
-  Has no return statement on any execution path of its body.


.. index::
   method body
   semicolon
   empty body
   block
   implementation
   implementation method
   abstract method
   native method
   empty body
   method body
   method declaration
   return statement
   return type
   normal completion

|

.. _Methods Returning this:

Methods Returning ``this``
==========================

.. meta:
    frontend_status: Done

A return type of an instance method can be ``this``.
It means that the return type is the class type to which the method belongs.
It is the only place where the keyword ``this`` can be used as type annotation
(see :ref:`Signatures` and :ref:`Return Type`).

The only result that is allowed to be returned from an instance method is
``this``. There are two options to have ``this`` returned:

-  Literally ``return this``; or
-  Return the result of any method that returns ``this``.


A call to another method can return ``this`` or ``this`` statement:

.. code-block:: typescript
   :linenos:

    class C {
        foo(): this {
            return this
        }
        bar(): this {
            return this.foo()
        }
    }

.. index::
    return type
    instance method
    type
    class
    method
    method signature
    signature
    this keyword
    this statement
    subclass
    annotation

The return type of an overridden method in a subclass must also be ``this``:

.. code-block:: typescript
   :linenos:

    class C {
        foo(): this {
            return this
        }
    }

    class D extends C {
        foo(): this {
            return this
        }
    }

    let x = new C().foo() // type of 'x' is 'C'
    let y = new D().foo() // type of 'y' is 'D'

Otherwise, a :index:`compile-time error` occurs.

.. index::
    return type
    overriding
    overridden method
    subclass

|

.. _Class Accessor Declarations:

Class Accessor Declarations
***************************

.. meta:
    frontend_status: Done


Class accessors are declared in the form of getters or setters, i.e., methods
with predefined signatures that suport using field access syntax to call such
methods. 

Class accessors are often used instead of fields to add additional control for
operations of getting or setting a field value.

The syntax of *class accessor declarations* is presented below:

.. code-block:: abnf

    classAccessorDeclaration:
        classAccessorModifier*
        ( 'get' identifier '(' ')' returnType? block?
        | 'set' identifier '(' parameter ')' block?
        )
        ;

    classAccessorModifier:
        'abstract'
        | 'static'
        | 'final'
        | 'override'
        | 'native'
        ;

.. index::
   class accessor declaration
   class accessor
   declaration
   identifier
   block
   parameter
   field
   control
   field value
   value
   getter
   setter

Accessor modifiers are a subset of method modifiers. The allowed accessor
modifiers have exactly the same meaning as the corresponding method modifiers
(see :ref:`Abstract Methods` for the modifier ``abstract``,
:ref:`Static Methods` for the modifier ``static``, :ref:`Final Methods` for the
modifier ``final``, :ref:`Overriding Methods` for the modifier ``override``, and
:ref:`Native Methods` for the modifier ``native``).

.. index::
   accessor modifier
   access modifier
   method modifier
   subset
   abstract modifier
   native modifier
   abstract modifier
   static method
   final method
   overriding method

.. code-block:: typescript
   :linenos:

    class Person {
      private _age: number = 0
      get age(): number { return this._age }
      set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        this._age = a
      }
    }

A *get-accessor* (*getter*) must have an explicit return type and no parameters,
or no return type at all on condition it can be inferred from the getter body.
A *set-accessor* (*setter*) must have a single parameter and no return type. The
use of getters and setters looks the same as the use of fields.
A :index:`compile-time error` occurs if:

-  Getters or setters are used as methods;
-  Getter return type cannot be inferred from the getter body;
-  *Set-accessor* (*setter*) has a single parameter that is optional (see
   :ref:`Optional Parameters`):

.. code-block:: typescript
   :linenos:

    class Person {
      private _age: number = 0
      get age(): number { return this._age }
      set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        this._age = a
      }
    }

    let p = new Person()
    p.age = 25        // setter is called
    if (p.age > 30) { // getter is called
      // do something
    }
    p.age(17) // Compile-time error, setter is used as a method
    let x = p.age() // Compile-time error, getter is used as a method

    class X {
        set x (p?: Object) {} // Compile-time error, setter has optional parameter
    }

.. index::
   get-accessor
   getter
   getter body
   inferred type
   type inference
   return type
   parameter
   set-accessor
   setter
   field
   method
   optional parameter

If a getter has no return type specified, then the type is inferred as in
:ref:`Return Type Inference`.

.. code-block:: typescript
   :linenos:

    class Person {
      private _age: number = 0
      get age() { return this._age } // return type is inferred as number
    }


A class can define a getter, a setter, or both with the same name.
If both a getter and a setter with a particular name are defined,
then both must have the same accessor modifiers. Otherwise, a
:index:`compile-time error` occurs.

Any accessor implementation can use a private or non-private field or fields to
store the data as in the examples above and below.

.. code-block:: typescript
   :linenos:

    class Person {
      forename: string = ""
      surname: string = ""
      get fullName(): string {
        return this.surname + " " + this.forename
      }
    }
    console.log (new Person().fullName)

A name of an accessor cannot be the same as that of a non-static field, or of a
method of class or interface. Otherwise, a :index:`compile-time error`
occurs:

.. index::
   getter
   return type
   inferred type
   type inference
   setter
   accessor
   private field
   accessor modifier
   implementation
   non-static field
   class
   interface
   class method
   interface method

.. code-block:: typescript
   :linenos:

    class Person {
      name: string = ""
      get name(): string { // Compile-time error, getter name clashes with the field name
          return this.name
      }
      set name(a_name: string) { // Compile-time error, setter name clashes with the field name
          this.name = a_name
      }
    }

In the process of inheriting and overriding (see :ref:`Overriding`),
accessors behave as methods. The getter parameter type follows the covariance
pattern, and the setter parameter type follows the contravariance pattern (see
:ref:`Override-Compatible Signatures`):

.. code-block:: typescript
   :linenos:

    class Base {
      get field(): Base { return new Base }
      set field(a_field: Derived) {}
    }
    class Derived extends Base {
      override get field(): Derived { return new Derived }
      override set field(a_field: Base) {}
    }
    function foo (base: Base) {
       base.field = new Derived // setter is called
       let b: Base = base.field // getter is called
    }
    foo (new Derived)

.. index::
   overriding
   inheritance
   accessor
   method
   getter parameter
   setter parameter
   parameter type
   covariance pattern
   contravariance pattern
   override-compatible signature

|

.. _Constructor Declaration:

Constructor Declaration
***********************

.. meta:
    frontend_status: Partly
    todo: native constructors
    todo: optional constructor names
    todo: Explicit Constructor Call - "Qualified superclass constructor calls" - not implemented

*Constructors* are used to initialize objects that are instances of a class. A
*constructor declaration* starts with the keyword ``constructor``, and has optional
name. In any other syntactical aspect, a constructor declaration is similar to
a method declaration with no return type:

.. code-block:: abnf

    constructorDeclaration:
        'native'? 'constructor' identifier? parameters constructorBody?
        ;

The syntax and semantics of a constructor鈥檚 formal parameters are identical
to those of a method.

A constructor defined in supertype cannot be used directly in a *new expression*
for a subtype, but is available for a call in all derived class constructors via
``super`` call (see :ref:`Explicit Constructor Call`).

.. code-block:: typescript
   :linenos:

    class C {
        constructor (s: string) {}
    }
    class D extends C {
    }

    new D("aa") // Compile-time error, 'D' has default constructor only

    class D1 extends C {
        constructor (n: number) {
            super("" + n) // OK
        }
    }

Constructors are called by the following:

.. index::
   constructor
   initialization
   object
   class instance
   instance
   constructor declaration
   constructor keyword
   optional name
   syntax
   method declaration
   return type
   optional identifier
   identifier

-  Class instance creation expressions (see :ref:`New Expressions`); and
-  Explicit constructor calls from other constructors (see :ref:`Constructor Body`).

Access to constructors is governed by access modifiers (see
:ref:`Access Modifiers` and :ref:`Scopes`). Declaring a constructor
inaccessible prevents class instantiation from using this constructor.
If the only constructor is declared inaccessible, then no class instance
can be created.

A ``native`` constructor (an experimental feature described in
:ref:`Native Constructors`) must have no *constructorBody*. Otherwise, a
:index:`compile-time error` occurs.

A non-``native`` constructor must have *constructorBody*. Otherwise, a
:index:`compile-time error` occurs.

.. index::
   class instance
   class instantiation
   expression
   constructor
   instance creation expression
   constructor keyword
   constructor declaration
   constructor call
   access modifier
   accessibility
   native constructor
   access
   native constructor
   non-native constructor

|

.. _Constructor Body:

Constructor Body
================

.. meta:
    frontend_status: Done

*Constructor body* is a block of code that implements a constructor.

The syntax of *constructor body* is presented below:

.. code-block:: abnf

    constructorBody:
        '{' statement* '}'
        ;

.. index::
   constructor body
   block of code
   constructor
   implementation
   syntax

The constructor body must provide correct initialization of new class instances.
Constructors have two variations:

- *Primary constructor* that initializes instance own fields directly;

- *Secondary constructor* that uses another same-class constructor to initialize
  its instance fields.

.. index::
   constructor body
   initialization
   class instance
   primary constructor
   instance own field
   secondary constructor
   constructor
   instance field

The high-level sequence of a *primary constructor* body includes
the following: 

1. Optional arbitrary code that uses neither ``this`` nor ``super``.

2. Call to a superconstructor (see :ref:`Explicit Constructor Call`)
   if a class has an extension clause (see :ref:`Class Extension Clause`).
   A :index:`compile-time error` occurs if:

   - Call is not a root-level statement within a constructor;

   - Call argument uses ``this`` or ``super``.


3. Implicit addition by the compiler of field initializers (if any)
   to be executed in the order they appear in a class body.

4. Code that neither uses ``this`` nor accesses fields through ``this``,
   i.e., fields not expliclity initialized in the body of a
   *primiary constructor* or during the step 3, are not read.

5. Arbitrary code after all fields are initialized as defined in **item 4**.

If the body has no call to a superconstructor (i.e., **item 2** above
is omitted), then the compiler implicitly adds a superconstructor call
with no arguments as the very first statement in the body.  
If the superconstructor requires a non-empty list of arguments,  
then a :index:`compile-time error` occurs as represented below:

.. code-block:: typescript
   :linenos:

    class C1 {
        constructor() {}
    }
    class D1 extends C1 {
        constructor () {
            // OK, call 'super()' is implicitly added
            /* other code here */
        } 
    }

    class C2 {
        constructor(n: number) {}
    }
    class D2 extends C2 {
        constructor () {
            // Compile-time error, call 'super()' cannot be implicitly added
            /*other code here*/
        }
    }
    
    class C3 {
        constructor(n?: number) {}
    }
    class D3 extends C3 {
        constructor () {
            // OK, call 'super()' is implicitly added
            /*other code here*/
        } 
    }
    
Field initialization referred in **item 4** above cannot be guaranteed at
compile time in all possible cases. The following strategy is taken: 

  - If the compiler can detect that a non-initialized field is accessed
    during compilation, then a :index:`compile-time error` occurs;
  - If the limitation of **item 4** is violated, then a
    :index:`compile-time warning` occurs;
  - Otherwise, the execution-time behavior is determined by the implementation.

.. code-block:: typescript
   :linenos:

    class Base {
      x: Object
      constructor() {
          this.x = new Object // Base object is fully initialized
          crash_this (this)   // A compiler may issue a compile-time error
      }
    }
    class Derived extends Base {
      y: Object
      constructor () {
          super() // mandatory call to base class constructor
          crash_this(this) // Compile-time warning as this.y is not initialized yet
                           // is guaranteed, however a compiler can issue a
                           // Compile-time error
          this.y = new Object
      }
    }
    function crash_this (b: Base) {
          if (b instanceof Derived) { // If b is of type Derived, then
                console.log ((b as Derived).y) // Access y field of Derived object
                // Depending on the compilation context, either the compiler reports
                // a compile-time error, or the runtime system is to detect the case
          }
    }

The manner new expressions (see :ref:`New Expressions`) work together with a
constructor body execution sequence is represented by the example below:

.. code-block:: typescript
   :linenos:

   let count = 0
   function trace (msg: string) {
      count++
      console.log (count + ": " + msg)
      return count
   }

   class C {
      C_field = trace("C fields initialization performed")
      constructor() {
         trace ("C constructor called")
      }
   }
   class B extends C {
      B_field = trace("B fields initialization performed")
      constructor() {
         super ()
         trace ("B constructor called")
      }
   }
   class A extends B {
      A_field = trace("A fields initialization performed")
      constructor(p: number) {
         super()
         trace ("A constructor called")
      }
   }
   new A (trace("constructor arguments evaluated"))

   // The output
   // "1: constructor arguments evaluated"
   // "2: C fields initialization performed"
   // "3: C constructor called "
   // "4: B fields initialization performed"
   // "5: B constructor called "
   // "6: A fields initialization performed"
   // "7: A constructor called "

.. index::
   primary constructor
   constructor body
   high-level sequence
   optional arbitrary code
   this
   super
   mandatory call
   field initializer
   class body
   compiler
   constructor call
   superconstructor
   value
   instance field
   initialization
   execution path
   constructor body
   extension clause
   execution
   this keyword
   compiler
   instance
   instance field
   initialization
   field with late initialization
   object field

*Primary constructors* are represented by the example below:

.. code-block:: typescript
   :linenos:

    class Point {
      x: number
      y: number
      constructor(x: number, y: number) {
        this.x = x
        this.y = y
      }
    }

    class ColoredPoint extends Point {
      static readonly WHITE = 0
      static readonly BLACK = 1
      color: number
      constructor(x: number, y: number, color: number) {
        super(x, y) // calls base class constructor
        this.color = color
      }
    }

   class BWPoint extends ColoredPoint {
      constructor(x: number, y: number, black: boolean) {
        console.log ("Code that uses neither 'this' nor 'super'")
        super (x, y, black ? ColoredPoint.BLACK : ColoredPoint.WHITE)
        console.log ("Any code after that point")
      }
    }

The high-level sequence of a *secondary constructor* body includes the following:

1. Optional arbitrary code that does not use ``this`` or ``super``.

2. Mandatory call to another same-class constructor that uses the keyword
   ``this`` (see :ref:`Explicit Constructor Call`).
   A :index:`compile-time error` occurs if:

   - The call is not a root-level statement within a constructor;

   - An argument of the call uses ``this`` or ``super``.

3. Optional arbitrary code.

The example below represents *primary* and *secondary* constructors:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    class Point {
      x: number
      y: number
      constructor(x: number, y: number) {
        this.x = x
        this.y = y
      }
    }

    class ColoredPoint extends Point {
      static readonly WHITE = 0
      static readonly BLACK = 1
      color: number

      // Primary constructor:
      constructor(x: number, y: number, color: number) {
        super(x, y) // Calls base class constructor as class has 'extends'
        this.color = color
      }
      // Secondary constructor:
      constructor (color: number) {
        this(0, 0, color) // Calls same class primary constructor
      }
    }

.. index::
   primary constructor
   secondary constructor
   readonly
   constructor
   class

A :index:`compile-time error` occurs if a constructor calls itself, directly or
indirectly through a series of one or more explicit constructor calls
using ``this``.

A constructor body looks like a method body (see :ref:`Method Body`), except
for the semantics as described above. Explicit return of a value (see
:ref:`Return Statements`) is prohibited. On the opposite, a constructor body
can use a return statement without an expression.

A constructor body can have no more than one call to the current class or
direct superclass constructor. Otherwise, a :index:`compile-time error` occurs.

.. index::
   constructor
   constructor call
   constructor body
   method body
   semantics
   value
   return statement
   expression
   class
   superclass

|

.. _Explicit Constructor Call:

Explicit Constructor Call
=========================

.. meta:
    frontend_status: Done

There are two kinds of *explicit constructor calls*:

-  *Superclass constructor calls* (used to call a constructor from the direct
   superclass) that begin with the keyword ``super``.
-  *Other constructor calls* that begin with the keyword ``this``
   (used to call another same-class constructor).

A :index:`compile-time error` occurs if:

-  *Superclass constructor call* refers to an inaccessible direct superclass
   constructor.
-  *Explicit constructor call* is used as expression.

A :index:`compile-time error` occurs if arguments of an explicit constructor
call refer to one of the following:

-  Any non-static field or instance method; or
-  ``this`` or ``super``.

.. code-block:: typescript
   :linenos:

    class Base {
        constructor () {}
    }
    class Derived extends Base {
        constructor () {
            super()        // Call Base class constructor
        }
    }
    class Derived2 extends Base {
        constructor (x: number) {
            super()        // Call Base class constructor
        }
    }

Semantic check for a ``super`` call is performed in accordance with
:ref:`Compatibility of Call Arguments`.


.. index::
   explicit constructor call
   constructor call
   superclass constructor call
   this keyword
   super keyword
   constructor
   superclass
   call
   superclass constructor call
   constructor call
   non-static field
   instance method
   base class

|

.. _Default Constructor:

Default Constructor
===================

.. meta:
    frontend_status: Done

If a class contains no constructor declaration, then a default constructor
is implicitly declared. This guarantees that every class effectively has at
least one constructor. The form of a default constructor has the following:

-  Default constructor has modifier ``public`` (see :ref:`Access Modifiers`).

-  Default constructor has no parameters.

Default constructor body for any class except class ``Object`` contains:

- Call to a superclass parameterless constructor.
- Mandatory execution of field initializers (if any) in the order they appear
  in a class body.

Default constructor body for the class ``Object`` (see :ref:`Type Object`)
is empty.


A :index:`compile-time error` occurs if a class has a default constructor, but
its superclass has no accessible constructor (see :ref:`Accessible`) without
parameters.

.. index::
   class
   constructor declaration
   constructor
   public modifier
   access modifier
   call
   constructor body
   superclass constructor
   argument
   class Object
   accessible constructor
   accessibility
   parameter
   execution
   field initializer
   class body
   default constructor
   superclass
   accessible constructor
   parameter
   access
   accessibility

.. code-block:: typescript
   :linenos:

   // Class declarations with default constructors declared implicitly
   class Base_no_ctor_declared {}
   class Derived_no_ctor_declared extends Base_no_ctor_declared {}

   // Example of an error case
   class A {
       private constructor () {}
   }
   class B0 extends A {} // Compile-time error as default constructor for B0
                         // cannot call super() as it is private
   class B1 extends A {
        constructor () {
            super ()   // Compile-time error as super() is private
        }
   }

.. index::
   class declaration
   constructor
   default constructor
   superclass
   error
   constructor call
   compilation
   super
   private
   access

|

.. _Inheritance:

Inheritance
***********

.. meta:
    frontend_status: Done

Class ``C`` inherits all non-static accessible members from its direct
superclass and direct superinterfaces (see :ref:`Accessible`), and optionally
overrides or implements some of the inherited members.

If ``C`` is not abstract, then it must implement all inherited abstract methods.
The method of each inherited abstract method must be defined with
*override-compatible* signatures (see :ref:`Override-Compatible Signatures`).

Semantic checks performed while overriding inherited methods and accessors are
described in :ref:`Overriding in Classes`.

Semantic checks performed while overriding fields and
implementing properties are described in the following sections:

- :ref:`Override Fields`,
- :ref:`Implementing Required Interface Properties`,
- :ref:`Implementing Optional Interface Properties`.

Constructors from the direct superclass of ``C``  are not subject of overriding
because such constructors are not accessible (see :ref:`Accessible`) in ``C``
directly, and can only be called from a constructor of ``C`` (see
:ref:`Constructor Body`).

.. index::
   class
   inheritance
   inherited member
   accessibility
   accessible member
   superclass
   superinterface
   direct superclass
   direct superinterface
   overriding
   semantic check
   abstract method
   override-compatible signature
   constructor
   constructor body
   accessor
   overriding

|

.. raw:: pdf

   PageBreak
