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

.. _Experimental Features:

Experimental Features
#####################

.. meta:
    frontend_status: Partly

This Chapter introduces the |LANG| features that are considered parts of
the language, but have no counterpart in |TS|, and are therefore not
recommended to those who seek a single source code for |TS| and |LANG|.

Some features introduced in this Chapter are still under discussion. They can
be removed from the final version of the |LANG| specification. Once a feature
introduced in this Chapter is approved and/or implemented, the corresponding
section is moved to the body of the specification as appropriate.

The *array creation* feature introduced in
:ref:`Resizable Array Creation Expressions` enables programmers to create
objects of the array type at runtime by providing the following as arguments:

- Array size;
- One element to fill the array with, or a lambda to generate a set of elements
  to fill the array with.

This addition is useful to other array-related features of the language, such
as array literals. This feature can also be used to create arrays of arrays.

Overloading functions, methods, or constructors is a practical and convenient
way to write program actions that are similar in logic but different in
implementation. |LANG| uses :ref:`Explicit Overload Declarations` as an innovative
form of *managed overloading*.

.. index::
   implementation
   array creation
   runtime expression
   array
   array literal
   constructor
   function
   method
   array type
   runtime
   array size
   function overloading
   method overloading
   implementation
   constructor overloading
   overload declaration

Section :ref:`Native Functions and Methods` introduces practically important
and useful mechanisms for the inclusion of components written in other languages
into a program written in |LANG|.

Sections :ref:`Final Classes` and :ref:`Final Methods`
discuss the well-known feature that
in many OOP languages provides a way to restrict class inheritance and method
overriding. Making a class *final* prohibits defining classes derived from it,
whereas making a method *final* prevents it from overriding in derived classes.

Section :ref:`Adding Functionality to Existing Types` discusses the way to
add new functionality to an already defined type.

.. index::
   native function
   native method
   function overloading
   method overloading
   final class
   final method
   object-oriented programming (OOP)
   OOP (object-oriented programming)
   inheritance

|

.. _Type char:

Type ``char``
*************

.. meta:
    frontend_status: Partly

Values of ``char`` type are 16-bit Unicode code units.
Any Unicode code point can be encoded with one or two ``char`` values.

.. list-table::
   :width: 100%
   :widths: 15 60
   :header-rows: 1

   * - Type
     - Type's Set of Values
   * - ``char`` (16-bits)
     - Symbols (code units) with codes from \U+0000 to \U+FFFF

Predefined constructors, methods, and constants for ``char`` type are
parts of the |LANG| :ref:`Standard Library`.

Type ``char`` is a class type that is a part of the
:ref:`Standard Library`. It means that type ``char`` is a subtype of
``Object``, and that it can be used at any place where a class name is
expected.

.. code-block:: typescript
   :linenos:

    let a_char: char = c'a'
    console.log (a_char)
    // Output is: a
    let o: Object = a_char // OK

.. index::
   char type
   Unicode code point
   set of values
   predefined constructor
   predefined method
   predefined constant
   char type

|

.. _char Literals:

``char`` Literals
=================

.. meta:
    frontend_status: Done

*Char literal* represents a 16-bit Unicode code unit that can be written as
a single UTF-16 symbol or a single escape sequence preceded by the characters
*single quote* (U+0027) and '*c*' (U+0063), and followed by a *single quote*.

The syntax of *character literal* is represented below:

.. code-block:: abnf

      CharLiteral:
          'c\'' SingleQuoteCharacter '\''
          ;

      SingleQuoteCharacter:
          ~['\\\r\n]
          | '\\' EscapeSequence
          ;

The examples are presented below:

.. code-block:: typescript
   :linenos:

      c'a'
      c'\n'
      c'\x7F'
      c'\u0000'

If a literal cannot be represented by an unsigned 16-bit value, then a
:index:`compile-time` occurs:

.. code-block:: typescript
   :linenos:

      c'\u{FFFFF}' // Compile-time error


*Char literals* are of type ``char``.

.. index::
   char literal
   value
   character
   syntax
   escape sequence
   single quote
   type char
   value

|

.. _char Operations:

``char`` Operations
===================

.. meta:
    frontend_status: Partly

Equality operators (see :ref:`Equality Expressions`) and relational operators
:ref:`Relational Expressions`) can be used if:

-  both operands are of ``char`` type; or
-  one operand is of ``char`` type and other is of a numeric type
   (see :ref:`char Conversions for Relational and Equality Operands`);
-  otherwise, a :index:`compile-time error` occurs.

In first case, the operation is performed as an integer comparison of two unsigned 16-bit values.
In the second case, the operation is performed as an integer comparison of the correspondent
numeric type.

.. code-block:: typescript
   :linenos:

   let c: char = c'A'
   let c1 = new char
   c1 = c'A'

   // The following lines both print true as values are equal
   console.log(c == c1)  // true
   console.log(c === c1) // true

   console.log(c == 0x41) // true
   
   c1 = c'B'
   console.log(c < c1)  // true
   console.log(c < 0x41)  // false
   
   console.log(c > 3.14)  // true
  
|

.. _Fixed-Size Array Types:

Fixed-Size Array Types
**********************

.. meta:
    frontend_status: Partly

*Fixed-size array type*, written as ``FixedArray<T>``, is the built-in type
characterized by the following:

-  Any instance of array type contains elements. The number of elements is known
   as *array length*, and can be accessed by using the property ``length``.
-  Array length is a non-negative integer number.
-  Array length is set once at runtime and cannot be changed later.
-  Array element is accessed by its index. *Index* is an integer number
   starting from *0* to *array length minus 1*.
-  Accessing an element by its index is a constant-time operation.
-  If passed to a non-|LANG| environment, an array is represented as a contiguous
   memory location.
-  Type of each array element is assignable to the element's type specified
   in the array declaration (see :ref:`Assignability`).

*Fixed-size arrays* differ from *resizable arrays* as follows:

- Fixed-size array length is set once to achieve better performance;
- Fixed-size arrays preserve the element type during the :ref:`Type Erasure`;
- Fixed-size arrays have no methods defined;
- Fixed-size arrays have several constructors (see
  :ref:`Fixed-Size Array Creation`);
- Fixed-size arrays are not compatible with *resizable arrays*.

Incompatibility between a resizable array and a fixed-size array is represented
by the example below:

.. code-block:: typescript
   :linenos:

    function foo(a: FixedArray<number>, b: Array<number>) {
        a = b // Compile-time error
        b = a // Compile-time error
    }

.. index::
   resizable array
   fixed-size array
   fixed-size array type
   built-in type
   instance
   array type
   length property
   array length
   index
   runtime
   access
   index
   integer number
   constant-time operation
   memory location
   assign
   assignability
   array declaration
   compatibility
   incompatibility

|

.. _Fixed-Size Array Creation:

Fixed-Size Array Creation
=========================

.. meta:
    frontend_status: Partly

*Fixed-size array* can be created by using :ref:`Array Literal` or
constructors defined for type ``FixedArray<T>``, where ``T`` must be a
type *preserved* by :ref:`Type Erasure`.

The use of an *array literal* to create an array is represented in following
examples:

.. code-block:: typescript
   :linenos:

    let a : FixedArray<number> = [1, 2, 3]
      /* create array with 3 elements of type number */
    a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
    let y = a[2] /* get the last element of array 'a' */
    let count = a.length // get the number of array elements
    y = a[3] // Will cause a runtime error - attempt to access non-existing array element

.. code-block:: typescript
   :linenos:

    function foo<T>(v: T): FixedArray<T | number> {
      return [v] // Compile-time error, T | number is not preserved by type erasure
    }
    let arr: FixedArray<string | number> = foo("a")

.. index::
   fixed-size array type
   array length
   array literal
   constructor
   fixed-size array
   integer
   array element
   access
   assignability
   resizable array
   runtime error

The following constructor creates an instance of ``FixedArray<T>``
of the specified length, filled with a single value ``elem``: 

- ``constructor(len: int, elem: T)``

.. code-block:: typescript
   :linenos:

    let a = new FixedArray<string>(3, "a") // creates array ["a", "a", "a"]

.. index::
   constructor
   array instance

|

.. _Value Array Types:

Value Array Types
*****************

.. meta:
    frontend_status: None

*Value array type* is the built-in type written as
``ValueArray<T>`` and characterized by the following: 

-  Any instance of array type contains elements of type ``T``. ``T`` must be
   a *value type* (see :ref:`Value Types`).
-  The number of elements is known as *array length*, and can be accessed
   by using the property ``length``.
-  Array length is a non-negative integer number.
-  Array length is set once at runtime and cannot be changed later.
-  Array element is accessed by its index. *Index* is an integer number
   starting from *0* to *array length minus 1*.
-  Accessing an element by its index is a constant-time operation.
-  If passed to a non-|LANG| environment, an array is represented as a contiguous
   memory location, filled by the primitive values (not references).
-  Type of each array element is equal to the element's type specified
   in the array declaration.
-  No subtyping relation holds between two ``ValueArray`` types, except where
   their type arguments are identical.   

.. note:: 

    - ``ValueArray<T>`` is not a generic type, despite using
      notation identical to generics.
    
    - Limitations imposed by ``ValueArray`` subtyping make it more performant
      compared to :ref:`Fixed-Size Array Types`.

.. index::
   value array type
   built-in type
   length property
   array length
   index
   runtime
   access
   index
   integer number
   constant-time operation

*Value array* can be created by using :ref:`Array Literal` or
constructors defined for type ``ValueArray<T>`` (see below).

The use of an *array literal* to create an array is represented in following
examples:

.. code-block:: typescript
   :linenos:

    let a : ValueArray<int> = [1, 2, 3]
      /* create array with 3 elements of type int */
    a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
    let y = a[2] /* get the last element of array 'a' */
    let count = a.length // get the number of array elements
    y = a[3] // runtime error, attempt to access non-existing array element

If ``ValueArray`` is used with non-value type argument,
then a :index:`compile-time error` occurs as follows: 

