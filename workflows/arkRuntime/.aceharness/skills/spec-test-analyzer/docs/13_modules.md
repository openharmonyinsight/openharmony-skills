# Namespaces and Modules {#Namespaces and Modules}

Programs in are structured as sequences of elements ready for compilation
in the form of *modules* (see `Module Declarations`{.interpreted-text role="ref"}). A module is a specific
form of a namespace called *top-level namespace*. A module can contain nested
namespaces (see `Namespace Declarations`{.interpreted-text role="ref"}).

| 

## Module Declarations {#Module Declarations}

Each module creates its own scope (see `Scopes`{.interpreted-text role="ref"}).
Variables, functions, classes, interfaces, or other declarations of a module
are only accessible (see `Accessible`{.interpreted-text role="ref"}) within such a scope if not
exported explicitly. Types of all exported entities must be set explicitly
(see details in `Export Directives`{.interpreted-text role="ref"}).

A variable, function, class, interface, or other declarations exported from
a module must be imported first by the module that is to use them.

::: {.note}
::: {.title}
Note
:::

Only exported declarations are available for the third party tools and
programs written in other programming languages.
:::

The modules can consist of one or more files (see `Multifile Module`{.interpreted-text role="ref"}).

All *modules* are stored in a file system or a database
(see `Modules in Host System`{.interpreted-text role="ref"}).

A *module* can optionally consist of the following parts:

1.  The module header that defines a module name;
2.  Import directives allow using declarations imported into the current module
    within this module;
3.  Top-level declarations;
4.  Top-level statements; and
5.  Re-export directives.

The syntax of *module* is presented below:

``` {.abnf}
moduleDeclaration:
    moduleHeader? importDirective* (topDeclaration | topLevelStatements | exportDirective)*
    ;
```

The accessibility of a module by import in other modules is determined by
the build system.

Every module can directly use a set of exported entities defined in the
standard library (see `Standard Library Usage`{.interpreted-text role="ref"}).

``` {.typescript}
// Hello, world! module
function main() {
  console.log("Hello, world!") // console is defined in the standard library
}
```

If a module has at least one top-level ambient declaration (see
`Ambient Declarations`{.interpreted-text role="ref"}), then all other declarations must be ambient,
and no top-level statement must be present (see `Top-Level Statements`{.interpreted-text role="ref"}).
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

``` {.typescript}
declare let x: number
function main() {}
// Compile-time error, ambient and non-ambient declarations are mixed
```

::: {.index}
module
module header
import directive
imported declaration
module
entity
top-level declaration
top-level statement
re-export directive
import
console
syntax
standard library
console
:::

| 

## Module Header {#Module Header}

*Module header* defines the optional modifier `export` and a *module name*.

The syntax of *module header* is presented below:

``` {.abnf}
moduleHeader:
    'declare'? 'export'? 'module' moduleName
    ;

moduleName:
    StringLiteral
    ;
```

If a *module header* has the `declare` modifier than the whole module is
ambient. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

The `export` modifier is used by the build system to make a module
accessible (see `Accessible`{.interpreted-text role="ref"}) in other modules by import (see
`Import Directives`{.interpreted-text role="ref"}).

The usage of *module header* is represented in the example below:

``` {.typescript}
export module "x"
import {A} from "some module"
export class B extends A {}
```

::: {.index}
module header
module name
:::

| 

## Namespace Declarations {#Namespace Declarations}

*Namespace declaration* introduces a named container of entities with
distinguishable names.
Each namespace creates its own scope (see `Scopes`{.interpreted-text role="ref"}). Variables,
functions, classes, interfaces, or other declarations of a namespace are only
accessible (see `Accessible`{.interpreted-text role="ref"}) within this scope if not exported explicitly.
Any use of exported entities is to be qualified with the name of a namespace.

The syntax of *namespace declarations* is presented below:

``` {.abnf}
namespaceDeclaration:
    'namespace' qualifiedName
    '{' (topDeclaration | topLevelStatements | staticBlock | exportDirective)* '}'
    ;
```

Namespaces can have *top-level statements* or a *static block*
which constitute a namespace initializer. The initializer is executed
only if at least one of the exported namespace members is used in the program
(see `Static Initialization`{.interpreted-text role="ref"} for detail).

*Static block* is to be deprecated in one of the future versions of ,
using *top-level statements* is recommended instead. Only one *static block*
is allowed in a namespace. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

The usage of namespaces is represented in the example below:

``` {.typescript}
namespace NS1 {
    export function foo(): void {  }
    export let variable: int = 1234
    export const constant: int = 1234
    export let someVar: string

    // Will be executed before any use of NS1 members
    someVar = "some string"
    console.log("Init for NS1 done")
    export function bar(): void {}
}

namespace NS2 {
    export const constant:int = 1
    // Will never be executed since NS2 members are never used
    console.log("Init for NS2 done")
    export function bar(): void {}
}

export function bar(): void {}  // That is a different bar()

if (NS1.variable == NS1.constant) {
    NS1.variable = 4321
}
NS1.bar()  // namespace bar() is called
bar()      // top-level bar() is called
```

::: {.index}
namespace
namespace declaration
qualified name
qualifier
access
entity
syntax
export
qualified name
initializer block
namespace variable
static initialization
call
:::

::: {.note}
::: {.title}
Note
:::

An exported namespace entity can be used in the form of a *qualifiedName*
outside a namespace in the same module. Any namespace entity can be and
typically is used inside a namespace without qualification, i.e., without a
namespace name. A *qualifiedName* inside a namespace can be used for a
namespace entity only when the entity is exported. Using a *qualifiedName*
for non-exported entity both inside and outside a namespace causes a
`compile-time error`{.interpreted-text role="index"}:

``` {.typescript}
namespace NS {
    export let a: number = 1
    let b = 2

    export function foo(): void {
        let v: number
        v = a // OK, no qualification
        v = NS.a // OK, `a` exported
    }

    export function bar(): void {
        let v: number
        v = b  // OK, no qualification
        v = NS.b // Compile-time error, `b` not exported
    }
}

NS.a = 1 // OK,  `NS.a` exported
NS.b = 1 // Compile-time error, `NS.b` not exported
```
:::

::: {.note}
::: {.title}
Note
:::

