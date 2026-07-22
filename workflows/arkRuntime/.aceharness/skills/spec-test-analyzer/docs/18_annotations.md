# Annotations {#Annotations}

*Annotation* is a special language element that changes the semantics of
the declaration to which it is applied by adding metadata.

Declaring and using an annotation is represented in the example below:

``` {.typescript}
// Annotation declaration:
@interface ClassAuthor {
    authorName: string
}

// Annotation use:
@ClassAuthor({authorName: "Bob"})
class MyClass {/*body*/}
```

The annotation *ClassAuthor* in the example above adds metadata to
the class declaration.

An annotation must be placed immediately before the declaration to which it is
applied. An annotation can include arguments as in the example above.

For an annotation to be used, the name of the annotation must be prefixed with
the character \'`@`\' (e.g., `@MyAnno`). No white space and line separator is
allowed between the character \'`@`\' and the name:

::: {.index}
annotation
semantics
language element
metadata
declaration
class declaration
prefix
space
white space
line separator
argument
name
:::

``` {.}
ClassAuthor({authorName: "Bob"}) // Compile-time error, no '@'
@ ClassAuthor({authorName: "Bob"}) // Compile-time error, space is forbidden
```

A `compile-time error`{.interpreted-text role="index"} occurs if the annotation name is not accessible
(see `Accessible`{.interpreted-text role="ref"}) at the place of use. An annotation declaration can be
exported and used in other modules.

Multiple annotations can be applied to a single declaration:

``` {.typescript}
@MyAnno()
@ClassAuthor({authorName: "John Smith"})
class MyClass {/*body*/}
```

::: {.index}
annotation
access
accessibility
annotation declaration
declaration
:::

| 

## Declaring Annotations {#Declaring Annotations}

Declaring an *annotation* is similar to declaring an interface where the
keyword `interface` is prefixed with the character `'@'`.

The syntax of *annotation declaration* is presented below:

``` {.abnf}
annotationDeclaration:
    '@interface' identifier '{' annotationField* '}'
    ;
annotationField:
    identifier ':' type constInitializer?
    ;
constInitializer:
    '=' constantExpression
    ;
```

As any other declared entity, an annotation can be exported by using the
keyword `export`.

*Type* in the annotation field is restricted (see `Types of Annotation Fields`{.interpreted-text role="ref"}).

The default value of an *annotation field* can be specified by using
*initializer* as *constant expression*. A `compile-time error`{.interpreted-text role="index"}
occurs if the value of this expression cannot be evaluated at compile time.

::: {.index}
annotation
declaration
interface
interface keyword
prefix
export keyword
syntax
annotation declaration
annotation field
declared entity
constant expression
compile time
initializer
expression
value
type
:::

*Annotation* must be defined at the top level. Otherwise, a
`compile-time error`{.interpreted-text role="index"} occurs.

*Annotation* cannot be extended as inheritance is not supported.

The name of an *annotation* cannot coincide with the name of another entity:

``` {.typescript}
@interface Position {/*properties*/}

class Position {/*body*/} // Compile-time error, duplicate identifier
```

An annotation declaration defines no type. No type alias can be applied to
the annotation or used as an interface:

``` {.typescript}
@interface Position {}
type Pos = Position // Compile-time error

class A implements Position {} // Compile-time error
```

::: {.index}
annotation
type alias
inheritance
annotation declaration
interface
entity
type
:::

| 

### Types of Annotation Fields {#Types of Annotation Fields}

The choice of *types for annotation fields* is limited to the following:

-   `Numeric Types`{.interpreted-text role="ref"};
-   Type `boolean` (see `Type boolean`{.interpreted-text role="ref"});
-   `Type string`{.interpreted-text role="ref"};
-   Enumeration types (see `Enumerations`{.interpreted-text role="ref"});
-   Array of the above types (e.g., `string[]`), including arrays of arrays
    (e.g., `string[][]`).

A `compile-time error`{.interpreted-text role="index"} occurs if any other type is used as the type of
an *annotation field*.

::: {.index}
annotation field
type for annotation field
numeric type
boolean type
string type
enumeration type
array
:::

| 

## Using Annotations {#Using Annotations}

The following syntax is used to apply an annotation to a declaration,
and to define the values of annotation fields:

``` {.abnf}
annotationUsage:
    AnnotationUsageNoParentheses |
    annotationUsageWithParentheses
    ;

annotationUsageNoParentheses:
    '@' qualifiedName
    ;

annotationUsageWithParentheses:
    '@' qualifiedName annotationValues
    ;
annotationValues:
    '(' (objectLiteral | constantExpression)? ')'
    ;
```

