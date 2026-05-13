Annotations
###########

.. meta:

*Annotation* is a special language element that changes the semantics of
the declaration to which it is applied by adding metadata.

Declaring and using an annotation is represented in the example below:

.. code-block:: typescript
   :linenos:

    // Annotation declaration:
    @interface ClassAuthor {
        authorName: string
    }

    // Annotation use:
    @ClassAuthor({authorName: "Bob"})
    class MyClass {/*body*/}

The annotation *ClassAuthor* in the example above adds metadata to
the class declaration.

An annotation must be placed immediately before the declaration to which it is
applied. An annotation can include arguments as in the example above.

For an annotation to be used, the name of the annotation must be prefixed with
the character '``@``' (e.g., ``@MyAnno``). No white space and line separator is
allowed between the character '``@``' and the name:

.. code-block::
   :linenos:

    ClassAuthor({authorName: "Bob"}) // Compile-time error, no '@'
    @ ClassAuthor({authorName: "Bob"}) // Compile-time error, space is forbidden

A :index:`compile-time error` occurs if the annotation name is not accessible
(see :ref:`Accessible`) at the place of use. An annotation declaration can be
exported and used in other modules.

Multiple annotations can be applied to a single declaration:

.. code-block:: typescript
   :linenos:

    @MyAnno()
    @ClassAuthor({authorName: "John Smith"})
    class MyClass {/*body*/}

Declaring Annotations
*********************

.. meta:

Declaring an *annotation* is similar to declaring an interface where the
keyword ``interface`` is prefixed with the character ``'@'``.

The syntax of *annotation declaration* is presented below:

.. code-block:: abnf

    annotationDeclaration:
        '@interface' identifier '{' annotationField* '}'
        ;
    annotationField:
    ...

As any other declared entity, an annotation can be exported by using the
keyword ``export``.

*Type* in the annotation field is restricted (see :ref:`Types of Annotation Fields`).

The default value of an *annotation field* can be specified by using
*initializer* as *constant expression*. A :index:`compile-time error`
occurs if the value of this expression cannot be evaluated at compile time.

*Annotation* must be defined at the top level. Otherwise, a
:index:`compile-time error` occurs.

*Annotation* cannot be extended as inheritance is not supported.

The name of an *annotation* cannot coincide with the name of another entity:

.. code-block:: typescript
   :linenos:

    @interface Position {/*properties*/}

    class Position {/*body*/} // Compile-time error, duplicate identifier

An annotation declaration defines no type. No type alias can be applied to
the annotation or used as an interface:

.. code-block:: typescript
   :linenos:

    @interface Position {}
    type Pos = Position // Compile-time error

    class A implements Position {} // Compile-time error

Types of Annotation Fields
==========================

.. meta:

The choice of *types for annotation fields* is limited to the following:

- :ref:`Numeric Types`;
- Type ``boolean`` (see :ref:`Type boolean`);
- :ref:`Type string`;
- Enumeration types (see :ref:`Enumerations`);
- Array of the above types (e.g., ``string[]``), including arrays of arrays
  (e.g., ``string[][]``).

A :index:`compile-time error` occurs if any other type is used as the type of
an *annotation field*.

Using Annotations
*****************

.. meta:

The following syntax is used to apply an annotation to a declaration,
and to define the values of annotation fields:

.. code-block:: abnf

    annotationUsage:
        AnnotationUsageNoParentheses |
        annotationUsageWithParentheses
        ;
    ...

An annotation declaration is represented in the example below:

.. code-block:: typescript
   :linenos:

    @interface ClassPreamble {
        authorName: string
        revision: number = 1
    }
    @interface MyAnno{}

In general, annotation field values are set by an *object literal*. In a
special case, an annotation field value is set by using an expression (see
:ref:`Using Single Field Annotations`).

A value for an annotation field must be:

- a constant expression, if the field is not of an array type; or

- an :ref:`Array Literal` with elements that are either
  constant expressions or, in case of array of array,
  enclosed array literals with constant expressions.

Otherwise, a :index:`compile-time error` occurs.

The use of annotation is presented in the example below. The annotations in
this example are applied to class declarations:

.. code-block:: typescript
   :linenos:

    @ClassPreamble({authorName: "John", revision: 2})
    class C1 {/*body*/}

    @ClassPreamble({authorName: "Bob"}) // default value for revision = 1
    class C2 {/*body*/}

    @MyAnno()
    class C3 {/*body*/}

Annotations can be applied to the following:

- :ref:`Top-Level Declarations`;

- Class members (see :ref:`Class Members`) except overridden fields
  (see the example below);

- Interface members (see :ref:`Interface Members`);

- Type usage (see :ref:`Using Types`);

- Parameters (see :ref:`Parameter List` and :ref:`Optional Parameters`);

- Lambda expression (see :ref:`Lambda Expressions` and
  :ref:`Lambda Expressions with Receiver`);

- :ref:`Constant Or Variable Declarations`.

Otherwise, a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    function foo () @MyAnno() {} // wrong target for annotation

A :index:`compile-time error` occurs if an annotation is applied to 
an overridden field (see :ref:`Override Fields`):