A namespace must be exported to be used in another module:

``` {.typescript}
// File1
namespace Space1 {
    export function foo(): void { ... }
    export let variable: int = 1234
    export const constant: int = 1234
}
export namespace Space2 {
    export function foo(p: number): void { ... }
    export let variable: int = "1234"
}

// File2
import {Space2 as Space1} from "File1"

// Compile-time error - there is no variable or constant called 'constant'
if (Space1.variable == Space1.constant) {
     // Compile-time error - incorrect assignment as type 'number'
     // is not compatible with type 'string'
    Space1.variable = 4321
}
Space1.foo()     // Compile-time error - there is no function 'foo()'
Space1.foo(1234) // OK
```
:::

::: {.index}
namespace
module
variable
constant
function
compatibility
string
embedded namespace
:::

::: {.note}
::: {.title}
Note
:::

Embedded namespaces are allowed:

``` {.typescript}
namespace ExternalSpace {
    export function foo(): void { ... }
    export let variable: number = 1234
    export namespace EmbeddedSpace {
        export const constant: int = 1234
    }
}

if (ExternalSpace.variable == ExternalSpace.EmbeddedSpace.constant) {
    ExternalSpace.variable = 4321
}
```
:::

::: {.note}
::: {.title}
Note
:::

Namespaces with identical namespace names in a single module merge their
exported declarations into a single namespace. A duplication causes a
`compile-time error`{.interpreted-text role="index"}. Exported and non-exported declarations with the
same name are also considered a `compile-time error`{.interpreted-text role="index"}. Only one of the
merging namespaces can have an initializer. Otherwise, a
`compile-time error`{.interpreted-text role="index"} occurs.
:::

::: {.index}
embedded namespace
namespace
namespace name
module
export
declaration
exported declaration
non-exported declaration
initializer
:::

``` {.typescript}
// One source file
namespace A {
    export function foo(): void { console.log ("1st A.foo() exported") }
    function bar(): void {  }
    export namespace C {
        export function too(): void { console.log ("1st A.C.too() exported") }
    }
}

namespace B {  }

namespace A {
    export function goo(): void {
        A.foo() // calls exported foo()
        foo()   /* calls exported foo() as well as all A namespace
                   declarations are merged into one */
        A.C.moo()
    }
    //export function foo(): void {  }
    // Compile-time error as foo() was already defined

    // function foo() { console.log ("2nd A.foo() non-exported") }
    // Compile-time error as foo() was already defined as exported
}

namespace A.C {
    export function moo(): void {
        too() // too()  accessible when namespace C and too() are both exported
        A.C.too()
    }
}

A.goo()

// File
namespace A {
    export function foo(): void { ... }
    export function bar(): void { ... }
}

namespace A {
    function goo() { bar() }  // exported bar() is accessible in the same namespace
    export function foo(): void { ... }  // Compile-time error as foo() was already defined
}
```

::: {.index}
namespace
export function
qualified name
notation
shortcut notation
embedded namespace
access
accessibility
export function
initializer
:::

::: {.note}
::: {.title}
Note
:::

A namespace name can be a qualified name. It is a shortcut notation of
embedded namespaces as represented below:

``` {.typescript}
namespace A.B {
    /*some declarations*/
}
```

The code above is a shortcut to the following code:

``` {.typescript}
namespace A {
    export namespace B {
      /*some declarations*/
    }
}
```

This code is illustrative of the use of declarations in the case below:

``` {.typescript}
namespace A.B.C {
    export function foo(): void { ... }
}

A.B.C.foo() // Valid function call, as 'B' and 'C' are implicitly exported
```

Where a namespace merges with qualified names, all qualification levels are
merged. A `compile-time error`{.interpreted-text role="index"} occurs in the case of a duplication.

``` {.typescript}
namespace A {
    function foo() { ... } // #1
    export namespace B {
       export function foo(): void { ... } // #2
    }
}

namespace A.B {
    export function foo(): void { ... } // #3
}

// Declarations of functions #2 and #3 lead to a compile-time error,
//   duplicated declaration of function A.B.foo()

// While function foo() in namespace A is a valid declaration
```
:::

If an ambient namespace (see `Ambient Namespace Declarations`{.interpreted-text role="ref"}) is defined
in a module (see `Module Declarations`{.interpreted-text role="ref"}), then all ambient namespace
declarations are accessible across all declarations and top-level statements of
the module.

``` {.typescript}
declare namespace A {
    function foo(): void
    type X = Array<number>
}

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

::: {.index}
namespace
export namespace
module
ambient namespace
declaration
accessible declaration
access
accessibility
top-level statement
module
:::

| 

## Import Directives {#Import Directives}

*Import directives* make entities exported from other modules (see
`Module Declarations`{.interpreted-text role="ref"}) available for use in the current module by using
different binding forms. These directives have no effect during
the program execution.

An import declaration has the following two parts:

-   Import path that determines from what module to import;
-   Import bindings that define what entities, and in what form (either
    qualified or unqualified) the current module can use.

::: {.index}
import directive
export
entity
binding
module
directive
import declaration
import path
import binding
qualified form
unqualified form
syntax
:::

The syntax of *import directives* is presented below:

``` {.abnf}
importDirective:
    'import' 'type'? bindings 'from' importPath
    ;

bindings:
    defaultBinding
    | (defaultBinding ',')? allBinding
    | (defaultBinding ',')? selectiveBindings
;

allBinding:
    '*' bindingAlias
    ;

bindingAlias:
    'as' identifier
    ;

defaultBinding:
    'type'? identifier
    ;

selectiveBindings:
    nameBinding (',' nameBinding)*
    ;

nameBinding:
    'type'? identifier bindingAlias?
    | 'default' 'as' identifier
    ;

importPath:
    StringLiteral
    ;
