Expressions
###########

.. meta:

This Chapter describes the meanings of expressions and the rules for the
evaluation of expressions, except the expressions described as experimental (see
:ref:`Lambda Expressions with Receiver`).

The syntax of *expression* is presented below:

.. code-block:: abnf

    expression:
        primaryExpression
        | instanceOfExpression
        | castExpression
        | typeOfExpression
    ...

The syntax below introduces several productions to be used by other
expression syntax rules:

.. code-block:: abnf

    objectReference:
        typeReference
        | 'super'
        | primaryExpression
        ;

``objectReference`` refers to one of the following three options:

- Class that is to handle static members;

- ``super`` that is to access constructors declared in the
  superclass, or the overridden method version of the superclass;

- *primaryExpression* that is to refer to a variable
  after evaluation, unless the manner of the
  evaluation is altered by the chaining operator ``'?.'`` (see
  :ref:`Chaining Operator`).

If the form of *primaryExpression* is *thisExpression*, then the pattern
``this?.`` is handled as a :index:`compile-time error`.

If the form of *primaryExpression* is *super*, then the pattern ``super?.``
is handled as a :index:`compile-time error`.

Operators
*********

An expression is a composition of an operator with its operands. Parentheses
are used to change the order of calculation.

*Operators*, or *operator signs*, are tokens that denote various actions, i.e.,
addition, subtraction, etc. (see :ref:`Operators and Punctuators`) to be
performed on the values of *operands*. Depending on the number of operands,
operators can be as follows:

- *Unary operator* has a single operand,
- *Binary operator* has two operands, and
- *Ternary operator* has three operands.

Some operators can be both unary and binary.

Each operator has *precedence* and *associativity* which are significant if
an expression has several operators:

- *Precedence* defines operator priority, i.e., the order of evaluation of
  operators with different precedence.
- *Associativity* defines the direction of evaluation (left-to-right or
  right-to-left) if several operators have the same precedence.

For example, the sum is calculated first due to the higher precedence of
``'+'``, and then assignments are processed from right to left due to the right
associativity of ``'='`` in the following chunk of code:

.. code-block:: typescript
   :linenos:

   let a: number = 1, b: number
   b = a = a+10
   console.log(b) // prints '11'

.. note::
   The parentheses ``'( )'`` are the *grouping operator* that has the highest
   precedence and allows changing the order of expression evaluation.

The complete list of operators indicating their precedence and associativity
is provided in :ref:`Operator Precedence`.

Operator Precedence
===================

.. meta:
    todo: fix 'await' precedence

The table below summarizes the entire information on the precedence and
associativity of operators. Each section on a particular operator
also contains detailed information.

.. list-table::
   :width: 100%
   :widths: 35 50 15
   :header-rows: 1

   * - Operator
     - Precedence
     - Associativity
   * - Grouping
     - ``'()'``
     - n/a
   * - Member access and chaining
     - ``'.'``, ``'?.'``
     - left-to-right
   * - Access and call
     - ``'[]'``, ``'.'``, ``'()'``, ``new``
     - n/a
   * - Postfix increment and decrement
     - ``'++'``, ``'--'``
     - n/a
   * - Postfix ``'!'`` (ensure-not-nullish operator)
     - ``'!'``
     - n/a
   * - Prefix increment and decrement, unary plus and minus,
       Prefix ``'!'`` (logical NOT), bitwise complement, ``typeof``, ``await``
     - ``'++'``, ``'--'``, ``'+'``, ``'-'``, ``'!'``, ``'~'``, ``typeof``, ``await``
     - n/a
   * - Exponentiation
     - ``'**'``
     - right-to-left
   * - Multiplicative
     - ``'*'``, ``'/'``, ``'%'``
     - left-to-right
   * - Additive
     - ``'+'``, ``'-'``
     - left-to-right
   * - Cast
     - ``as``
     - left-to-right
   * - Shift
     - ``'<<'``, ``'>>'``, ``'>>>'``
     - left-to-right
   * - Relational
     - ``'< >'``, ``'<='``, ``'>='``, ``instanceof``
     - left-to-right
   * - Equality
     - ``'=='``, ``'!='``
     - left-to-right
   * - Bitwise AND
     - ``'&'``
     - left-to-right
   * - Bitwise exclusive OR
     - ``'^'``
     - left-to-right
   * - Bitwise inclusive OR
     - ``'|'``
     - left-to-right
   * - Logical AND
     - ``'&&'``
     - left-to-right
   * - Logical OR
     - ``'||'``
     - left-to-right
   * - Null-coalescing
     - ``'??'``
     - left-to-right
   * - Ternary
     - ``condition?whenTrue:whenFalse``
     - right-to-left
   * - Assignment
     - ``'='``, ``'+='``, ``'-='``, ``'%='``, ``'*='``, ``'/='``, ``'&='``,
       ``'^='``, ``'|='``, ``'<<='``, ``'>>='``, ``'>>>='``
     - right-to-left

Evaluation of Expressions
*************************

.. meta:
    todo: needs more investigation, too much failing CTS tests (mostly tests are buggy)

The result of a program expression *evaluation* denotes the following:

-  Variable (the term *variable* is used here in the general, non-terminological
   sense to denote a modifiable lvalue in the left-hand side of an assignment);
   or
-  Value (results found elsewhere).

A variable or a value are equally considered the *value of the expression*
if such a value is required for further evaluation.

The type of an expression is determined at compile time (see
:ref:`Type of Expression`).

.. note::
   An expression is a sequence of operators and
   operands that specifies a computation. The
   evaluation of an expression can produce side
   effects. Any expression can be a subexpression
   of a more complex expression. E.g., the function
   call in `f()*3` is in turn a subexpression of a
   multiplication expression.

*Constant expressions* (see :ref:`Constant Expressions`) are the expressions
with values that can be determined at compile time.

Type of Expression
==================

.. meta:

Every expression in the ArkTS programming language has a type. The type of an
expression is determined at compile time.

In most contexts, an expression must be *compatible* with the type expected in
a context. This type is called *target type*. If no target type is available
in a context, then the expression is called a *standalone expression*:

.. code-block:: typescript
   :linenos:

    let a = expr // no target type is available

    function foo() {
        expr // no target type is available
    }

Otherwise, the expression is *non-standalone*:

.. code-block-meta:
   skip

.. code-block:: typescript
   :linenos:

    let a: number = expr // target type of 'expr' is number

    function foo(s: string) {}
    foo(expr) // target type of 'expr' is string

In some cases, the type of an expression cannot be inferred (see
:ref:`Type Inference`) from the expression itself (see
:ref:`Object Literal` as an example). If such an expression is used as a
*standalone expression*, then a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    class P { x: number, y: number }

    let x = { x: 10, y: 10 } // standalone object literal - compile time error
    let y: P = { x: 10, y: 10 } // OK, type of object literal is inferred

The evaluation of an expression type requires completing the following steps:

#. Collect information for type inference (type annotation,
   generic constraints, etc);

#. Perform :ref:`Type Inference`;

#. If the expression type is not yet inferred at a previous step, and the
   expression is a literal in the general sense, including :ref:`Array Literal`,
   then an attempt is made to evaluate the type from the expression itself.

A :index:`compile-time error` occurs if none of these steps produces an
appropriate expression type.

If the expression  type is ``readonly``, then the target type must
also be ``readonly``. Otherwise, a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

      let readonly_array: readonly number[] = [1, 2, 3]

      foo1(readonly_array) // OK
      foo2(readonly_array) // Compile-time error

      function foo1 (p: readonly number[]) {}
      function foo2 (p: number[]) {}

      let writable_array: number [] = [1, 2, 3]
      foo1 (writable_array) // OK, as always safe

Normal and Abrupt Completion of Expression Evaluation
=====================================================

.. meta:

The evaluation of an expression requires several
steps of computation. An expression is said to
be *evaluated normally* if all necessary steps of
the evaluation complete with no error thrown.
If an error thrown at any step stops the evaluation
of an expression, then the situation is defined as an
*abrupt completion*. The cause of an
*abrupt completion* is explained in the value
attached to the error object.

The evaluation of an expression can result in a
:index:`runtime error` as a result of as follows:

-  If the value of an array index expression is negative, or greater than, or
   equal to the length of the array, then an *array indexing expression* (see
   :ref:`Array Indexing Expression`) throws ``RangeError``.
-  If the type of a value being assigned to a fixed-size array element is not
   a subtype of an array element type, then an :ref:`Assignment` throws
   *ArrayStoreError*.
-  If a :ref:`Cast Expression` conversion cannot be performed at runtime, then
   it throws ``ClassCastError``.
-  If a right-hand expression has the zero value, then the integer division or
   integer remainder (see :ref:`Division` and :ref:`Remainder`) operator throws
   ``ArithmeticError``.

An error during the evaluation of an expression can be caused by a possible
hard-to-predict and hard-to-handle linkage and virtual machine error.

Abrupt completion of the evaluation of a subexpression results in the following:

-  Immediate abrupt completion of an expression that contains the subexpression
   (if the evaluation of the contained subexpression is required
   for the evaluation of the entire expression); and
-  Cancellation of all subsequent steps of the normal mode of evaluation.

The terms *complete normally* and *complete abruptly* can also denote
normal and abrupt completion of the execution of a statement (see
:ref:`Normal and Abrupt Statement Execution`). A statement can complete
abruptly for many reasons in addition to an error being thrown.

Order of Expression Evaluation
==============================

.. meta:

Subexpressions of an expression are evaluated
from left to right as represented in the examples
below:

-  Any right-hand-side expression of a
   binary operator is evaluated only after
   the left-hand-side expression is fully
   evaluated:

   .. code-block:: typescript
      :linenos:

      function arg(s: string): int { console.log(s); return 1; }

      arg("left") +  arg("right")
      // Prints:
      //    left
      //    right

-  The *condition* of a ternary operator is evaluated first. Then,
   either the subexpression *whenTrue* or the subexpression
   *whenFalse* is evaluated depending on the *condition* value:

   .. code-block:: typescript
      :linenos:

      function arg(s: string): int { console.log(s); return 1; }

      arg("condition True") ? arg("left 1") :  arg("right 1")
      arg("condition False")*0 ? arg("left 2") :  arg("right 2")
      // Prints:
    ...
      //    right 2

-  Operands of :ref:`Conditional-And Expression` and
   :ref:`Conditional-Or Expression` are evaluated from
   left to right. Depending on the value of the left-hand-side
   operands, the evaluation of the rightmost operand can
   be skipped:

   .. code-block:: typescript
      :linenos:

      function arg(s: string): int { console.log(s); return 1; }

      // Conditional And
      arg("left And (true)") && arg("right And")
      console.log("---")
    ...
      //    right Or

-  Assignment operator behavior requires additional
   clarification because the operator is right-associative.
   An expression containing two assignments is
   represented in the following example:

   .. code-block:: typescript
      :linenos:

      class A {
         constructor(s:string) { console.log(s); this.tag = s; }
         tag: string
      }
      function f(s: string) { return new A(s); }
    ...
      //    right

   The following evaluation steps are performed in the example above:

   -  All three subexpressions (left-hand-side, middle, and
      right-hand-side) are evaluated from left to right. The
      evaluation of left-hand-side and middle subexpressions
      results in *lhsExpression*.

   -  After that, two assignments are performed
      from right to left due to right associativity of
      the assignment operator. The value of the
      right-hand-side subexpression is assigned
      to the middle *lhsExpression*, and then the
      result of the middle expression is assigned
      to the left *lhsExpression*.

-  The ArkTS programming language follows the order of evaluation as indicated
   explicitly by parentheses, and implicitly by the precedence of operators.
   This rule particularly applies for infinity and ``NaN`` values of
   floating-point calculations.
   ArkTS considers integer addition and multiplication as provably associative.
   However, floating-point calculations must not be naively reordered because
   they are unlikely to be computationally associative (even though they appear
   mathematically associative).

Evaluation of Arguments
=======================

.. meta:

An evaluation of arguments always progresses from left to right up to the first
error, or through the end of the expression; i.e., any argument expression is
evaluated after the evaluation of each argument expression to its left
completes normally (including comma-separated argument expressions that appear
within parentheses in method calls, constructor calls, class instance creation
expressions, or function call expressions).

If the left-hand argument expression completes abruptly, then no part of the
right-hand argument expression is evaluated.

.. code-block:: typescript
   :linenos:

   function arg(s: string): int { console.log(s); return 1; }
   function errArg(s: string, v: int): int { console.log(s); return 1/v }
   function test(a: int, b: int, c: int) {}

   test(arg("left"), arg("middle"), arg("right"))
   test(errArg("errArg (left)", 0), arg("middle"), arg("right"))
   // Prints:
   //    left
   //    middle
   //    right
   //    errArg (left)
   //    ... divideByZero runtime error reported

Evaluation of Other Expressions
===============================

.. meta:

These general rules cannot cover the order of evaluation of certain expressions
when they from time to time cause exceptional conditions. The order of
evaluation of the following expressions requires specific explanation:

-  Class instance creation expressions (see :ref:`New Expressions`);
-  :ref:`Resizable Array Creation Expressions`;
-  :ref:`Indexing Expressions`;
-  Method call expressions (see :ref:`Method Call Expression`);
-  Assignments involving indexing (see :ref:`Assignment`);
-  :ref:`Lambda Expressions`.

Literal
*******

.. meta:

*Literals* (see :ref:`Literals`) denote fixed and unchanging values. Type of
a literal is the type of an expression. For numeric literals, type of a literal
is inferred using :ref:`Type Inference for Constant Expressions`.

Named Reference
***************

.. meta:

An expression can have the form of a *named reference* as described by the
syntax rule as follows:

.. code-block:: abnf

    namedReference:
      qualifiedName typeArguments?
      ;

Type of a *named reference* expression is the type of the entity to which a
*named reference* refers.

*QualifiedName* (see :ref:`Names`) is an expression that consists of
dot-separated names. If *qualifiedName* consists of a single identifier, then
it is called a *simple name*.

*Simple name* refers to the following:

-  Entity declared in the current module, i.e.,

   - Variable name,
   - Constant name,
   - Function name,
   - Accessor name.

-  Variable, constant, or parameter declared in a surrounding block, function,
   method, or lambda body.

If not a *simple name*, *qualifiedName* refers to the following:

-  Entity imported from a module,
-  Entity exported from a namespace,
-  Member of some class or interface, or
-  Special syntax form of :ref:`Record Indexing Expression`.

If *typeArguments* are provided, then *qualifiedName* is a valid instantiation
of the generic method or function. Otherwise, a :index:`compile-time error`
occurs.

A :index:`compile-time error` also occurs if a name referred by *qualifiedName*
is undefined or inaccessible.

Type of a *named reference* is the type of an expression.

If a *named reference* refers to a function name, it is called :ref:`Function Reference`.
If a *named reference* refers to a method name, it is called :ref:`Method Reference`.

Function Reference
==================

A *function reference* refers to a declared or imported function.
Type of a *function reference* is derived from the function signature:

.. code-block:: typescript
   :linenos:

   function foo(n: number): string { return n.toString() }
   let func = foo // type of func is '(n: number) => string'
   let x = func(1)  // foo() called via reference

A *function reference* can refer to a generic function but only
if :ref:`Explicit Generic Instantiations` is present, otherwise
a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    function gen<T> (x: T) {}

    let a = gen<string> // OK
    let b = gen // Compile-time error, no explicit type arguments

A :index:`compile-time error` occurs if the name of an *overloaded function*
(see :ref:`Implicit Function Overloading`) or the name of an *explicit overload*
(see :ref:`Explicit Function Overload`) is used as a function reference:

.. code-block:: typescript
   :linenos:

    function bar(n: number) {}
    function bar(s: string) {}

    let b = bar // Compile-time error, overloaded function name

    function foo1(n: number) {}
    function foo2(s: string) {}
    overload foo { foo1, foo2 }

    foo(1)          // OK, overload call
    let x = foo     // Compile-time error, explicit overload name
    let y = foo2    // OK, ref to foo2

Method Reference
================

A *method reference* refers to a *static* or *instance* method
of a class or an interface.
Type of a *method reference* is derived from the method signature:

.. code-block:: typescript
   :linenos:

    class C {
      static foo(n: number) {}
      bar (s: string): boolean { return true }
    }

    // Method reference to a static method
    const m1 = C.foo  // type of 'm1' is (n: number) => void

    // Method reference to an instance method
    const m2 = new C().bar // type of 'm1' is (s: string) => boolean

If *method reference* refers to an instance method, that the named reference
is bounded with the used instance of that class or interface.

.. code-block:: typescript
   :linenos:

    class C {
        field = 123
        method(): number { return this.field }
    }
    let c1 = new C
    let c2 = new C
    let m1 = c1.method // 'c1' is bounded
    let m2 = c2.method // 'c2' is bounded
    c1.field = 42
    console.log (m1(), m2()) // Outputs: 42 123

A *method reference* can refer to a generic method only if a generic
instantiation is explicitly present (see :ref:`Explicit Generic Instantiations`).
Otherwise, a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    class C {
        gen<T> (x: T) {}
    }

    let a = new C().gen<string> // OK
    let b = new C().gen // Compile-time error, no explicit type arguments

A :index:`compile-time error` occurs if the name of an *overloaded method*
(see :ref:`Implicit Method Overloading`, :ref:`Explicit Class Method Overload`,
and :ref:`Explicit Class Method Overload`) is used as a method reference:

.. code-block:: typescript
   :linenos:

    class C {
        foo1(n: number) {}
        foo2(s: string) {}
        overload foo { foo1, foo2 }

        function bar(n: number) {}
        function bar(s: string) {}
    }

    let c = new C()
    let f = c.foo // Compile-time error
    let b = c.bar // Compile-time error

Array Literal
*************

.. meta:
    todo: let x : int = [1,2,3][1] - valid?
    todo: let x = ([1,2,3][1]) - should be a compile-time error but is not
    todo: implement it properly for invocation context to get type from the context, not from the first element

*Array literal* is an expression that can be used to create an array or tuple
in some cases, with all element values explicitly defined.

The syntax of *array literal* is presented below:

.. code-block:: abnf

    arrayLiteral:
        '[' expressionSequence? ']'
        ;

    expressionSequence:
        expression (',' expression)* ','?
        ;

An *array literal* is a comma-separated list of *initializer expressions*
enclosed in square brackets ``'['`` and ``']'``. A trailing comma after the last
expression in an array literal is ignored:

.. code-block:: typescript
   :linenos:

    let x = [1, 2, 3] // OK
    let y = [1, 2, 3,] // OK, trailing comma is ignored

The number of initializer expressions enclosed in square brackets of the array
initializer determines the length of the array to be constructed.

If memory is allocated as required for an array literal, then an array of the
specified length is created, and all elements of the array are initialized to
the values specified by initializer expressions.

On the contrary, the evaluation of an *array literal* expression completes
abruptly if:

-  Not enough memory is available for a new array, and ``OutOfMemoryError`` is
   thrown; or
-  Some initialization expression completes abruptly.

Initializer expressions are executed from left to right. The *n*'th expression
specifies the value of the *n-1*'th element of the array.

Array literals can be nested (i.e., the initializer expression that specifies
an array element can be an array literal if that element is of array type).

Type of an *array literal expression* is inferred by the following rules:

-  If a context is available, then type is inferred from the context. If
   successful, then type of an array literal is the inferred type. Otherwise,
   a :index:`compile-time error` occurs.
-  If no context is available, then type is inferred from the types of array
   literal elements (see :ref:`Array Type Inference from Types of Elements`).

More details of both cases are presented below.

Array Literal Type Inference from Context
=========================================

.. meta:

Type of an array literal can be inferred from the *context* that can be
specified as one of the following:

- Explicit type annotation of a variable declaration;
- Left-hand part type of an assignment;
- Explicit return type of a function, a method, or a lambda in a return statement;
- Parameter type in a call;
- Target type of a cast expression; or
- Type of an array element or a class field.

Possible variants are represented in the following example:

.. code-block:: typescript
   :linenos:

    let a: number[] = [1, 2, 3] // OK, variable type in a declaration is used
    a = [4, 5] // OK, variable type is used

    let b = [1, 2, 3] as number[]    // OK, cast target type is used

    function min(x: number[]): number {
      let m = x[0]
      for (let v of x) {
        if (v < m) m = v
      }
      return m
    }
    min([1., 3.14, 0.99]); // OK, parameter type is used

    // Array of array initialization
    type Matrix = number[][]
    let m: Matrix = [
        [1, 2], [3, 4] // OK, element type is used
    ]

    class aClass {}
    //
    let b1: Array <aClass> = [new aClass, new aClass]
    let b2: Array <number> = [1, 2, 3]
    let b3: FixedArray<number> = [1, 2]
      /* Type of literal is inferred from the context
         taken from b1, b2 and b3 declarations */

A :index:`compile-time error` occurs if the type specified by context
is **not** one of the following:

- ``Any``;
- ``Object``;
- Tuple type;
- Fixed-size array type;
- Value array type;
- Resizable array type;
- Superinterface of a resizable array type;
- Union type that contains at least one constituent type from the above list.