.. code-block:: typescript
   :linenos:
   
    let x: ValueArray<string> = ["aa"]   // Compile-time error
    type A = ValueArray<int | undefined> // Compile-time error

The following constructor creates an instance of ``ValueArray<T>``
of the specified length, filled with a single value ``elem``: 

- ``constructor(len: int, elem: T)``

.. code-block:: typescript
   :linenos:

    let a = new ValueArray<double>(3, 7.) // creates array [7., 7., 7.]

.. index::
   constructor
   array instance

|

.. _Resizable Array Creation Expressions:

Resizable Array Creation Expressions
************************************

.. meta:
    frontend_status: Done

*Array creation expression* creates new objects that are instances of *resizable
arrays* (see :ref:`Resizable Array Types`). An array instance can be created
alternatively by using :ref:`Array literal`.

The syntax of *array creation expression* is presented below:

.. code-block:: abnf

    newArrayInstance:
        'new' arrayElementType dimensionExpression '(' arrayElement ')'
        ;

    arrayElementType:
        typeReference
        | '(' type ')'
        ;

    dimensionExpression:
        '[' expression ']'
        ;

    arrayElement: 
      expression
    ;

.. code-block:: typescript
   :linenos:

    let x = new number[3] (7) // create array instance: [7, 7, 7]

.. index::
   resizable array
   array creation expression
   object
   instance
   array
   array instance
   array literal
   syntax
   expression

*Array creation expression* creates an object that is a new array with the
elements of the type specified by ``arrayElementType``.

The type of the *dimension expression* must be assignable (see
:ref:`Assignability`) to an ``int`` type. Otherwise,
a :index:`compile-time error` occurs.

A :index:`compile-time error` occurs if the *dimension expression* is a
constant expression that is evaluated to a negative integer value at compile
time.

.. index::
   array creation expression
   array
   type
   dimension expression
   assignment
   conversion
   integer
   integer type
   negative integer value
   int type
   assignability
   type
   integer value
   type int
   constant expression
   compile time

Type of ``arrayElement`` ``expression`` must be be assignable (see
:ref:`Assignability`) to ``arrayElementType``.
Otherwise, a :index:`compile-time error` occurs.

.. index::
   dimension expression
   floating-point type
   compile-time error
   runtime error
   expression
   array element
   array dimension


.. code-block:: typescript
   :linenos:

      let x = new number[-3] (0) // Compile-time error

      let y = new number[3.14] (0) // Compile-time error

      function foo (length: int) {
         let y = new number[length] (0)  // runtime error
      }
      foo (-3)


.. index::
   class
   accessibility
   access
   parameterless constructor
   constructor
   parameter
   optional parameter
   default value

A :index:`compile-time error` occurs if ``arrayElementType`` is a type
parameter:

.. code-block:: typescript
   :linenos:

      class A<T> {
         foo(element: T) {
            new T[2] (element) // Compile-time error, 'T' is a type parameter
         }
      }

.. index::
   compile-time error
   constructor
   type parameter
   array

The creation of an array with a known number of elements is presented below:

.. code-block:: typescript
   :linenos:

      class A {
        constructor (x: number) {}
      }

      let array_size = 5

      let array = new A[array_size] (new A(1))
         /* Create array of 'array_size' elements and all of them will have
            initial value equal to an object created by new A expression */

The creation of exotic arrays with different kinds of element types is presented
below:

.. index::
   array
   array creation
   parameterless constructor
   default value
   type
   lambda function
   index

.. code-block:: typescript
   :linenos:

    let array_of_union = new (Object|undefined) [5] (undefined) // filled with undefined

    type Functor = () => void
    let array_of_functor = new Functor[5] ( (): void => {}) // filled with lambda    

    type Arr = number []
    let array_of_array = new Arr [5] ( [3.14] ) // filled with array literal

|

.. _Runtime Evaluation of Array Creation Expressions:

Runtime Evaluation of Array Creation Expressions
================================================

.. meta:
    frontend_status: Partly
    todo: initialize array elements properly - #14963, #15610

The evaluation of an array creation expression at runtime is performed
as follows:

#. The dimension expression is evaluated. If the dimension expression
   evaluation completes abruptly, then *array creation expression* also does
   so.

#. The value of dimension expression is checked. If its value is less than
   zero, then ``NegativeArraySizeError`` is thrown.

#. Space for the new array is allocated. If the available space is not
   sufficient to allocate the array, then ``OutOfMemoryError`` is thrown,
   and the evaluation of the array creation expression completes abruptly.

#. Then, a one-dimensional array is created. Each element of this array is
   initialized either with the value passed or by calls to the lambda
   generating a set of values.

.. index::
   runtime evaluation
   array
   array creation
   array creation expression
   evaluation
   dimension expression
   constructor
   abrupt completion
   expression
   space allocation
   class type
   runtime
   runtime evaluation
   evaluation
   initialization

|

.. _Indexable Types:

Indexable Types
***************

.. meta:
    frontend_status: Done

If a class or an interface declares one or two functions with names ``$_get``
and ``$_set``, and signatures *(index: Type1): Type2* and *(index: Type1,
value: Type2)* respectively, then an indexing expression (see
:ref:`Indexing Expressions`) can be applied to variables of such types:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    class SomeClass {
       $_get (index: number): SomeClass { return this }
       $_set (index: number, value: SomeClass) { }
    }
    let x = new SomeClass
    x = x[1] // This notation implies a call: x = x.$_get (1)
    x[1] = x // This notation implies a call: x.$_set (1, x)

If only one function is present, then only the appropriate form of indexing
expression (see :ref:`Indexing Expressions`) is available:

.. index::
   indexable type
   interface
   class
   declaration
   function name
   function
   signature
   indexing expression
   variable
   type

.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

    class ClassWithGet {
       $_get (index: number): ClassWithGet { return this }
    }
    let getClass = new ClassWithGet
    getClass = getClass[0]
    getClass[0] = getClass // Error - no $_set function available

    class ClassWithSet {
       $_set (index: number, value: ClassWithSet) { }
    }
    let setClass = new ClassWithSet
    setClass = setClass[0] // Error - no $_get function available
    setClass[0] = setClass

Type ``string`` can be used as a type of the index parameter:

.. index::
   function
   indexing expression
   string
   string type
   type
   index parameter

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    class SomeClass {
       $_get (index: string): SomeClass { return this }
       $_set (index: string, value: SomeClass) { }
    }
    let x = new SomeClass
    x = x["index string"]
       // This notation implies a call: x = x.$_get ("index string")
    x["index string"] = x
       // This notation implies a call: x.$_set ("index string", x)

Functions ``$_get`` and ``$_set`` are ordinary functions with compiler-known
signatures. The functions can be used like any other function.
The functions can be abstract, or defined in an interface and implemented later.
The functions can be overridden and provide a dynamic dispatch for the indexing
expression evaluation (see :ref:`Indexing Expressions`). The functions can be
used in generic classes and interfaces for better flexibility. A
:index:`compile-time error` occurs if these functions are marked as ``async``.

.. index::
   function
   ordinary function
   compiler
   compiler-known signature
   abstract function
   signature
   overriding
   interface
   implementation
   dynamic dispatch
   implementation
   indexing expression
   indexing expression evaluation
   generic class
   generic interface
   evaluation
   flexibility
   async function

.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

    interface ReadonlyIndexable<K, V> {
       $_get (index: K): V
    }

    interface Indexable<K, V> extends ReadonlyIndexable<K, V> {
       $_set (index: K, value: V)
    }

    class IndexableByNumber<V> implements Indexable<number, V> {
       private data: V[] = []
       $_get (index: number): V { return this.data [index] }
       $_set (index: number, value: V) { this.data[index] = value }
    }

    class IndexableByString<V> implements Indexable<string, V> {
       private data = new Map<string, V>
       $_get (index: string): V { return this.data [index] }
       $_set (index: string, value: V) { this.data[index] = value }
    }

    class BadClass extends IndexableByNumber<boolean> {
       override $_set (index: number, value: boolean) { index / 0 }
    }

    let x: IndexableByNumber<boolean> = new BadClass
    x[42] = true // This will be dispatched at runtime to the overridden
       // version of the $_set method
    x.$_get (15)  // $_get and $_set can be called as ordinary
       // methods

|

.. _Iterable Types:

Iterable Types
**************

.. meta:
    frontend_status: Done

A class or an interface is *iterable* if it implements the interface ``Iterable``
defined in the :ref:`Standard Library`, and thus has an accessible parameterless
method with the name ``$_iterator`` and a return type that is a subtype (see
:ref:`Subtyping`) of type ``Iterator`` as defined in the :ref:`Standard Library`.
It guarantees that an object returned by the ``$_iterator`` method is of the
type which implements ``Iterator``, and thus allows traversing an object of the
*iterable* type.

A union of iterable types is also *iterable*. It means that instances of such
types can be used in ``for-of`` statements (see :ref:`For-Of Statements`).

Array (see :ref:`Array Types`) and string (see :ref:`Type string`) types are
iterable.

An *iterable* class ``C`` is represented in the example below:

.. index::
   iterable class
   class
   iterable interface
   interface
   parameterless method
   access
   accessibility
   subtyping
   subtype
   iterator
   instance
   for-of statement
   return type
   traversing
   assignability
   type Iterator
   implementation
   iterable type
   union
   for-of statement
   object

.. code-block:: typescript
   :linenos:

      class C implements Iterable<string> {
        data: string[] = ['a', 'b', 'c']
        $_iterator() { // Return type is inferred from the method body
          return new CIterator(this)
        }
      }

      class CIterator implements Iterator<string> {
        index = 0
        base: C
        constructor (base: C) {
          this.base = base
        }
        next(): IteratorResult<string> {
          return {
            done: this.index >= this.base.data.length,
            value: this.index >= this.base.data.length ? "" : this.base.data[this.index++]
          }
        }
      }

      let c = new C()
      for (let x of c) {
            console.log(x)
      }

