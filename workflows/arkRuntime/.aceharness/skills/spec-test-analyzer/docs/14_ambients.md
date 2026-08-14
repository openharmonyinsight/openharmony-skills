# Ambient Declarations {#Ambient Declarations}

*Ambient declaration* specifies an entity declared elsewhere but usable in the
current context.

Ambient declarations:

-   Provide type information for entities declared elsewhere.
-   Introduce no new entities like regular declarations do.
-   Cannot include executable code, and thus
    -   Ambient variables, constants, and enumerations have no initializers;
    -   Ambient functions, methods, and constructors have no bodies.

::: {.index}
ambient declaration
declaration
module
entity
executable code
initializer
initialization
ambient function
ambient method
ambient constructor
function
method
constructor
function body
method body
constructor body
:::

The syntax of *ambient declaration* is presented below:

``` {.abnf}
ambientDeclaration:
    'declare'
    ( ambientConstantOrVariableDeclaration
    | ambientFunctionDeclaration
    | explicitFunctionOverload
    | ambientClassDeclaration
    | ambientInterfaceDeclaration
    | ambientEnumDeclaration
    | ambientNamespaceDeclaration
    | ambientAnnotationDeclaration
    | ambientAccessorDeclaration
    | typeAlias
    )
    ;
```

A `compile-time error`{.interpreted-text role="index"} occurs if the modifier `declare` is used in a
context that is already ambient:

``` {.typescript}
declare namespace A{
    declare function foo(): void // Compile-time error
}
```

::: {.index}
syntax
ambient declaration
enumeration type declaration
context
modifier declare
declare
declared type
prefix
const keyword
compatibility
ambient
:::

*Ambient declaration* by itself does not guarantee that non-ambient declartion
declared elsewhere for the same name entity is identical to the ambient one.
By its nature, any *ambient declaration* is a requirement only that the build
system (see `Build System`{.interpreted-text role="ref"}) provides a proper non-ambient declaration.

| 

## Ambient Constant or Variable Declarations {#Ambient Constant or Variable Declarations}

The syntax of *ambient* constant or variable declarations is presented below:

``` {.abnf}
ambientConstantOrVariableDeclaration:
    'const'|'let' ambientConstantOrVariableList ';'
    ;

ambientConstantOrVariableList:
    ambientConstantOrVariable (',' ambientConstantOrVariable)*
    ;

ambientConstantOrVariable:
    identifier ':' type
    ;
```

::: {.index}
ambient constant
ambient variable
constant declaration
variable declaration
declaration
:::

An *ambient constant* and *variable declaration* must have an explicit type
annotation, and must have no initializer. Otherwise,
a `compile-time error`{.interpreted-text role="index"} occurs:

``` {.typescript}
declare let v1: number // OK
declare let v2 = 1     // Compile-time error, ambient variable must have no initializer

declare const c1: number // OK
declare const c2 = 1     // Compile-time error, ambient constant must have no initializer
```

| 

## Ambient Function Declarations {#Ambient Function Declarations}

The syntax of *ambient function declaration* is presented below:

``` {.abnf}
ambientFunctionDeclaration:
    'function' identifier typeParameters? signature
    ;
```

A `compile-time error`{.interpreted-text role="index"} occurs if an ambient function declaration has the
following:

-   No explicit return type specified;
-   A parameter with the default value;
-   A function body, or;
-   Modifier `async` specified.

Examples below illustrate that:

``` {.typescript}
declare function ok1(x: number): void // OK
declare function bad1(x: number) // Compile-time error, no return specified

declare function ok2(x?: string): void // OK, optional parameters can be used
declare function bad2(y: number = 1): void // Compile-time error, parameter
                                           // has default value

declare function bad3(): void {} // Compile-time error, function body provided

declare async function bad4(): void // Compile-time error, async modifier is used 
```

::: {.index}
syntax
ambient function declaration
return type
function body
parameter
optional parameter
default value
modifier async
async modifier
function body
ambient context
:::

| 

## Ambient Overload Function Declarations {#Ambient Overload Function Declarations}

The syntax of *ambient overload function declaration* is identical to that of
`Explicit Function Overload`{.interpreted-text role="ref"}. The semantics of such declarations is
defined by the same rules.

``` {.typescript}
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
```

::: {.index}
ambient overload function declaration
ambient overload function
explicit function overload
semantics
syntax
:::

| 

## Ambient Class Declarations {#Ambient Class Declarations}

The syntax of *ambient class declaration* is presented below:

``` {.abnf}
ambientClassDeclaration:
    'class'|'struct' identifier typeParameters?
    classExtendsClause? implementsClause?
    '{' ambientClassMember* '}'
    ;

ambientClassMember:
    ambientAccessModifier?
    ( ambientFieldDeclaration
    | ambientConstructorDeclaration
    | ambientMethodDeclaration
    | explicitClassMethodOverload
    | ambientClassAccessorDeclaration
    | ambientIndexerDeclaration
    | ambientCallSignatureDeclaration
    | ambientIterableDeclaration
    )
    ;

ambientAccessModifier:
    'public' | 'protected'
    ;
```