If type used in a context is ``Any`` or ``Object``, then
:ref:`Array Type Inference from Types of Elements` is used:

.. code-block:: typescript
   :linenos:

    let a: Object = [1, 2, 3] // OK, array literal is of int[] type

If type used in a context is a *tuple type* (see :ref:`Tuple Types`),
then it is inferred as an array literal type on the following conditions:

- Number of expressions equals the number of constituent types;
- Type of each expression in the array literal is assignable (see
  :ref:`Assignability`) to the constituent type at the respective position.

Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    let tuple: [number, string] = [1, "hello"] // OK
    let incorrect: [number, string] = ["hello", 1] // Compile-time error

If type used in a context is a *fixed-size array type* (see
:ref:`Fixed-size Array Types`), and type of each expression is
assignable to an array element type, then an array literal is of
the specified type. Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    let a: FixedArray<string> = ["hello", "world"] // OK
    let b: FixedArray<string> = [1, 2]             // Compile-time error
    let c: FixedArray<Object> = [1, "hello"]       // OK

If type used in a context is a *value array type* (see
:ref:`Value Array Types`), and type of each expression is
assignable to an array element type, then an array literal is of
the specified type. Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    let a: ValueArray<int> = [1, 2]    // OK
    let b: ValueArray<double> = [1, 2] // OK
    let b: ValueArray<int> = [3.14]    // Compile-time error

If type used in a context is a *resizable array type* (see
:ref:`Resizable Array Types` and including :ref:`Readonly Array Types`),
and type of each expression is assignable to an array element type,
then an array literal is of the specified type.
Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    let a: Array<string> = ["aa", "bb"]     // OK
    let b: string[] = ["aa", "bb"]          // OK
    let c: readonly string[] = ["aa", "bb"] // OK

    let d: string[] = ["aa", 2]             // Compile-time error

    let o: Object[] = ["aa", 2]             // OK

If type used in a context is an interface ``I``, and:

- If ``I`` is a generic superinterface of a resizable array type with
  the single type parameter ``I<T>``, then an array literal is considered
  as an instance of ``Array<T>``. If each expression is assignable
  to ``T``, then the array literal is of ``I<T>``. Otherwise, a
  :index:`compile-time error` occurs;

- If ``I`` is a non-generic superinterface of a resizable array type,
  then an array literal type is evaluated by using
  :ref:`Array Type Inference from Types of Elements`, and
  then inferred as ``I``;

- Otherwise, a :index:`compile-time error` occurs.

This situation is represented in the following example:

.. code-block:: typescript
   :linenos:

    interface SomeI {}
    let a = [1, 2] as SomeI // Compile-time error, SomeI is not a superinterface of Array

    let b: ConcatArray<number> = [1, 2]  // OK, instance of Array<number>
    let c: ConcatArray<string> = [1, 2]  // Compile-time error, int is not assignable to string
    let d: ArrayLike<Object> = [1, "aa"] // OK, instance of Array<Object>

If a type used in a context is a *union type* (see :ref:`Union Types`),
then the step :ref:`Array Literal Type Inference from Context` is taken
repetitively trying to use each type of the *union type* as the context.
If only a single type is inferred, then this single type is used as the
type of the literal. Otherwise, a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

   let union_1: string[] | [int, int] = [1, 2]
   // OK, literal type is a tuple [int, int]

   let union_2: number[] | [number, number] = [1, 2]
   // Error, as both union types accept literal [1, 2] as valid values

   let union_3: (number | string )[] | [(number | string), number] = ["xxx", 2]
   // Error, as both union types accept literal ["xxx", 2] as valid values

   let union_4: (number | string )[] | [(number | string), number] | string = "xxx"
   // OK, as only type string matches the type of "xxx" literal

   let union_5: (number | string )[] | [(number | string), number, boolean] | string = [5, 5]
    // OK, literal type is an array (number | string )[]

Array Type Inference from Types of Elements
===========================================

.. meta:

Where no context is set, and thus the type of an array literal cannot be
inferred from the context (see :ref:`Type of Expression`), the type of array
literal ``[`` ``expr``:sub:`1`, ``...`` , ``expr``:sub:`N` ``]`` is inferred
from the initialization expression instead by using the following algorithm:

.. #. If there is no expression (*N == 0*), then type is ``Object[]``.

#. If array literal (*N == 0*) includes no element, then the type of
   the array literal cannot be inferred, and a :index:`compile-time error`
   occurs.

#. If at least one element of an expression type cannot be determined, then
   the type of the array literal cannot be inferred, and a
   :index:`compile-time error` occurs.

#. If all initialization expressions are of the same type ``T``,
   then the array literal type is ``T[]``.

#. If each initialization expression is of a numeric type (see
   :ref:`Numeric Types`), then the array literal type is ``number[]``.

#. Otherwise, the array literal type is constructed as the array of a union
   type:
   ``(T``:sub:`1` ``| ... | T``:sub:`N` ``)[]``,
   where ``T``:sub:`i` is the type of *expr*:sub:`i`, and then:

    - If ``T``:sub:`i` is a literal type, then it is replaced for its
      supertype;

    - If ``T``:sub:`i` is a union type comprised of literal types, then each
      constituent literal type is replaced for its supertype.

    - :ref:`Union Types Normalization` is applied to the resultant union type
      after the above replacements.

.. code-block:: typescript
   :linenos:

    type A = number
    let u : "A" | "B" = "A"

    let a = []                        // Compile-time error, type cannot be inferred
    let b = ["a"]                     // type is string[]
    let c = [1, 2, 3]                 // type is int[]
    let d = [1, 2.1, 3]               // type is number[]
    let e = ["a" + "b", 1, 3.14]      // type is (string | number)[]
    let f = [u]                       // type is string[]
    let g = [(): void => {}, new A()] // type is (() => void | A)[]

Object Literal
***************

.. meta:

*Object literal* is an expression that can be used to create a class instance
with methods and fields with initial values. In some cases it is more
convenient to use an *object literal* in place of a class instance creation
expression (see :ref:`New Expressions`).

The syntax of *object literal* is presented below:

.. code-block:: abnf

    objectLiteral:
       '{' objectLiteralMembers? '}'
       ;

    objectLiteralMembers:
    ...

An *object literal* is written as a comma-separated list of
*object literal members* enclosed in curly braces ``'{'`` and ``'}'``. A
trailing comma after the last member is ignored. Each *object literal member*
can be either an *object literal field* or an *object literal method* in case
when an *object literal* is of interface type.

More details are here :ref:`Object Literal of Class Type` and
:ref:`Object Literal of Interface Type`:

An *object literal field* consists of an identifier and an expression as follows:

.. code-block:: typescript
   :linenos:

    class Person {
      name: string = ""
      age: number = 0
    }
    let b: Person = {name: "Bob", age: 25}
    let a: Person = {name: "Alice", age: 18, } // OK, trailing comma is ignored
    let c: Person | number = {name: "Mary", age: 17} // Literal is of type Person

An *object literal method* is a complete declaration of a public method.
Examples of object literals with methods are provided in
:ref:`Object Literal of Interface Type`.

Type of an *object literal expression* is always some class ``C`` that is
inferred from the context. A type inferred from the context can be either a
class (see :ref:`Object Literal of Class Type`), or an anonymous class created
for the inferred interface type (see :ref:`Object Literal of Interface Type`).

A :index:`compile-time error` occurs if:

-  Type of an *object literal* cannot be inferred from the context (see
   :ref:`Type of Expression` for an example);
-  Inferred type is not a class or interface type;
-  Context is a union type, and an object literal can be treated
   as a valid value of several union component types;
-  New member in an *object literal* is declared;

.. code-block:: typescript
   :linenos:

    let p = {name: "Bob", age: 25}
            // Compile-time error, type cannot be inferred

    class A { field = 1 }
    class B { field = 2 }

    let q: A | B = {field: 6}
            // Compile-time error, type cannot be inferred as the literal
            // fits both A and B

    let u: A = { field: 1, otherField: 2 }
            // Compile-time error, cannot declare a new member in the literal

Object Literal of Class Type
=============================

.. meta:

If class type ``C`` is inferred from the context, then type of an object
literal is ``C``:

.. code-block:: typescript
   :linenos:

    class Person {
      name: string = ""
      age: number = 0
    }
    function foo(p: Person) { /*some code*/ }
    // ...
    let p: Person = {name: "Bob", age: 25} /* OK, variable type is
         used */
    foo({name: "Alice", age: 18}) // OK, parameter type is used

An identifier in each *object literal field* must name a field of class ``C``.

A :index:`compile-time error` occurs if the identifier does not name an
*accessible member field* (see :ref:`Accessible`) in type ``C``:

.. code-block:: typescript
   :linenos:

    class Friend {
      name: string = ""
      protected soname: string = ""
      private nick: string = ""
      age: number
      sex?: "male"|"female"
    }
    // Compile-time error, nick is private:
    let f: Friend = {name: "Alexander", age: 55, nick: "Alex"}
    // Compile-time error, soname is protected:
    let g: Friend = {name: "Alexander", age: 55, soname: "Reed"}

A :index:`compile-time error` occurs if type of an expression in an
*object literal field* is not assignable (see :ref:`Assignability`) to the
field type:

.. code-block:: typescript
   :linenos:

    let f: Friend = {name: 123} /* compile-time error, type of right hand-side
    is not assignable to the type of the left hand-side */

Only class fields that have default values (see :ref:`Default Values for Types`)
or explicit initializers (see :ref:`Variable and Constant Declarations`) can be
skipped in an object literal. Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    let f: Friend = {} /* OK, as name, nick, age, and sex have either default
                          value or explicit initializer */

    class C {
        f1: number
        f2: string
        f3!: Object
    }
    let c1: C = {f2: "xyz", f3: new Object} // OK, f1 type has a default value
    let c2: C = {f2: "xyz"} // Compile-time error, f3 value is not provided

If type of an object literal is class ``C``, then class ``C`` must have an
explicit or default *parameterless* constructor, or a constructor with all
parameters of the second form of optional parameters (see
:ref:`Optional Parameters`) that is *accessible* (see :ref:`Accessible`) in the
class-composite context. Otherwise, a :index:`compile-time error` occurs.

These situations are presented in the examples below:

.. code-block:: typescript
   :linenos:

    class C {
      constructor (p: number) {}
    }
    // ...
    let c: C = {} /* compile-time error, no parameterless
           constructor */

.. code-block:: typescript
   :linenos:

    class C {
      private constructor () {}
    }
    // ...
    let c: C = {} /* compile-time error, constructor is not
        accessible */

.. code-block:: typescript
   :linenos:

    class C {
      constructor (p?: number) {}
    }
    // ...
    let c: C = {} // OK as constructor of has an optional parameter

.. code-block:: typescript
   :linenos:

    class C {
    }
    // ...
    let c: C = {} // OK as default constructor is added

A compile-time error occurs if an *object literal of class type* explicitly sets
readonly fields of a class:

.. code-block:: typescript

    class C {
        field1 = 123
        readonly field2: number
        readonly field3: string
        constructor () {
            this.field3 = ""
        }
    ...
    let d: C = { field1: 654, field2: 3, field3: "text" }

If a class has accessor (see :ref:`Class Accessor Declarations`) in a form of
setter then its name can be used as a part of an object literal.
Otherwise, a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    class OK {
        set attr (attr: number) {}
    }
    const a: OK = {attr: 42} // OK, as the setter be called

    class Err {
        get attr (): number { return 42 }
    }
    const b: Err = {attr: 42} // Compile-time error, no setter for 'attr'

Object Literal of Interface Type
================================

.. meta:

If an interface type ``I`` is inferred from the context, then type of an
object literal is an anonymous class implicitly created for interface ``I``:

.. code-block:: typescript
   :linenos:

    interface Person {
      name: string
      set surname(s: string)
      get age(): number
    }
    let b: Person = {name: "Bob", surname: "Doe", age: 25}

In the example above, type of ``b`` is an anonymous class that contains the
same fields as properties of interface ``I``. An anonymous class created
for the example above has the following fields:

    - ``name: string``
    - ``surname: string``
    - ``age: number``

If a property is defined as a getter, then the type of a field is the
return type of the getter. If a property is defined as a setter,
then the type of a field is the type of the parameter.
If a property is defined as both a getter and a setter, then the parameter type
of the setter and the return type of the getter must be the same. Otherwise, a
:index:`compile-time error` occurs as described in
:ref:`Implementing Required Interface Properties`.

Any properties that are optional can be skipped in an object literal.
The values of such optional properties are set to ``undefined`` as follows:

.. code-block:: typescript
   :linenos:

    interface Person {
      name: string
      age: number
      sex?: "male"|"female"
    }
    let b: Person = {name: "Bob", age: 25}
         // 'sex' field has the value 'undefined'

Properties that are non-optional cannot be skipped in an object literal,
despite some property types having default values (see
:ref:`Default Values for Types`). If a non-optional property (e.g., *age* in
the example above) is skipped, then a :index:`compile-time error` occurs.

An object literal of interface type must provide an implementation for all
interface methods with no default implementation. All such methods are
public as in the interface.

.. code-block:: typescript
   :linenos:

    interface I {
      print_name (name: string): void
      print_something() { console.log ("Something") }
    }
    let i: I = {
      print_name (name: string) { console.log(name) }
      // No need to implement print_something()
    }
    i.print_name ("Alice")
    i.print_something()

Any reference to ``this`` in an object literal method is a reference to
an anonymous class (which is a subtype of the interface) created for the
inferred interface type:

*Object literal* can provide a method with an override-compatible signature
(see :ref:`Override-Compatible Signatures`):

.. code-block:: typescript
   :linenos:

    class Base {}
    class Drv1 extends Base {}
    class Drv2 extends Base {}

    interface A {
        foo (p: Drv1): Base
        foo (p: Drv2): Base
    }
    const a1: A = { foo(p: Base): Drv1 {} }
       /* OK, foo(p: Base) implements both foo (p: Drv1): base and foo (p: Drv2): Base */

    const a2: A = { // OK
       foo(p: Drv1): Drv1 { return new Drv1 } // implements foo (p: Drv1): Base
       foo(p: Drv2): Drv2 { return new Drv2 } // implements foo (p: Drv2): Base
    }

.. code-block:: typescript
   :linenos:

    interface I { method(i: I): I }
    const i: I = { method(i: I): I { return this } }

A :index:`compile-time error` occurs if an object literal of interface type
introduces a new method:

.. code-block:: typescript
   :linenos:

    interface I {}
    const i: I = { foo(): void {} } // Compile-time error

If an interface has a method implementation, then its object literal can
optionally  provide a new method implementation. Otherwise, the interface
implementation is used:

.. code-block:: typescript
   :linenos:

   interface I {
      method(): void { console.log ("method() from I is called") }
   }

   // Valid literal of anonymous class type using interface method
   const i1: I = {}
   i1.method()

   // Valid literal of anonymous class type using own method declaration
   const i2: I = {
      method(): void { console.log ("method() from object literal is called") }
   }

An interface property is set within an object literal by a value. It is
independent of the form it is defined in (see :ref:`Interface Properties`).
The definition within the interface determines how the the property is used:

.. code-block:: typescript
   :linenos:

    interface I1 {
        set attr (attr: number)
    }
    const i1: I1 = {attr: 42} // OK, 'attr' is writable property
    console.log (i1.attr) // Compile-time error as attr has no getter

    interface I2 {
        get attr (): number
    }
    const i2: I2 = {attr: 42} /* OK, 'attr' is in fact a getter which always returns 42 */
    i2.attr = 666 // Compile-time error as attr is readonly
    console.log (i2.attr) // OK, output is 42

    interface I3 {
        readonly attr: number
    }
    const i3: I3 = {attr: 42} /* OK, same as above */
    i3.attr = 666 // Compile-time error as attr is readonly
    console.log (i3.attr) // OK, output is 42

    interface I4 {
        attr: number
    }
    const i4: I4 = {attr: 42} /* OK, getter and setter work with object literal field */
    i4.attr = 666 // OK
    console.log (i4.attr) // OK

Object Literal of ``Record`` Type
=================================

.. meta:

Generic type ``Record<Key, Value>`` (see :ref:`Record Utility Type`) is used
to map properties of a type (type ``Key``) to another type (type ``Value``).
A special form of object literal is used to initialize the value of such
type:

The syntax of *record literal* is presented below:

.. code-block:: abnf

    recordLiteral:
       '{' keyValueSequence? '}'
       ;

    keyValueSequence:
    ...

The first expression in ``keyValue`` denotes a key and must be of type ``Key``.
The second expression denotes a value and must be of type ``Value``:

.. code-block:: typescript

    let map: Record<string, number> = {
        "John": 25,
        "Mary": 21,
    }

    console.log(map["John"]) // prints 25

.. code-block:: typescript

    interface PersonInfo {
        age: number
        salary: number
    }
    let map: Record<string, PersonInfo> = {
        "John": { age: 25, salary: 10},
        "Mary": { age: 21, salary: 20}
    }

If a key is a union of literal types, then all variants
must be listed in the object literal. Otherwise, a :index:`compile-time error`
occurs:

.. code-block:: typescript

    let map: Record<"aa" | "bb", number> = {
        "aa": 1,
    } // Compile-time error, "bb" key is missing

Object Literal Evaluation
=========================

.. meta:

The evaluation of an object literal of type ``C`` (where ``C`` is either
a named class type or an anonymous class type created for the interface)
is to be performed by the following steps:

-  Call to class ``C`` constructor with no arguments is executed to initialize
   an instance ``x`` of class ``C``. The evaluation of the object literal
   completes abruptly if so does the execution of the constructor.

-  All *object literal fields* are then processed from left to right in the
   textual order they occur in the source code. The following steps are
   performed for every *object literal field*:

   -  Evaluation of the expression; and
   -  If successful, then an assignment of the expression value to the
      corresponding field of ``x`` as its initial value. Otherwise, the
      evaluation of the object literal completes abruptly.

The execution of an object literal completes abruptly if so does
the execution of at least one of *object literal field* expression.

The evaluation of an object literal completes normally if:

- Class instance was created successfully;
- Class constructor was executed successfully;
- All class instance fields mentioned in the object literal have initial
  values resulting from the successful execution of all *object literal field*
  expressions.

Spread Expression
*****************

.. meta:

*Spread expression* can be used only within an array literal (see
:ref:`Array Literal`) or argument passing (see :ref:`Rest Parameter`).
The *expression* must be of an iterable type (see :ref:`Iterable Types`)
or of a tuple type (see :ref:`Tuple Types`).

Otherwise, a :index:`compile-time error` occurs.

The syntax of *spread expression* is presented below:

.. code-block:: abnf

    spreadExpression:
        '...' expression
        ;

A *spread expression* is evaluated:

-  At compile time by the compiler if *expression* is constant (see
   :ref:`Constant Expressions`);
-  Otherwise, at runtime.

Any iterable or tuple object referred by the *expression* is broken down
into a sequence of values by the evaluation. This sequence is used where
a *spread expression* is used. It can be an assignment, a call of a function,
method, or constructor. A sequence of types of these values is the type of the
*spread expression*.

*Spread expression* is one of the two ArkTS concepts that use the ``spread``
operator ``'...'`` as a prefix. The difference between *spread expressions* and
syntactically similar *rest parameters* is as follows:

- *Spread expression* **generates** a sequence of values. E.g., a sequence can
  be generated from a type with an iterator.
- *Rest parameter* **receives** a sequence of values and stores the values in
  an array or a tuple. A *rest parameter* knows nothing about the origin of the
  values, i.e., the sequence can be a product of a spread operator, or the
  values can be a result of a direct input.

It is represented in the following example:

.. code-block:: typescript
   :linenos:

   function f(...a: number[]) {} // Rest, put caller values into an array

   f(1,2)    // Thanks to Rest, we can put some values directly ...
   let arglist: number[] = [1, 2, 3]
   f(...arglist)  // or  say that all values from 'arglist' must be substituted

*Spread expression* of array type supports both :ref:`Resizable array types`
and :ref:`Fixed-size array types`. Any combination of *spread expressions*
with fixed-size and resizable arrays can be used in an array literal or in
a function call as illustrated in the following example:

.. code-block:: typescript
   :linenos:

   let array1: int[] = [1, 2, 3]
   let array2: FixedArray<int> = [4, 5]

   // A literal contains two spread expressions with arrays of variable and fixed size
   let array3: int[] = [...array1, ...array2] // spread array1 and array2 elements
                                        // while building new array literal at compile time
   console.log(array3) // prints [1, 2, 3, 4, 5]

   function foo (...array: int[]) {
      console.log (array)
   }

   // The next two calls are equivalent
   foo(...array2)
   foo (...[...array2])  // spread array2 elements into arguments of the foo() call

   // recall,  'array3 = [ ..array1, ..array2])' (see above)
   // next two calls are also equivalent
   foo(...array3)
   foo(...[...array1, ...array2])

   function run_time_spread_application1 (a1: int[], a2: FixedArray<int>) {
      console.log ([...a1, 42, ...a2])
      // Array literal is built at runtime
   }
   run_time_spread_application1 (array1, array2) // prints [1, 2, 3, 42, 4, 5]

*Spread expression* always copies values from original arrays. A callee
changes elements of its own copy, but not elements of arrays used in the call:

.. code-block:: typescript
   :linenos:

   let a: int[] = [1, 2, 3]

   function foo (...p: int[]) {
      p[1] = 4
      console.log ("inside foo()", p)
   }
   foo(...a)  // prints 'inside foo() 1,4,3'
   console.log ("outside foo()", a) // prints 'outside foo() 1,2,3'

Since a *spread expression* copies values, the attribute ``readonly`` of the
source array (see :ref:`Readonly Array Types`) does not affect an array created
by the *spread expression*. If a *spread expression* is to create a readonly
target array, then the attribute ``readonly`` must be used for the target array
or for the *rest parameter*:

.. code-block:: typescript
   :linenos:

   let a: readonly int[] = [1, 2, 3]
   let b: int[] = [1, 2, 3]

   // 'readonly' array in spread expr, can modify target array Elements
   let rw: int[] = [...a]
   rw[1] = 1 // OK
   function foo(...p_rw: int[]) {
      p_rw[1] = 1 // OK
   }

   // RW array in spread, readonly target
   let ro: readonly int[] = [...b]
      ro[1] = 1 // Compile-time error
   function foo(...p_ro: readonly int[]) {
      p_ro[1] = 1 // Compile-time error
   }

If a *spread expression* is used to pass arguments (see :ref:`Rest Parameter`),
then the sequence of spread expressions passed as sequential arguments yields
a single sequence of values.

.. code-block:: typescript
   :linenos:

   function accept_spreads_with_rest_parameter (...args: number[]) {
       console.log (args)
   }
   let arr = [1, 2, 3]
   accept_spreads_with_rest_parameter (...arr, ...arr)
      // Output: 1 2 3 1 2 3

   function g1() { return [1, 2] }
   function g2() { return [3, 4, 5] }
   accept_spreads_with_rest_parameter (...g1(), ...g2())
      // Output: 1 2 3 4 5

A spread expression for tuples is represented in the example below:

.. code-block:: typescript
   :linenos:

    let tuple1: [number, string, boolean] = [1, "2", true]
    let tuple2: [number, string] = [4, "5"]
     // spread tuple1 and tuple2 elements
    let tuple3: [number, string, boolean, number, string] = [...tuple1, ...tuple2]
       // while building new tuple object at compile time
    console.log(tuple3) // prints [1, 2, true, 4, 5]

    function bar (...tuple: [number, string]) {
      console.log (tuple)
    }
    bar (...tuple2)  // spread tuple2 elements into arguments of the foo() call

    function run_time_spread_application2 (a1: [number, string, boolean], a2: [number, string]) {
      console.log ([...a1, 42, ...a2])
        // Such an array literal is built at runtime
    }
    run_time_spread_application2 (tuple1, tuple2) // prints [1, 2, true, 42, 4, "5"]

A spread expression for a class that implements Iterable is represented in
the example below:

.. code-block:: typescript
   :linenos:

    class A<T> implements Iterable<T|undefined> { // variables of type A can be spread
        // To check code with TS, comment line with  `$_iterator()`
        // and uncomment one with `[Symbol.iterator]()`
        $_iterator(): Iterator<T|undefined>  {
        // [Symbol.iterator](): Iterator<T|undefined>  {
          return new MyIteratorResult<T|undefined>(this.data)
        }
        private data: T[]
        constructor (...data: T[]) { this.data = data }
    }
    class MyIteratorResult <T> implements Iterator<T|undefined> {
        private data: T[]
        private index: number = 0
        next(): IteratorResult<T|undefined> {
            if (this.index >= this.data.length) {
               return MyIteratorResult.end_of_sequence
            } else {
               this.current_element.value = this.data[this.index++]
               return this.current_element
            }
        }
        constructor (data: T[]) { this.data = data }
        private static end_of_sequence: IteratorResult<undefined> = {done: true, value: undefined}
        private current_element: IteratorResult<T|undefined> = {done: false, value: undefined}
    }
    function display<T> (...p: T[]) { console.log (p) }
    display (... new A<number> (1, 2, 3))        // Spread A with numbers
    display (... new A<string> ("aaa", "bbb"))   // Spread A with strings
    display (... new A<Object> (1, "aaa", true)) // Spread A with any objects
    display (... new A<undefined>)               // Spread A with no objects

    type UnionOfIterable = A<number> | new A<string>
    function show (...p: UnionOfIterable) { console.log (p) }
    show (... new A<number> (1, 2, 3))        // Spread A with numbers
    show (... new A<string> ("aaa", "bbb"))   // Spread A with strings

.. note::
   If an argument is spread at the call site, then an appropriate parameter
   must be of the rest kind (see :ref:`Rest Parameter`). A
   :index:`compile-time error` occurs if an argument is spread into a sequence
   of ordinary non-optional parameters as follows:

   .. code-block:: typescript
      :linenos:

       function foo1 (n1: number, n2: number) // non-rest parameters
          { ... }
       let an_array = [1, 2]
       foo1 (...an_array) // Compile-time error

    ...
       foo2 (...a_tuple) // Compile-time error

Parenthesized Expression
************************

.. meta:

The syntax of *parenthesized expression* is presented below:

.. code-block:: abnf

    parenthesizedExpression:
        '(' expression ')'
        ;

Type and value of a parenthesized expression are the same as those of
the contained expression.

``this`` Expression
*******************

.. meta:

The syntax of *this expression* is presented below:

.. code-block:: abnf

    thisExpression:
        'this'
        ;

The keyword ``this`` can be used as an expression in the body of an instance
method of a class (see :ref:`Method Body`) or an interface (see
:ref:`Default Interface Method Declarations`). A corresponding class or
interface type is the type of *this* expression. If a method is declared in an
object literal (see :ref:`Object Literal`), then the type of the object literal
is the type of ``this``. A class constructor body can also use ``this``, and
the exact semantics of such use are described in :ref:`Constructor Body`. 

The keyword ``this`` can also be used in the initializer of a class field (see
:ref:`Field Initialization`).

The keyword ``this`` can be used in a lambda expression only if it is allowed
in the context in which the lambda expression occurs. The type of ``this`` is
the type of a class or an interface in which it is declared, but not the type
of the surrounding object literal type, if any.

The keyword ``this`` in a *direct call* expression ``this(`` *arguments* ``)``
can only be used in an explicit constructor call statement (see
:ref:`Explicit Constructor Call`).

The keyword ``this`` can also be used in the body of a function with receiver
(see :ref:`Functions with Receiver`). The type of *this* expression is the
declared type of the parameter ``this`` in a function.

A :index:`compile-time error` occurs if the keyword ``this`` appears elsewhere.

The keyword ``this`` used as a primary expression denotes a value that is a
reference to the following:

-  Object for which the instance method is called; or
-  Object being constructed.

The parameter ``this`` in a lambda body and in the surrounding context denote
the same value.

The class of the actual object referred to at runtime can be ``T`` if ``T`` is
a class type, or a subclass of ``T`` (see :ref:`Subtyping`) .

The semantics of ``this`` in different contexts is represented in the example
below:

.. code-block:: typescript
   :linenos:

    interface anInterface {
        method() {
           this // type of 'this' is anInterface
        }
    }
    class aClass implements anInterface {
        method() {
           this // type of 'this' is aClass
        }
        field = (): void => {
           this // type of 'this' is aClass
        }
    }
    class AnotherClass {
        anotherMethod() {
            const obj: aClass = { // Object literal
              method () {
                  this // type of 'this' is aClass
              },
              field: (): void => {
                  this // type of 'this' is AnotherClass
              }
            }
        }
    }

Field Access Expression
***********************

.. meta:

*Field access expression* can access a class static field (see
:ref:`Accessing Static Fields`) or a field of an object to which an object
reference refers.
An object reference can have different forms as described in detail in
:ref:`Accessing Current Object Fields` and :ref:`Accessing SuperClass Accessors`.

The syntax of *field access expression* is presented below:

.. code-block:: abnf

    fieldAccessExpression:
        objectReference ('.' | '?.') identifier
        ;

A *field access expression* that contains ``'?.'`` (see :ref:`Chaining Operator`)
is called *safe field access* because it handles nullish object references
safely.

If object reference evaluation completes abruptly, then so does the entire
field access expression.

An object reference used to access a field must be a non-nullish reference
type ``T``. Otherwise, a :index:`compile-time error` occurs.

A field access expression is valid if the identifier refers to an accessible
member field (see :ref:`Accessible`) in type ``T``. Otherwise, a
:index:`compile-time error` occurs.

Type of a *field access expression* is the type of a member field.

If the identifier in a *field access expression* denotes the accessor defined
for a class or interface type, then either a getter or a setter is called
depending on the position of the *field access expression* (see
:ref:`Class Accessor Declarations`  and :ref:`Interface Properties` for
detail).

Accessing Static Fields
=======================

.. meta:

When accessing a static field, *objectReference* takes the form *typeReference*.

The result of a *field access expression* of a static field in a class is
one of the following:

-  ``variable`` if the field is not ``readonly``. The resultant value can
   be changed later.

-  ``value`` if the field is ``readonly``, except where *field access* occurs
   in an initializer block (see :ref:`Static Initialization`).

Accessing Current Object Fields
===============================

.. meta:

When accessing a current object field, *objectReference* takes the form
*primaryExpression*.

The process of runtime evaluation of a field access expression starts from the
evaluation of *primaryExpression*.

The result of this evaluation can be an instance field or an accessor of a
class, or a property of an interface. It is one of the following:

-  ``variable`` if the field is not ``readonly``. The resultant value can be
   changed later;

-  ``value`` if the field is ``readonly``, except where *field access* occurs
   in a constructor (see :ref:`Constructor Declaration`);

-  call to a proper getter if the *field access expression* is not assigned a
   new expression; or

-  call to a proper setter if the *field access expression* is in the
   left-hand-side of the assignment.

Only the *primaryExpression* type (not class type of an actual object
referred at runtime) is used to determine the field or property to be accessed.

Accessing SuperClass Accessors
===============================

.. meta:

The form ``super.identifier`` is valid to access a superclass accessor (see
:ref:`Class Accessor Declarations`).

A :index:`compile-time error` occurs if identifier in 'super.identifier'
denotes a field.

.. code-block:: typescript
   :linenos:

    class Base {
       get property(): number { return 1 }
       set property(p: number) { }
       field = 1234
    }
    class Derived extends Base {
       get property(): number { return super.property } // OK
       set property(p: number) { super.property = 42 }  // OK
       foo () {
          super.field = 42           // Compile-time error
          console.log (super.field)  // Compile-time error
       }
    }

Method Call Expression
**********************

.. meta:

A *method call expression* calls

- a static class method;
- an instance method of a class or an interface; or
- a function with receiver (see :ref:`Functions with Receiver`).

The syntax of *method call expression* is presented below:

.. code-block:: abnf

    methodCallExpression:
        objectReference ('.' | '?.') identifier typeArguments? callArguments
        ;

*Call arguments* are described in :ref:`Call Arguments`.

A method call with ``'?.'`` (see :ref:`Chaining Operator`) is called a
*safe method call* because it handles nullish values safely.

There are several steps that determine and check the entity to be called at
compile time (see :ref:`Step 1 Selection of Type to Use`,
:ref:`Step 2 Selection of Entity to Call`, and
:ref:`Step 3 Checking Modifiers`).

Step 1: Selection of Type to Use
================================

.. meta:

The *object reference* is used to determine the type in which to search for the
method. Three forms of *object reference* are possible:

.. table::
   :widths: 30, 70

   ============================== =================================================================
    Form of Object Reference        Type to Use
   ============================== =================================================================
   ``typeReference``               Type denoted by ``typeReference`` must refer to a class.
                                   Otherwise, a :index:`compile-time error` occurs.
   ``super``                       The superclass of the class that contains the method call.
   expression of type *T*          ``T`` if ``T`` is a class, interface, or union; ``T``'s
                                   constraint (:ref:`Type Parameter Constraint`) if ``T`` is a
                                   type parameter. Otherwise, a :index:`compile-time` error occurs.
   ============================== =================================================================

Step 2: Selection of Entity to Call
===================================

.. meta:
    todo: consider functions with receiver and warning

After the type to use is known (see :ref:`Step 1 Selection of Type to Use`),
the set of candidates to call is determined by the form of *object reference*,
*type to use* and the identifier:

.. table::
   :widths: 30, 70

   ================================= =================================================================
    Form of Object Reference           Set of Entities to Call
   ================================= =================================================================
   ``typeReference`` of type *T*      Static methods named ``identifier`` of class *T* .
   ``super``                          Instance methods named ``identifier`` of superclass of the class
                                      that contains the call.
   expression with *T* type to use    Instance methods named ``identifier`` of class or interface *T*
                                      and :ref:`Functions with Receiver` named ``identifier``
                                      with receiver type *T*.
                                      If *T* is a union type, common instance methods
                                      see :ref:`Access to Common Union Members`.
   ================================= =================================================================

A :index:`compile-time error` occurs set is empty, in other words,
no entity is available to call.

If a set contains more then one entity, then :ref:`Overload Resolution` is used
to select the method or function to call (see :ref:`Overload Set at Method Call`
for details).

:ref:`Dynamic resolution of method calls` is used during program execution to resolve
an actual method to be called in case of an instance method in accordance with the
method resolved in the step.

Step 3: Checking Modifiers
==========================

.. meta:

A single method to call is known at this step. A set of semantic checks for
each form of method call must be performed as follows:

-  ``typeReference.identifier``

   The method must be declared ``static``. Otherwise,
   a :index:`compile-time error` occurs.

-  ``expression.identifier``

   The method must not be declared ``static``. Otherwise,
   a :index:`compile-time error` occurs.

-  ``super.identifier``

   The method must not be declared ``abstract`` or ``static``. Otherwise,
   a :index:`compile-time error` occurs.

.. ESE26 ABSTRACT_CALL

Semantic check of a method call is performed in accordance with
:ref:`Compatibility of Call Arguments`.

Type of Method Call Expression
==============================

.. meta:

Type of a *method call expression* is the return type of the method.

.. code-block:: typescript
   :linenos:

    class A {
       static method() { console.log ("Static method() is called") }
       method()        { console.log ("Instance method() is called") }
    }

    let x = A.method()     // Compile-time error as void cannot be used as type annotation
    A.method ()            // OK
    let y = new A().method() // Compile-time error as void cannot be used as type annotation
    new A().method()         // OK

Function Call Expression
************************

.. meta:

*Function call expression* is used to call a function (see
:ref:`Function Declarations`), a variable of a function type
(:ref:`Function Types`), or a lambda expression (see :ref:`Lambda Expressions`).

The syntax of *function call expression* is presented below:

.. code-block:: abnf

    functionCallExpression:
        expression ('?.' | typeArguments)? callArguments
        ;

*Call arguments* are described in :ref:`Call Arguments`.

A :index:`compile-time error` occurs if the expression type is one of the
following:

-  Different than the function type;
-  Nullish type without ``'?.'`` (see :ref:`Chaining Operator`).

If the operator ``'?.'`` (see :ref:`Chaining Operator`) is present, and the
*expression* evaluates to a nullish value, then:

-  *Call arguments* are not evaluated;
-  Call is not performed; and
-  Result of *function call expression* is not produced as a consequence.

The function call is *safe* because it handles nullish values properly.

If the form of expression in the call is *qualifiedName*, and *qualifiedName*
refers to an *overloaded function* (see :ref:`Implicit Function Overloading`
and :ref:`Explicit Function Overload`), then :ref:`Overload Resolution`
is used to select the function to call.

A :index:`compile-time error` occurs if no function is available to call.

Semantic check for a call is performed in accordance with
:ref:`Compatibility of Call Arguments`.

Various forms of function calls are represented in the example below:

.. code-block:: typescript
   :linenos:

    function foo() { console.log ("Function foo() is called") }
    foo() // function call uses function name to call it

    call (foo)            // top-level function passed
    call ((): void => { console.log ("Lambda is called") }) // lambda is passed
    call (A.method)       // static method
    call ((new A).method) // instance method is passed

    class A {
       static method() { console.log ("Static method() is called") }
       method() { console.log ("Instance method() is called") }
    }

    function call (callee: () => void) {
       callee() // function call uses parameter name to call any functional object passed as an argument
    }

    ((): void => { console.log ("Lambda is called") }) () // function call uses lambda expression to call it

    let x = foo() // Compile-time error as void cannot be used as type annotation

Type of a *function call expression* is the return type of the function.

Call Arguments
==============

.. meta:

The syntax of a *call argument* is presented below:

.. code-block:: abnf

    callArguments:
        '(' argumentSequence? ')' trailingLambda?
        ;

    argumentSequence:
        expression (',' expression)* ','?
        ;

The ``callArguments`` grammar rule refers to the list of call arguments. Only
an argument that corresponds to a *rest parameter* can be a spread expression (see
:ref:`Spread Expression`).

*Trailing lambda call* is a special syntactic form of call arguments that
contains a *trailing lambda* (see :ref:`Trailing Lambdas` for details).

Indexing Expressions
********************

.. meta:

*Indexing expressions* are used to access elements of arrays (see
:ref:`Array Types`), strings (see :ref:`Type string`), and ``Record`` instances
(see :ref:`Record Utility Type`). Indexing expressions can also be applied to
instances of indexable types (see :ref:`Indexable Types`).

The syntax of *indexing expression* is presented below:

.. code-block:: abnf

    indexingExpression:
        expression ('?.')? '[' expression ']'
        ;

Any *indexing expression* has two subexpressions as follows:

-  *Object reference expression* before the left bracket; and
-  *Index expression* inside the brackets.

If the operator ``'?.'`` (see :ref:`Chaining Operator`) is present in an
indexing expression, then:

-  If an object reference expression is not of a nullish type, then the
   chaining operator has no effect.
-  Otherwise, object reference expression must be checked against a nullish
   value. If the value is ``undefined`` or ``null``,
   then the evaluation of the entire surrounding *primary expression* stops.
   The result of the entire primary expression is then ``undefined``.

If no ``'?.'`` is present in an indexing expression, then object reference
expression must be of array type or ``Record`` type. Otherwise, a
:index:`compile-time error` occurs.

Array Indexing Expression
=========================

.. meta:
    todo: implement floating point index support - #14001

*Index expression* for array indexing must be one of integer types, namely
``byte``, ``short``, or ``int``. Otherwise, a :index:`compile-time error`
occurs.

The conversion of ``byte`` and  ``short`` types (see
:ref:`Widening Numeric Conversions`) is performed on an *index expression* to
ensure that the resultant type is ``int``. Otherwise, a
:index:`compile-time error` occurs.

Other numeric types (``long``, ``float``, and ``double``/``number``) must be
converted explicitly by applying the methods defined in the classes of the
:ref:`Standard Library`.

.. code-block:: typescript
   :linenos:

    const a = ["Alice", "Bob", "Carol"]
    function demo (l: long, f: float, d: double, n: number) {
        console.log (
           a[l.toInt()], a[f.toInt()],
           a[d.toInt()], a[n.toInt()]
        ) // OK to access array using index expression conversion methods
    }

If the chaining operator ``'?.'`` (see :ref:`Chaining Operator`) is present,
and after its application the type of *object reference expression*
is an *array type*,
then it makes a valid *array reference expression*, and the type
of the array indexing expression is ``T``.

The result of an array indexing expression is a variable of type ``T`` (i.e., an
element of the array selected by the value of that *index expression*).

It is essential that, if type ``T`` is a reference type, then the fields of
array elements can be modified by changing the resultant variable fields:

.. code-block:: typescript
   :linenos:

    let names: string[] = ["Alice", "Bob", "Carol"]
    console.log(names[1]) // prints Bob
    names[1] = "Martin"
    console.log(names[1]) // prints Martin

    console.log (names["1"]) // Compile-time error as index of non-numeric type

    class RefType {
        field: number = 42
    }
    const objects: RefType[] = [new RefType(), new RefType()]
    const obj = objects [1]
    obj.field = 777            // change the field in the array element
    console.log(objects[0].field) // prints 42
    console.log(objects[1].field) // prints 777

    let an_array = [1, 2, 3]
    let element = an_array [3.5] // Compile-time error as index is not integer
    function foo (index: number) {
       let element = an_array [index] // Compile-time error as index is not integer
    }

An array indexing expression evaluated at runtime behaves as follows:

-  Object reference expression is evaluated first.
-  If the evaluation completes abruptly, then so does the indexing
   expression, and the index expression is not evaluated.
-  If the evaluation completes normally, then the index expression is evaluated.
   The resultant value of the object reference expression refers to an array.
-  If the index expression value of an array is less than zero, greater than
   or equal to that array's *length*, then ``RangeError`` is thrown.
-  Otherwise, the result of the array access is a type ``T`` variable within
   the array selected by the value of the index expression.

.. code-block:: typescript
   :linenos:

    function setElement(names: string[], i: int, name: string) {
        names[i] = name // runtime error, if 'i' is out of bounds
    }

String Indexing Expression
==========================

.. meta:
    todo: return type is string

*Index expression* for string indexing must be of one of integer types, namely
``byte``, ``short``, or ``int``. The same rules apply as in
:ref:`Array Indexing Expression`.

If the index expression value of a string is less than zero, greater than
or equal to that string's *length*, then ``RangeError`` is thrown.

.. code-block:: typescript
   :linenos:

    console.log("abc"[1]]) // prints: b
    console.log("abc"[3]]) // runtime exception