```

Each binding adds an entity or entities to the scope of a module
(see `Scopes`{.interpreted-text role="ref"}). Any entity so added must be distinguishable in the
declaration scope (see `Declarations`{.interpreted-text role="ref"}).

Import with `type` modifier is discussed in `Import Type Directive`{.interpreted-text role="ref"}.

A `compile-time error`{.interpreted-text role="index"} occurs if:

-   A non-import directive, declaration, or statement precedes an `import`
    directive;
-   Entity added to the scope of a module by a binding is not distinguishable;
-   Module imports itself directly, and `importPath` refers to a file in which
    the current module is stored; or
-   `import type` is used while `type` is also used by one of bindings.

A `compile-time warning`{.interpreted-text role="index"} occurs if the `importPath` refers to a file
with no code, where the grammar start symbol corresponds to an empty
one.

::: {.index}
binding
declaration
module
scope
declaration
declaration scope
import directive
type
type modifier
modifier
storage
import type
:::

| 

### Bind All with Qualified Access {#Bind All with Qualified Access}

Import binding `* as A` binds the single named entity *A* to the
declaration scope of the current module.

A qualified name consisting of *A* and the name of entity `A.name` is used
to access any entity exported from the module as defined by the *import path*.

+---------------------------------+---+-------------------------------+
| Import                          |   | Usage                         |
+=================================+===+===============================+
|                                 |   |                               |
+---------------------------------+---+-------------------------------+
| ``` {.typescript}               |   | ``` {.typescript}             |
| import * as Math from "..."     |   | let x = Math.sin(1.0)         |
| ```                             |   | ```                           |
+---------------------------------+---+-------------------------------+

This form of import is recommended because it simplifies the reading and
understanding of the source code when all exported entities are prefixed with
the name of the imported module.

::: {.index}
import binding
import
binding
qualified name
entity
declaration scope
module
name
access
export
import path
:::

| 

### Default Import Binding {#Default Import Binding}

Default import binding allows importing a declaration exported from a module
as default export. Knowing the actual name of a declaration is not required
as the new name is given at importing.
A `compile-time error`{.interpreted-text role="index"} occurs if another form of import is used to
import an entity initially exported as default.

There are two forms of *default import binding*:

-   Single identifier;
-   Special form of selective import with the keyword `default`.

``` {.typescript}
// Module 1
import DefaultExportedItemBindedName from "Module 2"
import {default as DefaultExportedItemNewName} from "Module 2"
function foo () {
  let v1 = new DefaultExportedItemBindedName()
  // instance of class 'SomeClass' to be created here
  let v2 = new DefaultExportedItemNewName()
  // instance of class 'SomeClass' to be created here
}

// Module 2
export default class SomeClass {}

// Module 3 - the same semantics as in Module 2
class SomeClass {}
export default SomeClass

// Module 4
export {default} from "Module 2" // Module 4 re-exports default export of Module 2
export {default as SomeClassNewName} from "Module 2" 
  // Module 4 re-exports default export of Module 2 as a new exported name
```

::: {.index}
import binding
entity
import
declaration
export
module
default keyword
identifier
selective import
:::

| 

### Selective Binding {#Selective Binding}

*Selective binding* allows to bind an entity exported as *identifier*,
or an entity exported by default (see `Default Import Binding`{.interpreted-text role="ref"}).

Binding with *identifier* binds an exported entity with the name
*identifier* to the declaration scope of the current module. If no *binding
alias* is present, then the entity is added to the declaration scope under
the original name. Otherwise, the identifier specified in *binding alias*
is used. In the latter case, the bounded entity is no longer accessible (see
`Accessible`{.interpreted-text role="ref"}) under the original name.

If an *identifier* refers to an *overloaded function* (see
`Overloading`{.interpreted-text role="ref"}), then all accessible overloaded functions are imported,
including *explicitly overloaded functions* (see
`Explicit Function Overload`{.interpreted-text role="ref"}).

``` {.typescript}
// File1
export function foo(p: number): void {} // #1
export function foo(p: string): void {} // #2
export function fooBoolean(p: Boolean): void {}
export overload foo {foo, fooBoolean}

function foo() {} // #3

// File2
import {foo} from "File1"  // all exported 'foo' are imported
foo(5)          // #1 is called
foo("a string") // #2 is called
foo(true)       // fooBoolean is called
foo()           // Compile-time error, as #3 is not exported
```

*Selective binding* that uses exported entities is represented in the examples
below:

::: {.index}
import binding
simple name
identifier
export
call
name
declaration scope
overloaded function
entity
access
accessibility
bound entity
selective binding
binding
:::

``` {.typescript}
export const PI: number = 3.14
export function sin(d: number): number {}
```

::: {.note}
::: {.title}
Note
:::

The import path of the module is irrelevant and replaced for `'...'`
in the examples below:
:::

+-------------------------------+---+-----------------------------------+
| Import                        |   | Usage                             |
+===============================+===+===================================+
|                               |   |                                   |
+-------------------------------+---+-----------------------------------+
| ``` {.typescript}             |   | ``` {.typescript}                 |
| import {sin} from "..."       |   | let x = sin(1.0)                  |
| ```                           |   | let f: float = 1.0                |
|                               |   | ```                               |
+-------------------------------+---+-----------------------------------+
|                               |   |                                   |
+-------------------------------+---+-----------------------------------+
| ``` {.typescript}             |   | ``` {.typescript}                 |
| import {sin as Sine} from "   |   | let x = Sine(1.0) // OK           |
|     ..."                      |   | let y = sin(1.0) /* Error ‘sin’   |
| ```                           |   |    is not accessible */           |
|                               |   | ```                               |
+-------------------------------+---+-----------------------------------+

A single import directive can list several names as follows:

+-----------------------------------+---+-------------------------------+
| Import                            |   | Usage                         |
+===================================+===+===============================+
|                                   |   |                               |
+-----------------------------------+---+-------------------------------+
| ``` {.typescript}                 |   | ``` {.typescript}             |
| import {sin, PI} from "..."       |   | let x = sin(PI)               |
| ```                               |   | ```                           |
+-----------------------------------+---+-------------------------------+
|                                   |   |                               |
+-----------------------------------+---+-------------------------------+
| ``` {.typescript}                 |   | ``` {.typescript}             |
| import {sin as Sine, PI} from "   |   | let x = Sine(PI)              |
|   ..."                            |   | ```                           |
| ```                               |   |                               |
+-----------------------------------+---+-------------------------------+

Complex cases with several bindings mixed on one import path are discussed
below in `Several Bindings for One Import Path`{.interpreted-text role="ref"}.

::: {.index}
import directive
import path
binding
import
:::

| 

### Import Type Directive {#Import Type Directive}

An import directive can have a `type` modifier exclusively for a better
syntactic compatibility with (also see `Export Type Directive`{.interpreted-text role="ref"}).
supports no additional semantic checks for entities imported by using
*import type* directives.

The semantic checks performed by the compiler in but not in
are represented by the following code:

``` {.typescript}
// File module.ets
console.log ("Module initialization code")