Ambient field declarations have no initializers.

::: {.index}
ambient field declaration
ambient class declaration
initializer
syntax
:::

The syntax of *ambient field declaration* is presented below:

``` {.abnf}
ambientFieldDeclaration:
    ambientFieldModifier* identifier ':' type
    ;

ambientFieldModifier:
    'static' | 'readonly'
    ;
```

Ambient constructor, method, and accessor declarations have no bodies.

Their syntax is presented below:

::: {.index}
ambient field declaration
ambient class declaration
ambient constructor declaration
ambient method declaration
ambient accessor declaration
initializer declaration
syntax
:::

``` {.abnf}
ambientConstructorDeclaration:
    'constructor' parameters
    ;

ambientMethodDeclaration:
    ambientMethodModifier* identifier signature
    ;

ambientMethodModifier:
    'static'
    ;

ambientClassAccessorDeclaration:
    ambientMethodModifier*
    ( 'get' identifier '(' ')' returnType
    | 'set' identifier '(' requiredParameter ')'
    )
    ;
```

Ambient methods can be overloaded similarly to non-ambient methods with the
same syntax and semantics (see `Explicit Class Method Overload`{.interpreted-text role="ref"}).

``` {.typescript}
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
```

::: {.index}
ambient method
overload
non-ambient method
syntax
semantics
method call
class method
:::

| 

### Ambient Indexer {#Ambient Indexer}

*Ambient indexer declarations* specify the indexing of a class instance
in an ambient context. The feature is provided for compatibility:

The syntax of *ambient indexer declaration* is presented below:

``` {.abnf}
ambientIndexerDeclaration:
    'readonly'? '[' identifier ':' type ']' returnType
    ;
```

::: {.index}
ambient indexer
ambient indexer declaration
indexing
class instance
ambient context
syntax
compatibility
:::

The use of *ambient indexer declarations* is represented in the example below:

``` {.typescript}
declare class C {
    [index: number]: number
}
declare class D {
    [index: int]: C
}
declare class E {
    [index: string]: string
}
```

The following restrictions apply:

-   Only one *ambient indexer declaration* is allowed in an ambient class declaration.
-   *Ambient indexer declaration* is supported in ambient contexts only.
    If written in , ambient class implementation must conform to
    `Indexable Types`{.interpreted-text role="ref"}.

::: {.index}
ambient indexer declaration
restriction
ambient class declaration
ambient context
ambient class
implementation
indexable type
:::

| 

### Ambient Call Signature {#Ambient Call Signature}

*Ambient call signature* declarations are used to specify *callable types*
in an ambient context. The feature is provided for compatibility:

The syntax of *ambient call signature declaration* is presented below:

``` {.abnf}
ambientCallSignatureDeclaration:
    signature
    ;
```

``` {.typescript}
declare class C {
    (someArg: number): boolean
    (someArg: string): boolean
    ...
}
```

*Ambient class signature declaration* is supported in ambient contexts
only. If written in , ambient class implementation must conform to
`Callable Types with $_invoke Method`{.interpreted-text role="ref"}.

Multiple *ambient call signatures* are allowed in an ambient class declaration
provided that they are distinct (see `Declaration Distinguishable by Signatures`{.interpreted-text role="ref"}).
Multiple distinct ambient call signatures are represented in the following
example:

``` {.typescript}
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
```

::: {.index}
ambient call signature declaration
ambient call signature
callable type
ambient context
compatibility
syntax
restriction
ambient class declaration
:::

| 

### Ambient Iterable {#Ambient Iterable}

*Ambient iterable declaration* indicates that a class instance is iterable
in an ambient context. The feature is provided for compatibility:

The syntax of *ambient iterable declaration* is presented below:

``` {.abnf}
ambientIterableDeclaration:
    '[Symbol.iterator]' '(' ')' returnType
    ;
```

The following restrictions apply:

-   *returnType* must be a type that implements `Iterator` interface defined
    in `Standard Library`{.interpreted-text role="ref"}.
-   Only one *ambient iterable declaration* is allowed in an ambient class
    declaration.

``` {.typescript}
declare class C {
    [Symbol.iterator] (): CIterator
}
```

::: {.note}
::: {.title}
Note
:::

*Ambient iterable declaration* is supported in ambient contexts only.
If written in , ambient class implementation must conform to
`Iterable Types`{.interpreted-text role="ref"}.
:::

::: {.index}
ambient iterable
ambient iterable declaration
class instance
ambient context
iterable class instance
ambient context
compatibility
syntax
return type
restriction
implementation
interface
ambient class
implementation
:::

| 

## Ambient Interface Declarations {#Ambient Interface Declarations}

The syntax of *ambient interface declaration* is presented below:

``` {.abnf}
ambientInterfaceDeclaration:
    'interface' identifier typeParameters?
    interfaceExtendsClause?
    '{' ambientInterfaceMember* '}'
    ;

ambientInterfaceMember
    : interfaceProperty
    | ambientInterfaceMethodDeclaration
    | ambientIndexerDeclaration
    | ambientIterableDeclaration
    ;

ambientInterfaceMethodDeclaration:
    'default'? identifier signature
    ;
```

