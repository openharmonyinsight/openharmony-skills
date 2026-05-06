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

.. _Statements:

Statements
##########

.. meta:
    frontend_status: Done

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
        i %= 100        // Statement belonging to 'block'
        console.log(i)  // Another statement belonging to 'block'
    }   //  'block' statement ends, 'if' statement end

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
        | ifStatement
        | loopStatement
        | breakStatement
        | continueStatement
        | returnStatement
        | switchStatement
        | throwStatement
        | tryStatement
        ;


The list of statements in |LANG| is as follows:

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

|

.. _Normal and Abrupt Statement Execution:

Normal and Abrupt Statement Execution
*************************************

.. meta:
    frontend_status: Done

The actions that every statement performs in a normal mode of execution are
specific for the particular kind of statement. Normal modes of evaluation for
each kind of statement are described in the following sections.

A statement execution is considered to *complete normally* if the desired
action is performed without an error being thrown. On the contrary, a statement
execution is considered to *complete abruptly* if it causes an error thrown.

.. index::
   statement
   execution
   control
   evaluation
   error
   statement execution
   normal completion
   abrupt completion
   mode of evaluation

|

.. _Expression Statements:

Expression Statements
*********************

.. meta:
    frontend_status: Done

Any expression can be used as a statement.

The syntax of an *expression statement* is presented below:

.. code-block:: abnf

    expressionStatement:
        expression
        ;

The execution of a statement leads to the execution of the expression. The
result of such execution is discarded.

.. index::
   statement
   expression
   expression statement
   syntax
   execution

|

.. _Block:

Block
*****

.. meta:
    frontend_status: Done

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

.. index::
   statement
   balanced braces
   block
   syntax
   error
   execution
   block statement
   type declaration
   return
   return type
   declaration body
   return statement

|

.. _Constant Or Variable Declarations:

Constant Or Variable Declarations
*********************************

.. meta:
    frontend_status: Done

*Constant or variable declarations* define new mutable or immutable variables within the
enclosing context.

``Let`` and ``const`` declarations have the initialization part that presumes
execution, and actually act as statements.

.. index::
   variable declaration
   constant declaration
   let declaration
   const declaration

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

.. index::
   enclosing context
   context
   mutable variable
   immutable variable
   initialization
   syntax
   execution
   function
   method
   surrounding function
   surrounding method
   block scope
   if statement
   for statement
   for-of statement
   annotation


|

.. _if Statements:

``if``  Statements
******************

.. meta:
    frontend_status: Done

An ``if`` statement allows executing alternative statements (if provided) under
certain conditions.

The syntax of an *if statement* is presented below:

.. code-block:: abnf

    ifStatement:
        'if' '(' expression ')' thenStatement
        ('else' elseStatement)?
        ;

    thenStatement:
        statement
        ;

    elseStatement:
        statement
        ;

Type of expression must be ``boolean``, or a type mentioned in
:ref:`Extended Conditional Expressions`. Otherwise, a
:index:`compile-time error` occurs.

.. index::
   if statement
   statement
   syntax
   expression
   type
   boolean type
   conditional expression

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

.. index::
   if statement
   statement
   expression
   evaluation
   block
   block scope
   scope
   else-block
   then-block

|

.. _Loop Statements:

Loop Statements
***************

.. meta:
    frontend_status: Done

|LANG| has four kinds of loops. A loop of each kind can be optionally labeled
with an *identifier*. The *identifier* can be used only by the
:ref:`Break Statements` and :ref:`Continue Statements` contained in the loop body.

.. index::
   loop statement
   loop
   loop label
   break statement
   continue statement
   identifier

The syntax of *loop statements* is presented below:

.. code-block:: abnf

    loopStatement:
        (identifier ':')?
        whileStatement
        | doStatement
        | forStatement
        | forOfStatement
        ;

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


.. index::
   loop statement
   loop
   syntax
   lambda
   lambda expression
   loop body
   label
   identifier

|

.. _While Statements and Do Statements:

``while`` Statements and ``do`` Statements
******************************************

.. meta:
    frontend_status: Done

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

    doStatement
        : 'do' statement 'while' '(' expression ')'
        ;

Type of expression must be ``boolean``, or a type mentioned in
:ref:`Extended Conditional Expressions`.
Otherwise, a :index:`compile-time error` occurs.