The result of a string indexing expression is a value of ``string`` type.

.. note::
   String value is immutable, and is not allowed to change a value of a string
   element by indexing.

   .. code-block:: typescript
      :linenos:

       let x = "abc"
       x[1] = "d" // Compile-time error, string value is immutable

Record Indexing Expression
==========================

.. meta:

*Indexing expression* for a type ``Record<Key, Value>`` (see
:ref:`Record Utility Type`) allows getting or setting a value of type ``Value``
at an index specified by the expression of type ``Key``.

The following two cases are to be considered separately:

1. Type ``Key`` is a union that contains literal types only;
2. Other cases.

**Case 1.** If type ``Key`` is a union that contains literal types only, then
an *index expression* can only be one of the literals listed in the type.
The result of the indexing expression is of type ``Value``.

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    type Keys = 'key1' | 'key2' | 'key3'

    let x: Record<Keys, number> = {
        'key1': 1,
        'key2': 2,
        'key3': 4,
    }
    let y = x['key2'] // y value is 2

A :index:`compile-time error` occurs if an index expression is not a valid
literal:

.. code-block:: typescript
   :linenos:

    console.log(x['key4']) // Compile-time error
    x['another key'] = 5 // Compile-time error

The compiler guarantees that an object of ``Record<Key, Value>`` for this type
``Key`` contains values for all ``Key`` keys.

**Case 2.** An *index expression* has no restriction.
The result of an indexing expression is of type ``Value | undefined``.

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    let x: Record<number, string> = {
        1: "hello",
        2: "buy",
    }

    function foo(n: number): string | undefined {
        return x[n]
    }

    function bar(n: number): string {
        let s = x[n]
        if (s == undefined) { return "no" }
        return s!
    }

    foo(3) // prints "undefined"
    bar(3) // prints "no"

    let y = x[3]

Type of *y* in the code above is ``string | undefined``. The value of
*y* is ``undefined``.

An indexing expression evaluated at runtime behaves as follows:

-  Object reference expression is evaluated first.
-  If the evaluation completes abruptly, then so does the indexing
   expression, and the index expression is not evaluated.
-  If the evaluation completes normally, then the index expression is
   evaluated.
   The resultant value of the object reference expression refers to a ``record``
   instance.
-  If the ``record`` instance contains a key defined by the index expression,
   then the result is the value mapped to the key.
-  Otherwise, the result is the literal ``undefined``.

Syntactically, the *record indexing expression* can be written by using a field
access notation (see :ref:`Field Access Expression`) if its *index expression*
is formed as an *identifier* of type *string*.

.. code-block:: typescript
   :linenos:

    type Keys = 'key1' | 'key2' | 'key3'

    let x: Record<Keys, number> = {
        'key1': 1,
        'key2': 2,
        'key3': 4,
    }
    console.log(x.key2) // the same as console.log(x['key2'])
    x.key2 = 8          // the same as x['key2'] = 8
    console.log(x.key2) // the same as console.log(x['key2'])

Chaining Operator
*****************

.. meta:

The *chaining operator* ``'?.'`` is used to effectively access values of
nullish types. It can be used in the following contexts:

- :ref:`Field Access Expression`,
- :ref:`Method Call Expression`,
- :ref:`Function Call Expression`,
- :ref:`Indexing Expressions`.

If the value of ``expr`` in ``expr?.`` is of a *nullish type*,
and is evaluated to ``undefined`` or ``null``,
then the evaluation of the entire surrounding *primary expression*
stops. The result of the entire primary expression evaluation is then
``undefined``. The entire primary expression is then of the union type
``undefined | T``, where ``T`` is a *non-nullish type* of the entire
primary expression:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    class Person {
        name: string
        spouse?: Person = undefined
        constructor(name: string) {
            this.name = name
        }
    }

    let bob = new Person("Bob")
    console.log(bob.spouse?.name) // prints "undefined"
       // type of bob.spouse?.name is undefined|string

    bob.spouse = new Person("Alice")
    console.log(bob.spouse?.name) // prints "Alice"
       // type of bob.spouse?.name is undefined|string

If the value of ``expr`` in ``expr?.`` is not of a *nullish type*,
then the chaining operator has no effect, and does not
influence the type of the entire primary expression:

.. code-block:: typescript
   :linenos:

    function foo(s1: string, s2: string | undefined) {
        let a = s1?.[0] // 's' is of non-nullish type, type of 'a' is string
        let b = s2?.[0] // type of 'b' is string | undefined
    }

The chaining operator is allowed in a method call expression for instance
methods only. Attempting to use it with a static method is syntactically correct
but causes a :index:`compile-time error`:

.. code-block:: typescript
   :linenos:

   class A {
      static f(): string {return "" }
      g(): string  { return "" }
   }

   let s: string|undefined

   s = A?.f()            // static method, compile-time error

   let b = new A
   s = b?.g()            // non-static method, OK

A :index:`compile-time error` occurs if a chaining operator is placed in the
context where a variable is expected, e.g., in the left-hand-side expression of
an assignment (see :ref:`Assignment`) or expression
(see :ref:`Postfix Increment`, :ref:`Postfix Decrement`,
:ref:`Prefix Increment`, or :ref:`Prefix Decrement`).

If an expression preceding a *chaining operator* is known at compile time to
always evaluate to a nullish value (``undefined`` or ``null``) or a non-nullish
value at runtime, then a :index:`compile-time warning` is issued:

.. code-block:: typescript
   :linenos:

    class C { f = 1}

    let c = new C()
    c?.f // warning, expression is always non-nullish

    let d: C | undefined = undefined
    d?.f // warning, expression is always evaluated as undefined

``New`` Expressions
*******************

.. meta:

There are two syntactical forms of the *new expression*:

.. code-block:: abnf

    newExpression:
        newClassInstance
        | newArrayInstance
        ;

Type of a *new expression* is ether ``class`` or ``array``.

A *new class instance expression* creates a new object that is an instance
of the specified class and it is described in full details below.

The creation of array instances is an experimental feature discussed in
:ref:`Resizable Array Creation Expressions`.

The syntax of *new class instance expression* is presented below:

.. code-block:: abnf

    newClassInstance:
        'new' typeReference typeArguments? arguments?
        ;

*Class instance creation expression* specifies a class to be instantiated.
It optionally lists all actual arguments for the constructor.

.. code-block:: typescript
   :linenos:

    class A {
       constructor(p: number) {}
    }

    new A(5) // create an instance and call constructor
    const a = new A(6) /* create an instance, call constructor and store
                          created and initialized instance in 'a' */

*Class instance creation expression* can throw an error
(see :ref:`Error Handling`, :ref:`Constructor Declaration`).

A *class instance creation expression* that refers to classes ``FixedArray``,
``Array``, or classes derived from ``Array``, instantiated with an array element
type of some class type, is a special form of *array creation expression*.

Attempting to create a *FixedArray* of elements of which the type is a type parameter
causes a :index:`compile-time error`.

.. code-block:: typescript
   :linenos:

    class A<T> {
       foo (element: T) {
          const a1 = new T[5] (element)  // OK, resizable array with 5 elements
                                         // is created
          const a2 = new FixedArray<T> (5, element) // compile-time error, fixed-size
                                         // array with 5 elements of type T cannot be
                                         // created
       }
    }

This situation is discussed in detail in :ref:`Fixed-Size Array Creation`
and :ref:`Resizable Array Creation Expressions`.

The execution of a class instance creation expression is performed as follows:

-  New instance of class is created;
-  Constructor of class is called to fully initialize the created
   instance.

The validity of the constructor call is similar to the validity of the method
call as discussed in :ref:`Step 2 Selection of Entity to Call`, except the cases
discussed in :ref:`Constructor Body`.

A :index:`compile-time error` occurs if ``typeReference`` is a type parameter.

.. note::
   If a *class instance creation expression* with no argument is used as object
   reference in a method call expression, then empty parentheses ``'( )'`` are
   to be used.

   .. code-block:: typescript
      :linenos:

       class A {  method() {} }

       new A.method()   // Compile-time error
       new A().method() // OK
       (new A).method() // OK
       let a = new A    // OK

``instanceof`` Expression
*************************

.. meta:

The syntax of *instanceof expression* is presented below:

.. code-block:: abnf

    instanceOfExpression:
        expression 'instanceof' type
        ;

Any ``instanceof`` expression in the form ``expr instanceof T`` is of type ``boolean``.

The result of an ``instanceof`` expression is ``true`` if the *actual type* of
evaluated ``expr`` is a subtype of ``T`` (see :ref:`Subtyping`). Otherwise,
the result is ``false``.

If type ``T`` is not *preserved up to undefined* by :ref:`Type Erasure`, then a
:index:`compile-time error` occurs.

*Generic type* (see :ref:`Generics`) in the form of *type name* (see
:ref:`Type References`) can be used as the operand ``T`` of an ``instanceof``
expression. In this case, the check is performed against the *erased* type
(see :ref:`Type Erasure`).

The approach is represented in the following example:

.. code-block:: typescript
   :linenos:

   class A<T> {}
   class B<T> extends A<T> {}

   function foo<T>(a: A<T>) {
      let c = a as B<T>   // OK
      let x = new B<string> // OK, explicit type parameter
      console.log(x instanceof B)        // OK
      console.log(x instanceof B<T>)     // Compile-time error, B<T> is not preserved up to undefined

      if(a instanceof B) {  // OK, type of instanceof is used for type
                            // checking in `if` clause
         let b = a as B<T>  // OK
      }
   }

   let a = new B<string>()
   foo(a)

If an *instanceof expression* is known at compile time
to always evaluate to ``false`` or ``true`` at runtime, then
a :index:`compile-time warning` is issued:

.. code-block:: typescript
   :linenos:

    class C {}
    class D extends C{}
    class E {}

    function foo(d: D) {
        console.log(d instanceof C) // warning, expression is always true
        console.log(d instanceof E) // warning, expression is always false
    }

The ``type`` of an ``instanceof`` expression is used for type checking if applicable.

``Cast`` Expression
*******************

.. meta:

The syntax of *cast expression* is as follows:

.. code-block:: abnf

    castExpression:
        expression 'as' type
        ;

*Cast expression* in the form ``expr as target`` applies the *cast operator*
``as`` to ``expr`` by issuing the value of a specified ``target`` type. Thus,
the type of a cast expression is always the ``target`` type.

.. code-block:: typescript
   :linenos:

    class X {}

    let x1 : X = new X()
    let ob : Object = x1 as Object // Object is the target type
    let x2 : X = ob as X // X is the target type

A :index:`compile-time error` occurs if the ``target`` type is type ``never``:

.. code-block:: typescript
   :linenos:

    1 as never // Compile-time error

If ``target`` type is not *preserved up to undefined* by :ref:`Type Erasure`,
then a :index:`compile-time warning` occurs.

.. code-block:: typescript
   :linenos:

    class X<out T> { }
    function foo(p1: X<Object>) {
        p1 as X<number> // Compile-time warning - such cast converison is type unsafe
    }

Two specific cases of a *cast expression* are described in the sections below:

- :ref:`Type Inference in Cast Expression` if ``expr`` is a numeric literal
  (see :ref:`Numeric Literals`), an :ref:`Array literal`, or an
  :ref:`Object Literal`;

- :ref:`Runtime Checking in Cast Expression` otherwise.

Type Inference in Cast Expression
=================================

.. meta:

The following combinations of ``expr`` and ``target`` are considered for the
``expr as target`` expression:

-  ``expr`` is a numeric literal, see :ref:`Type Inference for Constant Expressions`
   for detail;

-  ``expr`` is an :ref:`Array Literal`, and ``target`` is an *array type* or
   a *tuple type* (see :ref:`Array Literal Type Inference from Context` for
   detail);

-  ``expr`` is an :ref:`Object Literal`, and ``target`` is *class type*,
   *interface type*, or :ref:`Record Utility Type` (see the subsections of
   :ref:`Object Literal` for detail).

This kind of a *cast expression* results in inferring the target type for
``expr``. This expression never causes a :index:`runtime error`
by itself. However, the evaluation of array literal elements or
object literal properties can cause a :index:`runtime error`.

Casting for numeric literals is represented in the
example below:

.. code-block:: typescript
   :linenos:

   let x = 1 as byte // OK
   let y = 128 as byte // Compile-time error

Casting for array literals is represented in the example below:

.. code-block:: typescript
   :linenos:

   let a = [1, 2] as double[] // OK, [1.0, 2.0]
   let b = [1, 2] as double // Compile-time error, wrong target type
   let c = [1, "cc"] as double[] // Compile-time error, wrong element type
   let d = [1, "cc"] as [double, string] // OK, cast to the tuple type
   let e = [1.0, "cc"] as [int, string] // Compile-time error, wrong element type

.. note::
   *Assignability* check is applied to the elements of an array literal.

Examples with object literals are provided in :ref:`Object literal`.

Runtime Checking in Cast Expression
===================================

.. meta:

If :ref:`Type Inference in Cast Expression` cannot be applied, then
``expr as target`` checks if the type of ``expr`` is a subtype of
``target`` (see :ref:`Subtyping`).

If the *actual type* of ``expr`` is a subtype of ``target`` (see
:ref:`Subtyping`), then the result of an ``as`` expression is the result of
the evaluated ``expr``. Otherwise, ``ClassCastError`` is thrown.

If ``target`` type is not *preserved up to undefined* by :ref:`Type Erasure`,
then a check is performed against the *effective type* of the type. As the
*effective type* is less specific than ``target`` in the case described,
the usage of the resulting value can cause type violation, and ``ClassCastError``
is thrown as a consequence (see :ref:`Type Erasure` for detail).

Semantically, a *cast expression* of this kind is coupled tightly with
:ref:`instanceof Expression` as follows:

-  If the result of ``x instanceof T`` is ``true``, then ``x as T`` succeeds and
   causes no :index:`runtime error`;

-  If the result of ``x instanceof T`` is ``false``, then ``x as T`` causes
   ``ClassCastError`` thrown at runtime.

This situation is represented in the following example:

.. code-block:: typescript
   :linenos:

    function foo (x: Object) {
        x as string
    }

    foo("aa") // OK
    foo(1)    // runtime error is thrown in foo by 'as' operator application

:ref:`instanceof Expression` can be used to prevent a :index:`runtime error`.
Moreover, the :ref:`instanceof Expression` makes *cast conversion* unnecessary
in many cases:

.. code-block:: typescript
   :linenos:

    class Person {
        name: string
        constructor (name: string) { this.name = name }
    }

    function printName(x: Object) {
        if (x instanceof Person) {
            // no need to cast, access to 'name' is type-safe here
            console.log(x.name)
        } else {
            console.log("not a Person")
        }
    }

    printName(new Person("Bob")) // output: Bob
    printName(1)                 // output: not a Person

If the evaluation of a *cast expression* is known at compile time to
always succeed or throw ``ClassCastError`` at runtime, then
a :index:`compile-time warning` is issued:

.. code-block:: typescript
   :linenos:

    class C {}
    class D extends C {}
    class E extends C {}

    let a: C = new D()
    a as D // Compile-time warning, cast always succeeds
    a as E // Compile-time warning, cast always throws ClassCastError

``typeof`` Expression
*********************

.. meta:

The syntax of *typeof expression* is presented below:

.. code-block:: abnf

    typeOfExpression:
        'typeof' expression
        ;

Any ``typeof`` expression is of type ``string``.

If *typeof expression* refers to a name of an overloaded function or method,
then a :index:`compile-time error` occurs.

The evaluation of a *typeof expression* starts with the ``expression``
evaluation. If this evaluation causes an error, then the ``typeof`` expression
evaluation terminates abruptly. Otherwise, the value of a ``typeof expression``
is defined as follows:

1. The value of a ``typeof`` expression is known at compile time

+---------------------------------+-------------------------+-----------------------------+
|       Expression Type           |  typeof Result          |   Code Example              |
+=================================+=========================+=============================+
| ``string``                      | "string"                | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  let s: string = ...        |
|                                 |                         |  typeof s                   |
+---------------------------------+-------------------------+-----------------------------+
| ``boolean``                     | "boolean"               | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  let b: boolean = ...       |
|                                 |                         |  typeof b                   |
+---------------------------------+-------------------------+-----------------------------+
| ``bigint``                      | "bigint"                | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  let b: bigint = ...        |
|                                 |                         |  typeof b                   |
+---------------------------------+-------------------------+-----------------------------+
| any class or interface          | "object"                | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  let a: Object = ...        |
|                                 |                         |  typeof a                   |
+---------------------------------+-------------------------+-----------------------------+
| any function type               | "function"              | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  let f: () => void = ...    |
|                                 |                         |  typeof f                   |
+---------------------------------+-------------------------+-----------------------------+
| ``undefined``, ``void``         | "undefined"             | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  typeof undefined           |
|                                 |                         |  typeof void                |
+---------------------------------+-------------------------+-----------------------------+
| ``null``                        | "object"                | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  typeof null                |
+---------------------------------+-------------------------+-----------------------------+
| ``T|null``, when ``T`` is a     | "object"                | .. code-block:: typescript  |
| class (but not Object -         |                         |                             |
| see next table),                |                         |  class C {}                 |
| interface or array              |                         |  let x: C | null = ...      |
|                                 |                         |  typeof x                   |
+---------------------------------+-------------------------+-----------------------------+
| enumeration type                | name of enumeration     | .. code-block:: typescript  |
|                                 | base type               |                             |
|                                 |                         |  enum C {R, G, B}           |
|                                 |                         |  let c: C = ...             |
|                                 |                         |  typeof c // "int"          |
+---------------------------------+-------------------------+-----------------------------+
| ``number``, ``double``          | "number"                | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  let n: number = ...        |
|                                 |                         |  typeof n                   |
+---------------------------------+-------------------------+-----------------------------+
| Other numeric types:            | "byte", "short", "int", | .. code-block:: typescript  |
|                                 | "long" or "float",      |                             |
| ``byte``, ``short``, ``int``,   | depending on type of    |  let x: byte = ...          |
| ``long``, ``float``             | expression              |  typeof x // "byte"         |
+---------------------------------+-------------------------+-----------------------------+
| ``char``                        | "char"                  | .. code-block:: typescript  |
|                                 |                         |                             |
|                                 |                         |  let x: char = ...          |
|                                 |                         |  typeof x                   |
+---------------------------------+-------------------------+-----------------------------+

2. The value of a ``typeof`` expression is determined at runtime

The result is the name of an actual type used at runtime for the following
expression types:

+------------------------+-----------------------------+
|  Expression    Type    |   Code Example              |
+========================+=============================+
| Object                 | .. code-block:: typescript  |
|                        |                             |
|                        |  function f(o: Object) {    |
|                        |    typeof o                 |
|                        |  }                          |
+------------------------+-----------------------------+
| union type             | .. code-block:: typescript  |
|                        |                             |
|                        |  function f(p:A|B) {        |
|                        |    typeof p                 |
|                        |  }                          |
+------------------------+-----------------------------+
| type parameter         | .. code-block:: typescript  |
|                        |                             |
|                        |  class A<T|null|undefined> {|
|                        |     f: T                    |
|                        |     m() {                   |
|                        |        typeof this.f        |
|                        |     }                       |
|                        |     constructor(p:T) {      |
|                        |        this.f = p           |
|                        |     }                       |
|                        |  }                          |
+------------------------+-----------------------------+

Ensure-Not-Nullish Expression
*****************************

.. meta:

*Ensure-not-nullish expression* is a postfix expression with the operator
``'!'``. An *ensure-not-nullish expression* in the expression *e!* checks
whether *e* of a nullish type (see :ref:`Nullish Types`) evaluates to a
nullish value.

The syntax of *ensure-not-nullish expression* is presented below:

.. code-block:: abnf

    ensureNotNullishExpression:
        expression '!'
        ;

If the result of the evaluation of ``expr`` in ``expr!`` is not equal to
``null`` or ``undefined``, then the result of *ensure-not-nullish expression*
is the outcome of the evaluation of ``expr``, otherwise
``NullPointerError`` is thrown.

Type of ``expr!`` is the non-nullish variant of type of ``expr``.

.. note:
    If the expression ``expr`` is not of a nullish type, then the operator ``'!'``
    has no effect.

If an *ensure-not-nullish expression* is known at compile time to always
evaluate at runtime to a non-nullish or a nullish value (``undefined``
or ``null``), then a :index:`compile-time warning` is issued.
The 'NullPointerError' exception is always thrown at runtime in the latter
case as represented below:

.. code-block:: typescript
   :linenos:

    class C { f = 1}

    let c = new C()
    c!.f // Compile-time warning, expression is always non-nullish, operator '!' is ignored

    let d: C | undefined = undefined
    d!.f // Compile-time warning, operator '!' always throws 'NullPointerError', as it is applied to nullish value
         // runtime: throws 'NullPointerError'

Nullish-Coalescing Expression
*****************************

.. meta:

*Nullish-coalescing expression* is a binary expression that uses the operator
``'??'``.

The syntax of *nullish-coalescing expression* is presented below:

.. code-block:: abnf

    nullishCoalescingExpression:
        expression '??' expression
        ;

A *nullish-coalescing expression* checks whether the evaluation of the
left-hand-side expression equals the *nullish* value:

-  If so, then the right-hand-side expression evaluation is the result
   of a nullish-coalescing expression.
-  If not so, then the result of the left-hand-side expression evaluation is
   the result of a nullish-coalescing expression, and the right-hand-side
   expression is not evaluated (the operator ``'??'`` is thus *lazy*).

The type of a nullish-coalescing expression is a normalized *union type* (see
:ref:`Union Types`) formed from the following:

- Non-nullish variant of the type of the left-hand-side expression; and
- Type of the right-hand-side expression.

The semantics of a nullish-coalescing expression is represented in the
following example:

.. code-block:: typescript
   :linenos:

    let x = lhs_expression ?? rhs_expression

    let x$ = lhs_expression
    if (x$ == null || x == undefined) {x = rhs_expression} else x = x$!

    // Type of x is NonNullishType(lhs_expression)|Type(rhs_expression)

If the *nullish-coalescing operator* is mixed with a conditional-and
or a conditional-or operator without parentheses, then a
:index:`compile-time error` occurs as follows:

.. code-block:: typescript
   :linenos:

    function  foo(n: boolean | undefined, a: boolean, b: boolean) {
        n ?? a || b   // error, '??' and '||' operations cannot be mixed without parentheses
        n ?? (a || b) // OK
    }

If the result of a *nullish-coalescing expression* evaluation is known at
compile time as a value of the left-hand-side or right-hand-side expression,
then a :index:`compile-time warning` occurs:

.. code-block:: typescript
   :linenos:

    let a = 1
    let b = undefined

    a ?? 2 // warning, left-hand-side expression is always used
    b ?? 3 // warning, right-hand-side expression is always used

Unary Expressions
*****************

.. meta:

The syntax of *unary expression* is presented below:

.. code-block:: abnf

    unaryExpression:
        expression '++'
        | expression '--'
        | '++' expression
        | '--' expression
    ...

All expressions with *unary operators* (except postfix increment and postfix
decrement operators) group right-to-left for ``'~+x'`` to have the same meaning
as ``'~(+x)'``.

The type of *unaryExpression* is not necessarily the same as the type
of the operand provided. The type of *unaryExpression* for each *unary operator*
is stated explicitly in the following table:

+------------------------+-------------------------+---------------------------+
| **Unary Operator**     | **Type of Operand**     | **Type of Result**        |
+========================+=========================+===========================+
| '++', '--'             | byte                    | byte                      |
| (prefix or             +-------------------------+---------------------------+
| postfix)               | short                   | short                     |
|                        +-------------------------+---------------------------+
|                        | int                     | int                       |
|                        +-------------------------+---------------------------+
|                        | long                    | long                      |
|                        +-------------------------+---------------------------+
|                        | float                   | float                     |
|                        +-------------------------+---------------------------+
|                        | double                  | double                    |
|                        +-------------------------+---------------------------+
|                        | bigint                  | bigint                    |
+------------------------+-------------------------+---------------------------+
| '+', '-' (unary)       | byte, short, int        | int                       |
|                        +-------------------------+---------------------------+
|                        | long                    | long                      |
|                        +-------------------------+---------------------------+
|                        | float                   | float                     |
|                        +-------------------------+---------------------------+
|                        | double                  | double                    |
|                        +-------------------------+---------------------------+
|                        | bigint                  | bigint                    |
+------------------------+-------------------------+---------------------------+
| '~'                    | byte, short, int, float | int                       |
| (bitwise complement)   +-------------------------+---------------------------+
|                        | long, double            | long                      |
|                        +-------------------------+---------------------------+
|                        | bigint                  | bigint                    |
+------------------------+-------------------------+---------------------------+
| '!'                    | boolean or see          | boolean                   |
| (logical complement)   |                         |                           |
|                        | :ref:`extended          |                           |
|                        | conditional             |                           |
|                        | expressions`            |                           |
+------------------------+-------------------------+---------------------------+

Postfix Increment
=================

.. meta:

*Postfix increment expression* is an *expression* followed by the increment
operator ``'++'``.

The *expression* must be a *left-hand-side expression*
(see :ref:`Left-Hand-Side Expressions`), and denotes a variable.

A :index:`compile-time error` occurs if type of the
the *expression* is not numeric (see :ref:`Numeric Types`) or ``bigint``.

Type of a *postfix increment expression* is the type of the variable. The
result of a *postfix increment expression* is a value, not a variable.

If the evaluation of the operand *expression* completes normally at runtime,
then:

-  Value *1* of the same type as a variable is added to the value of the
   variable; and
-  Result of addition is stored back into the variable.

Otherwise, the *postfix increment expression* completes abruptly, and no
incrementation occurs.

The  value of the *postfix increment expression* is the value of the variable
*before* a new value is stored.

The operation of postfix increment is represented in the following code example:

.. code-block:: typescript

  let a: short  = 1
  let b: float  = 1.5f
  let c: bigint = 1n

  a++ // result '1', 'a' becomes '2' ('1 + 1')
  b++ // result '1.5f', 'b' becomes '2.5f'  ('1.5f + 1f')
  c++ // result '1n', 'c' becomes '2n' ('1n + 1n')

Postfix Decrement
=================

.. meta:
   todo: let a : Double = Double.Nan; a++; a--; ++a; --a; (assertion)

*Postfix decrement expression* is an expression followed by the decrement
operator ``'--'``. The expression must be a *left-hand-side expression* (see
:ref:`Left-Hand-Side Expressions`). It denotes a variable.

A :index:`compile-time error` occurs if type of the expression is not
numeric (see :ref:`Numeric Types`) or ``bigint``.

Type of a postfix decrement expression is the type of the variable. The
result of a postfix decrement expression is a value, not a variable.

If evaluation of the operand expression completes at runtime, then:

-  Value '*1*' of the same type as a variable is subtracted from the value
   of the variable; and
-  Result of the subtraction is stored back into the variable.

Otherwise, the *postfix decrement expression* completes abruptly, and
no decrementation occurs.

The value of the *postfix decrement expression* is the value of the variable
*before* a new value is stored.

The operation of postfix decrement is represented in the following code example:

.. code-block:: typescript

  let a: short  = 1
  let b: float  = 1.5f
  let c: bigint = 1n

  a-- // result '1', 'a' becomes '0' ('1 - 1')
  b-- // result '1.5f', 'b' becomes '0.5f'  ('1.5f - 1f')
  c-- // result '1n', 'c' becomes '0n' ('1n - 1n')

Prefix Increment
================

.. meta:

*Prefix increment expression* is an expression preceded by the operator
``'++'``. The expression must be a *left-hand-side expression* (see
:ref:`Left-Hand-Side Expressions`). It denotes a variable.

A :index:`compile-time error` occurs if the type of the expression is not
numeric (see :ref:`Numeric Types`) or ``bigint``.

Type of a prefix increment expression is the type of the variable. The
result of a prefix increment expression is a value, not a variable.

If evaluation of the operand *expression* completes normally at runtime, then:

-  Value *1* of the same type as a variable is added to the value of the
   variable; and
-  Result of the addition is stored back into the variable.

Otherwise, the *prefix increment expression* completes abruptly, and no
incrementation occurs.

The  value of the *prefix increment expression* is the value of the variable
*after* a new value is stored.

The operation of prefix increment is represented in the following code example:

.. code-block:: typescript

  let a: short  = 1
  let b: float  = 1.5f
  let c: bigint = 1n

  ++a // result '2', 'a' becomes '2' ('1 + 1')
  ++b // result '2.5f', 'b' becomes '2.5f'  ('1.5f + 1f')
  ++c // result '2n', 'c' becomes '2n' ('1n + 1n')

Prefix Decrement
================

.. meta:

*Prefix decrement expression* is an expression preceded by the operator
``'--'``. The expression must be a *left-hand-side expression* (see
:ref:`Left-Hand-Side Expressions`). It denotes a variable.

A :index:`compile-time error` occurs if type of the expression is not
numeric (see :ref:`Numeric Types`) or ``bigint``.

Type of a prefix decrement expression is the type of the variable. The
result of a prefix decrement expression is a value, not a variable.

If evaluation of the operand *expression* completes normally at runtime, then:

-  Value *1* of the same type as a variable is subtracted from the value of the
   variable; and
-  Result of the subtraction is stored back into the variable.

Otherwise, the *prefix decrement expression* completes abruptly, and no
decrementation occurs.

The value of a *prefix decrement expression* is the value of the variable
*after* a new value is stored.

The operation of prefix decrement is represented in the following code example:

.. code-block:: typescript

  let a: short  = 1
  let b: float  = 1.5f
  let c: bigint = 1n

  --a // result '0', 'a' becomes '0' ('1 - 1')
  --b // result '0.5f', 'b' becomes '0.5f'  ('1.5f - 1f')
  --c // result '0n', 'c' becomes '0n' ('1n - 1n')

Unary Plus
==========

.. meta:

*Unary plus expression* is an expression preceded by the operator ``'+'``.
Type of the operand expression with the unary operator ``'+'`` must be
either convertible (see :ref:`Implicit Conversions`) to a numeric type (see
:ref:`Numeric Types`), or of ``bigint`` type. Otherwise,
a :index:`compile-time error` occurs.

The result of a unary plus expression is always a value, not a variable (even if
the result of the operand expression is a variable).

Numeric widening occurs on the *expression* before a *unary plus* operator
is applied. The type of the *unary plus* is determined as follows:

  - Type of result is ``int`` for ``byte``, ``short``, and ``int``;
  - Type of result is the same as that of the initial *expression* for ``long``,
    ``float``, ``double``, and ``bigint``.

Unary Minus
===========

.. meta:
    todo: let a : Double = Double.Nan; a = -a; (assertion)

*Unary minus expression* is an expression preceded by the operator ``'-'``.
Type of an operand expression with the unary operator ``'-'`` must be either
convertible (see :ref:`Widening Numeric Conversions`) to a numeric type (see
:ref:`Numeric Types`), or of ``bigint`` type. Otherwise,
a :index:`compile-time error` occurs.

Numeric widening occurs on the *expression* before a *unary minus* operator is
applied. The type of the *unary minus* is determined as follows:

- Type of result is `int` for ``byte``, ``short``, and ``int``;
- Type of result is the same as that of the initial *expression* for ``long``,
  ``float``, ``double``, and ``bigint``.

The result of a unary minus expression is a value, not a variable (even if the
result of the operand expression is a variable).

The unary negation operation is always performed on, and the result is drawn
from the same value set as the promoted operand value.

Further value set conversions are then performed on the same result.

The value of a unary minus expression at runtime is the arithmetic negation
of the promoted value of the operand.

The negation of integer values is the same as subtraction from zero. The ArkTS
programming language uses two's-complement representation for integers. The
range of two's-complement value is not symmetric. The same maximum negative
number results from the negation of the maximum negative *int* or *long*.
In that case, an overflow occurs but throws no error. For any integer value
*x*, *-x* is equal to *(~x)+1*.

The negation of bigint values and subtraction from the value `0n` are the same.

The negation of floating-point values is *not* the same as subtraction from
zero (if *x* is *+0.0*, then *0.0-x* is *+0.0*, however *-x* is *-0.0*).

A unary minus merely inverts the sign of a floating-point number. Special
cases to consider are as follows:

-  Operand ``NaN`` results in ``NaN`` (``NaN`` has no sign).
-  Operand infinity results in the infinity of the opposite sign.
-  Operand zero results in zero of the opposite sign.

Bitwise Complement
==================

.. meta:

*Bitwise complement* operator ``'~'`` is applied to an operand
of a numeric type or type ``bigint``.

If the type of the operand is ``double`` or ``float``, then it is truncated
first to ``long`` or ``int``, respectively.
If the type of the operand is ``byte`` or ``short``, then the operand is
widened to ``int``.
If the type of the operand is ``bigint``, then no conversion is required.
Type of result is determined as follows:

- ``int`` for ``byte``, ``short``, ``int``, and ``float``.
- ``long`` for ``long`` and ``double``.
- ``bigint`` for ``bigint``.

The result of a unary bitwise complement expression is a value, not a variable
(even if the result of the operand expression is a variable).

The value of a unary bitwise complement expression at runtime is the bitwise
complement of the value of the operand. In all cases, *~x* equals
*(-x)-1*.

It is represented by the following example:

.. code-block:: typescript

  let b: byte  = 2
  let s: short  = 2
  let i: int = 2
  let f: float = 2.0f

  let l: long  = 2
  let d: double  = 2.0

  let B: bigint = 2n

  let rb = ~b
  console.log(rb, typeof rb) // prints '-3 int'
  let rs = ~s
  console.log(rs, typeof rs) // prints '-3 int'
  let ri = ~i
  console.log(ri, typeof ri) // prints '-3 int'
  let rf = ~f
  console.log(rf, typeof rf) // prints '-3 int'

  let rl = ~l
  console.log(rl, typeof rl) // prints '-3 long'
  let rd = ~d
  console.log(rd, typeof rd) // prints '-3 long'

  let rB = ~B
  console.log(rB, typeof rB) // prints '-3 bigint'

Logical Complement
==================

.. meta:

*Logical complement expression* is an expression preceded by the operator
``'!'``. Type of the operand expression with the unary ``'!'`` operator must be
``boolean`` or type mentioned in :ref:`Extended Conditional Expressions`.
Otherwise, a :index:`compile-time error` occurs.

The unary logical complement expression type is ``boolean``.

The value of a unary logical complement expression is ``true`` if the (possibly
converted) operand value is ``false``, and ``false`` if the operand value
(possibly converted) is ``true``.

Binary Expressions
******************

The syntax of *binary expression* is presented below:

.. code-block:: abnf

    binaryExpression:
        multiplicativeExpression
        | exponentiationExpression
        | additiveExpression
        | shiftExpression
    ...

Every *binaryExpression* has the form *expression 1* ``op`` *expression 2*,
where ``op`` is a binary operator (operator sign), and *expression 1* and
*expression 2* are its operands.

The subgroups of binary expressions are described further in this chapter.

Possible combinations of types of *expression 1* and *expression 2*,
as well as the type of the resulting *binaryExpression* are presented in the
table below. Type combinations not listed in the table cause a
:index:`compile-time error` if a combination is detected at compile time, or a
:index:`runtime error` otherwise.

+----------------+--------------------------------+-------------------------------+-------------------------+
| **Operator**   | **Type of One Operand**        | **Type of Other Operand**     | **Type of Result**      |
+================+================================+===============================+=========================+
| '*', '/', '%'  | byte, short, int               |  byte, short, int             |    int                  |
|                +--------------------------------+-------------------------------+-------------------------+
|                | long                           | any numeric except float      |    long                 |
|                |                                | or double                     |                         |
|                +--------------------------------+-------------------------------+-------------------------+
|                | float                          |  any numeric except double    |    float                |
|                +--------------------------------+-------------------------------+-------------------------+
|                | double                         |  any numeric                  |    double               |
|                +--------------------------------+-------------------------------+-------------------------+
|                | bigint                         |  bigint                       |    bigint               |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '**'           | any numeric type               |  any numeric type             |    double               |
|                +--------------------------------+-------------------------------+-------------------------+
|                | bigint                         |  bigint                       |    bigint               |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '+'            | string                         |  converted to a string        |    string               |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '+', '-'       | byte, short, int               |  byte, short, int             |    int                  |
|                +--------------------------------+-------------------------------+-------------------------+
|                | long                           |  any numeric except float     |    long                 |
|                |                                |  or double                    |                         |
|                +--------------------------------+-------------------------------+-------------------------+
|                | float                          |  any numeric except double    |    float                |
|                +--------------------------------+-------------------------------+-------------------------+
|                | double                         |  any numeric                  |    double               |
|                +--------------------------------+-------------------------------+-------------------------+
|                | bigint                         |  bigint                       |    bigint               |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '<<', '>>'     | bigint                         |  bigint                       |    bigint               |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '<<', '>>',    | byte, short, int,              |  any numeric                  |    int (see Note 2)     |
| and '>>>'      | float                          |                               |                         |
+                +--------------------------------+-------------------------------+-------------------------+
|                | long, double                   |  any numeric                  |    long (see Note 2)    |
|                |                                |                               |                         |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '<', '<=',     | string, string literal         |  string, string literal       |    boolean              |
| '>', '>='      +--------------------------------+-------------------------------+-------------------------+
|                | boolean                        |  boolean                      |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | numeric                        |  numeric                      |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | enum (numeric value)           |  enum (numeric value)         |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | enum (string value)            |  enum (string value)          |    boolean              |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '==', '===',   | string, string literal         |  string, string literal       |    boolean              |
| '!=',  '!=='   +--------------------------------+-------------------------------+-------------------------+
|                | boolean                        |  boolean                      |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | numeric                        |  numeric                      |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | bigint                         |  bigint                       |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | char                           |  char                         |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | enum                           |  enum                         |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | function                       |  function                     |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | null, undefined                |  null, undefined              |    boolean              |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '&', '^', '|'  | boolean                        | boolean                       |    boolean              |
|                +--------------------------------+-------------------------------+-------------------------+
|                | byte, short, int, float        | byte, short, int, float       |    int                  |
|                +--------------------------------+-------------------------------+-------------------------+
|                | long, double                   | long, double                  |    long                 |
|                +--------------------------------+-------------------------------+-------------------------+
|                | bigint                         | bigint                        |    bigint               |
+----------------+--------------------------------+-------------------------------+-------------------------+
| '&&', '||'     | boolean                        | boolean                       |    boolean              |
+                +--------------------------------+-------------------------------+-------------------------+
|                | other types, see Note 5        | other types, see Note 5       |    see Note 5           |
+----------------+--------------------------------+-------------------------------+-------------------------+

.. note::
   The following applies to the table above.

   #. For all operators, except shift operators, the order of operands does not influence
      the type of result.
   #. The type of result of shift operators '``<<``', '``>>``', '``>>>``' with
      operands of numeric types depends on the type of the 1st (left-hand-side)
      operand, and not on the type of the second (right-hand-side) operand.
   #. Equality operators '``==``', '``===``', '``!=``', and '``!==``' are
      defined for any type, but the combinations listed explicitly
      in the table have specific behaviors.
   #. Equality operators for the types that contain ``null`` or ``undefined``
      are described in :ref:`Extended Equality with null or undefined`.
   #. Types of operands (other than ``boolean``) and the resultant type for
      logical operators '``&&``' and '``||``' are discussed in
      :ref:`Extended Conditional Expressions`.

.. meta:

Multiplicative Expressions
**************************

.. meta:

Multiplicative expressions use *multiplicative operators* ``'*'``, ``'/'``,
and ``'%'``.

The syntax of *multiplicative expression* is presented below:

.. code-block:: abnf

    multiplicativeExpression:
        expression '*' expression
        | expression '/' expression
        | expression '%' expression
        ;

Multiplicative operators group left-to-right.

Type of both operands in a multiplicative operator must be one of the following:

- ``bigint``; or
- Convertible (see :ref:`Numeric Operator Contexts`) to a numeric type
  (see :ref:`Numeric Types`).

Otherwise, a :index:`compile-time error` occurs.

No implicit conversion is applied to a multiplicative expression with operands of
type ``bigint``,  and the inferred type is always ``bigint``.

This behavior is represented by the following example:

.. code-block:: typescript

   // OK, the inferred type of 'i' is ``bigint``
   let i = 1n * 2n
   // Compile-time error, one operand is not of 'bigint' type
   let i = 1n * 2

A numeric types conversion (see :ref:`Widening Numeric Conversions`)
of an expression with operands convertible (see :ref:`Numeric Operator Contexts`)
to a numeric type is performed on both operands to ensure
that the resultant type is the type of the multiplicative expression.

The resultant type of an expression with a numeric operand is inferred from
the largest type after promoting ``byte`` and ``short`` operands to ``int``:

- ``double`` if any operand is ``double``;
- ``float`` if any operand is ``float``, and no operand is ``double``;
- ``long`` if any operand is ``long``, and no operand is ``double`` or ``float``;
- ``int`` if all operands are of type ``byte``, ``short``, or ``int``.

This situation is represented in the following example:

.. code-block:: typescript
   :linenos:

   // Code below prints true 4 times
   let byte1: byte = 1
   let byte2: byte = 1
   let long1: long = 1
   let float1: float = 1
   let double1: double = 1

   let res_byte = byte1 * byte2  // int
   console.log(res_byte instanceof int)

   let res_long = byte1 * long1  // long
   console.log(res_long instanceof long)

   let res_float = byte1 * float1 // float
   console.log(res_float instanceof float)

   let res_double = byte1 * double1 // double
   console.log(res_double instanceof double)

Multiplication
==============

.. meta:
    todo: If either operand is NaN, the result should be NaN, but result is -NaN
    todo: Multiplication of an infinity by a zero should be NaN, but result is - NaN

The binary operator ``'*'`` performs multiplication, and returns the product of
its operands.

