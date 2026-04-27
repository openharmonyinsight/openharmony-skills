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

.. _Types:

Types
#####

.. meta:
    frontend_status: Partly

This chapter introduces the notion of type that is one of the fundamental
concepts of |LANG| and other programming languages.
Type classification as accepted in |LANG| is discussed below along
with all aspects of using types in programs written in the language.

The type of an entity is conventionally defined as the set of *values* the
entity (variable) can take, and the set of *operators* applicable to the entity
of a given type.

|LANG| is a statically typed language. It means that the type of every
declared entity and every expression is known at compile time. The type of
an entity is either set explicitly by a developer, or inferred implicitly
(see :ref:`Type Inference`) by the compiler.

The types integral to |LANG| are called *predefined types* (see
:ref:`Predefined Types`).

The types introduced, declared, and defined by a developer are called
*user-defined types*.
All *user-defined types* must have complete type declarations presented as
source code in |LANG|.

.. index::
   statically typed language
   expression
   compile time
   type inference
   compiler
   predefined type
   user-defined type
   type declaration
   source code
   value

|LANG| types are summarized in the table below:


   ========================= =========================
   Predefined Types          User-Defined Types
   ========================= =========================
   ``byte``, ``short``,      class types,
   ``int``,  ``long``,       interface types,
   ``float``, ``double``,    tuple types,
   ``number``,               union types,
   ``boolean``, ``char``,    function types,

   ``string``,               enumeration types,

   ``bigint``,               type parameters,

   ``Any``, ``Object``,      string literal types

   ``never``, ``void``,      

   ``undefined``, ``null``,  
   ``Array<T>`` or ``T[]``,  
   ``FixedArray<T>``,
   ``ValueArray<T>``
   ========================= =========================

.. note::
   Type ``number`` is an alias to ``double``.

.. index::
   user-defined type
   predefined type
   class type
   interface type
   array type
   fixed array type
   tuple type
   union type
   literal type
   function type
   type parameter
   enumeration type
   alias

Most *predefined types* have aliases to improve |TS| compatibility as follows:


+--------------+---------------+
| Primary Name | Alias         |
+==============+===============+
| ``number``   |   ``Number``  |
+--------------+---------------+
| ``byte``     |   ``Byte``    |
+--------------+---------------+
| ``short``    |   ``Short``   |
+--------------+---------------+
| ``int``      |   ``Int``     |
+--------------+---------------+
| ``long``     |   ``Long``    |
+--------------+---------------+
| ``float``    |   ``Float``   |
+--------------+---------------+
| ``double``   |   ``Double``  |
+--------------+---------------+
| ``boolean``  |   ``Boolean`` |
+--------------+---------------+
| ``char``     |   ``Char``    |
+--------------+---------------+
| ``string``   |   ``String``  |
+--------------+---------------+
| ``bigint``   |   ``BigInt``  |
+--------------+---------------+
| ``Object``   |   ``object``  |
+--------------+---------------+

Using primary names of *predefined types* is recommended in all cases.

.. index::
   predefined type
   primary name
   alias
   compatibility

|

.. _Predefined Types:

Predefined Types
****************

.. meta:
    frontend_status: Done

Predefined types include the following:

-  :ref:`Value Types`;
-  :ref:`Type Any`;
-  :ref:`Type Object`;
-  :ref:`Type never`;
-  :ref:`Type void or undefined`;
-  :ref:`Type null`;
-  :ref:`Type string`;
-  :ref:`Type bigint`;
-  :ref:`Array Types` (``Array<T>`` or ``T[]`` or ``FixedArray<T>``);
-  :ref:`Type Function`.

.. index::
   value
   type
   predefined type
   any
   Object
   never
   void
   undefined
   null
   string
   bigint
   array

|

.. _User-Defined Types:

User-Defined Types
******************

.. meta:
    frontend_status: Done

*User-defined* types include the following:

-  Class types (see :ref:`Classes`);
-  Interface types (see :ref:`Interfaces`);
-  Enumeration types (see :ref:`Enumerations`);
-  :ref:`Function Types`;
-  :ref:`Tuple Types`;
-  :ref:`Union Types`;
-  :ref:`Type Parameters`; and
-  :ref:`Literal Types`.

.. index::
   user-defined type
   class type
   interface type
   enumeration type
   function type
   union type
   type parameter
   literal type

|

.. _Using Types:

Using Types
***********

.. meta:
    frontend_status: Done

Source code can refer to a type by using the following:

-  Type reference for:

   + :ref:`Named Types`, or
   + Type aliases (see :ref:`Type Alias Declaration`);

-  In-place type declaration for:

   + :ref:`Array Types`,
   + :ref:`Tuple Types`,
   + :ref:`Function Types`,
   + :ref:`Function Types with Receiver`,
   + :ref:`Keyof Types`,
   + :ref:`Union Types`, or
   + Type in parentheses.

.. index::
   named type
   type alias
   in-place type declaration
   type reference
   array type
   function type
   function type with receiver
   union type
   tuple type
   type in parentheses

The syntax of *type* is presented below:

.. code-block:: abnf

    type:
        annotationUsageWithParentheses?
        ( typeReference
        | 'readonly'? arrayType
        | 'readonly'? tupleType
        | functionType
        | functionTypeWithReceiver
        | unionType
        | keyofType
        | StringLiteral
        )
        | '(' type ')'
        ;

The usage of annotations is discussed in :ref:`Using Annotations`.

Types with the prefix ``readonly`` are discussed in
:ref:`Readonly Array Types` and :ref:`Readonly Tuple Types`.

The usage of types is represented by the example below:

.. code-block:: typescript
   :linenos:

    let n: number   // Using identifier as a predefined value type name
    let o: Object   // Using identifier as a predefined class type name
    let a: number[] // Using array type
    let t: [number, number] // Using tuple type
    let f: ()=>number      // Using function type
    let u: number|string    // Using union type
    let l: "xyz"            // Using string literal type

    class C { n = 1; s = "aa"}
    let k: keyof C  // Using keyof to build union type


.. let f1: ()=>number      // Using function type
   let f2: <T>(p: T)=>T    // Using generic function type


Parentheses are used to specify the required type structure if the type is a
combination of array, function, or union types. Without parentheses, the symbol
``'|'`` that constructs a union type has the lowest precedence as represented
by the example below:

.. index::
   annotation
   prefix readonly
   readonly type
   array type
   tuple type
   identifier
   function type
   union type
   type structure
   construct
   precedence
   parentheses

.. code-block:: typescript
   :linenos:

    // A nullish array with elements of type string:
    let a: string[] |  undefined
    let s: string[] = []

    a = s    // OK
    a = undefined // OK, a is nullish type

    // An array with elements whose types are string or undefined:
    let b1: (string | undefined)[]
    b1 = undefined // Error, b1 is an array and is not nullish type
    b1 = ["aa", undefined] // OK

    // string or array of undefined elements:
    let b2: string | undefined[]
    b2 = undefined // Error, b2 - string or array of undefined - not nullish
    b2 = [undefined, undefined] // OK

    // A function type that returns string or undefined
    let c: () => string | undefined
    c = undefined // error, c is not nullish
    c = (): string | undefined => { return undefined } // OK

    // (A function type that returns string) or undefined
    let d: (() => string) | undefined
    d = undefined // OK, d is nullish
    d = (): string => { return "hi" } // OK


The annotation which is used in front of type always needs parentheses
(as highlighted in grammar snippet above). The reason is to prevent ambiguity
between annotation parentheses and parentheses used in a type declaration:

.. code-block:: typescript
   :linenos:

    let var_name1: @my_annotation() (A|B) // OK
    let var_name2: @my_annotation (A|B)  // Compile-time error

.. index::
   string
   null
   parentheses

|

.. _Named Types:

Named Types
***********

.. meta:
    frontend_status: Done

*Named types* are classes, interfaces, enumerations, aliases,
type parameters, and predefined types (see :ref:`Predefined Types`), except
built-in arrays. Other types (i.e., array, function, and union types) are anonymous
unless aliased. Respective named types are introduced by the following:

-  Class declarations (see :ref:`Classes`),
-  Interface declarations (see :ref:`Interfaces`),
-  Enumeration declarations (see :ref:`Enumerations`),
-  Type alias declarations (see :ref:`Type Alias Declaration`), and
-  Type parameter declarations (see :ref:`Type Parameters`).

Classes, interfaces and type aliases with type parameters are *generic types*
(see :ref:`Generics`). Named types without type parameters are
*non-generic types*.

*Type references* (see :ref:`Type References`) refer to named types by
specifying their type names and (where applicable) type arguments to be
substituted for the type parameters of a named type.

.. index::
   named type
   class
   interface
   enumeration
   alias
   type parameter
   predefined type
   function
   array
   union type
   built-in array
   anonymous type
   class declaration
   interface declaration
   enumeration declaration
   type alias declaration
   type parameter declaration
   type reference
   generic type
   non-generic type
   type argument
   type parameter

|

.. _Type References:

Type References
***************

.. meta:
    frontend_status: Done

*Type reference* refers to a type by one of the following:

-  *Simple* or *qualified* type name (see :ref:`Names`),
-  Type alias (see :ref:`Type Alias Declaration`).

*Type reference* that refers to a generic class or to an interface type is
valid if it is a valid instantiation of a generic. Its type arguments can be
provided explicitly or implicitly based on defaults.

.. index::
   type reference
   type name
   type parameter
   simple type name
   qualified type name
   identifier
   type alias
   type argument
   interface type
   generic class
   instantiation

The syntax of *type reference* is presented below:

.. code-block:: abnf

    typeReference:
        qualifiedName typeArguments?
        ;

.. code-block:: typescript
   :linenos:

    let map: Map<string, number> // Map<string, number> is the type reference

    class A<T> {...}
    class C<T> {
       field1: A<T>  // A<T> is a class type reference - class type reference
       field2: A<number> // A<number> is a type reference - class type reference
       foo (p: T) {} // T is a type reference - type parameter
       constructor () { /* some body to init fields */ }
    }

    type MyType<T> = A<T>[]
    let x: MyType<number> = [new A<number>, new A<number>]
      // MyType<number> is a type reference  - alias reference
      // A<number> is a type reference - class type reference