.. index::
   while statement
   do statement
   evaluation
   expression
   expression value
   execution
   statement
   syntax
   while statement
   do statement
   boolean type
   type
   extended conditional expression

|

.. _For Statements:

``for`` Statements
******************

.. meta:
    frontend_status: Done

The syntax of *for statements* is presented below:

.. code-block:: abnf

    forStatement:
        'for' '(' forInit? ';' forContinue? ';' forUpdate? ')' statement
        ;

    forInit:
        expressionSequence
        | variableDeclarations
        ;

    forContinue:
        expression
        ;

    forUpdate:
        expressionSequence
        ;

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

.. index::
   for statement
   syntax
   variable
   declaration
   loop index variable
   type
   inferred type
   initialization

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

|

.. _For-Of Statements:

``for-of`` Statements
*********************

.. meta:
    frontend_status: Partly
    todo: type of element for strings

A ``for-of`` loop iterates elements of an instance of an *iterable type*
(see :ref:`Iterable Types`) and executes the loop body having these elements
available.

The syntax of *for-of statements* is presented below:

.. code-block:: abnf

    forOfStatement:
        'for' '(' forVariable 'of' expression ')' statement
        ;

    forVariable:
        identifier | ('let' | 'const') identifier (':' type)?
        ;

If type of an expression is not iterable, then a :index:`compile-time error`
occurs.

The execution of a ``for-of`` loop starts from the evaluation of ``expression``.
Then, if the evaluation is successful, for every loop iteration *forVariable*
is set to the successive element as a result of iterator advancement, and the
loop body (i.e., ``statement``) is executed.

.. index::
   for-of statement
   loop
   instance
   iterable class
   iterable interface
   iterable type
   expression
   type
   array
   string
   for-of loop
   evaluation
   loop iteration
   iteration
   statement

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

.. index::
   compile-time error
   modifier
   modifier let
   let
   loop
   loop scope
   loop body
   instance
   iteration
   iterable type
   accessibility
   declaration
   inferred type
   modifier const
   const
   variable
   assignment
   modification
   for-of type annotation
   annotation
   iterator

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

.. index::
   annotation
   inferred type
   expression
   assignment

|

.. _Break Statements:

``break``  Statements
*********************

.. meta:
    frontend_status: Done
    todo: break with label causes compile time assertion

A ``break`` statement transfers control out of the enclosing ``loopStatement``
or ``switchStatement``. If a ``break`` statement is used outside a
``loopStatement`` or a ``switchStatement``, then a :index:`compile-time error`
occurs.

.. index::
   break statement
   control transfer
   compile-time error
   control transfer
   switch statement
   loop statement
   syntax

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

.. index::
   break statement
   label
   identifier
   control transfer
   statement
   enclosing statement
   surrounding function
   surrounding method
   function
   method
   label
   switch statement
   while statement
   do statement
   for statement
   for-of statement
   loop statement

|

.. _Continue Statements:

``continue`` Statements
***********************

.. meta:
    frontend_status: Done
    todo: continue with label causes compile time assertion

A ``continue`` statement terminates the execution of a current loop
iteration, and transfers control to the next iteration while keeping the
appropriate checks of the loop exit conditions in place.

The syntax of a *continue statement* is presented below:

.. code-block:: abnf

    continueStatement:
        'continue' identifier?
        ;

.. index::
   continue statement
   statement
   execution
   loop
   loop iteration
   control transfer
   iteration
   exit condition
   label
   syntax

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

.. index::
   continue statement
   control transfer
   statement
   iteration
   surrounding function
   surrounding method
   enclosing statement
   execution
   label
   label identifier
   exit condition
   loop statement
   surrounding function
   control transfer
   identifier
   function
   method

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


|

.. _return Statements:

``return`` Statements
*********************

.. meta:
    frontend_status: Done
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


.. index::
   return statement
   expression
   function body
   lambda body
   method body
   return type
   statement
   top-level statement
   function
   method
   void type
   return type
   class
   constructor
   constructor body
   return type
   statement
   syntax
   return expression
   function
   method
   lambda
   execution
   termination
   surrounding function
   function
   surrounding method
   method
   constructor
   evaluation

|

.. _Switch Statements:

``switch`` Statements
*********************

.. meta:
    frontend_status: Done
    todo: non literal constant expression () in case ==> causes an assertion error
    todo: when there is only a default clause in switchBlock then the default's statements/block are not executed