In the example above, class ``C`` method ``$_iterator`` returns
``CIterator<string>`` that implements ``Iterator<string>``. If executed,
this code prints out the following:

.. code-block:: typescript

    "a"
    "b"
    "c"

The method ``$_iterator`` is an ordinary method with a compiler-known
signature. This method can be used like any other method. It can be
abstract or defined in an interface to be implemented later. A
:index:`compile-time error` occurs if this method is marked as ``async``.

.. index::
   type inference
   inferred type
   method
   method body
   ordinary method
   class
   iterator
   compiler-known signature
   compiler
   signature
   implementation
   async method

.. note::
   To support the code compatible with |TS|, the name of the method
   ``$_iterator`` can be written as ``[Symbol.iterator]``. In this case, the
   class ``C`` from the example above looks as follows:

   .. code-block-meta:

   .. code-block:: typescript
      :linenos:

         class C implements Iterable<string>  {
           data: string[] = ['a', 'b', 'c'];
           [Symbol.iterator]() {
             return new CIterator(this)
           }
         }

The use of the name ``[Symbol.iterator]`` is considered deprecated.
It can be removed in the future versions of the language.

.. index::
   compatibility
   compatible code
   name
   class
   method
   iterator
   iterable class

|

.. _Callable Types:

Callable Types
**************

.. meta:
    frontend_status: Partly
    todo: add $_ to names

A type is *callable* if the name of the type can be used in a call expression.
A call expression that uses the name of a type is called a *type call
expression*. Only class type can be callable. To make a type
callable, a static method either with the name ``$_invoke`` or with the name
``$_instantiate`` must be defined:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    class C {
        static $_invoke() { console.log("invoked") }
    }
    C() // prints: invoked
    C.$_invoke() // also prints: invoked

In the above example, ``C()`` is a *type call expression*. It is the short
form of the normal method call ``C.$_invoke()``. Using an explicit call is
always valid for the methods ``$_invoke`` and ``$_instantiate``.

A class can define either the method ``$_invoke()`` or the method ``$_instantiate``
but not both. Otherwise, a :index:`compile-time error` occurs. However, a class
can define several implementations of the methods ``$_invoke`` or ``$_instantiate``
with different signatures:

..  code-block:: typescript
    :linenos:

    // Compile-time error, both $_invoke and $_instantiate defined
    class A {
        static $_invoke(i: int): int { return i; }
        static $_instantiate(factory: () => A): A { return factory(); }
    }

    // OK, two $_invoke with different signatures
    class B {
        static $_invoke(p: int): int { return p; }
        static $_invoke(): string { return "hello"; }
    }

Static methods have no access to type parameters of generic in |LANG|. It means
that the method ``$_instantiate`` cannot be declared for a generic type. The
method ``$_invoke`` can be declared, but the *type call expression* or explicit
call of ``$_invoke()`` must not use a type parameter.


.. index::
   callable type
   call expression
   type name
   expression
   instantiation
   invocation
   type call expression
   callable class type
   callable type
   class type
   type call expression
   method call
   inheritance
   static method
   normal method call
   call
   explicit call
   method

.. note::
   Only a constructor---not the methods ``$_invoke`` or ``$_instantiate``---is
   called in a *new expression*:

   .. code-block-meta:

   .. code-block:: typescript
      :linenos:

       class C {
           static $_invoke() { console.log("invoked") }
           constructor() { console.log("constructed") }
       }
       let x = new C() // constructor is called

The methods ``$_invoke`` and ``$_instantiate`` are similar but have differences
as discussed below.

.. index::
   constructor
   method
   instantiation
   invocation
   call
   new expression
   callable type

|

.. _Callable Types with $_invoke Method:

Callable Types with ``$_invoke`` Method
=======================================

.. meta:
    frontend_status: Done

The static method ``$_invoke`` can have an arbitrary signature. The method
is either called implicitly in a *type call expression*, or called explicitly.
The class can have several ``$_invoke`` methods with different signatures. If
the signature has parameters, then the call must contain corresponding arguments.

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    class Add {
        static $_invoke(a: number, b: number): number {
            return a + b
        }
        static $_invoke(a: string, b: string): string {
            return a + b
        }
    }
    console.log(Add(2, 2)) // prints: 4
    console.log(Add.$_invoke(2, 2)) // prints: 4
    console.log(Add("Number ", "one")) // prints "Number one"


A class can declare an instance method ``$_invoke``
but the method does not make the class *callable*.

.. index::
   static method
   invocation
   callable type
   arbitrary signature
   signature
   parameter
   method
   type call expression
   argument
   instance method
   type

|

.. _Callable Types with $_instantiate Method:

Callable Types with ``$_instantiate`` Method
============================================

.. meta:
    frontend_status: Done

The static method ``$_instantiate`` can have an arbitrary signature by itself.
If it is to be used in a *type call expression*, then
its first parameter must be a *factory* defined as
a parameterless function type returning the class
type in which the method ``$_instantiate`` is declared. The method can have or
not have other parameters which can be arbitrary. The return type of the method
``$_instantiate`` is typically the same as the return type of the factory,
but can be arbitrary instead. A class can contain several static
``$_instantiate`` methods with different sets of parameters. If a class declares
two ``$_instantiate`` methods that have the same parameter set but different
return types, then a :index:`compile-time error` occurs.

In a *type call expression*, the argument corresponding to the ``factory``
parameter is passed implicitly:

.. code-block:: typescript
   :linenos:

    class C {
        // #1, parameterless
        static $_instantiate(factory: () => C): C {
            return factory()
        }

        // #2. As #1, but with another return type
        // If uncommented, then a compile-time error occurs
        // static $_instantiate(factory: () => C): int {
        //     return 1
        // }

        // #3, with string parameter
        static $_instantiate(factory: () => C, s: string): string {
            return "hello " + s
        }
    }

    let x = C() // #1 called, factory is passed implicitly

    // Explicit call of #1 requires explicit 'factory':
    let y = C.$_instantiate(() => { return new C()})

    let s: string = C("world") // #3 called, factory is passed implicitly


.. index::
   static method
   callable type
   method
   instantiation
   signature
   arbitrary signature
   type call expression
   parameter
   factory parameter
   parameterless function type
   class type
   type call expression

If the method ``$_instantiate`` has additional parameters, then the call must
contain corresponding arguments:

.. code-block:: typescript
   :linenos:

    class C {
        name = ""
        static $_instantiate(factory: () => C, name: string): C {
            let x = factory()
            x.name = name
            return x
        }
    }
    let x = C("Bob") // factory is passed implicitly

A :index:`compile-time error` occurs in a *type call expression* with type ``T``,
if:

- ``T`` has neither method ``$_invoke`` nor  method ``$_instantiate``; or
- ``T`` has the method ``$_instantiate`` but its first parameter is not
  a ``factory``.


.. code-block-meta:
    expect-cte

.. code-block:: typescript
   :linenos:

    class C {
        static $_instantiate(factory: string): C {
            return factory()
        }
    }
    let x = C() // Compile-time error, wrong '$_instantiate' 1st parameter

Where the method ``$_instantiate`` is used implicitly
in the *type call expression*:

- If the method ``$_instantiate`` does not declare
  ``factory`` as an *optional parameter*, then a ``factory``
  implementation is generated automatically.

- If the method ``$_instantiate`` declares ``factory``
  as an *optional parameter* (see :ref:`Optional Parameters`), then the default
  implementation is used for ``factory``.

..  code-block:: typescript
    :linenos:

    class A {
        static $_instantiate(
            factory: () => A): A { return factory() }
    }
    class B {
        static $_instantiate(
            factory: () => B = () =>{
                console.log("default factory");
                return new B; } ): B
            { return factory() }
    }

    A() // Automatically generated factory is used
    B() // Default implementation is used for factory

A *type call expression* passes no arguments
to the ``factory`` function, and the latter uses
a parameterless class constructor. If a class has
no parameterless class constructor, then a
:index:`compile-time error` occurs:

..  code-block:: typescript
    :linenos:

    class A {
        constructor(p: int) {}
        static $_instantiate(factory: () => A): A { return factory() }
    }

    A() // Compile-time error, no parameterless constructor


..  note::
    Calling the method ``$_instantiate`` explicitly
    with such a class, or supplying the default
    implementation for the factory that uses
    a constructor with parameters, is still
    possible though useless:

    ..  code-block:: typescript
        :linenos:

        class A {
            constructor(p: int) {}
            static $_instantiate(
                factory: () => A = () => { return new A(1); }
                ): A { return factory() }
        }

        A() // OK, default is used for the optional factory
        A.$_instantiate(() => { return new A(1); }) // OK, explicit call


A class can declare an instance method ``$_instantiate``
but the method does not make the class *callable*.

.. index::
   method
   call
   factory
   type call expression
   instantiation
   invocation
   parameter
   callable type
   instance method
   instance

|

.. _Statements Experimental:

Statements
**********

.. meta:
    frontend_status: Done

|

.. _For-of Explicit Type Annotation:

For-of Explicit Type Annotation
===============================

.. meta:
    frontend_status: Partly
    todo: check assignability

An explicit type annotation is allowed for a *ForVariable*
(see :ref:`For-Of Statements`):

.. code-block:: typescript
   :linenos:

      // explicit type is used for a new variable,
      let x: string[] = ["aaa", "bbb", "ccc"]
      for (let str: string of x) {
        console.log(str)
      }

Type of elements in a ``for-of`` expression must be assignable
(see :ref:`Assignability`) to the type of the variable. Otherwise, a
:index:`compile-time error` occurs.

.. index::
   type annotation
   annotation
   for-variable
   expression
   assignability
   variable
   for-of type statement

|

.. _Explicit Overload Declarations:

Explicit Overload Declarations
******************************

.. meta:
    frontend_status: None

|LANG| supports conventional overloading for functions, methods, and
constructors (i.e. implicit overloading of same-name entities), and an
innovative form of explicit overload declarations that allows
a developer to specify a set of overloaded entities explicitly and to control
the overload resolution process.