If *type reference* refers to a type by a type alias (see
:ref:`Type Alias Declaration`), then the type alias is replaced for a
non-aliased type in all cases when dealing with types. The replacement is
potentially recursive.

.. code-block:: typescript
   :linenos:

   type T1 = Object
   type T2 = number
   function foo(t1: T1, t2: T2)  {
       t1 = t2      // Type compatibility test will use Object and number
       t2 = t2 + t2 // Operator validity test will use type number not T2
   }

.. index::
   type reference
   type alias
   non-aliased type
   type
   recursive replacement
   replacement
   compatibility
   Object
   operator validity test

|

.. _Value Types:

Value Types
***********

.. meta:
    frontend_status: Done

*Value types* are predefined integer types (see
:ref:`Integer Types and Operations`), floating-point types (see
:ref:`Floating-Point Types and Operations`), the boolean type (see
:ref:`Type boolean`), and the character type (see
:ref:`Type char`).

The values of such types do *not* share state with other
values.

.. note::

   Tables in :ref:`Unary Expressions` and :ref:`Binary Expressions`
   summarize information about valid combinations of operand types and
   resultant types of unary and binary operations.

.. index::
   value type
   predefined type
   integer type
   floating-point type
   boolean type
   character type
   enumeration
   user-defined type
   enumeration type
   value
   state

|

.. _Numeric Types:

Numeric Types
=============

.. meta:
    frontend_status: Done

*Numeric types* are integer and floating-point types (see
:ref:`Integer Types and Operations` and
:ref:`Floating-Point Types and Operations`).

Each numeric type has its own set of values.
:ref:`Widening Numeric Conversions` are used in expressions
to convert a value of a smaller type to a value of a larger type.

Numeric type hierarchy is defined in the following way:

- ``byte`` < ``short`` < ``int`` < ``long`` < ``float`` < ``double``, where
  the smallest type is ``byte``, and the largest type is ``double``.

Type ``bigint`` does not belong to this hierarchy. No implicit conversion from
numeric types to ``bigint`` occurs. The methods of class ``BigInt``
(which is a part of :ref:`Standard Library`) must be used to create
``bigint`` values from numeric type values.

*Numeric types* are represented by classes of the :ref:`Standard Library`. It
means that *numeric types* are of the class type nature, that all of them are
subtypes of ``Object``, and therefore can be used at any place where a class
name is expected.

.. code-block:: typescript
   :linenos:

    let a_number = new number
    let a_byte = new byte
    let an_integer = new int
    console.log (a_number, a_byte, an_integer)
    // Output is: 0 0 0


.. index::
   integer type
   floating-point type
   numeric type
   value
   double
   float
   long
   int
   short
   byte
   bigint

|

.. _Integer Types and Operations:

Integer Types and Operations
============================

.. meta:
    frontend_status: Done

+------------+--------------------------------------------------------------------+
| Type       | Corresponding Set of Values                                        |
+============+====================================================================+
| ``byte``   | All signed 8-bit integers (:math:`-2^7` to :math:`2^7-1`)          |
+------------+--------------------------------------------------------------------+
| ``short``  | All signed 16-bit integers (:math:`-2^{15}` to :math:`2^{15}-1`)   |
+------------+--------------------------------------------------------------------+
| ``int``    | All signed 32-bit integers (:math:`-2^{31}` to :math:`2^{31} - 1`) |
+------------+--------------------------------------------------------------------+
| ``long``   | All signed 64-bit integers (:math:`-2^{63}` to :math:`2^{63} - 1`) |
+------------+--------------------------------------------------------------------+
| ``bigint`` | All integers with no limits                                        |
+------------+--------------------------------------------------------------------+

.. note::

   :ref:`type bigint` is not a numeric type, yet it operates with integer values
   of arbitrary precision. That is why it is discussed in detail in the
   appropriate subsection.

|LANG| provides a number of operators to act on integer values as discussed
below.

-  Comparison operators that produce a value of type ``boolean``:

   +  Numeric relational operators ``'<'``, ``'<='``, ``'>'``, and ``'>='``
      (see :ref:`Numeric Relational Operators`);
   +  Numeric equality operators ``'=='`` and ``'!='`` (see
      :ref:`Numeric Equality Operators`);

-  Exponentiation operator ``'**'`` as a variant that produces a value of type
   ``bigint`` (see :ref:`Exponentiation Expression`);

-  Numeric operators that produce values of types ``int``, ``long``, or
   ``bigint``:

   + Unary plus ``'+'`` and minus ``'-'`` operators (see :ref:`Unary Plus` and
     :ref:`Unary Minus`);
   + Multiplicative operators ``'*'``, ``'/'``, and ``'%'`` (see
     :ref:`Multiplicative Expressions`);
   + Additive operators ``'+'`` and ``'-'`` (see :ref:`Additive Expressions`);
   + Increment operator ``'++'`` used as prefix (see :ref:`Prefix Increment`)
     or postfix (see :ref:`Postfix Increment`);
   + Decrement operator ``'--'`` used as prefix (see :ref:`Prefix Decrement`)
     or postfix (see :ref:`Postfix Decrement`);
   + Signed and unsigned shift operators ``'<<'``, ``'>>'``, and ``'>>>'`` (see
     :ref:`Shift Expressions`);
   + Bitwise complement operator ``'~'`` (see :ref:`Bitwise Complement`);
   + Integer bitwise operators ``'&'``, ``'^'``, and ``'|'`` (see
     :ref:`Integer Bitwise Operators`);

-  Ternary conditional operator ``'?:'`` (see :ref:`Ternary Conditional Expressions`);
-  String concatenation operator ``'+'`` (see :ref:`String Concatenation`) that,
   if one operand is ``string`` and the other is of an integer type, converts
   the integer operand to ``string`` with the decimal form, and then creates a
   concatenation of the two strings as a new ``string``.

.. index::
   byte
   short
   boolean
   int
   long
   bigint
   integer value
   comparison operator
   ternary conditional operator
   numeric relational operator
   numeric equality operator
   equality operator
   numeric operator
   type reference
   type name
   simple type name
   qualified type name
   type alias
   type argument
   interface type
   postfix
   prefix
   unary operator
   additive operator
   multiplicative operator
   increment operator
   numeric relational operator
   numeric equality operator
   decrement operator
   signed shift operator
   unsigned shift operator
   bitwise complement operator
   integer bitwise operator
   conditional operator
   cast operator
   integer value
   numeric type
   string concatenation operator
   operand
   string

If either operand of a binary integer operation except :ref:`Shift Expressions`
is of type ``long`` and the other operand is of a lesser type, then numeric
conversion (see :ref:`Widening Numeric Conversions`) is used to widen
the second operand first to type ``long``. In this case:

-  Operation implementation uses 64-bit precision; and
-  Result of the numeric operator is of type ``long``.


If otherwise neither operand is of type ``long`` and any operand is of a type
other than ``int``, then numeric conversion is used to widen the latter
first to type ``int``. In this case:

-  Operation implementation uses the 32-bit precision; and
-  Result of the numeric operator is of type ``int``.

Conversions between integer types and type ``boolean`` are not allowed.
However, the value of integer type can be used as a logical condition
in some cases (see :ref:`Extended Conditional Expressions`)

The integer operators cannot indicate an overflow or an underflow.

An integer operator can throw ``ArithmeticError`` if the right-hand-side operand
of an integer division operator '``/``' (see :ref:`Division`) and an integer
remainder operator ``'%'`` (see :ref:`Remainder`) is zero. The situation is
discussed in :ref:`Error Handling`.

.. index::
   constructor
   method
   constant
   operand
   numeric promotion
   predefined numeric types conversion
   numeric type
   widening
   long
   int
   boolean
   integer type
   cast
   operator
   overflow
   underflow
   division operator
   remainder operator
   error
   increment operator
   decrement operator
   additive expression
   error
   integer operator


Predefined constructors, methods, and constants for *integer types*
are parts of the |LANG| :ref:`Standard Library`.

.. index::
   predefined constructor
   predefined method
   predefined constant
   integer type

|

.. _Floating-Point Types and Operations:

Floating-Point Types and Operations
===================================

.. meta:
    frontend_status: Done

+-------------+-------------------------------------+
| Type        | Corresponding Set of Values         |
+=============+=====================================+
| ``float``   | The set of all IEEE 754 [3]_ 32-bit |
|             | floating-point numbers              |
+-------------+-------------------------------------+
| ``number``, | The set of all IEEE 754 64-bit      |
| ``double``  | floating-point numbers              |
+-------------+-------------------------------------+

.. index::
   IEEE 754
   floating-point number
   floating-point type
   number type


|LANG| provides a number of operators to act on floating-point type values as
discussed below.

-  Comparison operators that produce a value of type *boolean*:

   - Numeric relational operators ``'<'``, ``'<='``, ``'>'``, and ``'>='``
     (see :ref:`Numeric Relational Operators`);
   - Numeric equality operators ``'=='`` and ``'!='`` (see
     :ref:`Numeric Equality Operators`);

-  Numeric operators that produce values of type ``float`` or ``double``:

   + Unary plus ``'+'`` and minus ``'-'`` operators (see :ref:`Unary Plus` and
     :ref:`Unary Minus`);
-  + Exponentiation operator ``'**'`` as a variant that produces a value of type
     ``double`` (see :ref:`Exponentiation Expression`);

   + Multiplicative operators ``'*'``, ``'/'``, and ``'%'`` (see
     :ref:`Multiplicative Expressions`);
   + Additive operators ``'+'`` and ``'-'`` (see :ref:`Additive Expressions`);
   + Increment operator ``'++'`` used as prefix (see :ref:`Prefix Increment`)
     or postfix (see :ref:`Postfix Increment`);
   + Decrement operator ``'--'`` used as prefix (see :ref:`Prefix Decrement`)
     or postfix (see :ref:`Postfix Decrement`);

-  Numeric operators that produce values of type ``int`` or ``long``:

   + Signed and unsigned shift operators ``'<<'``, ``'>>'``, and ``'>>>'`` (see
     :ref:`Shift Expressions`);
   + Bitwise complement operator ``'~'`` (see :ref:`Bitwise Complement`);
   + Integer bitwise operators ``'&'``, ``'^'``, and ``'|'`` (see
     :ref:`Integer Bitwise Operators`);