Multiplication is a commutative operation if operand expressions have no
side effects.

Bigint multiplication is associative.

Integer multiplication is associative when all operands are of the same type.

Floating-point multiplication is not associative.

Type of a *multiplication expression* with numeric operands
is the *largest* type (see :ref:`Numeric Types`) of its operands *after* applying
:ref:`Widening numeric conversions`.

If overflow occurs during integer multiplication, then:

-  The result is the low-order bits of the mathematical product as represented
   in some sufficiently large two's-complement format.
-  The sign of the result can be other than the sign of the mathematical
   product of the two operand values.

A floating-point multiplication result is determined in compliance with the
IEEE 754 arithmetic:

-  The result is ``NaN`` if:

   -  Either operand is ``NaN``;
   -  Infinity is multiplied by zero.

-  If the result is not ``NaN``, then the sign of the result is as follows:

   -  Positive, where both operands have the same sign; and
   -  Negative, where the operands have different signs.

-  If infinity is multiplied by a finite value, then the multiplication results
   in a signed infinity (the sign is determined by the rule above).
-  If neither ``NaN`` nor infinity is involved, then the exact mathematical
   product is computed.

   The product is rounded to the nearest value in the chosen value set by
   using the IEEE 754 *round-to-nearest* mode. The ArkTS programming
   language requires gradual underflow support as defined by IEEE 754
   (see :ref:`Floating-Point Types and Operations`).

   If the magnitude of the product is too large to represent, then the
   operation overflows, and the result is an appropriately signed infinity.

The evaluation of a multiplication operator ``'*'`` never throws an error
despite possible overflow, underflow, or loss of information.

Division
========

.. meta:
   todo: If either operand is NaN, the result should be NaN, but result is -NaN
   todo: Division of infinity by infinity should be NaN, but result is - NaN
   todo: Division of a nonzero finite value by a zero results should be signed infinity, but "Floating point exception(core dumped)" occurs

The binary operator ``'/'`` performs division and returns the quotient of its
left-hand-side and right-hand-side expressions (``dividend`` and ``divisor``
respectively).

Bigint division rounds toward *0*, i.e., the quotient of bigint operands
*n* and *d* is the ``bigint`` value *q* with the largest possible magnitude that
satisfies :math:`|d\cdot{}q|\leq{}|n|`.

If the divisor value of the ``bigint`` division operator is *0n*, then either
a :index:`compile-time error` occurs if detected at compile time, or a
:index:`runtime error` is thrown during execution.

Integer division rounds toward *0*, i.e., the quotient of integer operands
*n* and *d*, after a numeric types conversion on both (see
:ref:`Widening Numeric Conversions` for details), is
the integer value *q* with the largest possible magnitude that
satisfies :math:`|d\cdot{}q|\leq{}|n|`.

.. note::
   The integer value *q* is:

   -  Positive, where \|n| :math:`\geq{}` \|d|, and *n* and *d* have the same
      sign; but
   -  Negative, where \|n| :math:`\geq{}` \|d|, and *n* and *d* have opposite
      signs.

The only special case that does not comply with this rule is where integer
overflow occurs. The result equals the dividend if the dividend is a negative
integer of the largest possible magnitude for its type, while the divisor
is *-1*. No error is thrown in this case despite the overflow.

However, if the divisor value of integer division is detected to be *0* during
compilation, then a :index:`compile-time error` occurs. Otherwise, an
``ArithmeticError`` is thrown during execution.

The result of a floating-point division is determined in compliance with the
IEEE 754 arithmetic:

-  The result is ``NaN`` if:

   -  Either operand is NaN;
   -  Both operands are infinity; or
   -  Both operands are zero.

-  If the result is not ``NaN``, then the sign of the result is:

   -  Positive, where both operands have the same sign; or
   -  Negative, where the operands have different signs.

-  Division produces a signed infinity (the sign is determined by
   the rule above) if:

   -  Infinity is divided by a finite value; and
   -  A nonzero finite value is divided by zero.

-  Division produces a signed zero (the sign is determined by the
   rule above) if:

   -  A finite value is divided by infinity; and
   -  Zero is divided by any other finite value.

-  If neither ``NaN`` nor infinity is involved, then the exact mathematical
   quotient is computed.

   If the magnitude of the product is too large to represent, then the
   operation overflows, and the result is an appropriately signed infinity.

The quotient is rounded to the nearest value in the chosen value set by
using the IEEE 754 *round-to-nearest* mode. The ArkTS programming
language requires gradual underflow support as defined by IEEE 754 (see
:ref:`Floating-Point Types and Operations`).

The evaluation of a floating-point division operator ``'/'`` never throws an
error despite possible overflow, underflow, division by zero, or loss of
information.

The type of a *division expression* with operands of numeric types is the
*largest* numeric type (see :ref:`Numeric Types`) of its operands  *after* applying
:ref:`Widening numeric conversions`.

Remainder
=========

.. meta:
    todo: If either operand is NaN, the result should be NaN, but result is -NaN
    todo: if the dividend is an infinity, or the divisor is a zero, or both, the result should be NaN, but this is -NaN

The binary operator ``'%'`` yields the remainder of its operands (``dividend``
as the left-hand-side, and ``divisor`` as the right-hand-side operand) from an
implied division.

The remainder operator in ArkTS accepts floating-point operands (unlike in
C and C++).

A remainder operation :math:`(a\%b)` on ``bigint`` operands produces a result
that makes :math:`(a/b)*b+(a\%b)` equal *a*. No implicit conversion is
applied to an operand.

If the divisor value of the ``bigint`` remainder operator is *0n*, then a
:index:`runtime error` is thrown during execution.

The remainder operation :math:`(a\%b)` on integer operands produces a result
that makes :math:`(a/b)*b+(a\%b)` equal *a*. Numeric type conversion on remainder
operation is discussed in :ref:`Widening Numeric Conversions`. A remainder
operation produces a value of type ``int`` for ``byte``, ``short``, ``int``,
and ``float`` operands, or a value of type ``long`` for ``long`` or ``double``
operands.

This equality holds even in the special case where the dividend is a negative
integer of the largest possible magnitude of its type, and the divisor is *-1*
(the remainder is then *0*). According to this rule, the result of the remainder
operation can only be one of the following:

-  Negative if the dividend is negative; or
-  Positive if the dividend is positive.

The magnitude of the result is always less than that of the divisor.

If the divisor value of integer remainder operator is detected to be *0* during
compilation, then a :index:`compile-time error` occurs. Otherwise, an
``ArithmeticError`` is thrown during execution.

The result of a floating-point remainder operation as computed by the operator
``'%'`` is different than that produced by the remainder operation defined by
IEEE 754. The IEEE 754 remainder operation computes the remainder from a rounding
division (not a truncating division), and its behavior is different from that
of the usual integer remainder operator. On the contrary, ArkTS presumes that
the operator ``'%'`` behaves on floating-point operations in the same manner as
the integer remainder operator (comparable to the C library function *fmod*).
The standard library (see :ref:`Standard Library`) routine ``Math.IEEEremainder``
can compute the IEEE 754 remainder operation.

The result of a floating-point remainder operation is determined in compliance
with the IEEE 754 arithmetic:

-  The result is ``NaN`` if:

   -  Either operand is ``NaN``;
   -  The dividend is infinity;
   -  The divisor is zero; or
   -  The dividend is infinity, and the divisor is zero.

-  If the result is not ``NaN``, then the sign of the result is the same as the
   sign of the dividend.
-  The result equals the dividend if:

   -  The dividend is finite, and the divisor is infinity; or
   -  If the dividend is zero, and the divisor is finite.

-  If infinity, zero, or ``NaN`` are not involved, then the floating-point remainder
   *r* from the division of the dividend *n* by the divisor *d* is determined
   by the mathematical relation :math:`r=n-(d\cdot{}q)`, where *q* is an
   integer that is only:

   -  Negative if :math:`n/d` is negative, or
   -  Positive if :math:`n/d` is positive.

-  The magnitude of *q* is the largest possible without exceeding the
   magnitude of the true mathematical quotient of *n* and *d*.

The evaluation of the floating-point remainder operator ``'%'`` never throws
an error, even if the right-hand operand is zero. Overflow, underflow, or
loss of precision cannot occur.

The type of a *remainder expression* with numeric operands is the
*largest* numeric type (see :ref:`Numeric Types`) of its operands   *after* applying
:ref:`Widening numeric conversions`.

Exponentiation Expression
*************************

.. meta:

.. meta:

Exponentiation expression uses the binary *exponentiation operator* '``**``'.

The binary operator '``**``' raises the first operand (base) to the power of
the second operand (exponent).

The syntax of an *exponentiation expression* is presented below:

.. code-block:: abnf

    exponentiationExpression:
        expression '**' expression
        ;

The operator '``**``' has two variants distinguishable by operand types, i.e.,
both operands are as follows:

- :ref:`Type bigint`; or
- :ref:`Numeric types`, in which case any operand that is not of type ``double``
  is converted to type ``double``.

Any other combination of operand types causes a :index:`compile-time error`.

The result of raising to power *0n* is always *1n*, including the case
*0n* ``**`` *0n*.

If the second operand of type ``bigint`` is negative, then either a
:index:`compile-time error` occurs if detected at compile time, or a
:index:`runtime error` is thrown during execution.

Both variants of the operator '``**``' are represented in example below:

.. code-block:: typescript
   :linenos:

   let a: bigint = 2n
   let b: double = 2
   let c: int = 2
   let d: int = 10

   let v = a ** 2n // OK 'bigint' ** 'bigint'
   let u = a ** 0n // OK 'bigint' ** 'bigint'
   let w = a ** -1n // Compile-time error, exponent must be non-negative

   let x = a ** c // Compile-time error, 'c' is not 'bigint'
   let y = b ** d // 'd' is converted to 'double'
   let z = c ** d // both 'c' and 'd' are converted to 'double'

The binary operator '``**``' with *numeric operands* is equivalent to
`Math.pow()`. It causes neither a :index:`compile-time error`, nor a
:index:`runtime error`.

Special cases of the binary operator '``**``' according to IEEE 754 are
represented below.

.. note::
   Since any numeric operand of '``**``' is implicitly converted to ``double``,
   the term ``integer`` effectively means ``double`` with zero in the fractional
   part (for example *-2.0*) as listed below:

   - `x ** +/-0` returns *1* even if *x* is *NaN*;
   - `+/-0 ** y` returns *+/-Infinity* if *y* is a negative odd integer;
   - `+/-0 ** -Infinity` returns *+Infinity*;
   - `+/-0 ** +Infinity` returns *+0*;
   - `+/-0 ** y` returns *+0* if *y* is a finite positive odd integer;
   - `-1 ** +Infinity` returns *1*;
   - `+1 ** y` returns *1* for any *y* (even for *NaN*);
   - `x, +Infinity` returns  *+0* for *-1 < x < 1*;
   - `x, +Infinity` returns *+Infinity* for *x < -1 or for *1 < x*
     (including *+/-Infinity*);
   - `x, -Infinity` returns *+Infinity* for *-1 < x < 1*;
   - `x, -Infinity` returns *+0* for *x < -1* or for *1 < x* (including +/-Infinity);
   - `+Infinity, y` returns *+0* for a number *y < 0*;
   - `+Infinity, y` returns *+Infinity* for a number *y > 0*;
   - `-Infinity, y` returns *-0* for a finite negative odd integer *y*;
   - `-Infinity, y` returns *-Infinity* for a finite positive odd integer *y*;
   - `-Infinity, y` returns *+0* if *y* for a finite *y < 0* and not an odd integer;
   - `-Infinity, y` returns *+Infinity* for a finite *y > 0* and not an odd integer;
   - `+/-0, y` returns *+Infinity* for a finite *y < 0* and not an odd integer;
   - `+/-0, y` returns *+0* for a finite *y > 0* and not an odd integer;
   - `x, y` returns *NaN* for a finite *x < 0* and a finite non-integer *y*.

Additive Expressions
********************

.. meta:

Additive expressions use *additive operators* ``'+'`` and ``'-'``.

The syntax of *additive expression* is presented below:

.. code-block:: abnf

    additiveExpression:
        expression '+' expression
        | expression '-' expression
        ;

Additive operators group left-to-right.

The following rules apply where the operator  ``'+'`` is used:

- If either operand is of type ``string``, then the operation
  is a string concatenation (see :ref:`String Concatenation`).
- If both operands are of type ``bigint``, then no implicit
  conversion is applied, and the inferred type is ``bigint``.
- In all other cases, type of each operand must be
  convertible (see :ref:`Widening Numeric Conversions`) to
  a numeric type (see :ref:`Numeric Types`).

Otherwise, a :index:`compile-time error` occurs.

The following rules apply where the operator  ``'-'`` is used:

- Either both operands must be of type ``bigint``; or
- Type of each operand of a binary operator must be convertible
  (see :ref:`Widening Numeric Conversions`) to a numeric type (see
  :ref:`Numeric Types`).

Otherwise, a :index:`compile-time error` occurs.

Type of an *additive expression* with a valid
combination of types is determined as follows:

-  If any operand is of type ``string``, then ``string``;
-  If both operands are of type ``bigint``, then ``bigint``;
-  If both operands are convertible to a numeric type, then the type inferred
   after widening operands of numeric types by the rules explained in the example
   in :ref:`Multiplicative Expressions`.

String Concatenation
====================

.. meta:

If one operand of an expression is of type ``string``, then the string
conversion (see :ref:`String Operator Contexts`) is performed on the other
operand at runtime to produce a string.

String concatenation produces a reference to a ``string`` object that is a
concatenation of two operand strings. The left-hand-side operand characters
precede the right-hand-side operand characters in a newly created string.

If the expression is not a constant expression (see :ref:`Constant Expressions`),
then a new ``string`` object is created (see :ref:`New Expressions`).

Additive Operators for Numeric Types
====================================

.. meta:
   todo: The sum of two infinities of opposite sign should be NaN, but it is -NaN

A numeric types conversion (see :ref:`Widening Numeric Conversions`)
performed on a pair of operands ensures that both operands are of a numeric
type. If the conversion fails, then a :index:`compile-time error` occurs.

The binary operator ``'+'`` performs addition and produces the sum of such
operands.

The binary operator ``'-'`` performs subtraction and produces the difference
of two numeric operands.

Type of an additive expression performed on numeric operands is the
largest type (see :ref:`Numeric Types`) to which operands of that
expression are converted (see :ref:`Multiplicative Expressions` for an example).

If the promoted type is ``int`` or ``long``, then integer arithmetic is
performed.
If the promoted type is ``float`` or ``double``, then floating-point arithmetic
is performed.

If operand expressions have no side effects, then addition is a commutative
operation.

If all operands are of the same type, then integer addition is associative.

Floating-point addition is not associative.

If overflow occurs on an integer addition, then:

-  Result is the low-order bits of the mathematical sum as represented in
   a sufficiently large two's-complement format.
-  Sign of the result is opposite to that of the mathematical sum of
   the operands'values.

The result of a floating-point addition is determined in compliance with the
IEEE 754 arithmetic as follows:

-  The result is ``NaN`` if:

   -  Either operand is ``NaN``; or
   -  The operands are two infinities of the opposite signs.

-  The sum of two infinities of the same sign is the infinity of that sign.
-  The sum of infinity and a finite value equals the infinite operand.
-  The sum of two zeros of opposite sign is positive zero.
-  The sum of two zeros of the same sign is zero of that sign.
-  The sum of zero and a nonzero finite value is equal to the nonzero operand.
-  The sum of two nonzero finite values of the same magnitude and opposite sign
   is positive zero.
-  If infinity, zero, or ``NaN`` are not involved, and the operands have the
   same sign or different magnitudes, then the exact sum is computed
   mathematically.

If the magnitude of the sum is too large to represent, then the operation
overflows. The result is an appropriately signed infinity.

Otherwise, the sum is rounded to the nearest value within the chosen value set
by using the IEEE 754 *round-to-nearest* mode. The ArkTS programming language
requires gradual underflow support as defined by IEEE 754 (see
:ref:`Floating-Point Types and Operations`).

When applied to two numeric type operands (see :ref:`Numeric Types`), the
binary operator ``'-'`` performs subtraction, and returns the difference of
such operands (``minuend`` as left-hand-side, and ``subtrahend`` as the
right-hand-side operand).

The result of *a-b* is always the same as that of *a+(-b)* in both integer and
floating-point subtraction.

The subtraction from zero for integer values is the same as negation. However,
the subtraction from zero for floating-point operands and negation is *not*
the same (if *x* is *+0.0*, then *0.0-x* is *+0.0*; however *-x* is *-0.0*).

The evaluation of a numeric additive operator never throws an error despite
possible overflow, underflow, or loss of information.

Shift Expressions
*****************

.. meta:
    todo: spec issue: uses 'L' postfix in example "(n >> s) + (2L << ~s)", we don't have it

*Shift expressions* use *shift operators* ``'<<'`` (left shift), ``'>>'``
(signed right shift), and ``'>>>'`` (unsigned right shift). The value to be
shifted is the left-hand-side operand in a shift operator, and the
right-hand-side operand specifies the shift distance.

The syntax of *shift expression* is presented below:

.. code-block:: abnf

    shiftExpression:
        expression '<<' expression
        | expression '>>' expression
        | expression '>>>' expression
        ;

Shift operators group left-to-right.

Both operands of a *shift expression* must be of numeric types
or type ``bigint``.

If the type of one or both operands is ``double`` or ``float``, then the
operand or operands are truncated first to ``long`` or ``int``, respectively.
If the type of the left-hand-side operand is ``byte`` or ``short``, then the
operand is converted to ``int``.
If both operands are of type ``bigint``, then no conversion is required.
A :index:`compile-time error` occurs if one operand is type ``bigint``, and the
other one is a numeric type.
Also, a :index:`compile-time error` occurs if ``'>>>'`` (unsigned right shift)
is applied to operands of type ``bigint``.

The result of a *shift expression* is of the type to which its first operand
converted.

If the left-hand-side operand is of the promoted type ``int``, then only five
lowest-order bits of the right-hand-side operand specify the shift distance
(as if using a bitwise logical AND operator ``'&'`` with the mask value *0x1f*
or *0b11111* on the right-hand-side operand). Thus, it is always within the
inclusive range of *0* through *31*.

If the left-hand-side operand is of the promoted type ``long``, then only six
lowest-order bits of the right-hand-side operand specify the shift distance
(as if using a bitwise logical AND operator ``'&'`` with the mask value *0x3f*
or *0b111111* the right-hand-side operand). Thus, it is always within the
inclusive range of *0* through *63*.

Shift operations are performed on the two's-complement integer
representation of the value of the left-hand-side operand at runtime.

The value of *n* ``<<`` *s* is *n* left-shifted by *s* bit positions. It is
equivalent to multiplication by two to the power *s* even in case of an
overflow.

The value of *n* ``>>`` *s* is *n* right-shifted by *s* bit positions with
sign-extension. The resultant value is :math:`floor(n / 2s)`. If *n* is
non-negative, then it is equivalent to truncating integer division (as computed
by the integer division operator by 2 to the power *s*).

The value of *n* ``>>>`` *s* is *n* right-shifted by *s* bit positions with
zero-extension, where:

-  If *n* is positive, then the result is the same as that of *n* ``>>`` *s*.
-  If *n* is negative, and type of the left-hand-side operand is ``int``,
   then the result is equal to that of the expression
   (*n* ``>>`` *s*) ``+ (2 << ~`` *s*).
-  If *n* is negative, and type of the left-hand-side operand is ``long``,
   then the result is equal to that of the expression
   (*n* ``>>`` *s*) ``+ ((2 as long) << ~`` *s*).

Relational Expressions
**********************

.. meta:
    todo: if either operand is NaN, then the result should be false, but Double.NaN < 2 is true, and assertion fail occurs with opt-level 2. (also fails with INF)
    todo: Double.POSITIVE_INFINITY > 1 should be true, but false (also fails with opt-level 2)

Relational expressions use *relational operators* ``'<'``, ``'>'``, ``'<='``,
and ``'>='``.

The syntax of *relational expression* is presented below:

.. code-block:: abnf

    relationalExpression:
        expression '<' expression
        | expression '>' expression
        | expression '<=' expression
        | expression '>=' expression
        ;

Relational operators group left-to-right.

A relational expression is always of type ``boolean``.

Relational expressions can be of the kinds described below.
The kind of a relational expression depends on types of operands. It is a
:index:`compile-time error` if at least one type of operands is different from
types described below.

Numeric Relational Operators
============================

.. meta:

Type of each operand in a ``numeric relational operator`` must be of a numeric type
(see :ref:`Numeric Types`, :ref:`Numeric Conversions for Relational and Equality Operands`).
Otherwise, a :index:`compile-time error` occurs.

Depending on the converted type of operands, a comparison is performed as follows:

-  Signed integer comparison, if the converted operand type is ``int``
   or ``long``.

-  Floating-point comparison, if the converted operand type is ``float``
   or ``double``.

The comparison of floating-point values drawn from any value set must be accurate.

A floating-point comparison must be performed in accordance with the IEEE 754
standard specification as follows:

-  The result of a floating-point comparison is false if either operand is ``NaN``.

-  All values other than ``NaN`` must be ordered with the following:

   -  Negative infinity less than all finite values; and
   -  Positive infinity greater than all finite values.

-  Positive zero equals negative zero.

Based on the presumption above, the following rules apply to integer
operands, floating-point operands other than ``NaN``:

-  The value produced by the operator ``'<'`` is ``true`` if the value of the
   left-hand-side operand is less than that of the right-hand-side operand.
   Otherwise, the value is ``false``.
-  The value produced by the operator ``'<='`` is ``true`` if the value of the
   left-hand-side operand is less than or equal to that of the right-hand-side
   operand. Otherwise, the value is ``false``.
-  The value produced by the operator ``'>'`` is ``true`` if the value of the
   left-hand-side operand is greater than that of the right-hand-side operand.
   Otherwise, the value is ``false``.
-  The value produced by the operator ``'>='`` is ``true`` if the value of the
   left-hand-side operand is greater than or equal to that of the right-hand-side
   operand. Otherwise, the value is ``false``.

The behavior of comparison of ``numeric`` type operands is represented
in the example below:

.. code-block:: typescript
   :linenos:

   // integer comparisons
   console.log( 1 < -3) // false
   console.log(-1 as long >= -1 as short) // true

   // floating-point comparisons
   console.log(1 <= 1.0f)  // true
   console.log(2 <= 1.0)   // false

Bigint Relational Operators
===========================

.. meta:

Relational operators can be applied to ``bigint`` values
(see :ref:`Type bigint`) if:

-  both operands are of ``bigint`` type; or
-  one operand is of ``bigint`` type and other is of a numeric type.

In the second case, a comparison is performed as follows:

-  If a numeric type operand is of an integer type, it is converted to
   ``bigint`` type and ``bigint`` comparison is performed;

-  If a numeric type operand is of ``double`` type, the ``bigint``
   operand is converted to ``double`` and then floating-point comparison
   is performed;

-  If a numeric type operand is of ``float`` type, both operands are converted to
   ``double`` and then floating-point comparison is performed.

The behavior of comparison of ``numeric`` type operands and
``bigint`` type operands is represented in the example below:

.. code-block:: typescript
   :linenos:

    let b = 2n

    // bigint against bigint
    console.log(b < 3n)  // true
    console.log(b >= 3n) // false

    // bigint against an integer type
    console.log(b < 3)         // true, '2' is converted implicitly to bigint
    console.log(b < BigInt(3)) // true, the same with explicit conversion

   // bigint against double
   console.log(b < 3.0)               // true, 'b' is converted to double
   console.log(b.doubleValue() < 3.0) // the same with explicit conversion

   // bigint against float
   const f = 3.f
   console.log(b < f) // true, 'b' and 'f' are converted to bigint

String Relational Operators
===========================

.. meta:

Results of all string comparisons are defined as follows:

-  Operator ``'<'`` delivers ``true`` if the string value of the left-hand-side
   operand is lexicographically less than the string value of the right-hand-side
   operand, or ``false`` otherwise.
-  Operator ``'<='`` delivers ``true`` if the string value of the left-hand-side
   operand is lexicographically less than or equal to the string value of the
   right-hand-side operand, or ``false`` otherwise.
-  Operator ``'>'`` delivers ``true`` if the string value of the left-hand-side
   operand is lexicographically greater than the string value of the
   right-hand-side operand, or ``false`` otherwise.
-  Operator ``'>='`` delivers ``true`` if the string value of the left-hand-side
   operand is lexicographically greater than or equal to the string value of
   the right-hand operand, or ``false`` otherwise.

Boolean Relational Operators
============================

.. meta:

Results of all boolean comparisons are defined as follows:

-  Operator ``'<'`` delivers ``true`` if the left-hand-side operand is ``false``,
   and the right-hand-side operand is true, or ``false`` otherwise.
-  Operator ``'<='`` delivers:

   - ``true`` when both operands are ``true``, or the left-hand-side operand
     is ``false`` for any right-hand value;
   - ``false`` when the left-hand-side operand is ``true``, and the
     right-hand-side operand is ``false``.

-  Operator ``'>'`` delivers ``true`` if the left-hand-side operand is ``true``,
   and the right-hand-side operand is ``false``, or ``false`` otherwise.
-  Operator ``'>='`` delivers:

   - ``true`` when both operands are ``false``, or the left-hand-side operand
     is ``true`` for any right-hand-side value;
   - ``false`` when the left-hand-side operand is ``false``, and the
     right-hand-side operand is ``true``.

``char`` Relational Operators
=============================

.. meta:

See :ref:`char Operations`.

Enumeration Relational Operators
================================

.. meta:

If both operands are of the same enumeration type (see :ref:`Enumerations`),
then :ref:`Numeric Relational Operators`
or :ref:`String Relational Operators` are used depending on the type of enumeration
base type. Otherwise, a :index:`compile-time error` occurs.

Equality Expressions
********************

.. meta:

Equality expressions use *equality operators* ``'=='``, ``'==='``, ``'!='``,
and ``'!=='``.

The syntax of *equality expression* is presented below:

.. code-block:: abnf

    equalityExpression:
        expression ('==' | '===' | '!=' | '!==') expression
        ;

Equality operators group left-to-right.
Equality operators are commutative if operand expressions cause no side
effects.

Similarly to relational operators, equality operators return ``true`` or
``false``.  Equality operators have lower precedence than relational operators,
for example, :math:`a < b==c < d` is `true` when both :math:`a < b`
and :math:`c < d` are ``true``.

Any equality expression is of type ``boolean``.

The result produced by ``a != b`` and ``!(a == b)`` is the same in all cases.
The result produced by ``a !== b`` and ``!(a === b)`` is the same.

The result of the operators ``'=='`` and ``'==='`` is the same in all cases
except when comparing the values ``null`` and ``undefined`` (see
:ref:`Extended Equality with null or undefined`).

A comparison that uses the operators ``'=='`` and ``'==='`` is evaluated to
``true`` if:

- Both operands are of :ref:`Type boolean` and have the same value;

- Both operands are of :ref:`Type string` or string literal type
  (see :ref:`String Literal Types`) and have the same contents;

- Both operands are of :ref:`Type bigint` and have the same value;

- Both operands are of :ref:`Numeric Types` and have the same value except ``NaN``
  (see :ref:`Numeric Equality Operators` for detail) after a numeric conversion
  (see :ref:`Widening numeric conversions`,
  :ref:`Numeric Conversions for Relational and Equality Operands`);

- Both operands are of :ref:`Type char` and have the same value, i.e., both
  operands represent the same 16-bit code unit (see :ref:`char Operations`);

- One operand is of :ref:`Type char`, other is of a numeric type and
  operand have the same numeric value (see :ref:`char Operations` and
  :ref:`char Conversions for Relational and Equality Operands`);

- Both operands are of enumeration types (see :ref:`Enumerations`) and
  have the same numeric value or the same string value;

- Function references refer to the same functional object (see
  :ref:`Function Type Equality Operators` for detail).

- Both operands are of the same type and refer to the same object.

An evaluation of equality expressions always uses the actual types of operands
as in the example below:

.. code-block:: typescript
   :linenos:

    function equ(a: Object, b: Object): boolean {
        return a == b
    }

    equ(1, 1) // true, values are compared
    equ(1, 2) // false, value are compared

    equ("aa", "aa") // true, string contexts are compared
    equ(1, "aa")    // false, not compatible types

    interface I1 {}
    interface I2 {}

    function equ1 (i1: I1, i2: I2) {
       return i1 == i2 // to be resolved during program execution
    }
    class A implements I1, I2 {}
    const a = new A
    equ1 (a, a) // true, the same values

An equality with values of two union types is represented in the example below:

.. code-block:: typescript
   :linenos:

    function f1(x: number | string, y: boolean | undefined): boolean {
        return x == y // Compile-time warning, always evaluates to false
    }

    function f2(x: number | string, y: boolean | "abc"): boolean {
        // OK, can be evaluated as true
        return x == y
    }

If an *equality expression* is known at compile time to always evaluate
to ``false`` or ``true`` at runtime, then a :index:`compile-time warning`
is issued as follows:

.. code-block:: typescript
   :linenos:

    5 == 5  // Compile-time warning, always true
    5 != 5  // Compile-time warning, always false
    5 === 5 // Compile-time warning, always true
    5 !== 5 // Compile-time warning, always false

    function  foo(b: boolean | undefined) {
        let n: number | boolean = 1
        b == n // Compile-time warning, expression is always false
               // (type of `n` is `number` and does not overlap with type of `b`)
        n == 1 // Compile-time warning, expression is
               // always true because `n` initialized with 1 and never modified
    }

    class B {
        f(): B|undefined { return undefined }
    }
    class D extends B {
        f(): D { return this }
    }

    function bar(c: B) {
        if (c instanceof D) {
            c.f() == undefined // warning, expression is always false
        }
    }

If two operands are of different enumeration types, then a
:index:`compile-time warning` occurs as follows:

.. code-block:: typescript
   :linenos:

    enum E1 {A, B}
    enum E2 {C, D}

    function test (e1: E1, e2: E2) {
       e1 == e2 // Compile-time warning, appears to be unintentional
    }

Numeric Equality Operators
==========================

.. meta:

Type of each operand in a ``numeric equality operator`` must be convertible
to a numeric type (see :ref:`Numeric Types`) or to a ``bigint`` type
(see :ref:`Type bigint`) as described in
:ref:`Numeric Conversions for Relational and Equality Operands`.
Otherwise, a :index:`compile-time error` occurs.

A widening conversion can occur (see :ref:`Widening Numeric Conversions`)
if type of one operand is smaller than type of the other operand (see
:ref:`Numeric Types`).

If the converted type of the operands is ``int`` or ``long``, then an
integer equality test is performed.

If the converted type is ``float`` or ``double``, then a floating-point
equality test is performed.

The floating-point equality test must be performed in accordance with the
following IEEE 754 standard rules:

-  The result of ``'=='`` or ``'==='`` is ``false`` but the result of ``'!='``
   is ``true`` if either operand is ``NaN``.

   The test ``x != x`` or ``x !== x`` is ``true`` only if *x* is ``NaN``.

-  Positive zero equals negative zero.

-  Equality operators consider two distinct floating-point values unequal
   in any other situation.

   For example, if one value represents positive infinity, and the other
   represents negative infinity, then each compares equal to itself and
   unequal to all other values.

Based on the above presumptions, the following rules apply to integer operands
or floating-point operands other than ``NaN``:

-  If the value of the left-hand-side operand is equal to that of the
   right-hand-side operand, then the operator ``'=='`` or ``'==='`` produces
   the value ``true``. Otherwise, the result is ``false``.

-  If the value of the left-hand-side operand is not equal to that of the
   right-hand-side operand, then the operator ``'!='`` or ``'!=='`` produces
   the value ``true``. Otherwise, the result is ``false``.

.. code-block:: typescript
   :linenos:

   5 == 5 // true
   5 != 5 // false

   5 === 5 // true

   5 == new Number(5) // true
   5 === new Number(5) // true

   5 == 5.0 // true

If *both* operands are of type ``bigint`` and have the same value, then the
operators ``'=='`` or ``'==='`` produce the value ``true``. Otherwise, the
result is ``false``. The result produced by ``a != b`` and ``a !== b``
is the same as the result of ``!(a == b)`` and ``!(a === b)``, respectively.

If one operand is of type ``bigint``, and the other is of a numeric type, then
the result is ``false``.

Function Type Equality Operators
================================

.. meta:

If both operands refer to the same function object, then the comparison
returns ``true``.
When comparing method references, not only the same method must be used,
but also its bounded instances must be equal.

.. code-block:: typescript
   :linenos:

    function foo() {}
    function bar() {}
    function goo(p: number) {}

    foo == foo // true, same function object
    foo == bar // false, different function objects
    foo == goo // false, different function objects

    class A {
       method() {}
       static method() {}
       foo () {}
    }
    const a = new A
    a.method == a.method // true, same function object
    A.method == A.method // true, same function object

    const aa = new A
    a.method == aa.method /* false, different function objects
         as 'a' and 'aa' are different bounded objects */
    a.method == a.foo // false, different function objects

Extended Equality with ``null`` or ``undefined``
================================================

.. meta:

ArkTS provides extended semantics for equalities with ``null`` and ``undefined``
to ensure better alignment with |TS|.

If one operand in an equality expression is ``null``, and other is ``undefined``,
then the operator ``'!='`` returns ``true``, and the operator ``'!=='`` returns
``false``:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    function foo(x: Object | null, y: Object | null | undefined) {
        console.log(x == y, x === y)
    }

    foo(null, undefined) // output: true, false
    foo(null, null)      // output: true, true

Comparison the values ``null`` and ``undefined`` directly is also allowed:

.. code-block-meta:

.. code-block:: typescript
   :linenos:

    console.log(null == undefined)  // output: true
    console.log(null === undefined) // output: false

Bitwise and Logical Expressions
*******************************

.. meta:

The *bitwise operators* and *logical operators* are as follows:

-  AND operator ``'&'``;
-  Exclusive OR operator ``'^'``; and
-  Inclusive OR operator ``'|'``.

The syntax of *bitwise and logical expression* is presented below:

.. code-block:: abnf

    bitwiseAndLogicalExpression:
        expression '&' expression
        | expression '^' expression
        | expression '|' expression
        ;

These operators have different precedence. The operator ``'&'`` has the highest,
while ``'|'`` has the lowest precedence.

Operators group left-to-right. Each operator is commutative if the
operand expressions have no side effects, and associative.

The bitwise and logical operators can compare two operands of a numeric
type, or two operands of the ``boolean`` type. Otherwise, a
:index:`compile-time error` occurs.

Integer Bitwise Operators
=========================

.. meta:

Integer bitwise operators are ``'&'``, ``'^'``, and ``'|'`` applied to operands
of numeric types or type ``bigint``.

If the type of one or both operands is ``double`` or ``float``, then the operand
or operands are truncated first to the appropriate integer type.
If the type of any operand is ``byte`` or ``short``, then the operand is
converted to ``int``.
If operands are of different integer types, then the operand of a smaller type
is converted to a larger type (see :ref:`Numeric types`) by using
:ref:`Widening Numeric Conversions`.
If both operands are of type ``bigint``, then no conversion is required.
A :index:`compile-time error` occurs if one operand of type ``bigint``, and the
other operand is of a numeric type.

The resultant type of the bitwise operator is the type of its operands.

The resultant value of ``'&'`` is the bitwise AND of the operand values.

The resultant value of ``'^'`` is the bitwise exclusive OR of the operand values.

The resultant value of ``'|'`` is the bitwise inclusive OR of the operand values.

Boolean Logical Operators
=========================

.. meta:

Boolean logical operators are ``'&'``, ``'^'``, and ``'|'`` applied to operands
of  type ``boolean``.

If both operand values are ``true``, then the resultant value of ``'&'`` is
``true``. Otherwise, the result is ``false``.

If the operand values are different, then the resultant value of ``'^'`` is
``true``. Otherwise, the result is ``false``.

If both operand values are ``false``, then the resultant value of ``'|'`` is
``false``. Otherwise, the result is ``true``.

Thus, *boolean logical expression* is of the boolean type.

Conditional-And Expression
**************************

.. meta:

The *conditional-and* operator ``'&&'`` is similar to ``'&'`` (see
:ref:`Bitwise and Logical Expressions`) but evaluates its right-hand-side
operand only if the value of the left-hand-side operand is ``true``.

The computation results of ``'&&'`` and ``'&'`` on ``boolean`` operands are
the same. The right-hand-side operand of ``'&&'`` is not necessarily evaluated.

The syntax of *conditional-and expression* is presented below:

.. code-block:: abnf

    conditionalAndExpression:
        expression '&&' expression
        ;

A *conditional-and* operator groups left-to-right.

A *conditional-and* operator is fully associative as regards both the result
value and side effects (i.e., the evaluations of the expressions *((a)* ``&&``
*(b))* ``&&`` *(c)* and *(a)* ``&&`` *((b)* ``&&`` *(c))* produce the same
result, and the same side effects occur in the same order for any *a*, *b*, and
*c*).

A *conditional-and* expression is always of type ``boolean`` except the
extended semantics (see :ref:`Extended Conditional Expressions`).

Each operand of the *conditional-and* operator must be of type ``boolean``,
or of a type mentioned in :ref:`Extended Conditional Expressions`.
Otherwise, a :index:`compile-time error` occurs.

The left-hand-side operand expression is first evaluated at runtime.

If the resultant value is ``false``, then the value of the *conditional-and*
expression is ``false``. The evaluation of the right-hand-side operand
expression is omitted.

If the value of the left-hand-side operand is ``true``, then the
right-hand-side expression is evaluated.
The resultant value is the value of the *conditional-and*
expression.

Conditional-Or Expression
*************************

.. meta:

The *conditional-or* operator ``'||'`` is similar to ``'|'`` (see
:ref:`Integer Bitwise Operators`) but evaluates its right-hand-side operand
only if the value of its left-hand-side operand is ``false``.

The syntax of *conditional-or expression* is presented below:

.. code-block:: abnf

    conditionalOrExpression:
        expression '||' expression
        ;

A *conditional-or* operator groups left-to-right.

A *conditional-or* operator is fully associative as regards both the result
value and side effects (i.e., the evaluations of the expressions *((a)* ``||``
*(b))* ``||`` *(c)* and *(a)* ``||`` *((b)* ``||`` *(c))* produce the same
result, and the same side effects occur in the same order for any *a*, *b*,
and *c*).

A *conditional-or* expression is always of type ``boolean``  except the
extended semantics (see :ref:`Extended Conditional Expressions`).

Each operand of the *conditional-or* operator must be of type ``boolean``
or type mentioned in :ref:`Extended Conditional Expressions`.
Otherwise, a :index:`compile-time error` occurs.

The left-hand-side operand expression is first evaluated at runtime.

If the resultant value is ``true``, then the value of the *conditional-or*
expression is ``true``, and the evaluation of the right-hand-side operand
expression is omitted.

If the resultant value is ``false``, then the right-hand-side expression is
evaluated.
The resultant value is the value of the *conditional-or* expression.

The computation results of ``'||'`` and ``'|'`` on ``boolean`` operands are
the same, but the right-hand-side operand in ``'||'`` cannot be evaluated.

Assignment
**********

.. meta:

All *assignment operators* group right-to-left (i.e., :math:`a=b=c` means
:math:`a=(b=c)`. The value of *c* is thus assigned to *b*, and then the value
of *b* to *a*).

The syntax of *assignment expression* is presented below:

.. code-block:: abnf

    assignmentExpression
        : lhsExpression assignmentOperator rhsExpression
        | destructuringAssignment
        ;

    ...

The first operand in an assignment operator represented by *lhsExpression* must
be a *left-hand-side expression* (see :ref:`Left-Hand-Side Expressions`). This
first operand denotes a variable.

The ``destructuringAssignment`` expression is discussed in
:ref:`Destructuring Assignment`.

Type of the variable is the type of the assignment expression.

The result of the *assignment expression* at runtime is not a variable itself
but the value of a variable after the assignment.

Simple Assignment Operator
==========================

.. meta:

The form of a simple assignment expression is ``lhsExpression = rhsExpression``.

A :index:`compile-time error` occurs in the following situations:

   - Type of *rhsExpression* is not assignable (see :ref:`Assignability`) to
     the type of a variable referred by the *lhsExpression*; or
   - Type of *lhsExpression* is one of the following:

       - ``readonly`` array (see :ref:`Readonly Parameters`), while the
         converted type of *rhsExpression* is a non-``readonly`` array;
       - ``readonly`` tuple (see :ref:`Readonly Parameters`), while the
         converted type of *rhsExpression* is a non-``readonly`` tuple.

Otherwise, the assignment expression is evaluated at runtime in one of the
following ways:

1. If *lhsExpression* is a field access expression in the form ``e.f`` (see
   :ref:`Field Access Expression`), where *e* is an expression and *f* is
   the name of the field, then:

   #. Expression *e* is evaluated: if the evaluation of *e* completes
      abruptly, then so does the assignment expression.
   #. *rhsExpression* is evaluated: if the evaluation completes abruptly, then
      so does the assignment expression.
   #. After both evaluations complete normally, the value of *rhsExpression*
      is converted to the type of the field *f*, and the result of the
      conversion is assigned to the field *f*.

2. If the *lhsExpression* is an array reference expression (see
   :ref:`Array Indexing Expression`) then:

   #. Array reference subexpression of *lhsExpression* is evaluated. If this
      evaluation completes abruptly, then so does the assignment expression. In
      that case, *rhsExpression* and the index subexpression are not evaluated,
      and no assignment occurs.
   #. If the evaluation completes normally, then the index subexpression of
      *lhsExpression* is evaluated. If this evaluation completes abruptly, then
      so does the assignment expression. In that case, *rhsExpression* is not
      evaluated, and no assignment occurs.
   #. If the evaluation completes normally, then *rhsExpression* is evaluated.
      If this evaluation completes abruptly, then so does the assignment
      expression, and no assignment occurs.
   #. If the evaluation completes normally, but the value of the index
      subexpression is less than zero, or greater than, or equal to the
      *length* of the array, then ``RangeError`` is thrown,
      and no assignment occurs.
   #. If *lhsExpression* denotes indexing of *fixed-size array*, and
      the type of *rhsExpression* is not a subtype of array element type,
      then *ArrayStoreError* is thrown, and no assignment occurs.
   #. Otherwise, the value of the index subexpression is used to select an
      element of the array referred to by the value of the array reference
      subexpression and the value of *rhsExpression* is converted to the type
      of the array element. In that case, the result of the conversion is
      assigned to the array element.