export class Class1 {/*body*/}

class Class2 {}
export type {Class2}

// MainProgram.ets

import {Class1} from "./module.ets"
import type {Class2} from "./module.ets"

let c1 = new Class1() // OK
let c2 = new Class2() // Compile-time error in |TS|, OK in |LANG|
```

Another form of *type import* is used when `type` is attached to a name
binding. This allows mixing general import and `type` import.

``` {.typescript}
// File module.ets
console.log ("Module initialization code")

class Class1 {/*body*/}
class Class2 {}
export {Class1, type Class2}

// MainProgram.ets

import {Class1, type Class2 } from "./module.ets"

let c1 = new Class1() // OK
let c2 = new Class2() // Compile-time error in |TS|, OK in |LANG|
```

::: {.index}
import binding
import directive
import
import type
import type directive
type modifier
semantic check
syntax
compatibility
name binding
binding
export type
compiler
module
general import
type import
:::

| 

### Import Path {#Import Path}

*Import path* is a string literal that determines where and how an imported
module is to be searched for.

*Import path* can include the following:

-   Initial dot `'.'` or two dots `'..'` followed by the slash character `'/'`.
-   One or more path components (the subset of characters and case sensitivity of
    path components must follow the path rules of a host file system).
-   Slash characters separating components of the path.

The slash character `'/'` is used in import paths irrespective of the host
system. The backslash character is not used in this context.

In most file systems, an import path looks like a file path. *Relative* (see
below) and *non-relative* import paths have different *resolutions* that map
the import path to a file path of the host system.

::: {.index}
import binding
string literal
import path
alpha-numeric character
import
compilation
import path
context
file system
relative import path
non-relative import path
resolution
path component
case sensitivity
subset
file path
path rule
slash character
backslash character
:::

The compiler uses its own algorithm to locate a module source that processes
the import path. If the import path specifies no file extension, then the
compiler can append some according to its own rules and priorities. If the
import path refers to a folder, then the way to handle the case is determined
by the actual compiler. If the compiler cannot locate a module source
definitely, then a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
compiler
import path
source
module
folder
extension
file
:::

A *relative import path* starts with `'./'` or `'../'`. Examples of relative
paths are presented below:

``` {.typescript}
"./components/entry"
"../constants/http"
```

Resolving *relative import* is relative to the importing file. *Relative
import* is used on modules to maintain their relative location.

``` {.typescript}
import * as Utils from "./mytreeutils"
```

Other import paths are *non-relative*.

Resolving a *non-relative path* depends on the compilation environment. The
definition of the compiler environment can be particularly provided in a
configuration file or environment variables.

The *base URL* setting is used to resolve a path that starts with `'/'`.
*Path mapping* is used in all other cases. Resolution details depend on
the implementation. For example, the compilation configuration file can contain
the following lines:

``` {.typescript}
"baseUrl": "/home/project",
"paths": {
    "std": "/arkts/stdlib"
}
```

In the example above, `/net/http` is resolved to `/home/project/net/http`,
and `std/components/treemap` to `/arkts/stdlib/components/treemap`.

File name, placement, and format are implementation-specific.

If the above configuration is in effect, the first path maps directly to
file system after applying `baseUrl`, while `std` in the second path is
replaced for `/arkts/stdlib`. Examples of non-relative paths are presented
below.

``` {.typescript}
"/net/http"
"std/components/treemap"
```

::: {.index}
relative import path
relative path
non-relative import path
non-relative path
compilation environment
compiler environment
imported file
relative location
configuration file
environment variable
resolving
base URL
path mapping
resolution
implementation
treemap
file system
:::

| 

### Several Bindings for One Import Path {#Several Bindings for One Import Path}

The same bound entities can use the following:

-   Several import bindings,
-   One import directive, or several import directives with the same import path:

+---------------------------------+-----------------------------------+
|                                 |                                   |
+---------------------------------+-----------------------------------+
| In one import directive         | ``` {.typescript}                 |
|                                 | import {sin, cos} from "..."      |
|                                 | ```                               |
+---------------------------------+-----------------------------------+
| In several import directives    | ``` {.typescript}                 |
|                                 | import {sin} from "..."           |
|                                 | import {cos} from "..."           |
|                                 | ```                               |
+---------------------------------+-----------------------------------+

No conflict occurs in the above example, because the import bindings
define disjoint sets of names.

The order of import bindings in an import declaration has no influence
on the outcome of the import.

The rules below prescribe what names must be used to add bound entities
to the declaration scope of the current module if multiple bindings are
applied to a single name:

::: {.index}
import binding
bound entity
import directive
import path
import declaration
import
import outcome
declaration scope
scope
entity
binding
module
name
:::

+-----------------------+----------------------+-----------------------+
| Case                  | Sample               | Rule                  |
+=======================+======================+=======================+
| A name is explicitly  | ``` {.typescript}    | OK. The compile-time  |
| used                  | import {sin, sin}    | warning is            |
| without an alias in   |    from "..."        | recommended.          |
| several               | ```                  |                       |
| bindings.             |                      |                       |
+-----------------------+----------------------+-----------------------+
| A name is used        | ``` {.typescript}    | OK. No warning.       |
| explicitly            | import {sin}         |                       |
| without alias in one  |    from "..."        |                       |
| binding.              | ```                  |                       |
+-----------------------+----------------------+-----------------------+
| A name is explicitly  | ``` {.typescript}    | OK. Both the name and |
| used                  | import {sin}         | qualified name can be |
| without alias, and    |    from "..."        | used:                 |
| implicitly with       |                      |                       |
| alias.                | import * as M        | sin and M.sin are     |
|                       |    from "..."        | accessible.           |
|                       | ```                  |                       |
+-----------------------+----------------------+-----------------------+
| A name is explicitly  | ``` {.typescript}    | OK. Only alias is     |
| used                  | import {sin as Sine} | accessible            |
| with alias.           |   from "..."         | for the name, but not |
|                       | ```                  | the                   |
|                       |                      | original name:        |
|                       |                      |                       |
|                       |                      | -   Sine is           |
|                       |                      |     accessible;       |
|                       |                      | -   sin is not        |
|                       |                      |     accessible.       |
+-----------------------+----------------------+-----------------------+
| A name is explicitly  | ``` {.typescript}    | OK. Both options can  |
| used with alias, and  | import {sin as Sine} | be                    |
| implicitly with       |    from "..."        | used:                 |
| alias.                |                      |                       |
|                       | import * as M        | -   Sine is           |
|                       |    from "..."        |     accessible;       |
|                       | ```                  | -   M.sin is          |
|                       |                      |     accessible.       |
+-----------------------+----------------------+-----------------------+
| A name is explicitly  | ``` {.typescript}    | OK. Both aliases are  |
| used                  | import {sin as Sine, | accessible. But       |
| with alias several    |    sin as SIN}       | warning can           |
| times.                |    from "..."        | be displayed.         |
|                       | ```                  |                       |
+-----------------------+----------------------+-----------------------+

::: {.index}
name
import
alias
access
binding
qualified name
accessibility
:::

| 

## Top-Level Declarations {#Top-Level Declarations}

*Top-level declarations* declare top-level types (`class`, `interface`, or
`enum` see `Type Declarations`{.interpreted-text role="ref"}), top-level variables (see
`Variable Declarations`{.interpreted-text role="ref"}), constants (see `Constant Declarations`{.interpreted-text role="ref"}),
functions (see `Function Declarations`{.interpreted-text role="ref"},
overloads (see `Explicit Function Overload`{.interpreted-text role="ref"}),
namespaces (see `Namespace Declarations`{.interpreted-text role="ref"}),
or other declarations (see `Ambient Declarations`{.interpreted-text role="ref"}, `Annotations`{.interpreted-text role="ref"},
`Accessor Declarations`{.interpreted-text role="ref"}, `Functions with Receiver`{.interpreted-text role="ref"}).
Top-level declarations can be exported.

The syntax of *top-level declarations* is presented below:

``` {.abnf}
topDeclaration:
    ('export' 'default'?)?
    annotationUsage?
    ( typeDeclaration
    | variableDeclarations
    | constantDeclarations
    | functionDeclaration
    | explicitFunctionOverload
    | namespaceDeclaration
    | ambientDeclaration
    | annotationDeclaration
    | accessorDeclaration
    | functionWithReceiverDeclaration
    )
    ;