-  Ternary conditional operator ``'?:'`` (see :ref:`Ternary Conditional Expressions`);
-  The string concatenation operator ``'+'`` (see :ref:`String Concatenation`)
   that, if one operand is of type ``string`` and the other is of a
   floating-point type, converts the floating-point type operand to type
   ``string`` with a value represented in the decimal form (without loss
   of information), and then creates a concatenation of the two strings as a
   new ``string``.

.. index::
   floating-point type
   floating-point number
   operator
   value
   exponentiation operator
   ternary conditional operator
   numeric relational operator
   numeric equality operator
   comparison operator
   boolean type
   numeric operator
   float
   double
   unary operator
   unary plus operator
   unary minus operator
   multiplicative operator
   multiplicative expression
   additive operator
   prefix
   postfix
   increment operator
   decrement operator
   signed shift operator
   shift expression
   unsigned shift operator
   cast operator
   bitwise complement operator
   integer bitwise operator
   conditional operator
   string concatenation operator
   operand
   numeric type
   string
   decimal form
   loss of information
   concatenation

An operation is called a *floating-point operation* when:

- Both  operands of an ``exponentiation operator`` are of a numeric type (see
  :ref:`Exponentiation expression`); or
- At least one operand in a binary operator is of a floating-point type even if
  the other operand is integer, and the operator is not a string concatenation.

The operation implementation for an ``exponentiation operator`` with numeric
operands always uses the 64-bit floating-point arithmetic. Operands are
converted to ``double`` values if needed. The result of the numeric operator is
a value of type ``double``.

The following rules apply to other floating-point operations:

- If at least one operand of the numeric operator is of type ``double``, then
  the operation implementation uses the 64-bit floating-point arithmetic. The
  result of the numeric operator is a value of type ``double``.

- If the first operand is of type ``double`` and the other operand is not, then
  the numeric conversion (see :ref:`Widening Numeric Conversions`) is used to
  widen the operand first to type ``double``.

- If neither operand is of type ``double``, then the operation implementation
  is to use the 32-bit floating-point arithmetic. The result of the numeric
  operator is a value of type ``float``.

- If the first operand is of type ``float`` and the other operand is not, then
  the numeric conversion is used to widen the operator first to type ``float``.


Any floating-point type value can be cast to or from any numeric type (see
:ref:`Numeric Types`).

.. index::
   constructor
   method
   constant
   integer
   standard library
   operation
   floating-point operation
   predefined numeric types conversion
   string concatenation
   numeric type
   operand
   implementation
   float
   double
   numeric promotion
   numeric operator
   binary operator
   floating-point type

Conversions between floating-point types and type ``boolean`` are
not allowed. However, the value of floating-point type can be used
as a logical condition in some cases
(see :ref:`Extended Conditional Expressions`)

Operators on floating-point numbers, except the remainder operator (see
:ref:`Remainder`), behave in compliance with the IEEE 754 Standard.
For example, |LANG| requires the support of IEEE 754 *denormalized*
floating-point numbers and *gradual underflow* which facilitate proving
the desirable properties of a particular numeric algorithm. Floating-point
operations do not *flush to zero* if the calculated result is a
denormalized number.

|LANG| requires the floating-point arithmetic to behave as if the floating-point
result of every floating-point operator is rounded to the result precision. An
*inexact* result is rounded to a representable value nearest to the infinitely
precise result. |LANG| uses the *round to nearest* principle (the default
rounding mode in IEEE 754), and prefers the representable value with the least
significant bit zero out of any two equally near representable values.

.. index::
   cast
   floating-point type
   floating-point number
   boolean type
   numeric type
   numeric types conversion
   widening
   operand
   implementation
   numeric promotion
   remainder operator
   gradual underflow
   underflow
   flush to zero
   round to nearest
   rounding mode
   denormalized number
   nearest value
   IEEE 754

|LANG| uses *round toward zero* to convert a floating-point value to an
integer value (see :ref:`Numeric Casting Conversions`). In this case
it acts as if the number is truncated, and the mantissa bits are discarded.
The result of *rounding toward zero* is the value of the format that is
closest to and no greater in magnitude than the infinitely precise result.

A floating-point operation with overflow produces a signed infinity.

A floating-point operation with underflow produces a denormalized value
or a signed zero.

A floating-point operation with no mathematically definite result
produces ``NaN``.

All numeric operations with a ``NaN`` operand result in ``NaN``.

Predefined constructors, methods, and constants for *floating-point types*
are parts of the |LANG| :ref:`Standard Library`.

.. index::
   round toward zero
   conversion
   predefined numeric types conversion
   numeric type
   truncation
   truncated number
   rounding toward zero
   mantissa bit
   denormalized value
   NaN
   numeric operation
   increment operator
   decrement operator
   error
   overflow
   underflow
   signed zero
   signed infinity
   integer
   floating-point operation
   floating-point operator
   floating-point value
   floating-point type
   throw
   predefined constructor
   predefined method
   predefined constant

|

.. _Type boolean:

Type ``boolean``
================

.. meta:
    frontend_status: Done

Type ``boolean`` represents logical values ``true`` and ``false``.

The boolean operators are as follows:

-  Equality operators (see :ref:`Equality Expressions`);
-  Logical complement operator ``'!'`` (see :ref:`Logical Complement`);
-  Logical operators ``'&'``, ``'^'``, and ``'|'`` (see :ref:`Boolean Logical Operators`);
-  Conditional-and operator ``'&&'`` (see :ref:`Conditional-And Expression`) and
   conditional-or operator ``'||'`` (see :ref:`Conditional-Or Expression`);
-  Ternary conditional operator ``'?:'`` (see :ref:`Ternary Conditional Expressions`);
-  String concatenation operator ``'+'`` (see :ref:`String Concatenation`)
   that converts an operand of type ``boolean`` to type ``string`` (``true`` or
   ``false``), and then creates a concatenation of the two strings as a new
   ``string``.

Type ``boolean`` is a class type that is a part of the :ref:`Standard Library`.
It means that type ``boolean  is a subtype of ``Object``, and therefore can be
used at any place where a class name is expected.

.. code-block:: typescript
   :linenos:

    let a_boolean = new boolean
    console.log (a_boolean)
    // Output is: false
    let o: Object = a_boolean // OK


.. index::
   boolean
   Boolean
   relational operator
   complement operator
   logical operator
   conditional-and operator
   conditional-or operator
   ternary conditional operator
   ternary conditional expression
   string concatenation operator
   floating-point expression
   comparison
   conversion
   nonzero value
   concatenation
   string

|

.. _Reference Types:

Reference Types
***************

.. meta:
    frontend_status: Done

*Reference types* can be of the following kinds:

-  *Class* types (see :ref:`Type Object` and :ref:`Classes`);
-  *Interface* types (see :ref:`Interfaces`);
-  :ref:`Array Types`;
-  :ref:`Fixed-Size Array Types`;
-  :ref:`Tuple Types`;
-  :ref:`Function Types`;
-  :ref:`Union Types`;
-  :ref:`Literal Types`;
-  :ref:`Type Any`;
-  :ref:`Type string`;
-  :ref:`Type bigint`;
-  :ref:`Type never`;
-  :ref:`Type null`;
-  :ref:`Type void or undefined`; and
-  :ref:`Type Parameters`.

.. index::
   reference type
   class type
   interface type
   array type
   fixed-size array type
   function type
   union type
   string type
   literal type
   never type
   null type
   undefined type
   void type
   type parameter

The term *Object* is used further in this document to denote any instance
pointed at by a variable or constant of a reference type
(see :ref:`Variable and Constant Declarations`).

Multiple references to an object are possible.

Objects can have states. A state of an object that is a class instance is
stored in its fields. A state of an object that is an array (see
:ref:`Array Types`) or a tuple (see :ref:`Tuple Types`) is stored in
its elements.

If two variables of a reference type contain references
to the same object, and either variable modifies the state of that object,
then the change of state is also visible in the other variable.

.. index::
   object
   subtype
   state
   array element
   variable
   instance
   reference

|

.. _Type Any:

Type ``Any``
************

.. meta:
    frontend_status: Partly

Type ``Any`` is a predefined type which is the supertype of all types. Type
``Any`` is a predefined *nullish-type* (see :ref:`Nullish Types`), i.e., a
supertype of :ref:`Type void or undefined` and :ref:`Type null` in particular.

Type ``Any`` has no methods or fields.

.. _Type Object:

Type ``Object``
***************

.. meta:
    frontend_status: Done

Type ``Object`` is a predefined class type which is the supertype
(see :ref:`Subtyping`) of all types except :ref:`Type void or undefined`,
:ref:`Type null`, :ref:`Nullish Types`, :ref:`Type Parameters`, and
:ref:`Union types` that contain type parameters.
Type ``Object`` is a subtype of type ``Any`` (see :ref:`Type Any`).
All subtypes of ``Object`` inherit all methods of class ``Object`` (see
:ref:`Inheritance`). All methods of class ``Object`` are described in full in
:ref:`Standard Library`.

The method ``toString`` used in the examples in this document returns a
string representation of any object.


.. index::
   class
   interface
   string type
   bigint type
   array
   union
   function type
   enum type
   method
   interface
   array
   type parameter
   union type
   inheritance
   string

|

.. _Type never:

Type ``never``
**************

.. meta:
    frontend_status: Done

Type ``never`` is assignable to any type (see :ref:`Assignability`).

Type ``never`` has no instance. Type ``never`` is used as one of the following:

- Return type for functions or methods that never return a value, but
  throw an error when completing an operation.
- Type of variables that never get a value (however, an assignment statement
  with type ``never`` in both left-hand and right-hand sides is valid).
- Type of parameters of a function or a method to prevent the body of that
  function or method from being executed.

.. code-block:: typescript
   :linenos:

    function foo (): never {
       // function foo never returns
       throw new Error("foo() never returns")
    }

    let x: never = foo() // x never gets a value

    function bar (p: never) {
       // function bar body is never executed
    }

    bar (foo()) // bar is never called as foo() call never returns