Regardless of implicit or explicit overloading being used, the actual entity
to be called is determined at compile time. As a result, *overloading* is
related to *compile-time polymorphism by name*. The semantic details are
discussed in :ref:`Overloading`.

.. index::
    polymorphism
    polymorphism by name
    entity
    overloading
    overloaded entity
    compile time
    compatibility
    semantics

An *explicit overload declaration* can be used for:

- Functions (see :ref:`Explicit Function Overload`), including functions in
  namespaces;
- Class or interface methods (see :ref:`Explicit Class Method Overload` and
  :ref:`Explicit Interface Method Overload`).

An *overload declaration* starts with the keyword ``overload`` and
declares an *ordered overload set*. The exact syntax of the declaration
is presented in the appropriate subsections.

.. index::
    overload declaration
    overloaded entity
    entity
    function
    method
    constructor
    overload declaration
    namespace
    class method
    interface method
    method declaration
    overload keyword
    overload set
    entity

The use of an explicit overload declaration is represented in the example below:

.. code-block:: typescript
   :linenos:

    function max2(a: number, b: number): number {
        return  a > b ? a : b
    }
    function maxN(...a: number[]): number {
        // return max element
    }

    // declare 'max' as an ordered set of functions max2 and maxN
    overload max { max2, maxN }

    max(1, 2)     // max2 is called
    max(3, 2, 4)  // maxN is called
    max("a", "b") // Compile-time error, no function to call

The semantics of an entity included into an *overload set* does not change.
Such entities follow the ordinary accessibility rules, and can be called
explicitly as follows:

.. code-block:: typescript
   :linenos:

    maxN(1, 2) // maxN is explicitly called
    max2(2, 3) // max2 is explicitly called

When calling an *explicit overload*, entities from an *overload set* are checked
in the listed order, and the first entity with an appropriate signature is
called (see :ref:`Overload resolution` for detail).
A :index:`compile-time error` occurs if no entity with an appropriate signature
is available:

.. index::
    function
    semantics
    entity
    overload
    accessibility
    overload set
    overload resolution
    signature

.. code-block-meta:
    expect-cte

.. code-block:: typescript
   :linenos:

    max(1)    // maxN is called
    max(1, 2) // max2 is called, as is the first appropriate in the set

    max("a", "b") // Compile-time error, no function to call

Each identifier in an *explicit overload declaration* must denote exactly one
accessible entity.

If an identifier denotes an implicitly overloaded name, then a
:index:`compile-time error` occurs.

An *explicit overload declaration* never expands an implicitly overloaded name
into several entities.

An overloaded entity in an *explicit overload declaration* can be *generic*
(see :ref:`Generics`).

If type arguments are provided explicitly in a call of an overloaded entity
(see :ref:`Explicit Generic Instantiations`), then only the entities that have
the number of type arguments compatible with the number of mandatory and
optional type parameters (i.e., entities with optional type parameters are the
entities that have type parameter default) are considered during
:ref:`Overload Resolution`:

.. code-block:: typescript
   :linenos:

    // Resolution with explicit type arguments
    function one<T>() { console.log("one") }
    function two<T, U=string>() { console.log("two") }
    function three<T, U=string, V=number>() { console.log("three") }

    overload numbers { one, two, three }

    numbers<string, number, int>() // Only 'three` considered

    numbers<string, number>() // 'two' and 'three; considered as both
                              // allow 2 type arguments

    numbers<int>()  // 'one', 'two' and 'three; considered as all
                    // allow 1 type argument


If *type arguments* are not provided explicitly (see
:ref:`Implicit Generic Instantiations`), then consideration is given to all
entities as represented in the example below:

.. index::
    entity
    call
    call site
    function call
    overloaded entity
    overload declaration
    generic
    generic instantiation
    type argument
    type parameter
    overload resolution

.. code-block:: typescript
   :linenos:

    function foo1(s: string) {}
    function foo2<T>(x: T) {}

    overload foo { foo1, foo2 }

    foo("aa")   // foo1 is called
    foo(1) // foo2 is called, implicit generic instantiation
    foo<string>("aa") // foo2 is called

An entity can be listed in several *explicit overload declarations*:

.. code-block:: typescript
   :linenos:

    function max2i(a: int, b: int): int {
        return  a > b ? a : b
    }
    function maxNi(...a: int[]): int {
        // return max element
    }
    function maxN(...a: number[]): number {
        // return max element
    }

    overload maxi { max2i, maxNi }
    overload max { max2i, maxNi, maxN }

.. index::
    entity
    function
    overload declaration
    generic instantiation

|

.. _Explicit Function Overload:

Explicit Function Overload
==============================

.. meta:
    frontend_status: None

*Explicit function overload* allows declaring a name for a set of functions
(see :ref:`Function Declarations`). The syntax is presented below:

.. code-block:: abnf

    explicitFunctionOverload:
        'overload' identifier overloadList
        ;
    overloadList:
        '{' identifier (',' identifier)* ','? '}'
        ;

.. index::
    explicit function overload
    set of functions
    function declaration
    function
    syntax
    qualified name

A :index:`compile-time error` occurs if an *identifier* in the list:

- refers to no accessible function;
- refers to an implicitly overloaded function name; or
- refers to a non-function entity.

All overloaded functions must be in the same module or namespace scope (see
:ref:`Scopes`). Otherwise, a :index:`compile-time error` occurs. The erroneous
overload declarations are represented in the example below:

.. code-block:: typescript
   :linenos:

    import {foo1} from "something"

    function foo2() {}
    overload foo {foo1, foo2} // Compile-time error

    namespace N {
        export function fooN() {}
        namespace M {
            export function fooM() {}
        }
        overload goo {M.fooM, fooN} // Compile-time error
    }
    overload bar {foo2, N.fooN} // Compile-time error

.. index::
    overloaded function
    module
    namespace
    namespace scope
    scope
    overload declaration
    import

A name of an *explicit function overload* can be the same as the name of a
function in the same scope only if that name denotes exactly one accessible
function and that function is used in the overloaded list. If that name denotes
an implicitly overloaded function set, then a :index:`compile-time error`
occurs.
This situation is represented in the following example:

.. code-block:: typescript
   :linenos:

    function foo(n: number): number {/*body1*/}
    function fooString(s: string): string {/*body2*/}

    overload foo {foo, fooString} // valid overload

    foo(1)    // function 'foo' is called
    foo("aa") // function 'fooString' is called

    function bar(): void {}

    // Invalid overload, as 'bar' does not appear in the list:
    overload bar {foo, fooString} // Compile-time error

    function baz(n: number): number {/*body1*/}
    function baz(s: string): string {/*body2*/}

    // Invalid overload, as 'baz' denotes an implicitly overloaded function set:
    overload baz {baz, fooString} // Compile-time error

    let name: string = "abc"

    // Invalid overload, as 'name' refers to a variable:
    overload name {foo, fooString, name} // Compile-time error

Using the name of a function as the name of an explicit overload causes no
ambiguity for it is considered at the call site only, i.e., a name of an
*explicit overload* is **not** considered in the following situations:

- List of the overloaded entities;

- :ref:`Function Reference`.

.. index::
    name
    overloaded function
    function
    entity
    function reference

.. code-block:: typescript
   :linenos:

    function foo(n: number): number {/*body1*/}
    function fooString(s: string): string {/*body2*/}
    overload foo {foo, fooString}

    let func1 = foo // 'foo' refers to function, not to explicit overload

A :index:`compile-time error` occurs, if an *explicit overload* is exported
but an overloaded function is not:

.. code-block:: typescript
   :linenos:

    export function foo1(p: string) {}
    function foo2(p: number) {}
    export overload foo { foo1, foo2 } // Compile-time error, 'foo2' is not exported
    overload bar { foo1, foo2 } // OK, as 'bar' is not exported

If an *explicit overload* is called like a function with receiver, i.e., syntax
of method call is used (see :ref:`Functions with Receiver`), then a
:index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    function bar1(this: string) {}
    function bar2(this: number) {}

    overload bar { bar1, bar2 }

    let s: string = "";
    let n: number = 1;

    bar(s) // OK
    bar(n) // OK
    s.bar()  // Compile-time error
    n.bar()  // Compile-time error

|

.. _Explicit Class Method Overload:

Explicit Class Method Overload
==================================

.. meta:
    frontend_status: None

*Explicit class method overload* allows declaring a name
for a set of class methods (see :ref:`Method Declarations`).
The syntax is presented below:

.. code-block:: abnf

    explicitClassMethodOverload:
        explicitClassMethodOverloadModifier*
        'overload' identifier overloadList
        ;

    explicitClassMethodOverloadModifier: 'static' | 'async';

The use of an *explicit class method overload* is represented in the example
below:

.. index::
    class method
    class member
    static method
    instance method
    method
    explicit class method overload
    syntax
    set of methods
    identifier

.. code-block:: typescript
   :linenos:

    class Processor {
        overload process { processNumber, processString }
        processNumber(n: number) {/*body*/}
        processString(s: string) {/*body*/}
    }

    let c = new C()
    c.process(42) // calls processNumber
    c.process("aa") // calls processString

The name of an *explicit method overload* can be the same as the name of a
method in the same class (see :ref:`Explicit Overload Name Same As Method Name`
for details).

*Static explicit overload* is represented in the example below:

.. code-block:: typescript
   :linenos:

    class C {
        static one(n: number) {/*body*/}
        static two(s: string) {/*body*/}
        static overload foo { one, two }
    }

A :index:`compile-time error` occurs if:

-  Method modifier is used more than once in an explicit method overload;

-  *Identifier* in the overloaded method list refers to no accessible
   method (either declared or inherited) of the current class;

-  *Identifier* in the overloaded method list refers to an implicitly
   overloaded method name;

-  *Explicit overload* is:

    - *Static* but the overloaded method is *non-static*;
    - *Non-static* but the overloaded method is *static*;
    - Marked ``async`` but the overloaded method is not; or
    - Not ``async`` but the overloaded method is.