A ``switch`` statement transfers control to a statement or a block by using the
result of successful evaluation of the value of a ``switch`` expression.

.. index::
   switch statement
   control transfer
   statement
   block
   evaluation
   switch expression

The syntax of a *switch statement* is presented below:

.. code-block:: abnf

    switchStatement:
        (identifier ':')? 'switch' '(' expression ')' switchBlock
        ;

    switchBlock
        : '{' caseClause* defaultClause? caseClause* '}'
        ;

    caseClause
        : 'case' expression ':' statement*
        ;

    defaultClause
        : 'default' ':' statement*
        ;

A ``switch`` expression can be of any type.

If available, an optional identifier allows the ``break`` statement to transfer
control out of a nested ``switch`` or ``loop`` statement (see
:ref:`Break statements`).

.. index::
   syntax
   switch statement
   switch expression
   expression type
   identifier
   control transfer
   nested statement
   switch statement
   loop statement
   break statement

A :index:`compile-time error` occurs if at least one of case expression types
is not assignable (see :ref:`Assignability`) to the type of the ``switch``
statement expression.

.. index::
   expression
   expression type
   switch statement
   assignability

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

.. index::
   expression
   break
   object
   function
   execution
   switch statement
   switch expression
   expression value
   execution transfer
   evaluation
   constant
   operator
   string
   match
   break statement

|

.. _throw Statements:

``throw`` Statements
********************

.. meta:
    frontend_status: Done

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

.. index::
   throw statement
   error object
   thrown value
   thrown object
   control transfer
   statement
   method
   method call
   function
   constructor
   try block
   try statement
   value
   assignment
   assignability
   expression
   assignability
   error
   type

|

.. _Try Statements:

``try`` Statements
******************

.. meta:
    frontend_status: Done

A ``try`` statement runs block of code, and provides optional ``catch`` clause
to handle errors (see :ref:`Error Handling`) which may occur during block of
code execution.

.. index::
   try statement
   block
   catch clause

The syntax of a *try statement* is presented below:

.. code-block:: abnf

    tryStatement:
          'try' block catchClause? finallyClause?
          ;

    catchClause:
          'catch' '(' identifier ')' block
          ;

    finallyClause:
          'finally' block
          ;

A ``try`` statement must contain:

- ``finally`` clause;
- ``catch`` clause, or
- Both a ``finally`` clause and a ``catch`` clause.

Otherwise, a :index:`compile-time error` occurs.

If the ``try`` block completes normally, then no ``catch`` clause block is
executed, if present.

If an error is thrown in the ``try`` block directly or indirectly, then the
control is transferred to the ``catch`` clause, if present.

.. index::
   syntax
   catch clause
   typed catch clause
   try statement
   try block
   normal completion
   control transfer
   finally clause
   block

|

.. _Catch Clause:

``catch`` Clause
================

.. meta:
    frontend_status: Done

A ``catch`` clause consists of two parts:

-  A *catch identifier* that provides access to an object associated with
   the *error* thrown; and

-  A block of code that handles the error.

The type of *catch identifier* inside the block is ``Error`` (see
:ref:`Error Handling`).

.. index::
   catch clause
   catch identifier
   access
   error
   block
   catch identifier
   Object

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

.. index::
   catch clause
   runtime
   runtime error
   function
   divisor


|

.. _Finally Clause:

``finally`` Clause
==================

.. meta:
    frontend_status: Done

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

.. index::
   finally clause
   block
   execution
   try-catch
   normal completion
   abrupt completion
   syntax
   finally block
   execution
   return

.. code-block:: typescript

    class SomeResource {
      // Some class members
      // ...
      close() {}
    }

    function ProcessFile(name: string) {
      let r = new SomeResource()
      try {
        // Some processing
      }
      finally {
        // Finally clause is executed after try-catch
            completes normally or abruptly
        r.close()
      }
    }

|

.. _Try Statement Execution:

``try`` Statement Execution
===========================

.. meta:
    frontend_status: Done

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

.. index::
   try statement
   execution
   try block
   normal completion
   abrupt completion
   error
   catch clause
   runtime
   statement
   catch clause
   assignability
   propagation
   surrounding scope
   caller scope
   scope
   environment

.. raw:: pdf

   PageBreak