.. index::
   never type
   instance
   return type
   method
   error
   throw
   variable
   assignment
   parameter
   function
   return
   value

|

.. _Type void or undefined:

Type ``void`` or ``undefined``
******************************

.. meta:
    frontend_status: Done

Type names ``void`` and ``undefined`` in fact refer to the same type with the
single value named ``undefined`` (see :ref:`Undefined Literal`), and are used
in this document interchangeably.

.. code-block:: typescript
   :linenos:

    function f1 (): void {
        return undefined // OK
    }

    function f2 (): undefined {
        return // OK
    }

    function f3 () {
        return undefined // OK
    }

    let v: void = undefined
    let u: undefined = undefined
    v = u // OK
    u = v // OK


Type name ``void`` is used typically as a return type to highlight that a
function, a method, or a lambda can contain :ref:`Return Statements` with no
expression, or no return statement at all:

.. code-block:: typescript
   :linenos:

    function foo (): void {} // no return at all

    class C {
        bar(): void {
            return // with no expression
        }
    }

    type FunctionWithNoParametersType = () => void

    let funcTypeVariable: FunctionWithNoParametersType = (): void => {}


Type name ``void`` can be used as a type argument that instantiates a generic
type, function, or method as follows:

.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

   class A<T> {
      f: T
      m(): T { return this.f }
      constructor (f: T) { this.f = f }
   }
   let a1 = new A<void>(undefined)      // OK, type name void used as type argument
   let a2 = new A<undefined>(undefined) // OK, type name undefined used as type argument

   console.log (a1.f, a2.m()) // Output is "undefined" "undefined"

   function foo<T>(p: T): T { return p }
   foo<void>(undefined) // OK, returns 'undefined' value

   type F1<T> = () => T
   const f1: F1<void> = (): void => {}
   const f2: F1<void> = () => {}
   const f3: F1<void> = (): undefined => { return undefined }

   // Array literals can be assigned to the array of void type name in any form
   type A1<T> = T[]
   type A2<T> = Array<T>
   const a1: A1<void> = [undefined]
   const a2: A2<void> = [undefined, undefined]
   const a3: void[] = [undefined]

.. index::
   void type
   type argument
   type parameter
   instantiation
   generic type
   undefined type

Type name ``undefined`` can be used also as type argument to instantiate a
generic type as follows:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

   class A<T> {}
   let a = new A<undefined>() // OK, type parameter is irrelevant
   function foo<T>(x: T) {}

   foo<undefined>(undefined) // OK

.. index::
   undefined type
   keyword undefined
   undefined literal
   literal
   type argument
   type annotation
   instantiation
   generic type
   annotation
   nullish type


.. _Type null:

Type ``null``
*************

.. meta:
    frontend_status: Done

The only value of type ``null`` is the literal ``null`` (see
:ref:`Null Literal`).

.. note::

    - Type ``null`` is supported for |TS| compatibility. 
      
    - Using ``undefined`` instead of ``null`` is considered the best practice
      in |TS| and |JS|.

    - Using type ``null`` as type annotation or in :ref:`Nullish Types` is not
      recommended if not required specifically. Using type ``undefined`` is
      recommended instead.

    - Type ``undefined`` provides a better performance than type ``null`` does.

.. index::
   null type
   null literal
   nullish type

|

.. _Type string:

Type ``string``
***************

.. meta:
    frontend_status: Done

Type ``string`` values are all string literals, e.g., '``abc``'. Type ``string``
stores sequences of characters as Unicode UTF-16 code units.

A ``string`` object is immutable, the value of a ``string`` object cannot be
changed after the object is created. The value of a ``string`` object can be
shared.

Type ``string`` has dual semantics, i.e.:

-  Type ``string`` behaves like a reference type (see :ref:`Reference Types`)
   if created, assigned, or passed as an argument;
-  Type ``string`` is handled as a value type by all
   ``string`` operations (see :ref:`String Concatenation`,
   :ref:`Equality Expressions`, and :ref:`String Relational Operators`).

As a result, reference type semantics of type ``string`` highlights that this
type is a class type. The appropriate class is a part of the
:ref:`Standard Library`, and type ``string`` is a subtype of ``Object``, and
can be used at any place where a class name is expected.

Moreover, type ``string`` is iterable (see :ref:`Iterable Types`),
and can be used at any place where an iterable type is expected. 

.. code-block:: typescript
   :linenos:

    let a_string = new string
    console.log (a_string)
    // Output is: <empty_string>
    let o: Object = a_string // OK

.. index::
   type string
   value
   Unicode code unit
   string literal
   literal
   character
   sequence
   string
   object
   dual semantics
   reference type
   expression
   equality
   relational operator

A number of operators can act on ``string`` values as follows:

-  Accessing the property ``length`` returns string length as ``int``
   type value. String length is a non-negative integer number.
   String length is set once at runtime and cannot be changed after that.

-  Concatenation operator '``+``' (see :ref:`String Concatenation`) produces
   a value of type ``string``. If the result is not a constant expression
   (see :ref:`Constant Expressions`), then the string concatenation operator
   can implicitly create a new ``string`` object;

-  Indexing a string value (see :ref:`String Indexing Expression`) returns a
   value of type ``string``. A new ``string`` object can be created implicitly.

A string value can contain any character, i.e., no character can be used to
indicate the end of a string. A character with the value '\0' is an ordinary
character inside a string as represented by the following example:

.. code-block:: typescript
   :linenos:

   console.log("a\0b".length) // output: 3

Using ``string`` in all cases is recommended, although the name ``String``
also refers to type ``string``.

.. index::
   string value
   access
   string type
   string literal
   string object
   string concatenation
   integer
   runtime
   indexing
   character
   reference type
   concatenation operator
   value type

|

.. _Type bigint:

Type ``bigint``
***************

.. meta:
    frontend_status: Done

|LANG| has the built-in ``bigint`` type that allows handling theoretically
arbitrary large integers. Values of type ``bigint`` can hold numbers that are
larger than the maximum value of type ``long``. Type ``bigint`` uses
the arbitrary-precision arithmetic. Type ``bigint`` does not belong to the
hierarchy of :ref:`Numeric Types`.
The consequences are as follows:

- No implicit conversion between ``bigint`` type and numeric types.
- Relational operators that use an operand of type ``bigint`` along with an
  operand of another type are illegal. Attempting to use such a relational
  operator produces a :index:`compile-time error`.
- Binary arithmetic expressions that use an operand of type ``bigint`` along
  with an operand of another type are illegal and produce a :index:`compile-time error`.
- The equality expression with ``bigint`` against non-``bigint`` always returns
  ``false``, and causes a :index:`compile-time warning`.

Values of type ``bigint`` can be created from the following:

- *Bigint literals* (see :ref:`Bigint Literals`); or
- Numeric type values, by using a call to the standard library class ``BigInt``
  methods or constructors (see :ref:`Standard Library`).

Similarly to ``string``, ``bigint`` type has dual semantics:

- If created, assigned, or passed as an argument, type ``bigint`` behaves
  like a reference type (see :ref:`Reference Types`).
- All applicable operations handle type ``bigint`` as a value type, 
  meaning the values of this type do not share state with other values.

Using ``bigint`` is recommended in all cases, although the name ``BigInt``
also refers to type ``bigint``. For |TS| compatibility, objects of type
``bigint`` can be created with help of ``BigInt`` static methods.

.. code-block:: typescript
   :linenos:

   let b1: bigint = new BigInt(5) // for Typescript compatibility
   let b2: bigint = 123n

Type ``bigint`` is a class type that has an appropriate class as a part of the
:ref:`Standard Library`. It means that type ``bigint`` is a subtype of
``Object``, and therefore can be used at any place where a class name is
expected.


.. code-block:: typescript
   :linenos:

    let a_bigint = new bigint
    console.log (a_bigint)
    // Output is: 0
    let o: Object = a_bigint // OK


.. index::
   bigint type
   built-in type
   arbitrary large integer
   integer
   long type
   bigint literal
   value type
   type annotation
   compatibility
   method
   static method
   numeric type
   value

|

.. _Literal Types:

Literal Types
*************

.. meta:
    frontend_status: Partly

*Literal types* are aligned with some |LANG| literals (see :ref:`Literals`).
Their names are the same as the names of their values, i.e., literals proper.
|LANG| supports only the following literal types:

- `String Literal Types`,
- ``null``, and
- ``undefined``.

.. code-block:: typescript
   :linenos:

    let a: "string literal" = "string literal"
    let b: null = null
    let c: undefined = undefined

    printThem (a, b, c)
    function printThem (p1: "string literal", p2: null, p3: undefined) {
        console.log (p1, p2, p3)
    }

There are no operations for literal types ``null`` and ``undefined``.

.. index::
   literal type
   truncation
   operation
   null type
   undefined type
   type name
   value name
   literal
   string


|

.. _String Literal Types:

String Literal Types
====================

.. meta:
    frontend_status: Done

Operations on variables of string literal types are identical to the operations
of their supertype ``string`` (see :ref:`Type string`). The
resulting operation type is the type specified for the operation in the
supertype:

.. code-block:: typescript
   :linenos:

    let s0: "string literal" = "string literal"
    let s1: string = s0 + s0   // + for string returns string

.. index::
   literal type
   string
   variable
   supertype
   subtyping
   operation type

|

.. _Array Types:

Array Types
***********

.. meta:
    frontend_status: Partly

*Array type* represents a data structure intended to comprise any non-negative
number of elements of types that are subtypes of the type specified in the
array declaration. |LANG| supports the following two predefined array types:

- :ref:`Resizable Array Types`; and

- :ref:`Fixed-Size Array Types` as an experimental feature.

*Resizable array types* are recommended for most cases.
*Fixed-size array types* can be used where performance is the major
requirement.

*Fixed-size arrays* differ from *resizable arrays* as follows:

- *Fixed-size arrays* have their length set only once to achieve a better
  performance.
- *Fixed-Size arrays* have no methods defined.

Any array type is a class type that has an appropriate class in the
:ref:`Standard Library`. It means that array types are subtypes of
``Object``, and that they can be used at any place where a class
name is expected. 
Moreover, array types are iterable (see :ref:`Iterable Types`), and can be
used at any place where an iterable type is expected. 


