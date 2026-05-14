Statements
##########

.. meta:

*Statements* are designed to control execution.

Some statements are simple like a single *expressionStatement* (see
:ref:`Expression Statements`), while others take several lines of program code
like :ref:`Block` or :ref:`if Statements`.

.. code-block:: typescript

    ...
    i++    // Statement consists of single expression
    ...
    if (i > 100) // 'if' statement starts
    {          // 'block' statement starts, it is a part of 'if' statement
    ...

.. note::
   The difference between statements and expressions is that :ref:`Expressions`
   evaluate a value of a certain type, while statements do not.

   From the viewpoint of grammar rules, any expression ending in the
   semicolon '``;``' forms an *expressionStatement*. A missing semicolon is added
   automatically to an expression used as a statement.

   A statement can consist of one or more expressions, or contain no expression
   at all. For example, the statement ``i = 1`` consists of an assignment
   expression that has the inferred type ``int``, and the evaluated value
   ``'1'``.

The syntax of *statements* is presented below:

.. code-block:: abnf

    statement:
        expressionStatement
        | block
        | constantOrVariableDeclaration
    ...

The list of statements in ArkTS is as follows:

.. list-table::
   :width: 100%
   :widths: 30 70
   :header-rows: 1

   * - Statement
     - Reference
   * - Expression statements
     - :ref:`Expression Statements`
   * - '{}' (block)
     - :ref:`Block`
   * - `let`, `const` (variable or constant declarations)
     - :ref:`Constant Or Variable Declarations`
   * - if-then-else
     - :ref:`if Statements`
   * - `while`, `do`, `for`, `for-of`
     - :ref:`Loop Statements`
   * - break
     - :ref:`break Statements`
   * - continue
     - :ref:`continue Statements`
   * - return
     - :ref:`return Statements`
   * - switch
     - :ref:`switch Statements`
   * - throw
     - :ref:`throw Statements`
   * - try-catch-finally
     - :ref:`try Statements`

Normal and Abrupt Statement Execution
*************************************

.. meta:

The actions that every statement performs in a normal mode of execution are
specific for the particular kind of statement. Normal modes of evaluation for
each kind of statement are described in the following sections.

A statement execution is considered to *complete normally* if the desired
action is performed without an error being thrown. On the contrary, a statement
execution is considered to *complete abruptly* if it causes an error thrown.

Expression Statements
*********************

.. meta:

Any expression can be used as a statement.

The syntax of an *expression statement* is presented below:

.. code-block:: abnf

    expressionStatement:
        expression
        ;

The execution of a statement leads to the execution of the expression. The
result of such execution is discarded.

Block
*****

.. meta:

A sequence of statements (see :ref:`Statements`) enclosed in balanced braces
forms a *block*.

The syntax of a *block statement* is presented below:

.. code-block:: abnf

    block:
        '{' statement* '}'
        ;

The execution of a block means that all block statements, except type
declarations, are executed one after another in the textual order of their
appearance within the block while an error is thrown (see :ref:`Errors`), or
until a return occurs (see :ref:`Return Statements`).

If a block is the body of a ``functionDeclaration`` (see
:ref:`Function Declarations`) or a ``classMethodDeclaration`` (see
:ref:`Method Declarations`) declared implicitly or explicitly with
return type ``void`` (see :ref:`Type void or undefined`), then the block can contain no
return statement at all. Such a block is equivalent to one that ends in a
``return`` statement, and is executed accordingly.

Constant Or Variable Declarations
*********************************

.. meta:

*Constant or variable declarations* define new mutable or immutable variables within the
enclosing context.

``Let`` and ``const`` declarations have the initialization part that presumes
execution, and actually act as statements.

The syntax of a *constant or variable declaration* is presented below:

.. code-block:: abnf

    constantOrVariableDeclaration:
        annotationUsage?
        ( variableDeclaration
        | constantDeclaration
        )
        ;

The visibility of declaration name is determined by the surrounding
module, namespace, function, or method, and by the block scope rules (see
:ref:`Scopes`). In order to avoid ambiguous interpretation, appropriate
sections of this Specification are dedicated to a detailed discussion of the
following entities: 

- :ref:`if Statements`,
- :ref:`For Statements`,
- :ref:`For-Of Statements`.

Any declaration can shadow another same-name declaration (if any) in the same
surrounding scope.

.. code-block:: typescript
   :linenos:

    let item: number = 123
    {
       const item: string = "123"
       // This 'item' is of type 'string'
    }
    // This 'item' is of type 'number'

    function foo (item: boolean) {
       // this 'item' is of type 'number'
       let item: number[] = [] // Compile-time error as parameter 'item' and
                               // local variable 'item' lead to duplication as
                               // they are in the same scope
    }

The usage of annotations is discussed in :ref:`Using Annotations`.

``if``  Statements
******************

.. meta:

An ``if`` statement allows executing alternative statements (if provided) under
certain conditions.

The syntax of an *if statement* is presented below:

.. code-block:: abnf

    ifStatement:
        'if' '(' expression ')' thenStatement
        ('else' elseStatement)?
        ;
    ...

Type of expression must be ``boolean``, or a type mentioned in
:ref:`Extended Conditional Expressions`. Otherwise, a
:index:`compile-time error` occurs.

If an expression is successfully evaluated as ``true``, then a ``thenStatement``
is executed. Otherwise, an ``elseStatement`` is executed (if provided).

Any ``else`` corresponds to the nearest preceding ``if`` of an ``if``
statement:

.. code-block:: typescript
   :linenos:

    if (Cond1)
    if (Cond2) statement1
    else statement2 // Executes only if: Cond1 && !Cond2

A :ref:`Block` can be used to combine the ``else`` part with the initial ``if``
as follows:

.. code-block:: typescript
   :linenos:

    if (Cond1) {
      if (Cond2) statement1
    }
    else statement2 // Executes if: !Cond1

If ``thenStatement`` or ``elseStatement`` is any kind of a statement but not a
block (see :ref:`Block`), then no *block scope* (see :ref:`Scopes`) is created
for such a statement.

.. code-block:: typescript
   :linenos:

    function foo(Cond1: boolean) {
      if (Cond1) let x: number = 1
      x = 2 // OK

      if (Cond1) {
        let x: number = 10;   // OK, then-block scope
        let y: number = x;
      }
      else {
        let x: number = 20   // OK, no conflict, else-block scope
        y = x;           // Compile-time error, no 'y' in scope
      }

      console.log(x)  // OK, prints 2
      console.log(y)  // Compile-time error, 'y' unknown
    }

Loop Statements
***************

.. meta:

ArkTS has four kinds of loops. A loop of each kind can be optionally labeled
with an *identifier*. The *identifier* can be used only by the
:ref:`Break Statements` and :ref:`Continue Statements` contained in the loop body.

The syntax of *loop statements* is presented below:

.. code-block:: abnf

    loopStatement:
        (identifier ':')?
        whileStatement
        | doStatement
    ...

A :index:`compile-time error` occurs if the label *identifier* is not used
within ``loopStatement``, or is used in lambda expressions (see
:ref:`Lambda Expressions`) within a loop body.

.. code-block:: typescript
   :linenos:

    label: for (i = 1; i < 10; i++) {
        const f1 = () => {
            while (true) {
                continue label // Compile-time error
            }
        }
        const f2 = () => {
            do
                break label // Compile-time error
            while (true)
        }
    }

``while`` Statements and ``do`` Statements
******************************************

.. meta:

A ``while`` statement and a ``do`` statement evaluate an expression and
execute the statement repeatedly till the expression value is ``true``.
The key difference is that a ``whileStatement`` starts from evaluating and
checking the expression value, and a ``doStatement`` starts from executing
the statement.

The syntax of *while and do statements* is presented below:

.. code-block:: abnf

    whileStatement:
        'while' '(' expression ')' statement
        ;

    ...

Type of expression must be ``boolean``, or a type mentioned in
:ref:`Extended Conditional Expressions`.
Otherwise, a :index:`compile-time error` occurs.

``for`` Statements
******************

.. meta:

The syntax of *for statements* is presented below:

.. code-block:: abnf

    forStatement:
        'for' '(' forInit? ';' forContinue? ';' forUpdate? ')' statement
        ;

    ...

Type of *forContinue* expression must be ``boolean``, or a type
mentioned in :ref:`Extended Conditional Expressions`. Otherwise, a
:index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    // The existing variable is used as a loop index variable
    let i: number
    for (i = 1; i < 10; i++) {
      console.log(i)
    }

    // A new variable is declared as a loop index variable with its type
    // explicitly specified
    for (let i: int = 1; i < 10; i++) {
      console.log(i)
    }

    // A new variable is declared as a loop index variable with its type
    // inferred from its initialization part of the declaration
    for (let i = 1; i < 10; i++) {
      console.log(i)
    }

A variable declared in the *forInit*-part has the loop scope. It can be used
in a ``forContinue`` expression, a ``forUpdate`` expression, a single-body
statement, or in a body block:

.. code-block:: typescript
   :linenos:

    // forInit declaration and no body block
    let k: int = 0
    for (let i: int = 1; i < 10; i++)
      k += i
    console.log(k)
    // i =  k  // Compile-time error if uncommented
    let i: int = k  // OK

``for-of`` Statements
*********************

.. meta:
    todo: type of element for strings

A ``for-of`` loop iterates elements of an instance of an *iterable type*
(see :ref:`Iterable Types`) and executes the loop body having these elements
available.

The syntax of *for-of statements* is presented below:

.. code-block:: abnf

    forOfStatement:
        'for' '(' forVariable 'of' expression ')' statement
        ;

    ...

If type of an expression is not iterable, then a :index:`compile-time error`
occurs.

The execution of a ``for-of`` loop starts from the evaluation of ``expression``.
Then, if the evaluation is successful, for every loop iteration *forVariable*
is set to the successive element as a result of iterator advancement, and the
loop body (i.e., ``statement``) is executed.

If *forVariable* contains modifiers ``let`` or ``const``, then *forVariable*
declares a new variable accessible inside the loop body only. Otherwise, the
variable declared elsewhere is used.

The modifier ``const`` forbids assignment into *forVariable*,
while the modifier ``let`` allows modifications.

The type of *forVariable* declared inside the loop is inferred to be that
of the *iterated* elements, namely:

-  ``T``, if ``Array<T>`` or ``FixedArray<T>`` instance is iterated;

-  ``string``, if a ``string`` value is iterated;

-  Type argument of the *iterator*, if an instance of the *iterable* type
   is iterated.

If *forVariable* is declared outside the loop, then the type of an iterated
element must be assignable (see :ref:`Assignability`) to the type of the
variable. Otherwise, a :index:`compile-time error` occurs.

.. code-block:: typescript
   :linenos:

    // The existing variable 's'
    let s : string
    for (s of "a string object") {
      console.log(s)
    }

    // New variable 's', its type is inferred from the expression after 'of'
    for (let s of "a string object") {
      console.log(s)
    }

    // New variable 'element', its type is inferred from the expression after 'of'
    // as 'const' it cannot be assigned a new value in the loop body
    for (const element of [1, 2, 3]) {
      console.log(element)
      element = 66 // Compile-time error as 'element' is 'const'
    }

Explicit type annotation of *forVariable* is allowed as an experimental
feature (see :ref:`For-of Explicit Type Annotation`).

``break``  Statements
*********************

.. meta:
    todo: break with label causes compile time assertion

A ``break`` statement transfers control out of the enclosing ``loopStatement``
or ``switchStatement``. If a ``break`` statement is used outside a
``loopStatement`` or a ``switchStatement``, then a :index:`compile-time error`
occurs.

The syntax of a *break statement* is presented below:

.. code-block:: abnf

    breakStatement:
        'break' identifier?
        ;

A ``break`` statement with the label *identifier* transfers control out of the
enclosing statement with the same label *identifier*. If there is no enclosing
loop statement with the same label identifier (within the body of the
surrounding function or method), then a :index:`compile-time error` occurs.

A statement without a label transfers control out of the innermost enclosing
``switch``, ``while``, ``do``, ``for``, or ``for-of`` statement. If
``breakStatement`` is placed outside ``loopStatement`` or ``switchStatement``,
then a :index:`compile-time error` occurs.

Examples of ``break`` statements with and without a label are presented below:

.. code-block:: typescript
   :linenos:

    // A single iteration
    while (true) {
      console.log("iteration")  // Gets printed exactly once
      break;
    }

    let a: number = 0
    outer:
      do {
        for (a = 0; a < 10; a++) {
            if (a == 1) break outer
            console.log("inner")    // Gets printed once only
        }
        console.log(a) // Never reached
      } while (true)   // Condition never used

``continue`` Statements
***********************

.. meta:
    todo: continue with label causes compile time assertion

A ``continue`` statement terminates the execution of a current loop
iteration, and transfers control to the next iteration while keeping the
appropriate checks of the loop exit conditions in place.

The syntax of a *continue statement* is presented below:

.. code-block:: abnf

    continueStatement:
        'continue' identifier?
        ;

A ``continue`` statement with no label transfers control to the next iteration
of the enclosing ``loop`` statement. If there is no enclosing ``loop`` statement
within the body of the surrounding function or method, then a
:index:`compile-time error` occurs.

A ``continue`` statement with the label *identifier* transfers control
to the next iteration of the enclosing loop statement with the same label
*identifier*.
If there is no enclosing loop statement with the same label *identifier*
(within the body of the surrounding function or method),
then a :index:`compile-time error` occurs.

Examples of ``continue`` statements with and without a label are presented below:

.. code-block:: typescript
   :linenos:

    // continue     // Compile-time error if uncommented

    // Continue without label
    // Prints 0, 1, 2, 4 (3 skipped)
    for (let a: int = 0; a < 5; a++){
      if (a == 3) continue
      console.log("a = " + a)
    }

    let a: number
    outer:
      do {
        for (a = 0; a < 10; a++) {
            if (a > 1) continue outer
            console.log("inner")    // Gets printed twice only
        }
        console.log("Outer") // Never reached
      } while (false)

``return`` Statements
*********************

.. meta:
    todo: return voidExpression

A ``return`` statement terminates the execution of a current function, method,
constructor, or lambda, and returns control to the caller. In case of a
function, method, and lambda call execution of a ``return`` statement implies
that the call returns a value defined as a result of the *return expression*
evaluation. 

The syntax of a *return statement* is presented below:

.. code-block:: abnf

    returnStatement:
        'return' expression?
        ;

If no *expression* is provided, then a *return statement* is semantically
equivalent to the form ``return undefined``.

A *return statement* in the plain form ``return`` (with no *expression*) can
occur inside one of the following:

- Constructor body;
- Function, method, or lambda body with return type ``void`` or ``undefined``
  (see :ref:`Type void or undefined`), or a union type (see :ref:`Union Types`)
  containing ``void`` or ``undefined``;
- Asynchronous function, method or lambda body with return type
  ``Promise<void>`` (see :ref:`Asynchronous execution`);

Otherwise, a :index:`compile-time error` occurs.

A :index:`compile-time error` also occurs if type of a return expression is not
assignable (see :ref:`Assignability`) to the surrounding function, method, or
lambda return type.

The semantics is represented in the examples below:

.. code-block:: typescript
   :linenos:

    return // Compile-time error, top-level statements cannot contain a return statement
    namespace NS {
       return // Compile-time error, top-level statements cannot contain a return statement
    }
    function f1 () {} // OK, no return statement equals the form 'return undefined'
    function f2 () { return } // OK, 'return' equals the form 'return undefined'
    function f3 (): void { return undefined } // Full syntax form

    function f4(cond: boolean): Base {
         if (cond) {
              return new Derived // OK, as Derived is assignable to Base
         } else {
              return new Object // Compile-time error, as Object is not assignable to Base
         }
    }
    
    class A {
        constructor () {
             return  // OK
        }
        constructor (p: number) {
             return undefined  // Compile-time error, such syntax form is forbidden
        }
    }

``switch`` Statements
*********************

.. meta:
    todo: non literal constant expression () in case ==> causes an assertion error
    todo: when there is only a default clause in switchBlock then the default's statements/block are not executed

A ``switch`` statement transfers control to a statement or a block by using the
result of successful evaluation of the value of a ``switch`` expression.

The syntax of a *switch statement* is presented below:

.. code-block:: abnf

    switchStatement:
        (identifier ':')? 'switch' '(' expression ')' switchBlock
        ;

    ...

A ``switch`` expression can be of any type.

If available, an optional identifier allows the ``break`` statement to transfer
control out of a nested ``switch`` or ``loop`` statement (see
:ref:`Break statements`).

A :index:`compile-time error` occurs if at least one of case expression types
is not assignable (see :ref:`Assignability`) to the type of the ``switch``
statement expression.

.. code-block:: typescript
   :linenos:

    let arg: string = prompt("Enter a value?");
    switch (arg) {
      case '0':
      case '1':
        console.log('One or zero')
        break
      case '2':
        console.log('Two')
        break
      default:
        console.log('An unknown value')
    }

    class A {}
    let a: A| null = assignIt()
    switch (a) {
      case null:
      case null: // One may have several case clauses with the same expression in
        console.log ("a is null")
        break
      case new A:
        console.log ("Never matches as new A is a new unique object")
        break
      default:
        console.log ("a is A")
    }
    function assignIt () {
        return new A
    }

The execution of a ``switch`` statement starts from the evaluation of the
``switch`` expression.

The value of the ``switch`` expression is compared repeatedly to the value
of case expressions. The comparison starts from the top and proceeds until the
first *match*. A *match* occurs when a particular case expression value equals
the value of the ``switch`` expression in terms of the operator ``'=='``. The
execution is transferred to the set of statements of the *caseClause* where the
match occurred. If this set of statements executes a ``break`` statement, then
the entire ``switch`` statement terminates. If no ``break`` statement is
executed, then the execution continues through statements of any remaining
*caseClause* and *defaultClause* until the first ``break`` statement occurs,
or until the ``switch`` statement ends.

If no *match* occurs while a *defaultClause* is present, then the execution is
transferred to the statements of the *defaultClause*.

``throw`` Statements
********************

.. meta:

A ``throw`` statement causes an *error* object to be created and raised
(see :ref:`Error Handling`). It immediately transfers control, and can exit
multiple statements, constructors, functions, and method calls until a ``try``
statement (see :ref:`Try Statements`) is found that catches the value thrown.
If no ``try`` statement is found, then ``UncaughtExceptionError`` is thrown.

The syntax of a *throw statement* is presented below:

.. code-block:: abnf

    throwStatement:
        'throw' expression
        ;

The expression type must be assignable (see :ref:`Assignability`) to type
``Error``. Otherwise, a :index:`compile-time error` occurs.

This implies that ``null`` or ``undefined`` cannot be thrown.

Errors can be thrown at any place in the code.

``try`` Statements
******************

.. meta:

A ``try`` statement runs block of code, and provides optional ``catch`` clause
to handle errors (see :ref:`Error Handling`) which may occur during block of
code execution.

The syntax of a *try statement* is presented below:

.. code-block:: abnf

    tryStatement:
          'try' block catchClause? finallyClause?
          ;

    ...

A ``try`` statement must contain:

- ``finally`` clause;
- ``catch`` clause, or
- Both a ``finally`` clause and a ``catch`` clause.

Otherwise, a :index:`compile-time error` occurs.

If the ``try`` block completes normally, then no ``catch`` clause block is
executed, if present.

If an error is thrown in the ``try`` block directly or indirectly, then the
control is transferred to the ``catch`` clause, if present.

``catch`` Clause
================

.. meta:

A ``catch`` clause consists of two parts:

-  A *catch identifier* that provides access to an object associated with
   the *error* thrown; and

-  A block of code that handles the error.

The type of *catch identifier* inside the block is ``Error`` (see
:ref:`Error Handling`).

.. code-block:: typescript
   :linenos:

    class ZeroDivisor extends Error {}

    function divide(a: number, b: number): number {
      if (b == 0)
        throw new ZeroDivisor()
      return a / b
    }

    function process(a: number, b: number): number {
      try {
        let res = divide(a, b)

        // Further processing ...
        return res
      }
      catch (e) {
        return e instanceof ZeroDivisor? -1 : 0
      }
    }

A ``catch`` clause handles all errors at runtime. It returns '*-1*' for
the ``ZeroDivisor``, and '*0*'  for all other errors.

``finally`` Clause
==================

.. meta:

A ``finally`` clause defines the set of actions in the form of a block to be
executed without regard to whether a ``try-catch`` completes normally or
abruptly.

The syntax of a *finally clause* is presented below:

.. code-block:: abnf

    finallyClause:
        'finally' block
        ;

A ``finally`` block is executed without regard to how (by reaching ``return``
or ``try-catch`` end or raising new *error*) the program control is
transferred out. The ``finally`` block is particularly useful to ensure
proper resource management.

Any required actions (e.g., flush buffers and close file descriptors)
can be performed while leaving the ``try-catch``:

.. code-block:: typescript

    class SomeResource {
      // Some class members
      // ...
      close() {}
    }
    ...

``try`` Statement Execution
===========================

.. meta:

#. A ``try`` block and the entire ``try`` statement complete normally if no
   ``catch`` block is executed. The execution of a ``try`` block completes
   abruptly if an error is thrown inside the ``try`` block.

#. The execution of a ``try`` block completes abruptly if error *x* is
   thrown inside the ``try`` block. If the ``catch`` clause is present, and the
   execution of the body of the ``catch`` clause completes normally, then the
   entire ``try`` statement completes normally. Otherwise, the ``try``
   statement completes abruptly.

#. If no ``catch`` clause is in place, then the error is propagated to the
   surrounding and caller scopes until reaching the scope with the ``catch``
   clause to handle the error. Subsequent steps are then defined by the
   execution environment.

#. If ``finally`` clause is in place, and its execution completes abruptly, then
   the ``try`` statement also completes abruptly.

.. raw:: pdf

   PageBreak
