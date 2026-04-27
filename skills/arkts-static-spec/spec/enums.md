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

.. _Enumerations:

Enumerations
############

.. meta:
    frontend_status: Done

Enumeration type ``enum`` specifies a distinct user-defined type with an
associated set of named readonly members that define its possible enumeration
values.

The syntax of *enumeration declaration* is presented below:

.. code-block:: abnf

    enumDeclaration:
        'const'? 'enum' identifier enumBaseType? '{' enumMemberList? '}'
        ;

    enumBaseType:
        ':' type
        ;

    enumMemberList:
        enumMember (',' enumMember)* ','?
        ;

    enumMember:
        identifier initializer?
        ;

    initializer:
        '=' expression
        ;

.. index::
   enumeration
   type enum
   user-defined type
   named member
   value
   enumeration declaration
   syntax

If an *enumeration declaration* is prefixed with the keyword
``const``, then a :index:`compile-time error` occurs. This restriction
is temporary, and the semantics of ``const enum`` is to be made
available in the future versions of |LANG|.

All member names in an enumeration must be unique. Otherwise,
a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    enum E3 { A = 5, A = 77 }      // Compile-time error
    enum E4 { A = 5, B = 5 }       // OK, values can be the same

Empty ``enum`` is supported as a corner case for compatibility with |TS|.

.. code-block:: typescript
   :linenos:

    enum Empty {} // OK

An enumeration member has a value that can be set
explicitly by an initializer expression or implicitly (see
:ref:`Initialization of Enumeration Members`). 

.. index::
   conversion
   enumeration type
   numeric type
   string type
   type enumeration
   conversion
   type string
   expression
   enum
   compatibility

Qualification by type name is mandatory to access the enumeration member,
except initializer expression:

.. code-block:: typescript
   :linenos:

    enum Color { 
        Red, 
        Green, 
        Blue, 
        Default = Red // Qualification can be omitted
    }
    let c: Color = Color.Red // Qualification is mandatory

.. index::
   qualification
   access

The following operators can be applied to operands of enumeration types:

- Relational operators (see :ref:`Enumeration Relational Operators`);
- Equality operators (see :ref:`Equality Expressions`).

Implicit conversions (see :ref:`Enumeration to Numeric Type Conversion`,
:ref:`Enumeration to string Type Conversion`) are used to convert
a value of enumeration type to numeric types or type ``string`` depends on the
enumeration base type:

.. code-block:: typescript
   :linenos:

    enum Color { Red, Green, Blue }
    let x: number = Color.Red + 1 // OK, implicit conversion to 'int'

    enum T { A = "hello", B = "Bye" }

    let s: string = T.A // OK, implicit conversion to 'string'

If enumeration type is exported, then all enumeration members are
exported along with the mandatory qualification.

For example, if *Color* is exported, then all members like ``Color.Red``
are exported along with the mandatory qualification ``Color``.

.. _Enumeration Base Type:

Enumeration Base Type
*********************

.. meta:
    frontend_status: Done

Each enumeration has an *enumeration base type*. A base type can be set
explicitly (see :ref:`Enumeration with Explicit Base Type`) or inferred from
initializers as follows:

- If at least one member does not have an initializer, the inferred type is
  ``int``. Types of all initializers must be assignable to type ``int``
  (see :ref:`Assignability`). Otherwise, a :index:`compile-time error` occurs.

- If types of all initializer expressions are assignable to type
  ``int`` then the inferred type is ``int``;

- If types of all initializer expressions are assignable to type
  ``string`` then the inferred type is ``string``;

- Otherwise, a :index:`compile-time error` occurs.

It is discussed in detail in :ref:`Initialization of Enumeration Members`.

Cases with base type inference are represented in the example below:

.. code-block:: typescript
   :linenos:

    enum E1 { A, B }     // OK, base type is 'int'
    enum E2 { A = 5, B } // OK, base type is 'int'

    enum E3 { A, B = "hello"}     // Compile-time error, base type cannot be inferred
    enum E4 { A = 5, B = "hello"} // Compile-time error, base type cannot be inferred

|

.. _Enumeration with Explicit Base Type:

Enumeration with Explicit Base Type
***********************************

.. meta:
    frontend_status: Done

*Enumeration base type* can be set explicitly as represented in the example
below:

.. code-block:: typescript
   :linenos:

    enum DoubleEnum: double { A = 0.0, B = 1, C = 3.14159 }
    enum ByteEnum: byte { A = 0, B = 1, C = 3 }

A :index:`compile-time error` occurs in the following situations:

- *Explicit type* is different from any numeric or string type.

- Type of explicit member initializer is not assignable
  (see :ref:`Assignability`) to the base type;

- Enumeration member has no explicit initializer and the base type is not
  an integer type (see :ref:`Initialization of Enumeration Members`).