```

``` {.typescript}
export let x: number[], y: number
```

::: {.index}
top-level declaration
top-level type
top-level variable
class
interface
enum
variable
constant
constant declaration
namespace
export
function
variable declaration
type declaration
function declaration
accessor declaration
function with receiver
accessor with receiver
explicit function overload
namespace
namespace declaration
declaration
ambient declaration
annotation
syntax
:::

The usage of annotations is discussed in `Using Annotations`{.interpreted-text role="ref"}.

| 

## Exported Declarations {#Exported Declarations}

Top-level declarations can use modifier `export` that make the declarations
accessible (see `Accessible`{.interpreted-text role="ref"}) in other modules by using import
(see `Import Directives`{.interpreted-text role="ref"}). The same result can be achieved by using an
export directive (see `Export Directives`{.interpreted-text role="ref"}) for a top-level declaration.
Declarations that are not exported as mentioned above can be used only
inside the module they are declared in.

``` {.typescript}
export class Point {}
export let Origin: Point = new Point(0, 0)
export function Distance(p1: Point, p2: Point): number {
  // ...
}
```

::: {.index}
top-level declaration
exported declaration
export modifier
access
accessible declaration
declaration
accessibility
module
import directive
import
:::

If a declaration is exported with the name of another exported declaration,
then a `compile-time error`{.interpreted-text role="index"} occurs.

The situation where an *export directive* uses *selectiveBindings* or
*bindingAlias* to give a new name to a declaration, and the new name clashes
with the name of another exported declaration is represented in the example
below:

``` {.typescript}
export function foo(): void {}
function bar(): void {}
export {bar as foo} // Compile-time error, entity named 'foo' is already exported
```

The same error occurs when `Re-Export Directive`{.interpreted-text role="ref"} is used as represented
in the example below:

``` {.typescript}
// file1.ets
export class A {}

// file2.ets
export class A {}

// Another file
export * from "./file1"
export * from "./file2" // Compile-time error, entity named 'A' is already exported
```

In addition, only one top-level declaration can be exported by using the default
export directive. It allows specifying no declared name when importing (see
`Default Import Binding`{.interpreted-text role="ref"} for details). A `compile-time error`{.interpreted-text role="index"}
occurs if more than one top-level declaration is marked as `default`.

``` {.typescript}
export default let PI: number = 3.141592653589
```

::: {.index}
top-level declaration
export
default export directive
declaration
name
import
import binding
:::

Another supported form of *export default* is using an expression as export
default target. This export directive effectively means that an anonymous
constant variable is created with a value equal to the value of the expression
evaluation result. The export can be imported only by providing a name for the
constant variable that is exported by using this export directive. Otherwise, a
`compile-time error`{.interpreted-text role="index"} occurs.

``` {.typescript}
// File1
class A {
  foo () {}
}
export default new A

// File2
import {default as a} from "File1"

a.foo()  // Calling method foo() of class A where 'a' is an instance of type A
a = new A // Compile-time error as 'a' is a constant variable

// File3
import * as a from "File1" /* compile-time error, such form of import
                              cannot be used for the default export */