.. code-block:: typescript
   :linenos:

    class C {
        field: int = 1
    }
    class D extends C {
        @MyAnno() // Compile-time error
        field: int = 2
    }

Repeatable annotations are not supported, i.e., an annotation can be applied
to an entity no more than once:

.. code-block:: typescript
   :linenos:

    @ClassPreamble({authorName: "John"})
    @ClassPreamble({authorName: "Bob"}) // Compile-time error
    class C {/*body*/}

When using an annotation, the order of values has no significance:

.. code-block:: typescript
   :linenos:

    @ClassPreamble({authorName: "John", revision: 2})
    // the same as:
    @ClassPreamble({revision: 2, authorName: "John"})

When using an annotation, all fields without default values must be listed.
Otherwise, a :index:`compile-time error` occurs:

.. code-block:: typescript
   :linenos:

    @ClassPreamble() // Compile-time error, authorName is not defined
    class C1 {/*body*/}

If a field of an array type for an annotation is defined, then its value is set
by using the array literal syntax:

.. code-block:: typescript
   :linenos:

    @interface ClassPreamble {
        authorName: string
        revision: number = 1
        reviewers: string[]
    }

    @ClassPreamble(
        {authorName: "Alice",
        reviewers: ["Bob", "Clara"]}
    )
    class C3 {/*body*/}

If setting annotation properties is not required, then parentheses can be
omitted after the annotation name:

.. code-block:: typescript
   :linenos:

    @MyAnno
    class C4 {/*body*/}

Using Single Field Annotations
==============================

.. meta:

If annotation declaration defines only one field, then it can be used with a
short notation to specify just one expression instead of an object literal:

.. code-block:: typescript
   :linenos:

    @interface deprecated{
        fromVersion: string
    }

    @deprecated("5.18")
    function foo() {}

    @deprecated({fromVersion: "5.18"})
    function goo() {}

A short notation and a notation with an object literal behave in exactly the
same manner.

Exporting and Importing Annotations
***********************************

.. meta:

An annotation can be exported and imported. However, a few forms of export and
import directives are supported.

An annotation declaration to be exported must be marked with the keyword
``export`` as follows:

.. code-block:: typescript
   :linenos:

    // a.ets
    export @interface MyAnno {}

If an annotation is imported as a part of an imported module, then the
annotation is accessed by its qualified name:

.. code-block:: typescript
   :linenos:

    // b.ets
    import * as ns from "./a"

    @ns.MyAnno
    class C {/*body*/}

Unqualified import is also allowed:

.. code-block:: typescript
   :linenos:

    // b.ets
    import { MyAnno } from "./a"

    @MyAnno
    class C {/*body*/}

An annotation declaration does not define a type. Using ``export type``
or ``import type`` notations to export or import an annotation causes a
:index:`compile-time error`:

.. code-block:: typescript
   :linenos:

    import type { MyAnno } from "./a" // Compile-time error

If annotations are used in the following cases, then a
:index:`compile-time error` also occurs:

- Export default,

- Import default,

- Rename in export, and

- Rename in import.

.. code-block:: typescript
   :linenos:

    import {MyAnno as Anno} from "./a" // Compile-time error

Ambient Annotations
*******************

.. meta:

The syntax of *ambient annotations* is presented below:

.. code-block:: abnf

    ambientAnnotationDeclaration:
        'declare' annotationDeclaration
        ;

Such a declaration does not introduce a new annotation but provides type
information that is required to use the annotation. The annotation itself
must be defined elsewhere. A :index:`runtime error` occurs if no annotation
corresponds to the ambient annotation used in the program.

An ambient annotation and the annotation that implements it must be exactly
identical, including field initialization:

.. code-block:: typescript
   :linenos:

    // a.d.ets
    export declare @interface NameAnno{name: string = ""}

    // a.ets
    export @interface NameAnno{name: string = ""} // OK

The code in the example below is incorrect because the ambient declaration is
not identical to the annotation declaration:

.. code-block:: typescript
   :linenos:

    // a.d.ets
    export declare @interface VersionAnno{version: number} // initialization is missing

    // a.ets
    export @interface VersionAnno{version: number = 1}

An ambient declaration can be imported and used in exactly the same manner
as a regular annotation:

.. code-block:: typescript
   :linenos:

    // a.d.ets
    export declare @interface MyAnno {}

    // b.ets
    import { MyAnno } from "./a"

    @MyAnno
    class C {/*body*/}

If an annotation is applied to an ambient declaration in the *.d.ets* file (see
the example below), then the annotation is to be applied to the implementation
declaration manually, because the annotation is not automatically applied to
the declaration that implements the ambient declaration:

.. code-block:: typescript
   :linenos:

    // a.d.ets
    export declare @interface MyAnno {}

    @MyAnno
    declare class C {}

Standard Annotations
********************

.. meta:

*Standard annotation* is an annotation that is defined in
:ref:`Standard Library`, or implicitly defined in the compiler
(*built-in annotation*).
*Standard annotation* is usually known to the compiler. It modifies the
semantics of the declaration it is applied to.