.. note::
   The term *array type* as used in this Specification applies to both
   *resizable array type* and *fixed-size array type*. The same holds true for
   *array value* and *array instance*.
   *Resizable arrays* and *fixed-size arrays* are not assignable to each other.

.. index::
   array length
   array type
   array value
   array instance
   resizable array type
   fixed-size array

|

.. _Resizable Array Types:

Resizable Array Types
=====================

.. meta:
    frontend_status: Partly

*Resizable array type* is a built-in type characterized by the following:

-  Any object of resizable array type contains elements. The number of elements
   is known as *array length*, and can be accessed by using the property
   ``length``.
-  Array length is a non-negative integer number.
-  Array length can be set and changed at runtime.
-  Array element is accessed by its index. The index is an integer number
   in the range from *0* to *array length minus 1*.
-  Accessing an element by its index is a constant-time operation.
-  If passed to non-|LANG| environment, an array is represented as a contiguous
   memory location.
-  Type of each array element is assignable to the element type specified
   in the array declaration (see :ref:`Assignability`).

.. index::
   resizable array type
   built-in type
   access
   array length
   non-negative integer number
   constant-time operation
   array type
   integer
   array element
   element type
   array declaration
   contiguous memory location
   assignability
   array declaration
   memory location
   access
   array

*Resizable array type* with elements of type ``T`` can have the following two
forms of syntax:

- ``T[]``, and
- ``Array<T>``.

The first form uses the following syntax:

.. code-block:: abnf

    arrayType:
       type '[' ']'
       ;

.. note::
   ``T[]`` and ``Array<T>`` specify identical, i.e., indistinguishable
   types (see :ref:`Type Identity`).

.. index::
   type identity
   element type
   syntax
   resizable array type
   type identity

Two basic operations with array elements take elements out of, and put
elements into an array by using the operator '``[]``'.

The same syntax can be used to work with :ref:`Indexable Types`,
some of such types are parts of :ref:`Standard Library`.

The number of elements in an array can be obtained by accessing the property
``length``. The length of an array can be set and changed in runtime using the
methods defined in :ref:`Standard Library`.

An array can be created by using :ref:`Array Literal`,
:ref:`Resizable Array Creation Expressions`, or the constructors
defined in :ref:`Standard Library`.

|LANG| allows setting a new value to ``length`` to shrink an array and provide
better |TS| compatibility. An error is caused by the following situations:

-  The value is of type ``number`` or other floating-point type,
   and the fractional part differs from 0;
-  The value is less than zero; or
-  The value is greater than previous length.

The above situations cause errors as follows:

-  A :index:`runtime error`, if the situation is identified at runtime,
   i.e., during program execution; and
-  A :index:`compile-time error`, if the situation is detected during
   compilation.

.. index::
   method
   array length
   array element
   access
   operator
   syntax
   indexable type
   resizable array
   compatibility
   floating-point type
   value
   runtime
   property length
   standard library

Array operations are illustrated below:

.. code-block:: typescript
   :linenos:

    let a : number[] = [0, 0, 0, 0, 0]
      /* allocate array with 5 elements of type number */
    a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
    let y = a[4] /* get the last element of array 'a' */
    let count = a.length // get the number of array elements
    a.length = 3 // shrink array
    y = a[2] // OK, 2 is the index of the last element now
    y = a[3] // Runtime error, attempt to access a non-existing array element

    let b: Array<number> = a // 'b' points to the same array as 'a'

A type alias can set a name for an array type (see :ref:`Type Alias Declaration`):

.. code-block:: typescript
   :linenos:

    type Matrix = number[][] /* array of array of numbers */

An array as an object is assignable to a variable of type ``Object``:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    let a: number[] = [1, 2, 3]
    let o: Object = a

.. index::
   alias
   array operation
   array element
   access
   type alias
   assignability
   array type
   object
   array
   assignment
   variable

|

.. _Readonly Array Types:

Readonly Array Types
====================

.. meta:
    frontend_status: Partly

*Readonly array type* is immutable, i.e.:

- Length of a variable of a *readonly array type* cannot be changed;
- Elements of a *readonly array type* cannot be modified after the initial
  assignment directly nor through a function or method call.

Otherwise, a :index:`compile-time error` occurs.


.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

    let x: readonly number [] = [1, 2, 3]
    x[0] = 42 // Compile-time error, array itself is readonly

*Readonly array type* with elements of type ``T`` can have the following two
syntax forms:

- ``readonly T[]``, and
- ``ReadonlyArray<T>``.

Both forms specify identical (indistinguishable) types (see :ref:`Type Identity`).

.. note::
   In arrays of arrays, all arrays are ``readonly``.

.. index::
   prefix readonly
   readonly array type
   array length
   assignment
   function call
   method call
   syntax
   array
   initial value

|

.. _Tuple Types:

Tuple Types
***********

.. meta:
    frontend_status: Done

*Tuple type* is a reference type created as a fixed set of other types.

The syntax of *tuple type* is presented below:

.. code-block:: abnf

    tupleType:
        '[' (type (',' type)* ','?)? ']'
        ;

The value of a tuple type is a group of values of types that comprise the tuple
type. The number of values in the group equals the number of types in a tuple
type declaration. The order of types in a tuple type declaration specifies the
type of the corresponding value in the group.

It implies that each element of a tuple has its own type.
The operator ``'[]'`` (square brackets) is used to access the elements of a
tuple in a manner similar to accessing the elements of an array.

An index expression operand must be a *constant expression*
(see :ref:`Constant Expressions`) of an integer type. The index of the first
tuple element is *0*:

.. code-block:: typescript
   :linenos:

   let tuple: [number, number, string, boolean, Object] =
              [     6,      7,  "abc",    true,    42]
   tuple[0] = 42
   console.log (tuple[0], tuple[4]) // `42 42` be printed

The number of elements of a tuple is known as *tuple length*, and can
be accessed by using the property ``length``:

.. code-block:: typescript
   :linenos:

   let tuple: [number, string]  = [1, "" ]
   console.log(tuple.length) // output: 2

Using the property ``length`` make sense for :ref:`Type Tuple`.

.. index::
   tuple type
   syntax
   reference type
   assignability
   operator
   object
   class
   reference type
   value
   type declaration
   array element
   index expression
   constant expression
   square bracket
   compatibility
   access

Any tuple type is subtype of type ``Tuple``
(see :ref:`Type Tuple`). Subtyping for tuples is discussed
in :ref:`Subtyping for Tuple Types`.

|

.. _Readonly Tuple Types:

Readonly Tuple Types
====================

.. meta:
    frontend_status: Done

If an *tuple* type has the prefix ``readonly``, then its elements cannot be
modified after the initial assignment directly or through a function or method
call. Otherwise, a :index:`compile-time error` occurs as follows:

.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

    let x: readonly [number, string] = [1, "abc"]
    x[0] = 42 // Compile-time error, tuple itself is readonly

.. index::
   prefix
   readonly
   tuple
   assignment
   tuple type
   initial value
   function call
   method call

|

.. _Type Tuple:

Type ``Tuple``
==============

.. meta:
    frontend_status: None

Type ``Tuple`` is a predefined type that is an *abstract superclass*
of any tuple type.

.. code-block:: typescript
   :linenos:

    let pair: [number, string] = [1, "abc"]

    let a: Tuple = pair // OK, subtyping

An empty tuple type is identical to ``Tuple``:

.. code-block:: typescript
   :linenos:

    let empty: [] = [] // empty tuple with no elements in it

Type ``Tuple`` is preserved by :ref:`Type Erasure`, and can be used
in :ref:`instanceof Expression` and :ref:`Cast Expression`.

An element of a ``Tuple`` value cannot be accessed directly.
The method ``unsafeGet`` with the signature can be used instead
to get an element value:

.. code-block:: typescript
   :linenos:

    unsafeGet(index: int): Any

Calls of the method ``unsafeGet`` cause a :index:`runtime error` if:

-  ``index`` value is less than zero; or
-  ``index`` value is greater than or equal to the actual tuple length.

.. index::
   runtime error

The usage of the method ``unsafeGet`` is illustrated below:

.. code-block:: typescript
   :linenos:

    function log_1(x: Object) {
        if (x instanceof Tuple) {
            console.log(x.unsafeGet(1))
        }
    }

    let a: [string, string] = ["aa", "bb"]
    log_1(a) // OK, output: 2, "bb"

    let b: [string] = ["aa"]
    log_1(b)     // Runtime error in ``unsafeGet`` call

No element of a ``Tuple`` value can be changed. |LANG| supports no
such change as it can cause a :index:`runtime error` at an unpredictable
place during execution.

|

.. _Function Types:

Function Types
**************

.. meta:
    frontend_status: Done

*Function type* can be used to express the expected signature of a function.
A function type consists of the following:

-  Optional type parameters;
-  List of parameters (which can be empty);
-  Optional return type.

.. index::
   function
   function type
   function signature
   signature
   return type
   parameter list

The syntax of *function type* is as follows:

.. code-block:: abnf

    functionType:
        '(' ftParameterList? ')' ftReturnType
        ;

    ftParameterList:
        ftParameter (',' ftParameter)* (',' ftRestParameter)?
        | ftRestParameter
        ;

    ftParameter:
        identifier ('?')? ':' type
        ;

    ftRestParameter:
        '...' ftParameter
        ;

    ftReturnType:
        '=>' type
        ;

The ``rest`` parameter is described in :ref:`Rest Parameter`.

.. code-block:: typescript
   :linenos:

    let binaryOp: (x: number, y: number) => number
    function evaluate(f: (x: number, y: number) => number) { }

A type alias can set a name for a *function type* (see
:ref:`Type Alias Declaration`):

.. index::
   alias
   rest parameter
   type alias
   function type
   syntax

.. code-block:: typescript
   :linenos:

    type BinaryOp = (x: number, y: number) => number
    let op: BinaryOp

If a function type has the ``'?'`` mark for a parameter name, then this
parameter and all parameters that follow (if any) are optional. Otherwise, a
:index:`compile-time error` occurs. The actual type of the parameter is then a
union of the parameter type and type ``undefined``. This parameter has no
default value.