```

forbids any exported declaration which, when
imported into a code, causes a module to access an unexported entity.
It applies to both global and namespace declarations.
Types of exported functions, variables, constants, public and protected members
of classes, default interface methods, interface getters and setters must be
set explicitly where applicable.

::: {.note}
::: {.title}
Note
:::

The statement *types of exported functions, \..., methods, \...* above
means not only the return type but the entire signature
of an entity, including, where applicable,
types of parameters. E.g., a *setter* has no return type
(not even `void`), but the type of its parameter must be
exported explicitly.
:::

Any entity declared in
the current module and used in an accessible part of an exported declaration must be
either directly available in (e.g., built-in type), or also be exported.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.note}
::: {.title}
Note
:::

By an [accessible part of an exported declaration]{.title-ref} we mean a set of entities
which can be used in another module after importing the declaration.
For example, public and protected members of an exported class belong to that
set while the private members do not belong.
:::

::: {.note}
::: {.title}
Note
:::

The above requirements of explicit type and explicit export are
also applied to `ambient declarations`{.interpreted-text role="ref"}.
:::

Here is a number of examples which violate the above rules and therefore
trigger a compile-time error,

-   Exported constants and variables, or non-private fields of exported classes
    do not have explicit types. Exported functions, or methods of exported interfaces,
    or non-private methods of exported classes do not have explicit return types.
    Exported getters (see `Accessor declarations`{.interpreted-text role="ref"}) at the top level or in a
    namespace do not have an explicit return types;
-   An exported function or an accessor uses an unexported entity in its signature.
    An exported variable, or constant uses an unexported entity as a type.
    Note, that use of an unexported entity as a default for an
    `optional parameters`{.interpreted-text role="ref"} is allowed.
-   An exported generic entity uses an unexported declaration as a type
    argument, type parameter constraint or a type parameter default (including cases
    when the type argument is not used elsewhere in exported the declaration);
-   An unexported class or interface is used in `extends` clause of exported
    class or interface, or an unexported interface is used in `implements` clause
    of an exported class. A public or protected class field uses an unexported
    entity as a type. A public or protected method of exported class uses an
    unexported entity in its signature;
-   An exported type alias declaration uses unexported type;
-   An annotation which is applied to the exported declaration is not exported or
    uses an unexported type;
-   An exported overload contains one or more unexported entities;

Here is the series of examples representing that cases:

1.  An exported declarations without explicit types or explicit return types.

    ``` {.typescript}
    // // functions, variables, constants
    export let a: int = 1 // OK
    export let b = 1 // Compile-time error - no explicit type

    export const c: int = 1 // OK
    export const d = 1 // Compile-time error - no explicit type

    export function foo(): void {} // OK

    export function bar() {}  // Compile-time error, no return type

    // // Fields and methods
    export class C {
       // static and instance fields and methods (public and protected)
       x = 1   // Compile-time error, no explicit type for a public field
       protected xx = 1   // Compile-time error, no explicit type for a protected field
       static v = 1 // Compile-time error, no explicit type for public field
       y: int = 1   // OK
       private z = 1 // OK - not a public/protected field

       foo() { return 1 } // Compile-time error, no explicit return type 
                        // for a public method

       static bar() {} // Compile-time error, no explicit
                       // return type for a public static method
       static bar_ok(): void {} // OK


       protected i_bar() { return 1 } // Compile-time error, no return
                                    // type for a protected method
       protected bar_ok(): int { return 1 } // OK

       private baz() { return "hello" } // OK, baz() is private
    }

    // // Interfaces
    // OK
    export interface I {
       get_count(): number { return 1; }
       set_count(n: number): void {}
    }

    // Compile-time error, no explicit return types for get_count and set_count
    export interface J {
       get_count() { return 1; }
       set_count(n: number) {}
    }

    // // getters
    let _counter: int = 1  // OK
    let _name = "empty"         // OK
    export get counter() { return _counter } // Compile-time error, no return type
    export get name(): string { return _name } // OK

    export namespace NS {
       get name() { return "Bob" } // OK since not exported
       export get age(): int { return 1 }  // OK
       export get sex() { return "male" } // Compile-time error, no explicit
                                          // return type
    }
    ```

2.  An exported function, a variable, a constant, or an accessor with unexported
    entity.

    ``` {.typescript}
    class A { constructor(a: A) {}; };

    // The following declarations cause compile-time errors
    // because 'A' is not exported
    export let v: A
    export function foo (p: A): A { return p; }
    export const x3: A = new A()
    export get val(): A { return new A() }
    export set val(a: A) {}

    export class B { constructor(B: B) {}; };
    class C extends B {};

    // Next is OK, can use an unexported default as an optional parameter
    export function bar(p: B = new C() ) {}
    ```

> | 

3.  An exported generic uses an unexported entity.

    ``` {.typescript}
    class Arg {};

    // OK since T is a type parameter
    export class G<T> {}

    // Compile-time error, type parameter default 'Arg' not exported
    export function foo<T = Arg>(): void {}
    // Compile-time error, type parameter constraint 'Arg' not exported
    export function foo<T extends Arg>(): void {}
    ```

> | 

4.  An exported class or interface uses an unexported entity as a type of a public
    or protected field or in a signature of public or protected method.

    ``` {.typescript}
    class C { constructor() {} ; };
    interface I {};

    // // unexported type in extends/implements
    // Compile-time error, 'C' and 'I' must be exported
    export class C1 extends C implements I {}
    // Compile-time error, 'I' must be exported
    export interface I1 extends I {}

    // // unexported entity inside a declaration
    export class C1 {
       // // Compile-time errors due to unexported 'C'
       f: C = new C;
       doIt(): C { return new C(); }
       protected tryMe(): C { return new C(); }

       // // OK, unexported 'C' can be used in private members/fields
       private secret(): C { return new C(); }
    }
    ```

> | 

5.  An exported type alias declaration refers to an unexported type.

    ``` {.typescript}
    class C {};

    // Compile-time error, 'C' must be exported
    export type A = C
    ```

    | 

6.  An annotation applied to an exported declaration not exported or uses an unexported type.

    ``` {.typescript}
    type Version = number[];

    // compile time error, ``Version`` not exported
    export @interface deprecated {
                      fromVersion: Version;
                   }

    export @deprecated([1, 1]) function bar() {};

    |
    ```

7.  One or more unexported entities in an exported overload:

    ``` {.typescript}
    function foo(): void  {};
    export function bar(): void  {};

    // Compile-time error, `foo` not exported
    export overload baz { foo, bar }
    ```

    | 

::: {.index}
exported declaration
expression
top-level declaration
modifier export
constant variable
evaluation result
export
default target
export target
export directive
accessibility
declaration
export
declared name
default export directive
import
value
:::

| 

## Export Directives {#Export Directives}

*Export directive* allows the following:

-   Specifying a selective list of exported declarations with optional
    renaming;
-   Specifying a name of one declaration;
-   Exporting a type; or
-   Re-exporting declarations from other modules.

The syntax of an *export directive* is presented below:

``` {.abnf}
exportDirective:
    selectiveExportDirective
    | singleExportDirective
    | exportTypeDirective
    | reExportDirective
    ;