.. index::
    method modifier
    explicit method overload
    identifier
    accessible method
    declaration
    inheritance
    overloaded method

An *explicit overload* and the overloaded methods can have different access
modifiers. A :index:`compile-time error` occurs if an *explicit overload* is:

-  ``public`` but at least one overloaded method is not ``public``;

-  ``protected`` but at least one overloaded method is ``private``.


Valid and invalid explicit overloads are represented in the example below:

.. index::
    overloaded method
    explicit overload
    access modifier
    public
    protected
    private

.. code-block:: typescript
   :linenos:

    class C {
        private foo1(x: number) {/*body*/}
        protected foo2(x: string) {/*body*/}
        public foo3(x: boolean) {/*body*/}
        foo4() {/*body*/} // implicitly public

        public overload foo { foo3, foo4 } // OK
        protected overload bar { foo2, foo3 } // OK
        private overload goo { foo1, foo2, foo3 } // OK

        public overload err1 {foo2, foo3} // Compile-time error, foo2 is not public
        protected overload err2 {foo2, foo1} // Compile-time error, foo1 is private
    }

Some or all overloaded functions can be ``native`` as follows:

.. code-block:: typescript
   :linenos:

    class C {
        native foo1(x: number)
        foo2(x: string) {/*body*/}
        overload foo { foo1, foo2 }
    }

.. index::
    public
    overload
    private
    overloaded function
    native

If a superclass has an *explicit overload*, then this declaration can be
overridden in a subclass. If a subclass does not override an
*explicit overload*, then the overload from the superclass is inherited.

If a subclass overrides an *explicit overload*, then this declaration must
list all methods of the *explicit overload* in a superclass, otherwise, a
:index:`compile-time error` occurs.

In addition, overriding an *explicit overload* in a subclass can include
new methods and change the order of methods.

An *explicit overload* is used like an ordinary class method except that it is
replaced in a call at compile time for one of overloaded methods that use the
type of *object reference*. An *explicit overload* in subtypes is
represented in the example below:

.. index::
    superclass
    overload declaration
    overriding
    subclass
    inheritance
    declaration
    superclass
    overloaded method
    object reference
    method

.. code-block:: typescript
   :linenos:

    class Base {
        overload process { processNumber, processString }
        processNumber(n: number) {/*body*/}
        processString(s: string) {/*body*/}
    }

    class D1 extends Base {
        // method is overridden
        override processNumber(n: number) {/*body*/}
        // overload declaration is inherited
    }

    class D2 extends Base {
        // method is added:
        processInt(n: int) {/*body*/}
        // new order for overloaded methods is specified:
        overload process { processInt, processNumber, processString }
    }

    new D1().process(1)   // calls processNumber from D1

    new D2().process(1)   // calls processInt from D2 (as it is listed earlier)
    new D2().process(1.0) // calls processNumber from Base (first appropriate)

Methods with special names (see :ref:`Indexable Types`, :ref:`Iterable Types`,
and :ref:`Callable Types`) can be overloaded like ordinary methods:

.. index::
    overloaded method
    overriding
    method
    name
    iterable type
    callable type
    inheritance
    ordinary method
    name

.. code-block:: typescript
   :linenos:

    class C {
        getByNumber(n: number): string {...}
        getByString(s: string): string {...}
        overload $_get { getByNumber, getByString }
    }

    let c = new C()

    c[1]     // getByNumber is used
    c["abc"] // getByString is used

If a class implements some interfaces with an *explicit overload* of the
same name, then a new *explicit overload* must include all overloaded
methods. Otherwise, a :index:`compile-time error` occurs.

.. index::
    overloaded method
    class
    interface
    overload declaration
    alias

.. code-block:: typescript
   :linenos:

    interface I1 {
        overload foo {f1, f2}
        // f1 and f2 are declared in I1
    }
    interface I2 {
        overload foo {f3, f4}
        // f3 and f4 are declared in I2
    }
    class C implements I1, I2 {
       // Compile-time error as no new overload is defined
    }
    class D implements I1, I2 {
        overload foo { f2, f3, f1, f4 } // OK, as new overload is defined
    }
    class E implements I1, I2 {
        overload foo { f2, f4 } // Compile-time error as not all methods are used
    }

    const i1: I1 = new D
    i1.foo(<arguments>) // call is valid if arguments fit first signature of {f1, f2} set

    const i2: I2 = new D
    i2.foo(<arguments>) // call is valid if arguments fit first signature of {f3, f4} set

    const d: D = new D
    d.foo(<arguments>) // call is valid if arguments fit first signature of {f2, f3, f1, f4} set

.. index::
    overloaded interface
    declaration
    method
    argument
    signature

|

.. _Explicit Interface Method Overload:

Explicit Interface Method Overload
======================================

.. meta:
    frontend_status: None

*Explicit interface method overload* allows declaring a name
for a set of interface methods (see :ref:`Interface Method Declarations`).
The syntax is presented below:

.. code-block:: abnf

    explicitInterfaceMethodOverload:
        'overload' identifier overloadList
        ;

Each identifier in an *explicit interface method overload* list must denote
exactly one accessible interface method.

A :index:`compile-time error` occurs if an identifier refers to no accessible
method, to a non-method entity, or to an implicitly overloaded method name.

The use of an *explicit interface method overload* is represented in the
example below:

.. code-block:: typescript
   :linenos:

    interface I {
        foo(): void
        bar(n?: string): void
        overload goo { foo, bar }
    }

    function example(i: I) {
        i.goo()        // calls i.foo()
        i.goo("hello") // calls i.bar("hello")
        i.bar()        // explicit call: i.bar(undefined)
    }

.. index::
    interface method
    explicit overload
    interface

The name of an *explicit method overload* can be the same as the name of a
method in the same interface (see
:ref:`Explicit Overload Name Same As Method Name` for details).

An *explicit overload* is used like an ordinary interface method, except that
one of the overloaded methods replaces it in a call at compile time by using
the type of *object reference*.

An *explicit interface overload* can be overridden in a class. In that case,
an *explicit overload* in a class must contain all the methods overloaded in the
interface. Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

   class D implements I {
        foo(): void {/*body*/}
        bar(n?: string): void {/*body*/}
        overload goo( bar, foo) // order is changes
   }

   let d = new D()
   d.goo() // d.bar(undefined) is used, as it is the first appropriate method

If a class does not override an *explicit overload* declared in an interface,
then it inherits the overload:

.. code-block:: typescript
   :linenos:

   // Using interface overload declaration
   class C implements I {
        foo(): void {/*body*/}
        bar(n?: string): void {/*body*/}
   }

   let c = new C()
   c.goo() // calls c.foo()

.. index::
    ordinary method
    interface method
    call
    compile time
    overloaded method
    object reference
    type
    class
    implementation

An *explicit overload* defined in a superinterface can be overridden in a
subinterface. In this case, the *overload declaration* of the subinterface
must contain all methods overloaded in superinterface. Otherwise, a
:index:`compile-time error` occurs.

An *explicit overload* defined in a superinterface must be overridden in a
subinterface if several *explicit overloads* of the same name are inherited
in the interface. Otherwise, a :index:`compile-time error` occurs.

.. index::
    interface
    class
    explicit overload
    superinterface
    method
    subinterface
    overloaded method
    interface
    override
    inheritance

.. code-block:: typescript
   :linenos:

    interface I1 {
        overload foo {f1, f2}
        // f1 and f2 are declared in I1
    }
    interface I2 {
        overload foo {f3, f4}
        // f3 and f4 are declared in I2
    }
    interface I3 extends I1, I2 {
       // Compile-time error as no new overload for 'foo' is defined
    }
    interface I4 extends I1, I2 {
        overload foo { f4, f1, f3, f2 } // OK, as new overload is defined
    }
    interface I5 extends I1, I2 {
        overload foo { f1, f3 } // Compile-time error as not all methods are included
    }

|

.. _Explicit Overload Name Same As Method Name:

Explicit Overload Name Same As Method Name
==========================================

.. meta:
    frontend_status: None

The name of an *explicit overload* of a class or an interface can be the same
as the name of the overloaded method. For example, a method defined in a
superclass can be used as one of the overloaded methods in an *explicit
overload* of the same-name subclass. This important case is represented in the
following example:

.. code-block:: typescript
   :linenos:

    class C {
        foo(n: number): number {/*body*/}
    }
    class D extends C {
        fooString(s: string): string {/*body*/}

        overload foo {
            foo, // method 'foo' from C
            fooString
        }
    }

    let d = new D()
    let c: C = d

    d.foo(1)    // 'foo' from C is called
    d.foo("aa") // 'fooString' from D is called
    c.foo(1)    // method 'foo' from is called (no overload)

.. index::
    method name
    explicit overload
    overloaded method
    superclass
    subclass

If names of a method and of an *explicit overload* are the same, then the method
can be overridden as usual:

.. code-block:: typescript
   :linenos:

    class C {
        foo(n: number): number {/*body*/}
    }
    class D extends C {
        foo(n: number): number {/*body*/} // method is overridden
        fooString(s: string): string {/*body*/}

        overload foo { foo, fooString }
    }

This feature is also valid in interfaces, or in an interface and a class that
implements the interface:

.. index::
    method
    name
    method name
    overriding
    overridden method
    interface
    class
    implementation

.. code-block:: typescript
   :linenos:

    interface I {
        foo(n: number): number {/*body*/}
    }
    interface J extends I {
        fooString(s: string): string
        overload foo { foo, fooString }
    }

    class K implements I {
        foo(n: number): number {/*body*/}
        fooString(s: string): string {/*body*/}

        overload foo { foo, fooString }
    }

The use of an *explicit overload* causes no ambiguity for it is considered
at the call site only. An *explicit overload*  name is **not** considered
in the following situations:

- :ref:`Overriding`;

- List of the overloaded entities (see :ref:`Explicit Class Method Overload`
  and :ref:`Explicit Interface Method Overload`);