An annotation that annotates a declaration of another annotation is called
*meta-annotation*.

Retention Annotation
====================

.. meta:

``@Retention`` is a standard *meta-annotation* that is used to annotate
a declaration of another annotation.
A :index:`compile-time error` occurs if it is used in other places.

The annotation has a single field ``policy`` of type ``string``. It is typically
used as follows:

.. code-block:: typescript
   :linenos:

    @Retention({policy: "RUNTIME"})
    @interface MyAnno {} // this annotation uses "RUNTIME" policy

    @MyAnno //
    class C {}

The value of this field determines at which point an annotation is used,
and discarded after use.
The retention policies can be of three types:

- "SOURCE"

  Annotations that use "SOURCE" policy are processed at compile time, and are
  discarded after compilation;

- "BYTECODE"

  Metadata specified in annotations that use "BYTECODE" policy are saved into
  the bytecode file, but are discarded at runtime.

- "RUNTIME"

  Metadata specified in annotations that use "RUNTIME" policy are saved into
  the bytecode file, are retained and can be accessed at runtime.

The default retention policy is "BYTECODE".

A :index:`compile-time error` occurs if any other string literal is used as
the value of ``policy`` field.

As ``@Retention`` has a single field, it can be used with a short notation
(see :ref:`Using Single Field Annotations`) as follows:

.. code-block:: typescript
   :linenos:

    @Retention("SOURCE")
    @interface Author {name: string} // this annotation uses "SOURCE" policy

Target Annotation
=================

.. meta:

``@Target`` is a standard *meta-annotation* that is used to annotate
a declaration of another annotation. A :index:`compile-time error` occurs
if ``@Target`` is used elsewhere.

``@Target`` specifies the set of source code contexts in which the declared
annotation can be used. The contexts are specified by using a set of values
of an ``AnnotationTargets`` enumeration defined in :ref:`Standard Library`.

The annotation ``@Target`` has a single field ``targets`` of type
``AnnotationTargets[]``. It is typically used as follows:

.. code-block:: typescript
   :linenos:

    // short form:
    @Target(["FUNCTION", "CLASS_METHOD"])
    @interface SpecialCall {/*some fields*/}

    // long form:
    @Target({targets: ["PARAMETER"]})
    @interface SpecialParameter {/*some fields*/}

If the annotation is present in the declaration of annotation ``X``, then
the compiler checks that ``X`` is used in the specified contexts only.
Otherwise, a :index:`compile-time error` occurs.

If no annotation is present in the declaration of annotation ``X``, then
the usage of ``X`` is not restricted.

An ``AnnotationTargets`` union type contains string literals for the following
targets:

-  Targets for :ref:`Top-Level Declarations`:

    - ``"CLASS"``;
    - ``"ENUMERATION"``;
    - ``"FUNCTION"``;
    - ``"FUNCTION_WITH_RECEIVER"``;
    - ``"INTERFACE"``;
    - ``"NAMESPACE"``;
    - ``"TYPE_ALIAS"``;
    - ``"VARIABLE"``;

-  Targets for :ref:`Class Members`:

    - ``"CLASS_FIELD"``;
    - ``"CLASS_METHOD"``;
    - ``"CLASS_GETTER"``;
    - ``"CLASS_SETTER"``;

-  Targets for :ref:`Interface Members`:

    - ``"INTERFACE_METHOD"``;
    - ``"INTERFACE_GETTER"``;
    - ``"INTERFACE_SETTER"``;

-  Other targets:

    - ``"LAMBDA"`` for :ref:`Lambda Expressions` and
      :ref:`Lambda Expressions with Receiver`;
    - ``"PARAMETER"`` for function, method, and lambda parameter;
    - ``"STRUCT"`` (see :ref:`Keyword struct and ArkUI`);
    - ``"TYPE"`` (see :ref:`Using Types`).

A :index:`compile-time error` occurs if an enumeration member is used more
than once in an ``@Target`` annotation:

.. code-block:: typescript
   :linenos:

    @Target(["CLASS", "INTERFACE", "CLASS"]) // Compile-time error
    @interface Anno {}

Runtime Access to Annotations
*****************************

.. meta:

For an annotation with *retention policy* (see :ref:`Retention Annotation`)
``BYTECODE`` or ``RUNTIME`` an abstract class with the name of the annotation
is implicitly declared. All fields of this class are ``readonly``.
If a field is of an array type, the array type is also ``readonly``.

For the following annotation:

.. code-block:: typescript
   :linenos:

    @Retention("RUNTIME")
    @interface MyAnno {
        name: string
        attrs: number[]
    }

--the abstract class is declared:

.. code-block:: typescript
   :linenos:

    abstract class MyAnno {
        readonly name: string
        readonly attrs: readonly number[]
    }

The use of such a class is represented in following example:

.. code-block:: typescript
   :linenos:

    @MyAnno({name: "someName", attr: [1, 2]})
    class A {}

    let my: MyAnno = // call of reflection library to get instance of annotation for type A
    console.log(my.name) // output: someName

.. raw:: pdf

   PageBreak