```

Limitations on exported declarations are described with examples in
`Exported declarations`{.interpreted-text role="ref"}.

::: {.index}
export directive
export
declaration
exported declaration
renaming
re-export
re-exporting declaration
module
syntax
:::

::: {.index}
default method
exported interface
explicit type
module with ambient declaration
ambient declaration
:::

| 

### Selective Export Directive {#Selective Export Directive}

Top-level declarations can be made *exported* by using a selective export
directive. The selective export directive provides an explicit list of names
of the declarations to be exported. Optional renaming allows having the
declarations exported with new names.

The syntax of *selective export directive* is presented below:

``` {.abnf}
selectiveExportDirective:
    'export' selectiveBindings
    ;
```

A selective export directive uses the same *selective bindings* as an import
directive:

``` {.typescript}
export { d1, d2 as d3}
```

The above directive exports \'d1\' by its name, and \'d2\' as \'d3\'. The name \'d2\'
is not accessible (see `Accessible`{.interpreted-text role="ref"}) in the modules that import this
module.

::: {.index}
selective export directive
selective export
top-level declaration
export
export directive
declaration
directive
renaming
import directive
selective binding
module
access
accessibility
:::

| 

### Single Export Directive {#Single Export Directive}

*Single export directive* allows specifying the declaration to be exported from
the current module by using the declaration\'s own name, or anonymously.

The syntax of *single export directive* is presented below:

``` {.abnf}
singleExportDirective:
    'export'
    ( 'type'? identifier
    | 'default' (expression | identifier)
    | '{' identifier 'as' 'default' '}'
    )
    ;
```

::: {.index}
export directive
declaration
export
declaration name
module
syntax
:::

If `default` is present, then only one such export directive is possible in
the current module. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

The directive in the example below exports variable \'v\' by its name:

``` {.typescript}
export v
let v: int = 1
```

The directive in the example below exports class \'A\' by its name as default
export:

``` {.typescript}
class A {}
export default A
export {A as default} // such syntax is also acceptable
```

::: {.index}
export directive
module
directive
syntax
:::

The directive in the example below exports a constant variable anonymously:

``` {.typescript}
class A {}
export default new A
```

*Single export directive* acts as re-export when the declaration referred to by
*identifier* is imported.

``` {.typescript}
import {v} from "some location"
export v
```

::: {.index}
export
directive
constant variable
export directive
re-export
declaration
identifier
import
:::

| 

### Export Type Directive {#Export Type Directive}

An export directive can have a `type` modifier exclusively for a better
syntactic compatibility with (also see `Import Type Directive`{.interpreted-text role="ref"}).

The *export type directive* syntax is presented below:

``` {.abnf}
exportTypeDirective:
    'export' 'type' selectiveBindings
    ;
```

supports no additional semantic checks for entities exported by using
*export type* directives.

If a binding refers to something other than `type`, then a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
export
declaration
export type
export directive
semantic check
entity
directive
binding
type
syntax
:::

| 

### Re-Export Directive {#Re-Export Directive}

In addition to exporting what is declared in the module, it is possible to
re-export declarations that are part of other modules\' export.
A particular declaration or all declarations can be re-exported from a module.
When re-exporting, new names can be given. This action is similar to importing
but has the opposite direction.

The syntax of *re-export directive* is presented below:

``` {.abnf}
reExportDirective:
    'export'
    ('*' bindingAlias?
    | selectiveBindings
    | '{' 'default' bindingAlias? '}'
    )
    'from' importPath
    ;
```

::: {.index}
export
module
declaration
re-export declaration
re-export
re-export directive
import
:::

An `importPath` cannot refer to the file the current module is stored in.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

If re-exported declarations are not distinguishable (see `Declarations`{.interpreted-text role="ref"})
within the scope of the current module, then a `compile-time error`{.interpreted-text role="index"}
occurs.

The re-exporting practices are represented in the following examples:

``` {.typescript}
export * from "path_to_the_module" // re-export all exported declarations
export * as qualifier from "path_to_the_module"
   // re-export all exported declarations with qualification
export { d1, d2 as d3} from "path_to_the_module"
   // re-export particular declarations some under new name
export {default} from "path_to_the_module"
   // re-export default declaration from the other module
export {default as name} from "path_to_the_module"
   // re-export default declaration from the other module under 'name'
```

::: {.index}
import path
module
storage
re-export
re-exported declaration
declaration
scope
:::

| 

## Top-Level Statements {#Top-Level Statements}

A module can contain sequences of statements that logically
comprise one sequence of statements.

The syntax of *top-level statements* is presented below:

``` {.abnf}
topLevelStatements:
    statement*
    ;
```

::: {.index}
top-level statement
module
statement
syntax
:::

A module can contain any number of top-level statements that logically
merge into a single sequence in the textual order:

``` {.typescript}
statements_1
/* top-declarations except constant and variable declarations */
statements_2
```

The sequence above is equal to the following:

``` {.typescript}
/* top-declarations except constant and variable declarations */
statements_1; statements_2
```

This situation is represented by the example below:

::: {.index}
module
top-level statement
variable declaration
constant declaration
declaration
:::

``` {.typescript}
// The actual text combination of the statements and declarations
console.log ("Start of top-level statements")
type A = number | string
let a: A = 56
function foo () {
   console.log (a)
}
a = "a string"