An annotation declaration is represented in the example below:

``` {.typescript}
@interface ClassPreamble {
    authorName: string
    revision: number = 1
}
@interface MyAnno{}
```

In general, annotation field values are set by an *object literal*. In a
special case, an annotation field value is set by using an expression (see
`Using Single Field Annotations`{.interpreted-text role="ref"}).

A value for an annotation field must be:

-   a constant expression, if the field is not of an array type; or
-   an `Array Literal`{.interpreted-text role="ref"} with elements that are either
    constant expressions or, in case of array of array,
    enclosed array literals with constant expressions.

Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
annotation
annotation declaration
syntax
declaration
annotation field
object literal
value
expression
:::

The use of annotation is presented in the example below. The annotations in
this example are applied to class declarations:

``` {.typescript}
@ClassPreamble({authorName: "John", revision: 2})
class C1 {/*body*/}

@ClassPreamble({authorName: "Bob"}) // default value for revision = 1
class C2 {/*body*/}

@MyAnno()
class C3 {/*body*/}
```

Annotations can be applied to the following:

-   `Top-Level Declarations`{.interpreted-text role="ref"};
-   Class members (see `Class Members`{.interpreted-text role="ref"}) except overridden fields
    (see the example below);
-   Interface members (see `Interface Members`{.interpreted-text role="ref"});
-   Type usage (see `Using Types`{.interpreted-text role="ref"});
-   Parameters (see `Parameter List`{.interpreted-text role="ref"} and `Optional Parameters`{.interpreted-text role="ref"});
-   Lambda expression (see `Lambda Expressions`{.interpreted-text role="ref"} and
    `Lambda Expressions with Receiver`{.interpreted-text role="ref"});
-   `Constant Or Variable Declarations`{.interpreted-text role="ref"}.

::: {.index}
annotation
declaration
class declaration
top-level declaration
class
type
interface
method
parameter
optional parameter
lambda expression
lambda expression with receiver
function
local declaration
:::

Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs:

``` {.typescript}
function foo () @MyAnno() {} // wrong target for annotation
```

A `compile-time error`{.interpreted-text role="index"} occurs if an annotation is applied to
an overridden field (see `Override Fields`{.interpreted-text role="ref"}):

``` {.typescript}
class C {
    field: int = 1
}
class D extends C {
    @MyAnno() // Compile-time error
    field: int = 2
}
```

Repeatable annotations are not supported, i.e., an annotation can be applied
to an entity no more than once:

``` {.typescript}
@ClassPreamble({authorName: "John"})
@ClassPreamble({authorName: "Bob"}) // Compile-time error
class C {/*body*/}
```

When using an annotation, the order of values has no significance:

``` {.typescript}
@ClassPreamble({authorName: "John", revision: 2})
// the same as:
@ClassPreamble({revision: 2, authorName: "John"})
```

When using an annotation, all fields without default values must be listed.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs:

``` {.typescript}
@ClassPreamble() // Compile-time error, authorName is not defined
class C1 {/*body*/}
```

::: {.index}
annotation
repeatable annotation
entity
array literal
array type
value
field
:::

If a field of an array type for an annotation is defined, then its value is set
by using the array literal syntax:

``` {.typescript}
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
```

If setting annotation properties is not required, then parentheses can be
omitted after the annotation name:

``` {.typescript}
@MyAnno
class C4 {/*body*/}
```

::: {.index}
field
array type
annotation
syntax
array literal
parentheses
annotation name
:::

| 

### Using Single Field Annotations {#Using Single Field Annotations}

If annotation declaration defines only one field, then it can be used with a
short notation to specify just one expression instead of an object literal:

``` {.typescript}
@interface deprecated{
    fromVersion: string
}

@deprecated("5.18")
function foo() {}

@deprecated({fromVersion: "5.18"})
function goo() {}
```

A short notation and a notation with an object literal behave in exactly the
same manner.

::: {.index}
field annotation
annotation declaration
field
notation
expression
object literal
:::

| 

## Exporting and Importing Annotations {#Exporting and Importing Annotations}

An annotation can be exported and imported. However, a few forms of export and
import directives are supported.

An annotation declaration to be exported must be marked with the keyword
`export` as follows:

``` {.typescript}
// a.ets
export @interface MyAnno {}
```

If an annotation is imported as a part of an imported module, then the
annotation is accessed by its qualified name:

``` {.typescript}
// b.ets
import * as ns from "./a"

@ns.MyAnno
class C {/*body*/}
```

Unqualified import is also allowed:

::: {.index}
export
import
annotation
annotation declaration
export keyword
import directive
export directive
imported module
qualified name
access
unqualified import
:::

``` {.typescript}
// b.ets
import { MyAnno } from "./a"

@MyAnno
class C {/*body*/}
```

An annotation declaration does not define a type. Using `export type`
or `import type` notations to export or import an annotation causes a
`compile-time error`{.interpreted-text role="index"}:

``` {.typescript}
import type { MyAnno } from "./a" // Compile-time error
```

If annotations are used in the following cases, then a
`compile-time error`{.interpreted-text role="index"} also occurs:

-   Export default,
-   Import default,
-   Rename in export, and
-   Rename in import.

::: {.index}
annotation
export type
import type
import annotation
export annotation
annotation
notation
type
notation
import annotation
export default
import default
renaming
:::

``` {.typescript}
import {MyAnno as Anno} from "./a" // Compile-time error
```

| 

## Ambient Annotations {#Ambient Annotations}

The syntax of *ambient annotations* is presented below:

``` {.abnf}
ambientAnnotationDeclaration:
    'declare' annotationDeclaration
    ;
```

Such a declaration does not introduce a new annotation but provides type
information that is required to use the annotation. The annotation itself
must be defined elsewhere. A `runtime error`{.interpreted-text role="index"} occurs if no annotation
corresponds to the ambient annotation used in the program.

An ambient annotation and the annotation that implements it must be exactly
identical, including field initialization:

::: {.index}
syntax
ambient annotation
declaration
annotation
type
runtime error
field initialization
initialization
:::

``` {.typescript}
// a.d.ets
export declare @interface NameAnno{name: string = ""}

// a.ets
export @interface NameAnno{name: string = ""} // OK
```

The code in the example below is incorrect because the ambient declaration is
not identical to the annotation declaration:

``` {.typescript}
// a.d.ets
export declare @interface VersionAnno{version: number} // initialization is missing

// a.ets
export @interface VersionAnno{version: number = 1}
```

An ambient declaration can be imported and used in exactly the same manner
as a regular annotation:

``` {.typescript}
// a.d.ets
export declare @interface MyAnno {}

// b.ets
import { MyAnno } from "./a"

@MyAnno
class C {/*body*/}
```

If an annotation is applied to an ambient declaration in the *.d.ets* file (see
the example below), then the annotation is to be applied to the implementation
declaration manually, because the annotation is not automatically applied to
the declaration that implements the ambient declaration:

``` {.typescript}
// a.d.ets
export declare @interface MyAnno {}

@MyAnno
declare class C {}
```

::: {.index}
annotation declaration
initialization
import
annotation
ambient declaration
declaration
implementation
:::

| 

## Standard Annotations {#Standard Annotations}

*Standard annotation* is an annotation that is defined in
`Standard Library`{.interpreted-text role="ref"}, or implicitly defined in the compiler
(*built-in annotation*).
*Standard annotation* is usually known to the compiler. It modifies the
semantics of the declaration it is applied to.

An annotation that annotates a declaration of another annotation is called
*meta-annotation*.

::: {.index}
standard annotation
annotation
standard annotation
compiler
built-in annotation
call
semantics
declaration
meta-annotation
:::

| 

### Retention Annotation {#Retention Annotation}

`@Retention` is a standard *meta-annotation* that is used to annotate
a declaration of another annotation.
A `compile-time error`{.interpreted-text role="index"} occurs if it is used in other places.

The annotation has a single field `policy` of type `string`. It is typically
used as follows:

``` {.typescript}
@Retention({policy: "RUNTIME"})
@interface MyAnno {} // this annotation uses "RUNTIME" policy

@MyAnno //
class C {}
```

::: {.index}
meta-annotation
retention annotation
standard annotation
annotation
declaration
declaration annotation
field
string type
:::

The value of this field determines at which point an annotation is used,
and discarded after use.
The retention policies can be of three types:

-   \"SOURCE\"

    Annotations that use \"SOURCE\" policy are processed at compile time, and are
    discarded after compilation;

-   \"BYTECODE\"

    Metadata specified in annotations that use \"BYTECODE\" policy are saved into
    the bytecode file, but are discarded at runtime.

-   \"RUNTIME\"

    Metadata specified in annotations that use \"RUNTIME\" policy are saved into
    the bytecode file, are retained and can be accessed at runtime.

The default retention policy is \"BYTECODE\".

A `compile-time error`{.interpreted-text role="index"} occurs if any other string literal is used as
the value of `policy` field.

As `@Retention` has a single field, it can be used with a short notation
(see `Using Single Field Annotations`{.interpreted-text role="ref"}) as follows:

``` {.typescript}
@Retention("SOURCE")
@interface Author {name: string} // this annotation uses "SOURCE" policy
```

::: {.index}
source
runtime
value
field
compile time
bytecode
metadata
annotation
policy
bytecode file
string literal
notation
:::

| 

### Target Annotation {#Target Annotation}

`@Target` is a standard *meta-annotation* that is used to annotate
a declaration of another annotation. A `compile-time error`{.interpreted-text role="index"} occurs
if `@Target` is used elsewhere.

`@Target` specifies the set of source code contexts in which the declared
annotation can be used. The contexts are specified by using a set of values
of an `AnnotationTargets` enumeration defined in `Standard Library`{.interpreted-text role="ref"}.

The annotation `@Target` has a single field `targets` of type
`AnnotationTargets[]`. It is typically used as follows:

::: {.index}
target annotation
annotation
meta-annotation
declaration
source code
context
value
:::

``` {.typescript}
// short form:
@Target(["FUNCTION", "CLASS_METHOD"])
@interface SpecialCall {/*some fields*/}

// long form:
@Target({targets: ["PARAMETER"]})
@interface SpecialParameter {/*some fields*/}
```

If the annotation is present in the declaration of annotation `X`, then
the compiler checks that `X` is used in the specified contexts only.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

If no annotation is present in the declaration of annotation `X`, then
the usage of `X` is not restricted.

An `AnnotationTargets` union type contains string literals for the following
targets:

::: {.index}
annotation
declaration
compiler
compiler check
context
restriction
enumeration
constant
:::

-   Targets for `Top-Level Declarations`{.interpreted-text role="ref"}:

    > -   `"CLASS"`;
    > -   `"ENUMERATION"`;
    > -   `"FUNCTION"`;
    > -   `"FUNCTION_WITH_RECEIVER"`;
    > -   `"INTERFACE"`;
    > -   `"NAMESPACE"`;
    > -   `"TYPE_ALIAS"`;
    > -   `"VARIABLE"`;

-   Targets for `Class Members`{.interpreted-text role="ref"}:

    > -   `"CLASS_FIELD"`;
    > -   `"CLASS_METHOD"`;
    > -   `"CLASS_GETTER"`;
    > -   `"CLASS_SETTER"`;

-   Targets for `Interface Members`{.interpreted-text role="ref"}:

    > -   `"INTERFACE_METHOD"`;
    > -   `"INTERFACE_GETTER"`;
    > -   `"INTERFACE_SETTER"`;

-   Other targets:

    > -   `"LAMBDA"` for `Lambda Expressions`{.interpreted-text role="ref"} and
    >     `Lambda Expressions with Receiver`{.interpreted-text role="ref"};
    > -   `"PARAMETER"` for function, method, and lambda parameter;
    > -   `"STRUCT"` (see `Keyword struct and ArkUI`{.interpreted-text role="ref"});
    > -   `"TYPE"` (see `Using Types`{.interpreted-text role="ref"}).

::: {.index}
class
enumeration
function
interface
namespace
type alias
variable
class member
function with receiver
class field
class method
class getter
class setter
interface method
interface getter
interface setter
target
lambda
parameter
struct
type
annotation
:::

A `compile-time error`{.interpreted-text role="index"} occurs if an enumeration member is used more
than once in an `@Target` annotation:

``` {.typescript}
@Target(["CLASS", "INTERFACE", "CLASS"]) // Compile-time error
@interface Anno {}
```

| 

## Runtime Access to Annotations {#Runtime Access to Annotations}

For an annotation with *retention policy* (see `Retention Annotation`{.interpreted-text role="ref"})
`BYTECODE` or `RUNTIME` an abstract class with the name of the annotation
is implicitly declared. All fields of this class are `readonly`.
If a field is of an array type, the array type is also `readonly`.

::: {.index}
runtime
access
annotation
retention policy
retention annotation
bytecode
readonly field
array type
:::

For the following annotation:

``` {.typescript}
@Retention("RUNTIME")
@interface MyAnno {
    name: string
    attrs: number[]
}
```

\--the abstract class is declared:

``` {.typescript}
abstract class MyAnno {
    readonly name: string
    readonly attrs: readonly number[]
}
```

The use of such a class is represented in following example:

``` {.typescript}
@MyAnno({name: "someName", attr: [1, 2]})
class A {}

let my: MyAnno = // call of reflection library to get instance of annotation for type A
console.log(my.name) // output: someName
```

::: {.index}
annotation
abstract class
declaration
readonly name
:::

```{=pdf}
PageBreak
```