.. index::
   explicit type
   enum member
   integer type
   non-explicit type
   integer value
   assignability
   numeric type
   string type

.. code-block:: typescript
   :linenos:

    enum DoubleEnum: double { A = 0.0, B = 1, C = 3.14159 } // OK
    enum LongEnum: long { A = 0, B = 1, C = 3 } // OK

    enum Wrong1: double { A, B, C } // Compile-time error, must be explicitly initialized
    enum Wrong2: long { A = 1, B = "abc" } // Compile-time error, not assignable to 'long'

|

.. _Initialization of Enumeration Members:

Initialization of Enumeration Members
*************************************

.. meta:
    frontend_status: Done

An enumeration member value can be set explicitly by an initializer
expression. An initializer expression can be omitted if an
*enumeration base type* is an integer type. Otherwise, a
:index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    enum E1 { A, B, C }    // OK, base type is 'int'
    enum E2: long { K, L } // OK, base type is 'long'

    enum E3 { A = "a", B }   // Compile-time error, wrong base type
    enum E4: string { A, B } // Compile-time error, base type is not an integer type
    enum E5: double { C, D } // Compile-time error, base type is not an integer type

If initializers for all members are omitted, then the first member is assigned
the value zero. The other member is assigned the value of the
immediately preceding member plus one.

If some but not all members have their values set explicitly, then
the values of the members are set by the following rules:

-  If an initializer is not a *constant expression*
   (see :ref:`Constant Expressions`), then all subsequent members must be
   explicitly initialized. Otherwise, a :index:`compile-time error` occurs.

-  Member which is the first and has no explicit initializer
   gets the zero value.
-  Member with an explicit initializer has that explicit value.
-  Member that is not the first and has no explicit initializer takes the value
   of the immediately preceding constant plus one.

In the example below, the value of ``Red`` is 0, of ``Blue``, 5, and of
``Green``, 6:

.. code-block:: typescript
   :linenos:

    enum Color { Red, Blue = 5, Green }

.. index::
   int type
   constant
   value

The example below illustrates the requirement to have explicit initializers
after non-constant initializer:

.. code-block:: typescript
   :linenos:

    function foo() { return 1 }

    enum Wrong {
        A,
        B = foo(),
        C // Compile-time error, must have explicit initializer
    }

|

.. _Enumeration Methods:

Enumeration Methods
*******************

.. meta:
    frontend_status: Done

The name of enumeration type can be indexed by the value of this enumeration
type to get the name of the member:

.. code-block:: typescript
   :linenos:

    enum Color { Red, Green = 10, Blue }
    let c: Color = Color.Green
    console.log(Color[c]) // Prints: Green

If several enumeration members have the same value, then the textually last
member has the priority:

.. code-block:: typescript
   :linenos:

   enum E { One = 1, one = 1, oNe = 1 }
   console.log(E[E.fromValue(1)]) // Prints: oNe
   console.log(E.fromValue(1).getName()) // Prints: oNe

Several static methods are available for each enumeration class type as
follows:

-  Method ``static values()`` returns an array of enumeration members
   in the order of declaration.
-  Method ``static getValueOf(name: string)`` returns an enumeration member
   with the given name, or throws an error if no member with such name
   exists.
-  Method ``static fromValue(value: T)``, where ``T`` is the base type
   of the enumeration, returns an enumeration member with a given value, or
   throws an error if no member has such a value.

.. index::
   enumeration method
   static method
   enumeration type
   enumeration member
   value

.. code-block:: typescript
   :linenos:

      enum Color { Red, Green, Blue = 5 }
      let colors = Color.values()
      // colors[0] is the same as Color.Red

      let red = Color.getValueOf("Red")

      Color.fromValue(5) // OK, returns Color.Blue
      Color.fromValue(6) // Throws runtime error

Methods for instances of an enumeration type are as follows:

-  Method ``toString()`` converts a value of enumeration member to
   type ``string``:

.. index::
   value
   conversion
   type
   string type
   method

.. code-block:: typescript
   :linenos:

    enum Color { Red, Green = 10, Blue }
    let c: Color = Color.Green
    console.log(c.toString()) // Prints: 10

-  Method ``valueOf()`` returns a numeric or ``string`` value of an enumeration
   member depending on the enumeration base type.

-  Method ``getName()`` returns the name of an enumeration member.

.. code-block-meta:

.. code-block:: typescript
   :linenos:

      enum Color { Red, Green = 10, Blue }
      let c: Color = Color.Green
      console.log(c.valueOf()) // Prints 10
      console.log(c.getName()) // Prints Green

.. note::
   Methods ``c.toString()`` and ``c.valueOf().toString()`` return the same
   value.

.. index::
   instance
   method
   enumeration type
   value
   name
   enumeration member

|

.. raw:: pdf

   PageBreak