3. If *lhsExpression* is a record access expression (see
   :ref:`Record Indexing Expression`) then:

   #. Object reference subexpression of *lhsExpression* is evaluated.
      If this evaluation completes abruptly, then so does the assignment
      expression. In that case, *rhsExpression* and the index subexpression are
      not evaluated, and no assignment occurs.
   #. If the evaluation completes normally, the index subexpression of
      *lhsExpression* is evaluated. If this evaluation completes abruptly,
      then so does the assignment expression. In that case, *rhsExpression* is
      not evaluated, and no assignment occurs.
   #. If the evaluation completes normally, *rhsExpression* is evaluated. If
      this evaluation completes abruptly, then so does the assignment
      expression. In that case, no assignment occurs.
   #. Otherwise, the value of the index subexpression is used as the ``key``,
      and the value of *rhsExpression* converted to the type of the record
      value is used as the ``value``. In that case, the assignment results in
      storing the key-value pair in the record instance.

If none of the above is true, then the following three steps are performed:

#. *lhsExpression* is evaluated to produce a variable. If the evaluation
   completes abruptly, then so does the assignment expression. In that case,
   *rhsExpression* is not evaluated, and no assignment occurs.

#. If the evaluation completes normally, then *rhsExpression* is evaluated. If
   the evaluation completes abruptly, then so does the assignment expression.
   In that case, no assignment occurs.

#. If that evaluation completes normally, then the value of *rhsExpression*
   is converted to the type of the left-hand-side variable. In that case, the
   result of the conversion is assigned to the variable.

Assignment expressions for different kinds of *lhsExpression* are represented
in the example below:

.. code-block:: typescript
   :linenos:

   // Case 1: field access lhsExpression
   class A { f: double }
   new A().f = 1

   // Case 2: array indexing lhsExpression
   let b: double[] = [1, 1, 1 ]
   b[1] = 2

   // Case 3: record indexing lhsExpression
   type Keys = 'key1' | 'key2' | 'key3'
   let x: Record<Keys, number> = { 'key1': 1, 'key2': 2, 'key3': 3 }
   x['key2'] = 8

   // None of {field access|array indexing|record indexing}
   let c: double
   c = 1
   c += 2

Compound Assignment Operators
=============================

.. meta:

A compound assignment expression in the form ``lhsExpression op= rhsExpression``
is equivalent to ``lhsExpression = ((lhsExpression) op (rhsExpression)) as T``,
where ``T`` is the type of *lhsExpression*, except that *lhsExpression*
is evaluated only once.

While the nullish-coalescing assignment (``??=``) only evaluates the right
operand, and assigns to the left operand if the left operand is ``null`` or
``undefined``.

An assignment expression can be evaluated at runtime in one
of the following ways:

1. Where *lhsExpression* is not an indexing expression:

   -  *lhsExpression* is evaluated to produce a variable. If the
      evaluation completes abruptly, then so does the assignment expression.
      In that case, *rhsExpression* is not evaluated, and no
      assignment occurs.

   -  If the evaluation completes normally, then the value of *lhsExpression*
      is saved, and *rhsExpression* is evaluated. If the
      evaluation completes abruptly, then so does the assignment expression.
      In that case, no assignment occurs.

   -  If the evaluation completes normally, then the saved value of the
      left-hand-side variable, and the value of *rhsExpression* are
      used to perform the binary operation as indicated by the compound
      assignment operator. If the operation completes abruptly, then so does
      the assignment expression. In that case, no assignment occurs.

   -  If the evaluation completes normally, then the result of the binary
      operation converts to the type of the left-hand-side variable.
      The result of such conversion is stored into the variable.

2. Where *lhsExpression* is an array reference expression (see
   :ref:`Array Indexing Expression`), then:

   -  Array reference subexpression of *lhsExpression* is evaluated.
      If the evaluation completes abruptly, then so does the assignment
      expression. In that case, the index
      subexpression, and *rhsExpression* are not evaluated,
      and no assignment occurs.

   -  If the evaluation completes normally, then the index subexpression of
      *lhsExpression* is evaluated. If the evaluation completes abruptly,
      then so does the assignment expression. In that case, *rhsExpression*
      is not evaluated, and no assignment occurs.

   -  If the evaluation completes normally, the value of the array
      reference subexpression refers to an array, and the value of the
      index subexpression is less than zero, greater than, or equal to
      the *length* of the array, then ``RangeError`` is
      thrown. In that case, no assignment occurs.

   -  If the evaluation completes normally, then the value of the index
      subexpression is used to select an array element referred to by
      the value of the array reference subexpression. The value of this
      element is saved, and then *rhsExpression* is evaluated.
      If the evaluation completes abruptly, then so does the assignment
      expression. In that case, no assignment occurs.

   -  If the evaluation completes normally, consideration must be given
      to the saved value of the array element selected in the previous
      step. While this element is a variable of type ``S``, and ``T`` is
      type of *lhsExpression* of the assignment operator
      determined at compile time:

      - If ``T`` is a predefined value type, then ``S`` is the same as ``T``.

        The saved value of the array element, and the value of
        *rhsExpression* are used to perform the binary operation of the
        compound assignment operator.

        If this operation completes abruptly, then so does the assignment
        expression. In that case, no assignment occurs.

        If this evaluation completes normally, then the result of the binary
        operation converts to the type of the selected array element.
        The result of the conversion is stored into the array element.

      - If ``T`` is a reference type, then it must be ``string``.

        ``S`` must also be a ``string`` because the class ``string`` is the
        *final* class. The saved value of the array element, and the value of
        *rhsExpression* are used to perform the binary operation (string
        concatenation) of the compound assignment operator ``'+='``. If
        this operation completes abruptly, then so does the assignment
        expression. In that case, no assignment occurs.

      - If the evaluation completes normally, then the ``string`` result of
        the binary operation is stored into the array element.

3. If *lhsExpression* is a record access expression (see
   :ref:`Record Indexing Expression`):

   -  The object reference subexpression of *lhsExpression* is
      evaluated. If this evaluation completes abruptly, then so does the
      assignment expression. In that case, the index subexpression
      and *rhsExpression* are not evaluated, and no assignment occurs.

   -  If this evaluation completes normally, then the index subexpression of
      *lhsExpression* is evaluated. If the evaluation completes abruptly,
      then so does the assignment expression. In that case, *rhsExpression*
      is not evaluated, and no assignment occurs.

   -  If this evaluation completes normally, the value of the object reference
      subexpression and the value of index subexpression are saved, then
      *rhsExpression* is evaluated. If the evaluation completes
      abruptly, then so does the assignment expression. In that case, no
      assignment occurs.

   -  If this evaluation completes normally, the saved values of the object
      reference subexpression and index subexpression (as the *key*) are used
      to get the *value* that is mapped to the *key* (see
      :ref:`Record Indexing Expression`), then this *value* and the value of
      *rhsExpression* are used to perform the binary operation as
      indicated by the compound assignment operator. If the operation
      completes abruptly, then so does the assignment expression. In that case,
      no assignment occurs.

    - If the evaluation completes normally, then the result of the binary
      operation is stored as the key-value pair in the record instance
      (as in :ref:`Simple Assignment Operator`).

Left-Hand-Side Expressions
==========================

.. meta:

A *left-hand-side expression* is an *expression* that refers to one of the
following:

-  Variable (see :ref:`Named Reference`);
-  Parameter, except any parameter named ``this``
   (see :ref:`Named Reference`);
-  Field or setter resultant from a field access (see
   :ref:`Field Access Expression`); or
-  Array or record element access (see :ref:`Indexing Expressions`).

Otherwise, a :index:`compile-time error` occurs.

A :index:`compile-time error` occurs if an *expression*:

- Contains the chaining operator ``'?.'`` (see :ref:`Chaining Operator`); or
- Refers to a readonly entity.

Ternary Conditional Expressions
*******************************

.. meta:
    todo: implement full LUB support (now only basic LUB implemented)

The ternary conditional expression ``condition?whenTrue:whenFalse``
uses the boolean value of the first expression (``condition``) to
decide which of other two expressions to evaluate:

.. code-block:: abnf

    ternaryConditionalExpression:
        expression '?' expression ':' expression
        ;

The ternary conditional operator groups
right-to-left (i.e., the meaning of
:math:`a?b:c?d:e?f:g` and :math:`a?b:(c?d:(e?f:g))` is the same).

The ternary conditional operator ``condition?whenTrue:whenFalse`` consists
of three operand expressions
with the separators ``'?'`` between the first and the second expression, and
``':'`` between the second and the third expression.

.. A :index:`compile-time error` occurs if the first expression is not of type
   ``boolean``, or a type mentioned in
   :ref:`Extended Conditional Expressions`.

Type of an expression ``condition?whenTrue:whenFalse`` is determined as follows:

- If the value of ``condition`` is evaluated as ``true`` at compile time, then
  the expression has the type of ``whenTrue``.
- If the value of ``condition`` is evaluated as ``false`` at compile time, then
  the expression has the type of ``whenFalse``.
- If the value of ``condition`` is unknown at compile time, then the expression
  type is a union of types ``whenTrue`` and ``whenFalse`` further normalized
  in accordance with the process discussed in :ref:`Union Types Normalization`.

The following steps are performed as the evaluation of a ternary
conditional expression occurs at runtime:

#. The first operand (``condition``) of a ternary conditional
   expression is evaluated first.

#. If the value of the first operand is ``true``, then the second operand
   expression (``whenTrue``) is evaluated. Otherwise, the third operand
   expression (``whenFalse``) is evaluated. The result of successful
   evaluation is the result of the ternary conditional expression.

The examples below represent different scenarios with standalone expressions:

.. code-block:: typescript
   :linenos:

    class A {}
    class B extends A {}

    // Assuming value of `condition` is unknown at compile time
    condition ? new A() : new B() // A | B => A

    condition ? 5 : 6             // int

    condition ? "5" : 6           // "5" | int
    true      ? "5" : 6           // "5"
    false     ? "5" : 6           // int

String Interpolation Expressions
********************************

.. meta:

'*String interpolation expression*' is a multiline string literal, i.e., a
string literal delimited with backticks (see :ref:`Multiline String Literal` for
detail) that contains at least one *embedded expression*.

The syntax of *string interpolation expression* is presented below:

.. code-block:: abnf

    stringInterpolation:
        '`' (BackticksContentCharacter | embeddedExpression)* '`'
        ;

    embeddedExpression:
        '${' expression '}'
        ;

An '*embedded expression*' is an expression specified inside curly braces
preceded by the *dollar sign* ``'$'``. A string interpolation expression is of
type ``string`` (see :ref:`Type String`).

When evaluating a *string interpolation expression*, the result of each
embedded expression substitutes that embedded expression. An embedded
expression must be of type ``string``. Otherwise, the implicit conversion
to ``string`` takes place in the same way as with the string concatenation
operator (see :ref:`String Concatenation`):

.. code-block:: typescript
   :linenos:

    let a = 2
    let b = 2
    console.log(`The result of ${a} * ${b} is ${a * b}`)
    // prints: The result of 2 * 2 is 4

The string concatenation operator can be used to rewrite the above example
as follows:

.. code-block:: typescript
   :linenos:

    let a = 2
    let b = 2
    console.log("The result of " + a + " * " + b + " is " + a * b)

An embedded expression can contain nested multiline strings.

Lambda Expressions
******************

.. meta:

*Lambda expression* fully defines an instance of a function type (see
:ref:`Function Types`) by providing optional annotation usage
(see :ref:`Using Annotations`), optional ``async`` mark
(see :ref:`Async Lambdas`), mandatory lambda signature, and its body. The
declaration of *lambda expression* is generally similar to that of a function
declaration (see :ref:`Function Declarations`), except that a lambda expression
has no function name specified, and can have types of parameters omitted.

The syntax of *lambda expression* is presented below:

.. code-block:: abnf

    lambdaExpression:
        annotationUsage? 'async'? lambdaSignature '=>' lambdaBody
        ;

    lambdaBody:
    ...

The usage of annotations is represented in the examples below and further
discussed in :ref:`Using Annotations`:

.. code-block:: typescript
   :linenos:

    (x: number): number => { return Math.sin(x) } // block as lambda body
    (x: number) => Math.sin(x)                    // expression as lambda body
    e => e                                        // shortest form of lambda

A *lambda expression* evaluation creates an instance of a function type (see
:ref:`Function Types`) as described in detail in
:ref:`Runtime Evaluation of Lambda Expressions`.

Lambda Signature
================

.. meta:

Similarly to function declarations (see :ref:`Function Declarations`),
a *lambda signature* is composed of formal parameters and
optional return types. Type inference (see :ref:`Type Inference`) allows to
omit type annotations of formal parameters in some cases.

.. code-block:: typescript
   :linenos:

    // Lambda expressions has no type annotations

    const func: (p: Object) => Object = e => e

    function foo<T>(p: (p: T) => T) {}
    foo <Object> (e => e)

The specification of scope is discussed in :ref:`Scopes`, and shadowing details
of formal parameter declarations in :ref:`Shadowing by Parameter`.

A :index:`compile-time error` occurs if:

- Lambda expression declares two formal parameters with the same name.
- Formal parameter contains no type provided, and type cannot be derived
  by :ref:`Type Inference`.

Lambda Body
===========

.. meta:

*Lambda body* can be a single expression or a block (see :ref:`Block`).
Similarly to the body of a method or a function, a lambda body describes the
code to be executed when a lambda expression call occurs (see
:ref:`Function Call Expression`).

The meanings of names, and of the keywords ``this`` and ``super`` (along with
the accessibility of the referred declarations) are the same as in the
surrounding context. However, lambda parameters introduce new names.

If any local variable or formal parameter of the surrounding context is
used but not declared in a lambda body, then the local variable or formal
parameter is *captured* by the lambda.

If an instance member of the surrounding type is used in the lambda body
defined in a method, then ``this`` is *captured* by the lambda.

A :index:`compile-time error` occurs if a local variable is used in a lambda
body but is neither declared in nor assigned before it.

If a *lambda body* is a single ``expression``, then it is handled as follows:

-  If the expression is a *call expression* with return type ``void``, then
   the body is equivalent to the block: ``{ expression }``.

-  Otherwise, the body is equivalent to the block: ``{ return expression }``.

If *lambda signature* return type is neither ``void`` (see
:ref:`Type void or undefined`) nor ``never`` (see :ref:`Type never`), and the
execution path of the lambda body has neither a return statement (see
:ref:`Return Statements`) nor a single expression as a body, then a
:index:`compile-time error` occurs.

Lambda Expression Type
======================

.. meta:

*Lambda expression type* is a function type (see :ref:`Function Types`)
that has the following:

-  Lambda parameters (if any) as parameters of the function type; and

-  Lambda return type as the return type of the function type.

.. note::
   Lambda return type can be inferred from the *lambda body* and thus the return
   type can be dropped off.

 .. code-block:: typescript
    :linenos:

      const lambda = () => { return 123 }  // Type of the lambda is () => int
      const int_var: int = lambda()

Runtime Evaluation of Lambda Expressions
========================================

.. meta:

The evaluation of a lambda expression itself never causes the execution of the
lambda body. If completing normally at runtime, the evaluation of a lambda
expression produces a new instance of a function type (see
:ref:`Function Types`) that corresponds to the lambda signature. In that case,
it is similar to the evaluation of a class instance creation expression (see
:ref:`New Expressions`).

If the available space is not sufficient for a new instance to be created,
then the evaluation of the lambda expression completes abruptly, and
``OutOfMemoryError`` is thrown.

Every time a lambda expression is evaluated, the outer variables referred to by
the lambda expression are captured as follows:

.. code-block:: typescript
   :linenos:

     function foo() {
        let y: int = 1
        let x = () => { return y+1 } // 'y' is *captured*.
        console.log(x())             // Output: 2
     }

The captured variable is not a copy of the original variable. If the
value of the variable captured by the lambda changes, then the original
variable is implied to change:

.. code-block:: typescript
   :linenos:

     function foo() {
       let y: int = 1
       let x = () => { y++ } // 'y' is *captured*.
       console.log(y) // Output: 1
       x()
       console.log(y) // Output: 2
     }

Capturing within the function scope is highlighted by the following example:

.. code-block:: typescript
   :linenos:

     function capturingFunction() { // Function scope
       let v: number = 0 // A captured variable
       return  (p: number) => {
           console.log ("Previous value: ", v, " new value: ", p)
           v = p
       }
     }

     const func1 = capturingFunction ()
     const func2 = capturingFunction ()
     // Note: func1 and func2 are two different function type instances

     func1(11) // Previous value: 0 new value: 11
     func2(22) // Previous value: 0 new value: 22
     func1(33) // Previous value: 11 new value: 33
     func2(44) // Previous value: 22 new value: 44
     /* Note:
           func1 calls work with their own version of variable 'v'
           func2 calls work with their own version of variable 'v'
     */

Capturing within the loop scope is highlighted by the following example:

.. code-block:: typescript
   :linenos:

     const l = () => {}
     const storage = [l, l, l, l, l]  // fill array with some lambdas

     for (let index = 0; index < 5; index++) {
        storage [index] = () => { console.log ("Index ", index) }
        // Every lambda captures loop index variable
     }
     for (let index = 0; index < 5; index++) {
        storage[index]() // Captured indices printed
     }

Constant Expressions
********************

.. meta:

*Constant expressions* are expressions with values that can be evaluated at
compile time. If the evaluation *completes abruptly*, then a
:index:`compile-time error` occurs.

The syntax of *constant expression* is presented below:

.. code-block:: abnf

    constantExpression:
        expression
        ;

A *constant expression* can be either of a value type (see
:ref:`Value Types`) or of type ``string``, while being composed only of the
following:

-  Literals of a predefined value types, and literals of type ``string`` (see
   :ref:`Literals`);

-  Simple names that refer to constants declared in a surrounding block,
   function, method, or lambda body, if the initializer of the referenced
   constant declaration is itself a constant expression;

-  Unary operators ``'+'``, ``'-'``, ``'~'``, and ``'!'``, but not ``'++'``
   or ``'--'`` (see :ref:`Unary Plus`, :ref:`Unary Minus`,
   :ref:`Prefix Increment`, and :ref:`Prefix Decrement`);

-  Casting conversions to numeric types (see :ref:`Cast Expression`);

-  Multiplicative operators ``'*'``, ``'/'``, and ``'%'`` (see
   :ref:`Multiplicative Expressions`);

-  Additive operators ``'+'`` and ``'-'`` (see :ref:`Additive Expressions`);

-  Shift operators ``'<<'``, ``'>>'``, and ``'>>>'`` (see
   :ref:`Shift Expressions`);

-  Relational operators ``'<'``, ``'<='``, ``'>'``, and ``'>='`` (see
   :ref:`Relational Expressions`);

-  Equality operators ``'=='`` and ``'!='`` (see :ref:`Equality Expressions`);

-  Bitwise and logical operators ``'&'``, ``'^'``, and ``'|'`` (see
   :ref:`Bitwise and Logical Expressions`);

-  Conditional-and operator ``'&&'`` (see :ref:`Conditional-And Expression`),
   and conditional-or operator ``'||'`` (see :ref:`Conditional-Or Expression`);

-  Ternary conditional operator ``condition?whenTrue:whenFalse``
   (see :ref:`Ternary Conditional Expressions`);

-  Parenthesized expressions (see :ref:`Parenthesized Expression`) that contain
   constant expressions.

Specifics of Constant Expressions Evaluation
============================================

.. meta:

If a constant expression contains an unary or a binary operator applied
to numeric operands, the operator is evaluated as follows:

- If any of operands are of type ``double`` or the operator is
  *exponentiation operator*, other operands are converted to type ``double``
  before operator evaluation and the result type is ``double``;

- If any of operands are of type ``float``, other operands are converted
  to type ``float`` before operator evaluation and the result type is
  ``float``; or

- Otherwise, all operands are converted to *some big integer type* that allows
  handling arbitrary-precision integers (like ``bigint`` type) or integers
  larger than the maximum value of type ``long``.

If a constant expression consists of a single integer literal or
a constant of an integer type, it is also converted to the same big integer type.

:ref:`Type Inference for Constant Expressions` is always used to infer the
type of constant expression. In other words, *big integer type* is an
internal compiler type and values of this type cannot occur during execution.

In case of mixed constant expression, each numeric subexpression is evaluated
as described above:

.. code-block:: typescript
   :linenos:

    const c = 3

    c > 1 && c*2 < 8 // numeric subexpressions: (c > 1) and (c*2 < 8)

.. raw:: pdf

   PageBreak