.. code-block:: typescript
   :linenos:

    type FuncTypeWithOptionalParameters = (x?: number, y?: string) => void
    let foo: FuncTypeWithOptionalParameters
        = ():void => {}          // OK, arguments are just ignored
    foo = (p: number):void => {} // Compile-time error, call with zero arguments is invalid
    foo = (p?: number):void => {} // OK, call with zero or one argument is valid
    foo = (p1: number, p2?: string):void => {} // Compile-time error, call with zero arguments is invalid
    foo = (p1?: number, p2?: string):void => {} // OK

    foo()
    foo(undefined)
    foo(undefined, undefined)
    foo(42)
    foo(42, undefined)
    foo(42, "a string")

    type IncorrectFuncTypeWithOptionalParameters = (x?: number, y: string) => void
       // Compile-time error, no mandatory parameter can follow an optional parameter

    function bar (
       p1?: number,
       p2:  number|undefined
    ) {
       p1 = p2 // OK
       p2 = p1 // OK
       // Types of p1 and p2 are identical
    }


More details on function types assignability are provided in
:ref:`Subtyping for Function Types`.

.. index::
   function type
   parameter name
   parameter type
   undefined type
   assignability
   context
   conversion
   mandatory parameter
   optional parameter
   subtyping

|

.. _Type Function:

Type ``Function``
=================

.. meta:
    frontend_status: Done

Type ``Function`` is a predefined type that is a *direct superinterface*
of any function type.

A value of type ``Function`` cannot be called directly. A developer must use
the ``unsafeCall`` method instead. This method checks the arguments of type
``Function``, and calls the underlying function value if the number and types
of the arguments are valid.

.. code-block:: typescript
   :linenos:

   function foo(n: number) {}

   let f: Function = foo

   f(1) // Compile-time error, cannot be called

   f.unsafeCall(3.14) // correct call and execution
   f.unsafeCall() // Runtime error, wrong number of arguments

Another important property of type ``Function`` is ``name``.
It is a string that contains the name associated with the function object
in the following way:

-  If a function or a method is assigned to a function object, then the
   associated name is that of the function or of the method;

-  If a lambda is assigned to a variable of ``Function`` type, then the
   associated name is that of the variable;

-  Otherwise, the string is empty.

.. index::
   function type
   predefined type
   direct superinterface
   value
   method
   argument
   runtime error
   assignment
   function object
   lambda
   string

.. code-block:: typescript
   :linenos:

   function print_name (f: Function) {
      console.log (f.name)
   }

   function foo() {}
   print_name (foo) // Output: "foo"

   class A {
      static sm() {}
      m() {}
   }
   print_name (A.sm)      // Output: "sm"
   print_name (new A().m) // Output: "m"

   let x: Function = (): void => {}
   print_name (x) // Output: "x"

   let y = x
   print_name (y) // Output: "x"

   print_name (():void=>{}) // Output: ""

The declarations of the ``unsafeCall`` method, ``name`` property, and all other
methods and properties of type ``Function`` are included in the |LANG|
:ref:`Standard Library`.

.. index::
   property
   method
   Function type

|

.. _Union Types:

Union Types
***********

.. meta:
   frontend_status: Partly
   todo: fix grammar - two types are mandatory
   todo: support string literal in union
   todo: implement using common fields and methods, fix related issues


*Union* type is a reference type created as a combination of other types.

The syntax of *union type* is as follows:

.. code-block:: abnf

    unionType:
        type '|' type ('|' type)*
        ;

The values of a *union* type are valid values of all types the union is created
from.

A :index:`compile-time error` occurs if type in the right-hand side of a
union type declaration leads to a circular reference.

A :index:`compile-time error` occurs if *type* is a function type (see
:ref:`Function Types`) not enclosed in parentheses.


.. index::
   union type
   reference type
   type declaration
   circular reference
   union
   declaration
   circular reference

Typical usage examples of *union* types are represented below:

.. code-block:: typescript
   :linenos:

   type OperationResult = "Done" | "Not done"
   function do_action(): OperationResult {
      if (someCondition) {
         return "Done"
      } else {
         return "Not done"
      }
   }

   class Cat {
      // ...
   }
   class Dog {
     // ...
   }
   class Frog {
      // ...
   }
   type Animal = Cat | Dog | Frog | number
   // Cat, Dog, and Frog are some types (class type or interface type)

   let animal: Animal = new Cat()
   animal = new Frog()
   animal = 42
   // One may assign the variable of the union type with any valid value

    enum StringEnum {One = "One", Two = "Two"}

    type Union1 = string | StringEnum // OK, to be reduced during normalization

    type Invalid = string | () => string | number // Compile-time error, function type with no parenthesis around
    type Valid1 = string | (() => string) | number // OK
    type Valid21 = string | (() => string | number) // OK


.. index::
   union type
   class type
   interface type
   value
   normalization

Values of particular types can be received from a *union* by using different
mechanisms as follows:

.. code-block:: typescript
   :linenos:

    class Cat { sleep () {}; meow () {} }
    class Dog { sleep () {}; bark () {} }
    class Frog { sleep () {}; leap () {} }

    type Animal = Cat | Dog | Frog

    let animal: Animal = new Cat()
    if (animal instanceof Frog) {
        // animal is of type Frog here, conversion can be used:
        let frog: Frog = animal as Frog
        frog.leap()
    }

    animal.sleep () // Any animal can sleep

.. index::
   type
   value
   union
   conversion

Predefined types are represented by the following example:

.. code-block:: typescript
   :linenos:

    type Predefined = number | boolean
    let p: Predefined = 7
    if (p instanceof number) {
       // type of 'p' is number here
    }

Literal types are represented by the following example:

.. code-block:: typescript
   :linenos:

    type BMW_ModelCode = "325" | "530" | "735"
    let car_code: BMW_ModelCode = "325"
    if (car_code == "325"){
       car_code = "530"
    } else if (car_code == "530"){
       car_code = "735"
    } else {
       // pension :-)
    }

.. index::
   literal type
   predefined type
   union type
   conversion
   literal value
   value

|

.. _Union Types Normalization:

Union Types Normalization
=========================

.. meta:
   frontend_status: Partly
   todo: depends on literal types, maybe issues can occur for now

Union types normalization allows minimizing the number of types within a union
type, while keeping type safety. Some types can also be replaced for more
general types.

Union type ``T``:sub:`1` | ... | ``T``:sub:`N`, where ``N`` > 1, can be formally
reduced to type ``U``:sub:`1` | ... | ``U``:sub:`M`, where ``M`` <= ``N``,
or even to a non-union type *V*. In this latter case *V* can be a predefined
value type or a literal type.

The normalization process presumes that the following steps are performed one
after another:

.. index::
   union type
   type safety
   non-union type
   normalized union type
   normalization
   literal type

#. All nested union types are linearized.
#. All type aliases (if any and except recursive ones) are recursively replaced
   for non-alias types.
#. Identical types within a union type are replaced for a single type with
   account to the ``readonly`` type flag priority.
#. If one type in a union is ``string``, then all string literal types (if
   any) are removed.
#. If one type in a union is ``never``, then type ``never`` is removed.


   This procedure is performed recursively until none of the above steps can
   can be performed again.

.. index::
   union type
   nested union type
   linearization
   non-nullish type
   never type
   union type
   type alias
   numeric type
   numeric literal type
   readonly
   Any type
   alias
   non-alias
   literal type
   Object type
   subtyping

The normalization process results in a normalized union type. The process
is represented by the examples below:

.. code-block:: typescript
   :linenos:

    ( T1 | T2) | (T3 | T4) // normalized as T1 | T2 | T3 | T4. Linearization

    type A = A[] | string  // No changes. Recursive type alias is kept

    type B = number
    type C = string
    type D = B | C // normalized as number | string. Type aliases are unfolded

    number | number // normalized as number. Identical types elimination

    (number[]) | (readonly number[]) // normalized as readonly number[]. Readonly version wins

    "1" | string | number // normalized as  string | number. Literal type value belongs to another type values

    class Base {}
    class Derived extends Base {}
    Base | Derived // normalized as Base | Derived (no change)

The |LANG| compiler applies normalization while processing union types and
handling type inference for array literals (see
:ref:`Array Type Inference from Types of Elements`).

.. index::
   normalization
   union type
   normalized union type
   array literal
   type inference
   array literal
   linearization
   string
   readonly

|

.. _Access to Common Union Members:

Access to Common Union Members
==============================

.. meta:
    frontend_status: Partly

Where ``u`` is a variable of union type ``T``:sub:`1` | ... | ``T``:sub:`N`,
|LANG| supports access to a common member of ``u.m`` if the following
conditions are fulfilled:

- Each ``T``:sub:`i` is an interface or class type;

- Each ``T``:sub:`i` has a non-static member with the name ``m``; and

- For any ``T``:sub:`i`, ``m`` is one of the following:

    - Method or accessor with an equal signature; or
    - Same-type field.

Otherwise, a :index:`compile-time error` occurs as follows:

.. index::
   interface type
   method
   class type
   accessor
   signature
   field

.. code-block:: typescript
   :linenos:

    class A {
        n = 1
        s = "aa"
        foo() {}
        goo(n: number) {}
        static foo () {}
    }
    class B {
        n = 2
        s = 3.14
        foo() {}
        goo() {}
        static foo () {}
    }

    let u: A | B = new A

    let x = u.n // OK, common field
    u.foo() // OK, common method

    console.log(u.s) // Compile-time error, field types differ
    u.goo() // Compile-time error, signatures differ

    type AB = A | B
    AB.foo() // Compile-time error, foo() is a static method

.. index::
   field
   signature
   method

A :index:`compile-time error` occurs if in some ``T``:sub:`i`
the name ``m`` is overloaded (see :ref:`Overloading`):

.. code-block:: typescript
   :linenos:

    class C {
        overload foo { foo1, foo2 }
        foo1(a: number): void {}
        foo2(a: string): void {}
    }
    class D {
        foo(a: number): void {}
        foo2(a: string): void {}
    }

    function test(x: C | D) {
        x.foo() // Compile-time error, 'foo' in C is the explicit overload
        x.foo2("aa") // OK, 'foo2' in both C and D is a method
    }