*Ambient interface* can contain additional members in the same manner as
an ambient class (see `Ambient Indexer`{.interpreted-text role="ref"}, and `Ambient Iterable`{.interpreted-text role="ref"}).

::: {.index}
syntax
ambient interface
ambient interface declaration
ambient class
ambient indexer
ambient iterable
:::

If an interface method declaration is marked with the keyword `default`, then
a non-ambient interface must contain the default implementation for the method
as follows:

``` {.typescript}
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
```

::: {.index}
interface method
default keyword
non-ambient interface
runtime error
method
ambient interface declaration
ambient class
default implementation
:::

| 

## Ambient Enumeration Declarations {#Ambient Enumeration Declarations}

The syntax of *ambient enumeration declaration* is presented below:

``` {.abnf}
ambientEnumDeclaration
    : 'const'? 'enum' identifier enumBaseType? '{' ambientEnumMemberList? '}'
    ;

ambientEnumMemberList:
    identifier (',' identifier)* ','?
    ;
```

If an *enumeration declaration* is prefixed with the keyword
`const`, then a `compile-time error`{.interpreted-text role="index"} occurs. This restriction
is temporary, and the semantics of `const enum` is to be made
available in the future versions of .

No member of an enum declaration can have an initializer.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs as represented
in the example below:

``` {.typescript}
declare enum RGB {Red, Green, Blue} // OK

declare enum Err1 { A = 5 }      // Compile-time error, initializer is present
```

| 

## Ambient Namespace Declarations {#Ambient Namespace Declarations}

Namespaces are used to logically group multiple entities. supports
*ambient namespaces* for better compatibility. often uses ambient
namespaces to specify the platform API or a third-party library API.

The syntax of *ambient namespace declaration* is presented below:

``` {.abnf}
ambientNamespaceDeclaration:
    'namespace' identifier '{' ambientNamespaceElement* '}'
    ;

ambientNamespaceElement:
    ambientNamespaceElementDeclaration | exportDirective
;

ambientNamespaceElementDeclaration:
    'export'?
    ( ambientConstantOrVariableDeclaration
    | ambientFunctionDeclaration
    | ambientClassDeclaration
    | ambientInterfaceDeclaration
    | ambientNamespaceDeclaration
    | ambientAccessorDeclaration
    | 'const'? enumDeclaration
    | typeAlias
    )
    ;
```

An *enumeration type declaration* can be prefixed with the keyword `const`
for compatibility. The prefix has no influence on the declared type.
Only exported entities can be accessed outside a namespace.

Namespaces can be nested:

``` {.typescript}
declare namespace A {
    export namespace B {
        export function foo(): void;
    }
}
```

A namespace is not an object but merely a scope for entities that can be
accessed by using qualified names only.

::: {.index}
namespace
ambient namespace
ambient namespace declaration
entity
compatibility
syntax
platform API
third-party library API
ambient iterable declaration
declared type
access
const keyword
enumeration type declaration
prefix
declared type
:::

If an ambient namespace is imported from a module, then all ambient
namespace declarations are accessible (see `Accessible`{.interpreted-text role="ref"}) across
all declarations and top-level statements of the current module.

``` {.typescript}
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
```

A `compile-time error`{.interpreted-text role="index"} occurs if an *ambient namespace* declaration
contains an *exportDirective* that refers to a declaration which is not a part
of the namespace.

``` {.typescript}
export declare namespace A {
     export {foo} // Compile-time error, no 'foo' in namespace 'A'
}
function foo() {}
```

::: {.index}
ambient namespace
ambient namespace declaration
accessible declaration
access
accessibility
top-level statement
module
:::

| 

### Implementing Ambient Namespace Declaration {#Implementing Ambient Namespace Declaration}

If an *ambient namespace* is implemented in , a namespace with the
same name must be declared (see `Namespace Declarations`{.interpreted-text role="ref"}) as the
top-level declaration of a module. All namespace names of a nested
namespace (i.e. a namespace embedded into another namespace) must be the same
as in ambient context.

::: {.index}
ambient namespace declaration
ambient namespace
entity
implementation
namespace declaration
namespace name
declaration
top-level declaration
module
ambient context
nested namespace
embedded namespace
:::

| 

## Ambient Accessor Declarations {#Ambient Accessor Declarations}

*Ambient accessor declaration* is an ambient version of
`Accessor Declarations`{.interpreted-text role="ref"}. The syntax of an *ambient accessor declaration*
is presented below:

``` {.abnf}
ambientAccessorDeclaration:
    ( 'get' identifier '(' receiverParameter? ')' returnType
    | 'set' identifier '(' (receiverParameter ',')? requiredParameter ')'
    )
    ;
```

A compile-time error occurs if explicit return type for an ambient getter
declaration is not specified.

``` {.typescript}
declare get name(): string // OK
declare get age() // Compile-time error, return type must be specified
```

See `Accessor Declarations`{.interpreted-text role="ref"} for details.

```{=pdf}
PageBreak
```