- :ref:`Method Reference`.

.. index::
    number
    interface
    string
    overload
    call site
    overriding
    overloaded entity
    method reference
    class method overload declaration
    method reference

.. code-block:: typescript
   :linenos:

    class C {
        foo(n: number): number {/*body*/}
    }

    class D extends C {
        fooString(s: string): string {/*body*/}

        overload foo { foo, fooString }
    }

    let d = new D()
    let c: C = d

    let func1 = c.foo // method 'foo' is used
    let func2 = d.foo // method 'foo' is used

A :index:`compile-time error` occurs if the name of an *explicit overload*
is the same as the name of a method (with the same static or non-static
modifier) that is not listed as an overloaded method as follows:

.. code-block:: typescript
   :linenos:

    class C {
        foo(n: number) {/*body*/}
        fooString(s: string) {/*body*/}
        fooBoolean(b: boolean) {/*body*/}

        overload foo { // Compile-time error
            fooBoolean, fooString
        }
    }

.. index::
    number
    string
    method
    static modifier
    non-static modifier
    overloaded method

|


.. _Native Functions and Methods:

Native Functions and Methods
****************************

.. meta:
    frontend_status: Done


.. _Native Functions:

Native Functions
================

.. meta:
    frontend_status: Done

*Native function* is a function marked with the keyword ``native`` (see
:ref:`Function Declarations`).

*Native function* implemented in a platform-dependent code is typically written
in another programming language (e.g., *C*). A :index:`compile-time error`
occurs if a native function has a body.

.. index::
   native keyword
   function
   native function
   native method
   function body

|

.. _Native Methods Experimental:

Native Methods
==============

.. meta:
    frontend_status: Done

*Native method* is a method marked with the keyword ``native`` (see
:ref:`Method Declarations`).

*Native methods* are the methods implemented in a platform-dependent code
written in another programming language (e.g., *C*).

A :index:`compile-time error` occurs if:

-  Method declaration contains the keyword ``abstract`` along with the
   keyword ``native``.

-  *Native method* has a body (see :ref:`Method Body`) that is a block
   instead of a simple semicolon or empty body.


.. index::
   native method
   method
   implementation
   platform-dependent code
   native keyword
   method body
   block
   method declaration
   abstract keyword
   semicolon
   empty body

|

.. _Native Constructors:

Native Constructors
===================

.. meta:
    frontend_status: Done

*Native constructor* is a constructor marked with the keyword ``native`` (see
:ref:`Constructor Declaration`).

*Native constructors* are the constructors implemented in a platform-dependent
code written in another programming language (e.g., *C*).

A :index:`compile-time error` occurs if a *native constructor* has a non-empty
body (see :ref:`Constructor Body`).

.. index::
   native constructor
   constructor
   constructor declaration
   platform-dependent code
   native keyword
   implementation
   non-empty body

|

.. _Classes Experimental:

Classes Experimental
********************

.. meta:
    frontend_status: Done


.. _Final Classes:

Final Classes
=============

.. meta:
    frontend_status: Done

A class can be declared ``final`` to prevent extension, i.e., a class declared
``final`` can have no subclasses. No method of a ``final`` class can be
overridden.

If a class type ``F`` expression is declared *final*, then only a class ``F``
object can be its value.

A :index:`compile-time error` occurs if the ``extends`` clause of a class
declaration contains another class that is ``final``.

.. index::
   final class
   class
   class type
   subclass
   object
   extension
   method
   overriding
   class
   class extension
   extends clause
   class declaration

|

.. _Final Methods:

Final Methods
=============

.. meta:
    frontend_status: Done

A method can be declared ``final`` to prevent it from being overridden (see
:ref:`Overriding Methods`) in subclasses.

A :index:`compile-time error` occurs if:

-  The method declaration contains the keyword ``abstract`` or ``static``
   along with the keyword ``final``.

-  A method declared ``final`` is overridden.

.. index::
   final method
   overriding
   instance method
   final method
   overridden method
   subclass
   method declaration
   abstract keyword
   static keyword
   final keyword

.. |
   .. _Sealed Classes:
   Sealed Classes
   ==============
   .. meta:
   frontend_status: None
   A class can be declared ``sealed`` to prevent an extension outside of the
   current module or namespace, i.e., a class declared ``sealed`` can have
   subclasses only within its module or namespace. It limits the number of
   subclasses to subclasses defined within the same module or namespace.
   A ``sealed`` class is ``final`` outside of its module or namespace.
   A :index:`compile-time error` occurs if the ``extends`` clause of a class
   declaration outside of the current module or namespace contains another class
   that is ``sealed``.
   .. code-block:: typescript
   :linenos:
   // File1
   export sealed class A{}
   class B extends A {} // OK as A and B are in the same module
   export namespace X {
   export sealed class A{}
   class B extends A {} // OK as A and B are in the same scope
   }
   // File2
   import {A, X.A} from "File1"
   class C extends A {} // Compile-time error, A is final while imported
   .. index::
   sealed class
   class
   class type
   extension
   namespace
   module
   subclass
   class extension
   extends clause
   class declaration

|

.. _Default Interface Method Declarations:

Default Interface Method Declarations
*************************************

.. meta:
    frontend_status: Done

The syntax of *interface default method* is presented below:

.. code-block:: abnf

    interfaceDefaultMethodDeclaration:
        'private'? identifier signature block
        ;

A default method can be explicitly declared ``private`` in an interface body.

A block of code that represents the body of a default method in an interface
provides a default implementation for any class if such a class does not
override the method that implements the interface.

.. index::
   method declaration
   interface method declaration
   default method
   private method
   implementation
   interface
   block
   class
   method body
   interface body
   default implementation
   overriding
   syntax

|

.. _Adding Functionality to Existing Types:

Adding Functionality to Existing Types
**************************************

.. meta:
    frontend_status: Done

|LANG| supports adding functions and accessors to already defined types. The
usage of functions so added looks the same as if they are methods and accessors
of such types. The mechanism is called :ref:`Functions with Receiver`. This
feature is often used to add new functionality to a class or an interface
without having to inherit from the class or to implement the interface. 
However, it can be used not only for classes and interfaces but also for other
types.

Moreover, :ref:`Function Types with Receiver` and
:ref:`Lambda Expressions with Receiver` can be defined and used to make the
code more flexible.

.. index::
   functionality
   function
   type
   accessor
   method
   function with receiver
   interface
   inheritance
   class
   implementation
   function type
   lambda expression
   lambda expression with receiver
   flexibility

|

.. _Functions with Receiver:

Functions with Receiver
=======================

.. meta:
    frontend_status: Done

*Function with receiver* declaration is a top-level declaration
(see :ref:`Top-Level Declarations`) that looks almost the same as
:ref:`Function Declarations`, except that the first mandatory parameter uses
keyword ``this`` as its name.

The syntax of *function with receiver* is presented below:

.. code-block:: abnf

    functionWithReceiverDeclaration:
        'function' identifier typeParameters? signatureWithReceiver block
        ;

    signatureWithReceiver:
        '(' receiverParameter (', ' parameterList)? ')' returnType?
        ;

    receiverParameter:
        annotationUsage? 'this' ':' type
        ;

.. index::
   function with receiver
   function with receiver declaration
   declaration
   top-level declaration
   function declaration
   parameter
   this keyword

*Function with receiver* can be called in the following two ways by making:

-  Ordinary function call (see :ref:`Function Call Expression`) when the first
   argument is the receiver object;

-  Method call (see :ref:`Method Call Expression`) when the receiver is an
   ``objectReference`` before the function name passed as the first argument
   of the call.

All other arguments are handled in an ordinary manner.

.. index::
   function with receiver
   function call
   expression
   parameter
   method call
   method call expression
   derived class
   derived interface
   argument
   object reference
   receiver
   function name

The keyword ``this`` must be used in the parameter list for the first parameter
only. If it is used for other parameters, then a :index:`compile-time error`
occurs.

The keyword ``this`` can be used inside a *function with receiver* where
it corresponds to the first parameter. The type of parameter ``this`` is called
*receiver type* (see :ref:`Receiver Type`):

.. code-block:: typescript
   :linenos:

      class A {
        num: number = 1
        foo(): void { console.log(this.num); }
      }
      function bar(this: A) {
        this.num = 5
      }
      let a = new A()
      a.foo() // method is called
      a.bar() // Function with receiver is called
      a.foo() // method is called

The first parameter named ``this`` is readonly.

If the *receiver type* is a class or interface type, then ``private`` or
``protected`` members are not accessible (see :ref:`Accessible`) within the
body of a *function with receiver*. Only ``public`` members can be accessed:

.. index::
   this keyword
   function with receiver
   receiver type
   type parameter
   call
   interface type
   public member
   private member
   protected member
   access
   accessibility
   parameter

.. code-block:: typescript
   :linenos:

      class A {
          foo () { ... this.bar() ... }
                       // function bar() is accessible here
          protected member_1 ...
          private member_2 ...
      }
      function bar(this: A) { ...
         this.foo() // Method foo() is accessible as it is public
         this.member_1 // Compile-time error as member_1 is not accessible
         this.member_2 // Compile-time error as member_2 is not accessible
         ...
      }
      let a = new A()
      a.foo() // Ordinary class method is called
      a.bar() // Function with receiver is called

Derived classes or interfaces can be used as receivers:

.. code-block:: typescript
   :linenos:

      class C {}

      function foo(this: C) {}
      function bar(this: C, n: number): void {}

      let c = new C()

      // as a function call:
      foo(c)
      bar(c, 1)

      // as a method call:
      c.foo()
      c.bar(1)

      interface D {}
      function foo1(this: D) {}
      function bar1(this: D, n: number): void {}

      function demo (d: D) {
         // as a function call:
         foo1(d)
         bar1(d, 1)

         // as a method call:
         d.foo1()
         d.bar1(1)
      }

      class E implements D {}
      const e = new E

      // derived class is used as a receiver for a method call:
      e.foo1()
      e.bar1(1)

      // the same as a function call:
      foo1(e)
      bar1(e, 1)