|

.. _Keyof Types:

``Keyof`` Types
===============

.. meta:
   frontend_status: Done

``Keyof`` type is a special form of a union type that is built by using the
keyword ``keyof``. The keyword ``keyof`` is applied to a class or an interface
type (see :ref:`Classes` and :ref:`Interfaces`). The resultant new type is a
union of names (as string literal types) of all accessible members (see
:ref:`Accessible`) of the class or the interface type.

The syntax of ``keyof`` type is presented below:

.. code-block:: abnf

    keyofType:
        'keyof' typeReference
        ;

.. index::
   keyof type
   union type
   keyof keyword
   interface type
   semantics

A :index:`compile-time error` occurs if ``typeReference`` is neither a class
nor an interface type. The semantics of type ``keyof`` is represented by the
example below:


.. code-block-meta:
   expect-cte:

.. code-block:: typescript
   :linenos:

    class A {
       field: number
       method() {}
    }
    type KeysOfA = keyof A // "field" | "method"
    let a_keys: KeysOfA = "field" // OK
    a_keys = "any string different from field or method"
      // Compile-time error, invalid value for the type KeysOfA

If a class or an interface is empty, then its type ``keyof`` is equivalent
to type ``never``:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    class A {} // Empty class
    type KeysOfA = keyof A // never

.. index::
   class
   interface type
   never type
   keyof type

|

.. _Nullish Types:

Nullish Types
*************

.. meta:
    frontend_status: Done

|LANG| has *nullish types* that are in fact a specific form of union types (see
:ref:`Union Types`). The following unions can be used as the type to specify a
nullish version of type ``T``:

- ``T | undefined``;
- ``T | null``;  or
- ``T | undefined | null``.


.. note::

    Using type ``T | undefined`` in *nullish types* is recommended.
    The details are discussed in :ref:`Type null`.

All predefined types except :ref:`Type Any`, and all user-defined types are
non-nullish types. Non-nullish types cannot have a ``null`` or ``undefined``
value at runtime.

A variable declared to have type ``T | null`` can hold the values of type ``T``
and its derived types, or the value ``null``.

A variable declared to have type ``T | undefined`` can hold the values of
type ``T`` and its derived types, or the value ``undefined``.

A variable declared to have type ``T | null | undefined`` can hold values
of type ``T`` and its derived types, and the values ``undefined`` or ``null``.

*Nullish type* is a reference type (see :ref:`Union Types`).
A reference that is ``null`` or ``undefined`` is called a *nullish value*.

An operation that is safe with no regard to the presence or absence of
*nullish values* (e.g., re-assigning one nullish value to another) can
be used 'as is' for *nullish types*.

.. index::
   union type
   user-defined type
   type declaration
   type inference
   array literal
   nullish type
   non-nullish type
   predefined type declaration
   user-defined type declaration
   undefined value
   runtime
   derived type
   reference type
   nullish value
   nullish-safe option
   null safety
   access
   assignment
   re-assignment

The following nullish-safe options exist for dealing with nullish type ``T``:

-  Using safe operations:

   -  Safe method call (see :ref:`Method Call Expression` for details);
   -  Safe field access expression (see :ref:`Field Access Expression`
      for details);
   -  Safe indexing expression (see :ref:`Indexing Expressions` for details);
   -  Safe function call (see :ref:`Function Call Expression` for details);

-  Converting from ``T | null`` or ``T | undefined`` to ``T``:

   -  :ref:`Cast Expression`;
   -  Ensure-not-nullish expression (see :ref:`Ensure-Not-Nullish Expressions`
      for details);

-  Supplying a value to be used if a *nullish value* is present:

   -  Nullish-coalescing expression (see :ref:`Nullish-Coalescing Expression`
      for details).

.. note::
   *Nullish types* are not compatible with type ``Object``:

.. code-block:: typescript
   :linenos:

   function nullish (
      o: Object, nullish1: null, nullish2: undefined, nullish3: null|undefined,
      nullish4: AnyClassOrInterfaceType|null|undefined
   ) {
      o = nullish1 /* compile-time error, type 'null' is not compatible with
                      Object */
      o = nullish2 /* compile-time error, type 'undefined' is not compatible
                      with Object */
      o = nullish3 /* compile-time error, type 'null|undefined' is not
                      compatible with Object */
      o = nullish4 /* compile-time error, type
                      'AnyClassOrInterfaceType|null|undefined' is not
                      compatible with Object */
   }

.. index::
   method call
   field access expression
   indexing expression
   function call
   cast expression
   ensure-not-nullish expression
   nullish-coalescing expression
   nullish-safe option
   nullish value
   nullish type
   safe operation
   safe method call
   safe field access
   safe indexing expression
   safe function call
   conversion
   compatibility

|

.. _Utility Types:

Utility Types
*************

.. meta:
    frontend_status: Done

|LANG| supports several built-in types, called *utility* types. Utility types
allow constructing new types by adjusting properties of initial types, for
which purpose notations identical to generics are used. If the initial types
are class or interface, then the resultant utility types are also handled as
class or interface types.
All utility type names are accessible as simple names (see :ref:`Accessible`)
in any module across all its scopes. Using these names as user-defined entities
causes a :index:`compile-time error` in accordance with :ref:`Declarations`. An
alphabetically sorted list of utility types is provided below.

.. index::
   built-in type
   class
   interface
   accessibility
   module
   user-defined entity
   declaration
   utility type

|

.. _Awaited Utility Type:

Awaited Utility Type
====================

.. meta:
    frontend_status: None

Type ``Awaited<T>`` constructs a type which includes no type ``Promise``. It
is similar to ``await`` in ``async`` functions, or to the method ``.then()``
in *Promises*. Any occurrence of type ``Promise`` is recursively removed until
a generic, a function, an array, or a tuple type is detected. If type ``Promise``
is not a part of a type ``T`` declaration, then ``Awaited<T>`` leaves ``T``
intact.

If ``T`` in ``Awaited<T>`` is a type parameter, then subtyping for ``Awaited<T>``
is based on the subtyping for ``T``. In other words, ``Awaited<T>``
is a subtype of ``Awaited<U>`` if ``T`` is a subtype of ``U``. The use of type
``Awaited<T>`` is represented in the example below:

.. code-block:: typescript
   :linenos:

    type A = Awaited<Promise<string>>           // type A is string

    type B = Awaited<Promise<Promise<number>>>  // type B is number

    type C = Awaited<boolean | Promise<number>> // type C is boolean | number

    type D = Awaited <Object>                   // type D is Object

    type E = Awaited<Promise<Promise<number>|Promise<string>|Promise<boolean>>>
                                                // type E is number|string|boolean

    type F = Awaited<Promise<(p: Promise<string>) => Promise<number>>>
                                                // type F is (p: Promise<string>) => Promise<number>>

    type G = Awaited<Promise<Array<Promise<number>>>>
                                                // type F is Array<Promise<number>>

    function foo <T extends SuperType> (p: Awaited<T>) {}
    function bar <T extends SubType> (p: Awaited<T>) {
        foo (p) // is a valid call as Awaited<T extends SubType> <: Awaited<T extends SuperType>
    }


.. index::
   utility type
   awaited
   promise
   async function
   method

|

.. _NonNullable Utility Type:

NonNullable Utility Type
========================

.. meta:
    frontend_status: None

Type ``NonNullable<T>`` constructs a type by excluding ``null`` and ``undefined``
types (see :ref:`Type null` and :ref:`Type void or undefined`). It can be
expressed formally as follows (see :ref:`Difference Types`):

``NonNullable<T> = T - null - undefined``.

It implies the following:

- ``NonNullable<T>`` leaves ``T`` intact if type ``T`` contains neither ``null``
  nor ``undefined``;
- ``NonNullable<null>``,  ``NonNullable<undefined>``, or application of
  ``NonNullable<>`` to the union of ``null`` and ``undefined`` returns ``never``;
- ``NonNullable<Any> = Any - null - undefined``.


The use of type ``NonNullable<T>`` is represented in the example below:

.. code-block:: typescript
   :linenos:

    type X = Object | null | undefined
    type Y = NonNullable<X> // Type of 'Y' is Object

    class A <T> {
      field: NonNullable<T> // This is a non-nullable version of the type parameter
      constructor (field: NonNullable<T>) {
        this.field = field
      }
    }

    const a = new A<Object|undefined> (new Object)
    a.field // Type of field is Object

.. index::
   utility type
   null type
   undefined type
   field

|

.. _Partial Utility Type:

Partial Utility Type
====================

.. meta:
    frontend_status: Done

Type ``Partial<T>`` constructs a type with all fields (see
:ref:`Field Declarations`) and properties in their field form (see
:ref:`Interface Properties`) of ``T`` set to optional. ``T`` must be a class or
an interface type. Otherwise, a :index:`compile-time error` occurs. No method
(not even any getter or setter) of ``T`` is a part of the ``Partial<T>`` type.
The use is represented in the example below:

.. code-block:: typescript
   :linenos:

    interface Issue {
        title: string
        description: string
    }

    function process(issue: Partial<Issue>) {
        if (issue.title != undefined) {
            /* process title */
        }
    }

    process({title: "aa"}) // description is undefined

In the example above, type ``Partial<Issue>`` is transformed to a distinct but
analogous type as follows:

.. code-block:: typescript
   :linenos:

    interface /*some name*/ {
        title?: string
        description?: string
    }

.. index::
   type
   property
   optional property
   class type
   interface type
   method
   getter
   setter
   distinct type

Type ``T`` is not assignable to ``Partial<T>`` (see
:ref:`Assignability`), and no subtyping relation (see
:ref:`Subtyping`) holds between ``T``
and ``Partial<T>``. Variables of ``Partial<T>`` are to be initialized
with valid object literals.

If ``U`` is a subtype of ``T``, then ``Partial<U>`` is a subtype of ``Partial<T>``.

.. note::
   If class ``T`` has a user-defined getter, setter, or both, then none of
   those is called when object literal is used with ``Partial<T>`` variables.
   Object literal has its own built-in getters and setters to modify its
   variables. It is represented in the example below:

.. code-block:: typescript
   :linenos:

    interface I {
        property: number
    }
    class A implements I {
        _property: number
        set property(property: number) {
            console.log ("Setter called")
            this._property = property
        }
        get property(): number {
            console.log ("Getter called");
            return this._property
        }
    }

    function foo (partial: Partial<A>) {
        partial.property = 42 // Setter to be called
        console.log(partial.property) // Getter to be called
    }

    foo ({property: 1}) // No getter or setter from class A is called
    // 42 is printed as object literal has its own setter and getter

.. index::
   type
   assignability
   assignable type
   variable
   initialization
   object literal
   class
   user-defined getter
   built-in getter
   getter
   setter
   user-defined setter
   built-in setter
   property

|

.. _Required Utility Type:

Required Utility Type
=====================

.. meta:
    frontend_status: Done

Type ``Required<T>`` is opposite to ``Partial<T>``, and constructs a type with
all fields (see :ref:`Field Declarations`) and properties in their field form
(see :ref:`Interface Properties`) of ``T`` set to required (i.e., not optional).
``T`` must be a class or an interface type, otherwise a
:index:`compile-time error` occurs. No method (not even any getter or setter)
of ``T`` is part of the  ``Required<T>`` type. Its usage is represented in the
example below:

.. code-block:: typescript
   :linenos:

    interface Issue {
        title?: string
        description?: string
    }

    let c: Required<Issue> = { // Compile-time error, 'description' should be defined
        title: "aa"
    }

In the example above, type ``Required<Issue>`` is transformed to a distinct
but analogous type as follows:

.. code-block:: typescript
   :linenos:

    interface /*some name*/ {
        title: string
        description: string
    }

Type ``T`` is not assignable to ``Required<T>`` (see
:ref:`Assignability`), and no subtyping relation (see
:ref:`Subtyping`) holds between ``T`` and
``Required<T>``. Variables of ``Required<T>`` are to be initialized
with valid object literals.

If ``U`` is a subtype of ``T``, then
``Required<U>`` is a subtype of ``Required<T>``.

.. index::
   type
   interface type
   utility type
   assignability
   assignable type
   property
   required property
   method
   getter
   setter
   type
   object literal
   class type
   interface type
   distinct type
   initialization
   variable

|

.. _Readonly Utility Type:

Readonly Utility Type
=====================

.. meta:
    frontend_status: Done

Type ``Readonly<T>`` constructs a type with all fields (see
:ref:`Field Declarations`) and properties in their field form (see
:ref:`Interface Properties`) of ``T`` set to ``readonly``. It means that such
fields and properties of the constructed type cannot be reassigned. ``T`` must
be a class or an interface type, otherwise a :index:`compile-time error`
occurs. No method (not even any getter or setter) of ``T`` is part of the
``Readonly<T>`` type. Its usage is represented in the example below:

.. code-block:: typescript
   :linenos:

    interface Issue {
        title: string
    }

    const myIssue: Readonly<Issue> = {
        title: "One"
    };

    myIssue.title = "Two" // Compile-time error, readonly property

.. index::
   type
   readonly type
   utility type
   type readonly
   constructed value
   method
   reassignment
   assignability
   assignable type
   property
   interface type
   getter
   setter

Type ``T`` is assignable (see :ref:`Assignability`) to ``Readonly<T>``,
and allows assignments as a consequence:

.. code-block:: typescript
   :linenos:

    class A {
       f1: string = ""
       f2: number = 1
       f3: boolean = true
    }
    let x = new A
    let y: Readonly<A> = x // OK

|

Type ``T`` is a subtype (see :ref:`Subtyping`) of ``Readonly<T>``.

If type ``U`` is a subtype of ``T``, then ``Readonly<U>`` is a subtype
of ``Readonly<T>``.

.. _Record Utility Type:

Record Utility Type
===================

.. meta:
    frontend_status: Done

Type ``Record<K, V>`` constructs a container that maps keys (of type ``K``)
to values of type ``V``.

Type ``K`` is restricted to numeric types (see :ref:`Numeric Types`), type
``string``, string literal types, and union types constructed from
these types.

A :index:`compile-time error` occurs if any other type, or literal of any other
type is used in place of this type.

Its usage is represented in the example below:

.. index::
   record utility type
   utility type
   value
   container
   restriction
   union type
   numeric type
   string type
   literal
   string literal type
   compile-time error
   type
   key
   union type


.. code-block:: typescript
   :linenos:

    type R1 = Record<number, Object>             // OK
    type R2 = Record<boolean, Object>            // Compile-time error
    type R3 = Record<"salary" | "bonus", Object> // OK
    type R4 = Record<"salary" | boolean, Object> // Compile-time error
    type R5 = Record<"salary" | number, Object>  // OK
    type R6 = Record<string | number, Object>    // OK

Type ``V`` has no restrictions.

A special form of object literals is supported for instances of type ``Record``
(see :ref:`Object Literal of Record Type`).

Access to ``Record<K, V>`` values is performed by an *indexing expression* like
*r[index]*, where *r* is an instance of type ``Record``, and *index* is the
expression of type ``K`` (see :ref:`Record Indexing Expression` for detail).

Variables of type ``Record<K, V>`` can be initialized by a valid object
literal of Record type (see :ref:`Object Literal of Record Type`) where the
literal is valid if the type of key expression is compatible with key type
``K``, and the type of value expression is compatible with the type ``V``.

.. code-block:: typescript
   :linenos:

    type Keys = 'key1' | 'key2' | 'key3'

    let x: Record<Keys, number> = {
        'key1': 1,
        'key2': 2,
        'key3': 4,
    }
    console.log(x['key2']) // prints 2
    x['key2'] = 8
    console.log(x['key2']) // prints 8

In the example above, ``K`` is a union of literal types and thus the result of
an indexing expression is of type ``V``. In this case it is ``number``.

.. index::
   restriction
   object literal
   literal
   instance
   Record type
   access
   indexing expression
   index expression
   index
   number
   expression
   variable
   compatibility
   value

|

.. _ReturnType Utility Type:

ReturnType Utility Type
=======================

.. meta:
    frontend_status: None

Type ``ReturnType<T>`` constructs a new type from the return type of a function
type ``T`` (see :ref:`Function Types`). A :index:`compile-time error` occurs if
a non-function type except type ``never`` is provided. The usage is represented
in the example below:

.. code-block:: typescript
   :linenos:

   type MyString = ReturnType<()=> string> // OK
   type Incorrect = ReturnType<string>     // Compile-time error

   function foo<P extends Function, R = ReturnType<P>>() {}
   /* OK, default type for the second type parameter is the return type of
      the function type provided as the first type argument */

   foo<()=>number>()  // R is number

   type anAny = ReturnType<Function>  // anAny is Any
   type aNever = Return Type<never>   // aNever is never


|

.. _Utility Type Private Fields:

Utility Type Private Fields
===========================

.. meta:
    frontend_status: Done

Utility types are built on top of other types. Private fields of the initial
type stay in the utility type but they are not accessible (see
:ref:`Accessible`) and cannot be accessed in any way. It is represented in the
example below:

.. code-block:: typescript
   :linenos:

   function foo(): string {  // Potentially some side effect
      return "private field value"
   }

   class A {
      public_field = 444
      private private_field = foo()
   }

   function bar (part_a: Readonly<A>) {
      console.log (part_a)
   }

   bar ({public_field: 777}) // OK, object literal has no field `private_field`
   bar ({public_field: 777, private_field: ""}) // Compile-time error, incorrect field name

   bar (new A) // OK, object of type Readonly<A> has field `private_field`

.. index::
   utility type
   private field
   type
   access
   accessibility
   field name

|

.. _Nesting Utility Types:

Nesting Utility Types
===========================

.. meta:
    frontend_status: Partly

If more than one utility types are required then they can be nested as in example below:

.. code-block:: typescript
   :linenos:

   interface Issue {
     title?: string
   }

   const myIssue: Required<Readonly<Issue>> = {
      title: "One"
   };
   console.log(myIssue.title)  // Safe: required property
   myIssue.title = "Two" // Compile-time error, readonly property

.. index::
   utility type
   private field
   nesting
   readonly property
   required property
   type
   access
   accessibility

|

.. _Default Values for Types:

Default Values for Types
************************

.. meta:
    frontend_status: Done

.. note::
   This |LANG| feature is experimental.

So-called *default values* are used by the following types for variables
that require no explicit initialization (see :ref:`Variable Declarations`):

- :ref:`Value Types`;
- Type ``undefined`` and all its supertypes

All other types, including reference types, enumeration types, and type
parameters have no default values.

Default values of value types are as follows:

.. index::
   default value
   variable
   explicit initialization
   literal type
   undefined type
   type parameter
   reference type
   enumeration type
   initialization
   supertype

+--------------+--------------------+
|   Data Type  |   Default Value    |
+==============+====================+
| ``number``   | 0 as ``number``    |
+--------------+--------------------+
| ``byte``     | 0 as ``byte``      |
+--------------+--------------------+
| ``short``    | 0 as ``short``     |
+--------------+--------------------+
| ``int``      | 0 as ``int``       |
+--------------+--------------------+
| ``long``     | 0 as ``long``      |
+--------------+--------------------+
| ``float``    | +0.0 as ``float``  |
+--------------+--------------------+
| ``double``   | +0.0 as ``double`` |
+--------------+--------------------+
| ``char``     | ``u0000``          |
+--------------+--------------------+
| ``boolean``  | ``false``          |
+--------------+--------------------+

Value ``undefined`` is the default value of each type to which this value can
be assigned.

.. code-block-meta:

.. code-block:: typescript
   :linenos:

   class A {
     f1: string|undefined
     f2?: boolean
   }
   let a = new A()
   console.log (a.f1, a.f2)
   // Output: undefined, undefined

   let o1: Any
   let o2: void
   let o3: undefined
   console.log (o1, o2, o3)
   // Output: undefined, undefined, undefined


.. index::
   number
   byte
   short
   int
   long
   float
   double
   char
   boolean
   type
   null
   undefined type
   data type
   assignment

-------------

.. [3]
   Any mention of IEEE 754 in this Specification refers to the latest
   revision of "754-2019--IEEE Standard for Floating-Point Arithmetic".

.. raw:: pdf

   PageBreak