// The logically ordered text - declarations then statements
type A = number | string
function foo () {
   console.log (a)
}
console.log ("Start of top-level statements")
let a: A = 56
a = "a string"
```

::: {.index}
top-level statement
declaration
module
statement
:::

-   If a module is imported by some other module, then the semantics of
    top-level statements is to initialize the imported module. It means that all
    top-level statements are executed only once before a call to any other
    function, or before the access to any top-level variable of the module.
-   If a module is used as a program, then top-level statements are used
    as a program entry point (see `Program Entry Point`{.interpreted-text role="ref"}). The set of
    top-level statements being empty implies that the program entry point is also
    empty and does nothing. If a module has the `main` function, then
    it is executed after the execution of the top-level statements.

::: {.index}
module
imported module
semantics
top-level statement
initialization
import
module
call
access
accessibility
program entry point
function
:::

``` {.typescript}
// Source file A
{ // Block form
  console.log ("A.top-level statements")
}

// Source file B
import * as A from "Source file A "
function main () {
   console.log ("B.main")
}
```

The output is as follows:

A.  Top-level statements,
B.  Main.

``` {.typescript}
// One source file
console.log ("A.Top-level statements")
function main () {
   console.log ("B.main")
}
```

A `compile-time error`{.interpreted-text role="index"} occurs if top-level statements contain a
return statement (`Expression Statements`{.interpreted-text role="ref"}).

The execution of top-level statements means that all statements, except type
declarations, are executed one after another in the textual order of their
appearance within the module until an error is thrown (see
`Errors`{.interpreted-text role="ref"}), or last statement is executed.

Thus, if a top-level statement refers to a variable or constant and the
declaration of that variable or constant (see
`Variable and Constant Declarations`{.interpreted-text role="ref"}) is textually located after the
the current statement, then a `compile-time error`{.interpreted-text role="index"} occurs.

``` {.typescript}
console.log (a, b) // Compile-time error
let a = 1
const b = a
```

See details for variable or constant declarations validity in
`Validity of Initializer`{.interpreted-text role="ref"}.

::: {.index}
top-level statement
return statement
expression statement
expression
statement
type declaration
module
error
:::

| 

## Multifile Module {#Multifile Module}

*Multifile module* is a module that consists of several source files
which have the same *module header* (see `Module header`{.interpreted-text role="ref"}).

If two *module headers* (see `Module header`{.interpreted-text role="ref"}) have the same *moduleName*
but different `export` modifiers, then a `compile-time error`{.interpreted-text role="index"} occurs.

A *multifile module* combines `Import Directives`{.interpreted-text role="ref"},
`Top-Level Declarations`{.interpreted-text role="ref"}, and `Export Directives`{.interpreted-text role="ref"}
for all files of the module.

A *multifile module* has the following limitations:

-   If top-level statements (see `Top-Level Statements`{.interpreted-text role="ref"}) are
    located in different files, then a `compile-time error`{.interpreted-text role="index"}
    occurs.

A correct *multifile module* is represented in the example below:

``` {.typescript}
// file1
export module "x"
import {A} from "some module"
export a

// file2
export module "mod1"
let a = new A()
```

``` {.typescript}
// file1
module "x"
function foo() {}
function bar() {}
namespace NS1 {
    function foo() {}
    function bar() {}
}

// file2
module "x"
class A {}
```

An incorrect *multifile module* is represented in the example below:

``` {.typescript}
// file1
module "y"
let a = 8
namespace NS1 {
    let a = 9
}

// file2
module "y"
let b = 4       // Compile-time error, the top-level statements located in several files
namespace NS1 {
    let b = 6   // Compile-time error, the top-level statements located in several files
}
```

::: {.index}
multifile module
:::

| 

## Standard Library Usage {#Standard Library Usage}

A set of entities exported from the standard library (see
`Standard Library`{.interpreted-text role="ref"})
is accessible as simple names (see `Accessible`{.interpreted-text role="ref"}) at module scope and
in nested scopes if not redefined.
Using these names as names of programmer-defined entities at the module scope
causes a `compile-time error`{.interpreted-text role="index"} as discussed in `Declarations`{.interpreted-text role="ref"}.

``` {.typescript}
console.log("Hello, world!") // OK, 'console' is defined in the standard library

let console = 5 // Compile-time error
```

::: {.index}
entity
export
scope
name
accessibility
access
simple name
standard library
access
declaration
:::

| 

## Program Entry Point {#Program Entry Point}

Modules can act as programs (applications). Program execution starts
from the execution of a *program entry point* which can be of the following two
kinds:

-   Top-level statements for modules (see `Top-Level Statements`{.interpreted-text role="ref"}); or
-   Entry point function (see below).

::: {.index}
module
top-level statement
return statement
execution
program entry point
entry point function
:::

A module can have the following forms of entry point:

-   Sole entry point function (`main` or other as described below);
-   Sole top-level statement (the first statement in the top-level statements
    acts as the entry point);
-   Both top-level statement and entry point function (same as above, plus the
    function called after the top-level statement execution is completed).

::: {.index}
module
entry point
entry point function
top-level statement
statement
:::

Entry point functions have the following features:

-   Any exported top-level function can be used as an entry point. An entry point
    is selected by the compiler, the execution environment, or both;
-   Entry point function must either have no parameters, or have one parameter of
    type `FixedArray<string>` that provides access to the arguments of a program command
    line;
-   Entry point function return type is either `void` (see
    `Type void or undefined`{.interpreted-text role="ref"}) or `int`;
-   Entry point function cannot be overloaded;
-   Entry point function is called `main` by default.

::: {.index}
entry point
entry point function
function
compiler
execution
parameter
string type
access
argument
return type
void type
int type
overloading
top-level statements
default
:::

Different forms of valid and invalid entry points are represented in the example
below:

``` {.typescript}
function main() {
  // Option 1: a return type is inferred from the body of main().
  // It will be 'int' if the body has 'return' with the integer expression
  // and 'void' if no return at all in the body
}

function main(): void {
  // Option 2: explicit :void - no return in the function body required
}

function main(): int {
  // Option 3: explicit :int - return is required
  return 0
}

function main(): string { // Compile-time error, incorrect main signature
  return ""
}

function main(p: number) { // Compile-time error, incorrect main signature
}

// Option 4: top-level statement is the entry point
console.log ("Hello, world!")

// Option 5: top-level exported function
export function entry(): void {}

// Option 5: top-level exported function with command-line arguments
export function entry(cmdLine: FixedArray<string>): void {}
```

::: {.index}
entry point
entry point function
command-line argument
signature
function body
inferred type
integer expression
function body
:::

| 

```{=pdf}
PageBreak
```