*Function with receiver* can be generic as in the following example:

.. index::
   function with receiver
   access
   accessibility
   instance method
   derived class
   name
   method
   receiver type
   generic function

.. code-block:: typescript
   :linenos:

    class G<T> {}

    function foo<T>(this: G<T>, p: T) {
        console.log (p)
    }

    class C {}

    let g = new G<C>
    g.foo(new C)    // implicit instantiation
    g.foo<C>(new C) // explicit instantiation

When the receiver type contains an accessible
instance method (see :ref:`Accessible`) with the same name as the
function with receiver, the instance method has a priority
over the implicitly called function with receiver. The function with receiver
still can be called explicitly:

.. code-block:: typescript
   :linenos:

      class A {
          foo (): int { return 1; }
      }

      function foo(this: A): int { return 2; }

      console.log((new A).foo())  // instance method called, prints '1'
      console.log(foo(new A)) // explicit call of a receiver function, prints '2'


*Functions with receiver* are dispatched statically. What function is being
called is known at compile time based on the receiver type specified in the
declaration. A *function with receiver* can be applied to the receiver of any
derived class until it is overridden within the derived class:

.. code-block:: typescript
   :linenos:

      class Base { ... }
      class Derived extends Base { ... }

      function foo(this: Base) { console.log ("Base.foo is called") }

      let b: Base = new Base()
      b.foo() // `Base.foo is called` to be printed
      b = new Derived()
      b.foo() // `Base.foo is called` to be printed

A *function with receiver* can be defined in a module other than the one that
defines the receiver type. This is represented in the following example:

.. index::
   function with receiver
   static dispatch
   function call
   compile time
   receiver type
   declaration
   receiver
   derived class
   class
   module

.. code-block:: typescript
   :linenos:

      // file a.ets
      class A {
          foo() { ... }
      }

      // file ext.ets
      import {A} from "a.ets" // name 'A' is imported
      function bar(this: A) () {
         this.foo() // Method foo() is called
      }

A *function with receiver* can be defined in a namespace (see
:ref:`Namespace Declarations`). A *function with receiver* cannot be called by
using the *method call* syntax outside the namespace, though, because an entity
exported from a namespace can be accessed in the form of a ``qualifiedName``
only.

This situation is represented in the following example:

.. code-block:: typescript
   :linenos:

    namespace NS {
        export function foo(this: int) {}
        function bar(i: int) {
            i.foo() // OK, method call is used
        }
    }

    let i = 1
    NS.foo(i)  // OK, function call is used
    i.foo()    // Compile-time error, 'foo' is not resolved
    i.NS.foo() // Compile-time error, 'NS' is not defined for 'int'

.. note::
    While a function with receiver can be used in an explicit overload list,
    such an overload cannot be called by using the method access syntax as
    in the example provided in :ref:`Explicit Function Overload`.

|

.. _Receiver Type:

Receiver Type
=============

.. meta:
    frontend_status: Done

*Receiver type* is the type of the *receiver parameter* in a function,
function type, and lambda with receiver.  A *receiver type* can be
an interface type, a class type, or an array type.
Otherwise, a :index:`compile-time error` occurs.

Using array type as a *receiver type* is presented in the example below:

.. code-block:: typescript
   :linenos:

      function addElements(this: number[], ...s: number[]) {
       ...
      }

      let x: number[] = [1, 2]
      x.addElements(3, 4)

.. index::
   receiver type
   receiver parameter
   type
   function
   function type
   lambda with receiver
   interface type
   class type
   array type
   type parameter
   array type

|

.. _Function Types with Receiver:

Function Types with Receiver
============================

.. meta:
    frontend_status: Done

*Function type with receiver* specifies the signature of a function or lambda
with receiver. It is almost the same as *function type* (see :ref:`Function Types`),
except that the first parameter is mandatory, and the keyword ``this`` is used
as its name:

The syntax of *function type with receiver* is presented below:

.. code-block:: abnf

    functionTypeWithReceiver:
        '(' receiverParameter (',' ftParameterList)? ')' ftReturnType
        ;

The type of a *receiver parameter* is called the *receiver type* (see
:ref:`Receiver Type`).

.. index::
   function type with receiver
   signature
   function
   lambda
   function with receiver
   lambda with receiver
   function type
   this keyword
   syntax
   parameter
   receiver type
   receiver parameter

.. code-block:: typescript
   :linenos:

      class A {...}

      type FA = (this: A) => boolean
      type FN = (this: number[], max: number) => number

*Function type with receiver* can be generic as in the following example:

.. code-block:: typescript
   :linenos:

      class B<T> {...}

      type FB<T> = (this: B<T>, x: T): void
      type FBS = (this: B<string>, x: string): void

The usual rule of function type compatibility (see
:ref:`Subtyping for Function Types`) is applied to
*function type with receiver*, and parameter names are ignored.

.. index::
   function type with receiver
   generic
   function type
   compatibility
   subtyping
   parameter name

.. code-block:: typescript
   :linenos:

      class A {...}

      type F1 = (this: A) => boolean
      type F2 = (a: A) => boolean

      function foo(this: A): boolean {}
      function goo(a: A): boolean {}

      let f1: F1 = foo // OK
      f1 = goo // OK

      let f2: F2 = goo // OK
      f2 = foo // OK
      f1 = f2 // OK

The sole difference is that only an entity of *function type with receiver*
nut not an entity of a compatible *function type* can be used in
:ref:`Method Call Expression`.

.. code-block:: typescript
   :linenos:

      let a = new A()
      a.f1() // OK, function type with receiver
      f1(a)  // OK

      a.f2() // Compile-time error
      f2(a) // OK

.. index::
   entity
   function type with receiver
   method call
   expression
   compile-time error


.. note::
    The limitation of the method call syntax can be easily bypassed by assigning
    an ordinary function to a compatible *function type with receiver*.
    A snippet of code illustrative of parameter type with receiver is
    represented by the example below.

Function type with receiver can be used as a parameter type. Using parameter
type with receiver is represented by the example below:

.. code-block:: typescript
   :linenos:

    function foo(p: number, f: (this: number)=> number) {
        console.log(p.f(), f(p))
    }

    function goo(this: number) { return this - 1 }
    function bar(this: number) { return this + 1 }
    function compat(n: number) { return n }

    let n: number = 1
    foo(n, goo)  // prints `0 0`
    foo(n, bar)  // prints `2 2`
    foo(n, compat)  // prints `1 1`


The method call syntax cannot be used when assigning the actual entity to a
variable of *function type with receiver*. Attempting to do so causes a
:index:`compile-time error`:

.. code-block:: typescript
   :linenos:

   function foo<T extends Object>(this: T, functor: (this: T)=> void): void {
      // following two calls are equivalent
      functor(this)
      this.functor()
   }

   function bar<T>(this: T): void {
      console.log(this)
   }

   let x = 5
   x.foo(bar<int>) // OK
   let y = bar<int> // OK
   x.foo(y) // OK

   // compile time error - can not assign entity with method call syntax
   // to a function type
   x.foo(x.bar)
   x.foo(x.bar<int>)
   let z = x.bar
   let y = x.bar<int>

|

.. _Lambda Expressions with Receiver:

Lambda Expressions with Receiver
================================

.. meta:
    frontend_status: Done

*Lambda expression with receiver* defines an instance of a *function type with
receiver* (see :ref:`Function Types with Receiver`). It looks almost the same
as an ordinary lambda expression (see :ref:`Lambda Expressions`), except that
the first parameter is mandatory, and the keyword ``this`` is used as its name:

The syntax of *lambda expression with receiver* is presented below:

.. code-block:: abnf

    lambdaExpressionWithReceiver:
        annotationUsage?
        '(' receiverParameter (',' lambdaParameterList)? ')'
        returnType? '=>' lambdaBody
        ;

The use of annotations is discussed in :ref:`Using Annotations`.

The keyword ``this`` can be used inside a *lambda expression with receiver*,
It corresponds to the first parameter:

.. index::
   lambda expression with receiver
   lambda expression
   instance
   function type with receiver
   lambda expression
   parameter
   this keyword
   annotation

.. code-block:: typescript
   :linenos:

      class A { name = "Bob" }

      let show = (this: A): void {
          console.log(this.name)
      }

Lambda can be called in two syntactical ways represented by the example below:

.. code-block:: typescript
   :linenos:

      class A {
        name: string
        constructor (n: string) {
            this.name = n
        }
      }

      function foo(aa: A[], f: (this: A) => void) {
        for (let a of aa) {
            a.f() // first way
            f (a) // second way
        }
      }

      let aa: A[] = [new A("aa"), new A("bb")]
      foo(aa, (this: A) => { console.log(this.name)} ) // output: "aa" "bb"

.. index::
   lambda
   syntax
   constructor
   function
   class

.. note::
   If *lambda expression with receiver* is declared in a class or interface,
   then ``this`` use in the lambda body refers to the first lambda parameter and
   not to the surrounding class or interface. Any lambda call outside a class
   has to use the ordinary syntax of arguments as represented by the example
   below:


   .. code-block:: typescript
      :linenos:

         class B {
           foo() { console.log ("foo() from B is called") }
         }
         class A {
           foo() { console.log ("foo() from A is called") }
           bar() {
               let lambda1 = (this: B): void => { this.foo() } // local lambda
               new B().lambda1()
           }
           lambda2 = (this: B): void => { this.foo() } // class field lambda
         }
         new A().bar() // Output is 'foo() from B is called'
         new A().lambda2 (new B) // Argument is to be provided in its usual place

         interface I {
            lambda: (this: B) => void // Property of the function type
         }
         function foo (i: I) {
            i.lambda(new B) // Argument is to be provided in its usual place
         }

.. index::
   lambda expression with receiver
   class
   interface
   this keyword
   lambda body
   lambda parameter
   surrounding class
   surrounding interface
   syntax
   argument
   function type

|

.. _Trailing Lambdas:

Trailing Lambdas
****************

.. meta:
    frontend_status: Done

The *trailing lambda* is a special form of notation for function
or method call when the last parameter of a function or a method is of
function type, and the argument is passed as a lambda using the
:ref:`Block` notation. The *trailing lambda* syntactically looks as follows:

.. code-block:: abnf

    trailingLambda:
        'async'? block
        ;

.. index::
   trailing lambda
   notation
   function call
   method call
   parameter
   function type
   method
   parameter
   lambda
   block notation

The modifier ``async`` is used optionally to mark :ref:`Async Lambdas`.

The use of a trailing lambda is represented in the example below:

.. code-block:: typescript
   :linenos:

      class A {
          foo (f: ()=>void) { ... }
      }

      let a = new A()
      a.foo() { console.log ("method lambda argument is activated") }
      // method foo receives last argument as the trailing lambda

Currently, no parameter can be specified for the type of a trailing lambda,
except a receiver parameter (see :ref:`Lambda Expressions with Receiver`).
Otherwise, a :index:`compile-time error` occurs.

A block immediately after a call is always handled as *trailing lambda*.
A :index:`compile-time error` occurs if the last parameter of the called entity
is not of a function type.

The semicolon ``';'`` separator can be used between a call and a block to
indicate that the block does not define a *trailing lambda*. When calling an
entity with the last optional parameter (see :ref:`Optional Parameters`), it
means that the call must use the default value of the parameter.

.. index::
   trailing lambda
   syntax
   parameter
   receiver parameter
   optional parameter
   lambda expression with receiver
   block
   function type
   lambda
   semicolon
   separator
   default value
   call

.. code-block:: typescript
   :linenos:

      function foo (f: ()=>void) { ... }

      foo() { console.log ("trailing lambda") }
      // 'foo' receives last argument as the trailing lambda

      function bar(f?: ()=>void) { ... }

      bar() { console.log ("trailing lambda") }
      // function 'bar' receives last argument as the trailing lambda,
      bar(); { console.log ("that is the block code") }
      // function 'bar' is called with parameter 'f' set to 'undefined'

      function goo(n: number) { ... }

      goo() { console.log("aa") } // Compile-time error as goo() requires an argument
      goo(); { console.log("aa") } // Compile-time error as goo() requires an argument


If there are optional parameters in front of an optional function type parameter,
then calling such a function or method can skip optional arguments and keep the
trailing lambda only. This implies that the value of all skipped arguments is
``undefined``.

.. code-block:: typescript
   :linenos:

    function foo (p1?: number, p2?: string, f?: ()=>string) {
        console.log (p1, p2, f?.())
    }

    foo()                           // undefined undefined undefined
    foo() { return "lambda" }       // undefined undefined lambda
    foo(1) { return "lambda" }      // 1 undefined lambda
    foo(1, "a") { return "lambda" } // 1 a lambda

.. index::
   optional parameter
   optional argument
   trailing lambda
   argument
   operational function
   function
   function type
   parameter
   method
   function call
   method call
   string
   lambda

|

.. _Accessor Declarations:

Accessor Declarations
*********************

.. meta:
    frontend_status: None

Accessor is either a top-level declaration (see
:ref:`Top-level Declarations`) or a declaration inside a namespace
(see :ref:`Namespace Declarations`) that declares a getter, a setter, or
functions with predefined signatures. The syntatic form of accessor usage
mimics code patterns used to work with variables, i.e., getting or setting a
variable value.

The syntax of *accessor declarations* is presented below:

.. code-block:: abnf

    accessorDeclaration:
        'native'?
        ( 'get' identifier '(' ')' returnType? block?
        | 'set' identifier '(' requiredParameter ')' block?
        )
        ;

.. index::
   accessor
   accessor declaration
   top-level declaration
   variable
   control
   getter
   setter
   value

The modifier ``native`` indicates that the accessor is a *native accessor*
(similarly to :ref:`Native Functions`).

A non-native accessor must have a body. A :index:`compile-time error` occurs if:

- Native accessor has a body; or
- Non-native accessor has no body.

A *get-accessor* (*getter*) must have an explicit return type and no parameters,
or no return type at all on condition the type can be inferred from the getter
body (see :ref:`Return Type Inference`).
A *set-accessor* (*setter*) must have a single parameter and no return type.

.. note::
   If an *accessor* is an entity of a namespace, then the same rules apply to
   it when exporting and using qualified names as the rules that apply to other
   namespace entities (see :ref:`Namespace Declarations`).

A :index:`compile-time error` occurs if:

-  Getter or setter is used in a call expression (like a function);
-  Getter return type cannot be inferred from the getter body; or
-  *Set-accessor* (*setter*) has an optional parameter (see
   :ref:`Optional Parameters`):

.. index::
   native modifier
   accessor
   native accessor
   native function
   non-native accessor
   get-accessor
   set-accessor
   getter
   setter
   return type
   accessor declaration
   top-level declaration
   parameter
   type inference


The typical use of an accessor to control value setting is represented in the
following example:

.. code-block:: typescript
   :linenos:

    let saved_age = 0

    export get age(): number { return saved_age }
    export set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        saved_age = a
    }

Which accessor (getter or setter) is to be called is defined by the place of
use:

.. code-block:: typescript
   :linenos:

   get name(): string { return "" }
   set name(x: string) { }

   console.log (name) // Getter is called
   name = "some string" // Setter is called

.. index::
   accessor
   value setting
   control
   getter
   setter
   function

However, an accessor declaration must be distinguishable from other entities,
and a :index:`compile-time error` occurs if:

- Accessor name is the same as that of another entity in a scope;
- Names of two getters or two setters in a scope are the same.

.. code-block:: typescript
   :linenos:

   let name = "Bob"
   get name(): string { return "Alice" } // Compile-time error

No additional restrictions are imposed on signatures of getters and
setters that have the same name.

.. code-block:: typescript
   :linenos:

   set hashCode(x: string) {/*body*/}
   get hashCode(): long {/*body*/} // OK

   hashCode = "some string"
   const l: long = hashCode

.. index::
   accessor declaration
   accessor
   entity
   scope
   getter
   setter
   name
   restriction
   signature

The use of getters and setters looks identical to the use of variables.
A :index:`compile-time error` occurs if:

- Getter is used in the position of a *left-hand-side expression* in an
  :ref:`Assignment`;
- Setter is used to get a value.

.. code-block:: typescript
   :linenos:

    get magicNumber(): number { return 42 }
    set randomSeed(a: number) {}

    console.log(magicNumber) // OK, getter is used
    magicNumber = 15 // Compile-time error, setter is not defined

    randomSeed = 42 // OK, setter is used
    console.log(randomSeed) // Compile-time error, getter is not defined

.. index::
   getter
   setter
   variable
   expression
   assignment
   value

Accessors can be declared at all places where :ref:`Top-Level Declarations`
including namespaces can be used:

.. code-block:: typescript
   :linenos:

    namespace N {
        let saved_age = 0

        export get age(): number { return saved_age }
        export set age(a: number) {
            if (a < 0) { throw new Error("wrong age") }
            saved_age = a
        }
    }

    N.age = 18
    console.log(N.age)

.. index::
   accessor
   declaration
   top-level declaration

|

.. _Pattern Matching:

Pattern Matching
****************

.. meta:
    frontend_status: None

*Pattern Matching* is a set of powerful features supported by most modern
programming languages. *Pattern matching* generally allows checking a value
against a pattern, and executing a corresponding action after a match is
successful. A successful match can also deconstruct a value into its constituent
parts.

The current version of |LANG| supports a simple *pattern matching* feature
called *destructuring assignment*. Other features are to be added in the
forthcoming revisions of this specification.

|

.. _Destructuring Assignment:

Destructuring Assignment
========================

*Destructuring assignment* allows extracting values from arrays or tuples, and
assigning them to distinct variables.

The syntax of a *destructuring assignment* is as follows:

.. code-block:: abnf

    destructuringAssignment:
        '[' lhsExpression? (',' lhsExpression?)* ']' '=' rhsExpression
        ;

The definitions of ``lhsExpression`` and ``rhsExpression`` are provided in
:ref:`Assignment`.

``rhsExpression`` must be of array type or tuple type. Otherwise, a
:index:`compile-time error` occurs.

*Destructuring assignment* can be considered a compact form of a set of
assignments (see :ref:`Simple Assignment Operator`).
Items in a *left-hand-side* expression (whether ``lhsExpression`` or none)
correspond to the sequence of elements in ``rhsExpression`` staring from the
first element (i.e., the element with the index ``0``) of an array or a tuple:

.. code-block:: typescript
   :linenos:

    function foo(x: string[]) {
        let a = ""
        let b = "";
        [a, , b] = x
        // this line works the same as the previous line:
        a = x[0]; b = x[2]
    }

In the example above, ``a`` takes the value ``x[0]``, and ``b`` takes the
value ``x[2]``. If an attempt is made to have an array element with an index
greater than or equal to the length of the array, then *RangeError* is thrown
in exactly the same way as in :ref:`Array Indexing Expression`.

If ``lhsExpression`` is missing, then the corresponding element of an array or
of a tuple is ignored.

A :index:`compile-time error` occurs if:

- Type of an array element or of a tuple element is not assignable to the type
  of a corresponding ``lhsExpression`` (see :ref:`Assignability`);
- ``rhsExpression`` is of a tuple type, and ``lhsExpression`` corresponds to
  the missing tuple element.

Valid and erroneous destructuring is represented in the following example:

.. code-block:: typescript
   :linenos:

    function foo(x: [string, number, string]) {
        let a: string
        let b: number
        [a] = x; // OK
        [, b, a] = x; // OK
        [, b, a,,,,] = x; // OK
        [b] = x; // Compile-type error, x[0] is not assignable to 'b'
        [, b] = x; // OK
        [,,,b] = x; // Compile-time error, there is no element for variable 'b'
    }


.. raw:: pdf

   PageBreak
