# Semantic Rules {#Semantic Rules}

This Chapter contains semantic rules to be used throughout this Specification
document. The description of the rules is more or less informal. Some details
are omitted to simplify the understanding.

::: {.index}
semantic rule
:::

| 

## Semantic Essentials {#Semantic Essentials}

The section gives a brief introduction to the major semantic terms
and their usage in several contexts.

::: {.index}
semantic term
context
:::

| 

### Type of Standalone Expression {#Type of Standalone Expression}

*Standalone expression* (see `Type of Expression`{.interpreted-text role="ref"}) is an expression for
which there is no target type in the context where the expression is used.

The type of a *standalone expression* is determined as follows:

-   In case of `Numeric Literals`{.interpreted-text role="ref"}, the type is the default type of a literal:

    > -   Type of `Integer Literals`{.interpreted-text role="ref"} is `int` or `long`;
    > -   Type of `Floating-Point Literals`{.interpreted-text role="ref"} is `double` or `float`.

-   In case of `Constant Expressions`{.interpreted-text role="ref"}, the type is inferred from operand
    types and operations.

-   In case of an `Array Literal`{.interpreted-text role="ref"}, the type is inferred from the elements
    (see `Array Type Inference from Types of Elements`{.interpreted-text role="ref"}).

-   Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs. Specifically,
    a `compile-time error`{.interpreted-text role="index"} occurs if an *object literal* is used
    as a *standalone expression*.

The situation is represented in the example below:

::: {.index}
standalone expression
type of expression
expression
target type
context
type
integer literal
floating-point literal
constant expression
inferred type
operand type
operand
array literal
object literal
:::

``` {.typescript}
function foo() {
  1    // type is 'int'
  1.0  // type is 'number'
  [1.0, 2.0]  // type is number[]
  [1, "aa"] // type is (int | string)
}
```

| 

### Specifics of Assignment-like Contexts

*Assignment-like context* (see `Assignment-like Contexts`{.interpreted-text role="ref"}) can be
considered as an assignment `x = expr`, where `x` is a left-hand-side
expression, and `expr` is a right-hand-side expression. E.g., there is an
implicit assignment of `expr` to the formal parameter `foo` in the call
`foo(expr)`, and implicit assignments to elements or properties in
`Array Literal`{.interpreted-text role="ref"} and `Object Literal`{.interpreted-text role="ref"}.

*Assignment-like context* is specific in that the type of a left-hand-side
expression is known, but the type of a right-hand-side expression is not
necessarily known in the context as follows:

-   If the type of a right-hand-side expression is known from the expression
    itself, then the `Assignability`{.interpreted-text role="ref"} check is performed as in the example
    below:

::: {.index}
assignment-like context
context
assignment
expression
type
assign
assignability
:::

``` {.typescript}
function foo(x: string, y: string) {
    x = y // OK, assignability is checked
}
```

-   Otherwise, an attempt is made to apply the type of the left-hand-side
    expression to the right-hand-side expression. A `compile-time error`{.interpreted-text role="index"}
    occurs if the attempt fails as in the example below:

``` {.typescript}
function foo(x: int, y: double[]) {
    x = 1 // OK, type of '1' is inferred from type of 'x'
    y = [1, 2] // OK, array literal is evaluated as [1.0, 2.0]
}
```

::: {.index}
assignability
expression
type
:::

| 

### Specifics of Variable Initialization Context

If the variable or a constant declaration (see
`Variable and Constant Declarations`{.interpreted-text role="ref"}) has an explicit type annotation,
then the same rules as for *assignment-like contexts* apply. Otherwise, there
are two cases for `let x = expr` (see `Type Inference from Initializer`{.interpreted-text role="ref"})
as follows:

-   The type of the right-hand-side expression is known from the expression
    itself, then this type becomes the type of the variable as in the example
    below:

``` {.typescript}
function foo(x: int) {
    let y = x // type of 'y' is 'int'
}
```

-   Otherwise, the type of `expr` is evaluated as type of a standalone
    expression as in the example below:

``` {.typescript}
function foo() {
    let x = 1 // x is of type 'int' (default type of '1')
    let y = [1, 2] // x is of type 'number[]'
}
```

::: {.index}
variable
initialization
context
constant declaration
assignment-like context
annotation
declaration
type inference
initializer
expression
standalone expression
function
:::

| 

### Specifics of Numeric Operator Contexts {#Specifics of Numeric Operator Contexts}

The `postfix` and `prefix` `increment` and `decrement`
operators evaluate `byte` and `short` operands without
widening. It is also true for an `assignment` operator (considering
`assignment` as a binary operator).

For other numeric operators, the operands of unary and binary numeric expressions
are widened to a larger numeric
type. The minimum type is `int`. None of those operators
evaluates values of types `byte` and `short` without widening. Details of
specific operators are discussed in corresponding sections of the Specification.

::: {.index}
numeric operator
context
numeric operator context
operand
unary numeric expression
binary numeric expression
widening
numeric type
type
:::

| 

### Specifics of String Operator Contexts {#Specifics of String Operator Contexts}

If one operand of the binary operator `'+'` is of type `string`, then the
string conversion applies to another non-string operand to convert it to string
(see `String Concatenation`{.interpreted-text role="ref"} and `String Operator Contexts`{.interpreted-text role="ref"}).

::: {.index}
string operator
string operator context
context
operand
binary operator
string type
string conversion
non-string operand
string concatenation
:::

| 

### Other Contexts {#Other Contexts}

The only semantic rule for all other contexts, and specifically for
`Overriding`{.interpreted-text role="ref"}, is to use `Subtyping`{.interpreted-text role="ref"}.

::: {.index}
context
semantic rule
overriding
subtyping
:::

| 

### Specifics of Type Parameters {#Specifics of Type Parameters}

If the type of a left-hand-side expression in *assignment-like context* is a
type parameter, then it provides no additional information for type inference
even where a type parameter constraint is set.

If the *target type* of an expression is a *type parameter*, then the type of
the expression is inferred as the type of a *standalone expression*.

The semantics is represented in the example below:

::: {.index}
type parameter
type
assignment-like context
context
type inference
constraint
target type
expression
standalone expression
semantics
:::

``` {.typescript}
class C<T extends number> {
    constructor (x: T) {}
}

new C(1) // Compile-time error
```

The type of `'1'` in the example above is inferred as `int` (default type of
an integer literal). The expression is considered `new C<int>(1)` and causes
a `compile-time error`{.interpreted-text role="index"} because `int` is not a subtype of `number`
(type parameter constraint).

Explicit type argument `new C<number>(1)` must be used to fix the code.

::: {.index}
inferred type
default type
integer literal
expression
subtype
parameter constraint
type
argument
:::

| 

### Semantic Essentials Summary {#Semantic Essentials Summary}

Major semantic terms are listed below:

-   `Type of Expression`{.interpreted-text role="ref"};
-   `Assignment-like Contexts`{.interpreted-text role="ref"};
-   `Type Inference from Initializer`{.interpreted-text role="ref"};
-   `Numeric Operator Contexts`{.interpreted-text role="ref"};
-   `String Operator Contexts`{.interpreted-text role="ref"};
-   `Subtyping`{.interpreted-text role="ref"};
-   `Assignability`{.interpreted-text role="ref"};
-   `Overriding`{.interpreted-text role="ref"};
-   `Overloading`{.interpreted-text role="ref"};
-   `Type Inference`{.interpreted-text role="ref"}.

::: {.index}
semantics
type inference
initializer
string operator
context
subtyping
assignment-like context
expression
assignability
numeric operator
overriding
overloading
:::

| 

## Subtyping {#Subtyping}

*Subtype* relationship between types `S` and `T`, where `S` is a
subtype of `T` (recorded as `S<:T`), means that any object of type
`S` can be safely used in any context to replace an object of type `T`.
The opposite relation (recorded as `T:>S`) is called *supertype* relationship.
Each type is its own subtype and supertype (`S<:S` and `S:>S`).

By the definition of `S<:T`, type `T` belongs to the set of *supertypes*
of type `S`. The set of *supertypes* includes all *direct supertypes*
(discussed in subsections), and all their respective *supertypes*.
More formally speaking, the set is obtained by reflexive and transitive
closure over the direct supertype relation.

The terms *subclass*, *subinterface*, *superclass*, and *superinterface* are
used in the following sections as synonyms for *subtype* and *supertype*
when considering non-generic classes, generic classes, or interface types.

If a relationship of two types is not described in one of the following
sections, then the types are not related to each other. Specifically, two
`Resizable Array Types`{.interpreted-text role="ref"} and two `Tuple Types`{.interpreted-text role="ref"} are not related to each
other, except where they are identical (see `Type Identity`{.interpreted-text role="ref"}).

``` {.typescript}
class Base {}
class Derived extends Base {}

function not_a_subtype (
   ab: Array<Base>, ad: Array<Derived>,
   tb: [Base, Base], td: [Derived, Derived],
) {
   ab = ad // Compile-time error
   tb = td // Compile-time error
}
```

::: {.index}
subtyping
subtype
subclass
subinterface
type
object
closure
supertype
superclass
superinterface
direct supertype
reflexive closure
transitive closure
array type
array
resizable array
fixed-size array
tuple type
:::

| 

### Subtyping for Non-Generic Classes and Interfaces {#Subtyping for Non-Generic Classes and Interfaces}

`S` for non-generic classes and interfaces is a direct *subclass* or
*subinterface* of `T` (or of `Object` type) when one of the following
conditions is true:

-   Class `S` is a *direct subtype* of class `T` (`S<:T`) if `T` is
    mentioned in the `extends` clause of `S` (see `Class Extension Clause`{.interpreted-text role="ref"}):

    ``` {.typescript}
    // Illustrating S<:T
    class T {}
    class S extends T {}
    function foo(t: T) {}

    // Using T
    foo(new T)

    // Using S (S<:T)
    foo(new S)
    ```

-   Class `S` is a *direct subtype* of class `Object` (`S<:Object`) if
    `S` has no `Class Extension Clause`{.interpreted-text role="ref"}:

    ``` {.typescript}
    // Illustrating S<:Object
    class S {}
    function foo(o: Object) {}

    // Using Object
    foo(new Object)

    // Using S (S<:Object)
    foo(new S)
    ```

-   Class `S` is a *direct subtype* of interface `T` (`S<:T`) if `T` is
    mentioned in the `implements` clause of `S` (see
    `Class Implementation Clause`{.interpreted-text role="ref"}):

    ``` {.typescript}
    // Illustrating S<:T
    // S is class, T is interface
    interface T {}
    class S implements T {}
    function foo(t: T) {}
    let s: S = new S

    // Using T
    let t: T = s
    foo(t)

    // Using S (S<:T)
    foo(s)
    ```

-   Interface `S` is a *direct subtype* of interface `T` (`S<:T`) if `T`
    is mentioned in the `extends` clause of `S` (see
    `Superinterfaces and Subinterfaces`{.interpreted-text role="ref"}):

    ``` {.typescript}
    // Illustrating S<:T
    // S is interface, T is interface
    interface T {}
    interface S extends T {}
    function foo(t: T) {}
    let t: T
    let s: S

    // Using T
    class A implements T {}
    t = new A
    foo(t)

    // Using S (S<:T)
    class B implements S {}
    s = new B
    foo(s)
    ```

-   Interface `S` is a *direct subtype* of class `Object` (`S<:Object`) if
    `S` has no `extends` clause (see `Superinterfaces and Subinterfaces`{.interpreted-text role="ref"}).

    ``` {.typescript}
    // Illustrating subinterface of Object
    interface S {}
    function foo(o: Object) {}

    // Using Object
    foo(new Object)

    // Using subinterface of Object
    class A implements S {}
    let s: S = new A;
    foo(s)
    ```

::: {.index}
subtype
subclass
subinterface
supertype
superclass
superinterface
interface type
implementation
non-generic class
extension clause
implementation clause
Object
class extension
:::

| 

### Subtyping for Generic Classes and Interfaces {#Subtyping for Generic Classes and Interfaces}

A *generic class* or *generic interface* is declared as
`C` \<`F`~1~ `,..., F`~n~\>, where *n*\>0 is a *direct subtype* of
another generic class or interface `T`, if one of the following conditions is
true:

-   `T` is a *direct superclass* of `C` \<`F`~1~ `,..., F`~n~\>
    mentioned in the `extends` clause of `C`:

    ``` {.typescript}
    // T<U, V>  is direct superclass of C<U,V>
    // T<U, V> >: C<U, V>

    class T<U, V> {
       foo(p: U|V): U|V { return p }
    }

    class C<U, V> extends T<U, V> {
       bar(u: U): U { return u }
    }


    // OK, exact match
    let t: T<int, boolean>  = new T<int, boolean>
    let c: C<int, boolean> = new C<int, boolean>


    // OK, assigning to direct superclass
    t =  new C<int, boolean>

    // Compile-time error, cannot assign to subclass
    c =  new T<int, boolean>
    ```

-   `T` is one of direct superinterfaces of `C`
    \<`F`~1~ `,..., F`~n~\> (see
    `Superinterfaces and Subinterfaces`{.interpreted-text role="ref"}):

    ``` {.typescript}
    // Interface I<U, V>  is direct superinterface
    // of J<U,V>, X<U, V>

    interface I<U, V> {
       foo(u: U): U;
       bar(v: V): V;
    }

    // J<U, V> <: I<U, V>
    // since J extends I
    interface J<U, V> extends I<U, V>
    {
       foo(u: U): U
       bar(v: V): V

       foo1(p: U|V): U|V
    }

    // X<U, V> <: I<U, V>
    // since X implements I
    class X<U, V> implements I<U,V> {
      foo(u: U): U { return u }
      bar(v: V): V { return v }
    }

    // Y<U,V> <: J<U, V>  (directly)
    // Also Y<U, V> <: I<U, V> (transitively)
    class Y<U, V> implements J<U,V> {
      foo(u: U): U { return u }
      bar(v: V): V { return v }

      foo1(p: U|V): U|V { return p }
    }

    let i: I<int, boolean>
    let j: J<int, boolean>
    let x = new X<int, boolean>
    let y = new Y<int, boolean>

    // OK, assigning to direct supertypes
    i = x
    j = y

    // OK, assigning subinterface (J<:I)
    i = j

    // Compile-time error, cannot assign superinterface (I>:JJ
    j = i
    ```

-   `T` is type `Object` (C\<:Object) if
    `C` \<`F`~1~ `,..., F`~n~\>
    is either a generic class type with no *direct superclasses*,
    or a generic interface type with no direct superinterfaces:

    ``` {.typescript}
    // Object is direct superclass and for C<U,V>
    // and direct superinterface for I<U,V>
    //
    class C<U, V> {
       foo(u: U): U { return u }
       bar(v: V): V { return v }
    }
    interface I<U, V> {
       foo(u: U): U { return u }
       bar(v: V): V { return v }
    }

    let o: Object = new Object
    let c: C<int, boolean> = new C<int, boolean>
    let i: I<int, boolean>

    // // example1 - C<U,V> <: Object
    function example1(o: Object) {}

    // OK, example(Object)
    example1(o)
    // OK, C<int, boolean> <: Object
    example1(c)

    // // example2 - I<U,V> <: Object
    function example2(o: Object) {}
    class D<U, V> implements I<U, V> {}
    i = new D<int, boolean>

    // OK, example2(Object)
    example2(o)
    // OK, I<int, boolean> <: Object
    example2(i)
    ```

The direct supertype of a type parameter is the type specified as the
constraint of that type parameter.

If type parameters of a generic class or an interface have a variance specified
(see `Type Parameter Variance`{.interpreted-text role="ref"}), then the subtyping for instantiations of
the class or interface is determined in accordance with the variance of the
appropriate type parameter. For example, if a generic class `G<in T1,out T2>`
is defined, `S>:U` and `T<:V`, then `G<S,T> <: G<U, V>`.
It is represented by the following code:

``` {.typescript}
// Subtyping illustration for a generic with parameter variance

// U1 <: U0
class U0 {}
class U1 extends U0 {}

// Generic with contravariant parameter
class E<in T> {}

let e0: E<U0> = new E<U1> // Compile-time error, E<U0> is subtype of E<U1>
let e1: E<U1> = new E<U0> // OK, E<U1> is supertype for E<U0>

// Generic with covariant parameter
class F<out T> {}

let f0: F<U0> = new F<U1> // OK, F<U0> is supertype for F<U1>
let f1: F<U1> = new F<U0> // Compile-time error, F<U1> is subtype of F<U0>
```

::: {.index}
direct supertype
generic type
generic class
generic interface
interface type declaration
direct superinterface
type parameter
superclass
supertype
type
constraint
type parameter
superinterface
variance
subtyping
instantiation
class
interface
bound
Object
:::

| 

### Subtyping for Literal Types {#Subtyping for Literal Types}

Any `string` literal type (see `String Literal Types`{.interpreted-text role="ref"}) is *subtype* of type
`string`. It affects overriding as shown in the example below:

``` {.typescript}
class Base {
    foo(p: "1"): string { return "42" }
}
class Derived extends Base {
    override foo(p: string): "1" { return "1" }
}
// Type "1" <: string

let base: Base = new Derived
let result: string = base.foo("1")
/* Argument "1" (value) is compatible to type "1" and to type string in
   the overridden method
   Function result of type string accepts "1" (value) of literal type "1"
*/
```

Literal type `null` (see `Literal Types`{.interpreted-text role="ref"}) is a subtype and a supertype to
itself. Similarly, literal type `undefined` is a subtype and a supertype to
itself.

::: {.index}
literal type
subtype
subtyping
string type
overriding
supertype
string literal
null type
undefined type
literal type
supertype
:::

| 

### Subtyping for Tuple Types {#Subtyping for Tuple Types}

Any tuple type is a subtype of type `Tuple` (see `Type Tuple`{.interpreted-text role="ref"}).

Tuple type `T` (`P`~1~ `, ... , P`~n~) is a subtype of
type `S` (`P`~1~ `, ... , P`~m~), where `n` $\geq$ `m`.
I.e., a tuple type is a subtype of a tuple type with fewer identical
constituent types (`Type Identity`{.interpreted-text role="ref"}).

``` {.typescript}
function foo(t1: [number], t2: [string, number]) {
    let a: [] = t1       // OK
    let b: [string] = t2 // OK

    t1 = t2 // Compile-time error
    t2 = t1 // Compile-time error

    let d: [string, number, boolean] = ["a", 1, true]
    let t2 = d // OK
    let d = t2 // Compile-time error
}
```

| 

### Subtyping for Union Types {#Subtyping for Union Types}

A union type `U` participates in a subtyping relationship
(see `Subtyping`{.interpreted-text role="ref"}) in the following cases:

1\. Union type `U` (`U`~1~ `| ... | U`~n~) is a subtype of
type `T` if each `U`~i~ is a subtype of `T`.

``` {.typescript}
let s1: "1" | "2" = "1"
let s2: string = s1 // OK

let a: string | number | boolean = "abc"
let b: string | number = 42
a = b // OK
b = a // Compile-time error, boolean is absent is 'b'

class Base {}
class Derived1 extends Base {}
class Derived2 extends Base {}

let x: Base = ...
let y: Derived1 | Derived2 = ...

x = y // OK, both Derived1 and Derived2 are subtypes of Base
y = x // Compile-time error

let x: Base | string = ...
let y: Derived1 | string ...
x = y // OK, Derived1 is subtype of Base
y = x // Compile-time error
```

::: {.index}
union type
subtyping
subtype
type
string
boolean
:::

2\. Type `T` is a subtype of union type `U`
(`U`~1~ `| ... | U`~n~) if for some `i`
`T` is a subtype of `U`~i~.

``` {.typescript}
let u: number | string = 1 // OK
u = "aa" // OK
u = 1.0  // OK, 1.0 is of type 'number' (double)
u = 1    // Compile-time error, type 'int' is not a subtype of 'number'
u = true // Compile-time error
```

::: {.index}
union type
union type normalization
subtype
number type
:::

::: {.note}
::: {.title}
Note
:::

If union type normalization produces a single type, then this type is used
instead of the initial set of union types. This concept is represented
in the example below:

``` {.typescript}
let u: "abc" | "cde" | string // type of 'u' is string
```
:::

::: {.note}
::: {.title}
Note
:::

A case of two union types is clarified as follows: union type `U2`
(`U2`~1~ `| ... | U2`~n~) is a subtype of union type `U1`
(`U1`~1~ `| ... | U1`~m~) if Step 1 applies first,
followed by Step 2 applied to every type of `U2`.

``` {.typescript}
class T1 {}
class T2 {}
class T3 extends T1 {}  // T3 <: T1
class T4 extends T2 {}  // T4 <: T2
class T5 {}

type U1 = T1 | T2
type U2 = T3 | T4 | T5

function foo (u1: U1, u2: U2) {
    u1 = u2
    // step 1. U2 to be a subtype of U1 iff T3 <: U1 and T4 <: U1 and T5 <: U1
    // step 2.
    //         T3 to be a subtype of T1 or T2 - T1 true
    //         T4 to be a subtype of T1 or T2 - T2 true
    //         T5 to be a subtype of T1 or T2 - false for both
    // Compile-time error as a result
}
```
:::

::: {.index}
union type
subtype
supertype
:::

| 

### Subtyping for Function Types {#Subtyping for Function Types}

Function type `F` with parameters `FP`~1~ `, ... , FP`~m~,
rest parameter `FPrest` (if present) and return type `FR` is a
*subtype* of function type `S` with parameters
`SP`~1~ `, ... , SP`~n~, rest parameter `SPrest`
(if present) and return type `SR` if **all** of the following conditions
are met:

-   Number of optional and required parameters of `F` (`m`) is equal or
    less than number of optional and required parameters of `S` (`n`).
-   Number of required parameters of `F` is equal or less than number
    of required paramers of `S`.
-   If the rest parameter `FPrest` is present then `SPrest` is present.
-   For each `i <= m`, type of `SP`~i~ is a subtype of type
    of `FP`~i~.
-   If the rest parameter `FPrest` is present:
    -   For each `i > m`, parameter type `SP` must be a subtype of the
        element type of type of `FPrest`.
    -   Type of `SPrest` should be a subtype of type of `FPrest`.
-   The resultant type `FR` is a subtype of `SR`.

::: {.index}
function type
subtype
subtyping
parameter type
contravariance
rest parameter
parameter
covariance
return type
optional parameter
:::

``` {.typescript}
class Base {}
class Derived extends Base {}

function check(
   bb: (p: Base) => Base,
   bd: (p: Base) => Derived,
   db: (p: Derived) => Base,
   dd: (p: Derived) => Derived
) {
   bb = bd
   /* OK: identical parameter types, and covariant return type */
   bb = dd
   /* compile-time error, parameter types are not contravariant */
   db = bd
   /* OK: contravariant parameter types, and covariant  return type */

   let f: (p: Base, n: number) => Base = bb
   /* OK: subtype has less parameters */

   let g: () => Base = bb
   /* compile-time error, less parameters than expected */
}

let foo: (x?: number, y?: string) => void = (): void => {} // OK: ``m <= n``
foo = (p?: number): void => {}                             // OK:  ``m <= n``
foo = (p1?: number, p2?: string): void => {}               // OK: Identical types
foo = (p: number): void => {}
      // Compile-time error, 1st parameter in type is optional but mandatory in lambda
foo = (p1: number, p2?: string): void => {}
      // Compile-time error,  1st parameter in type is optional but mandatory in lambda
```

::: {.index}
type
parameter type
covariance
contravariance
covariant return type
contravariant return type
supertype
parameter
lambda
:::

| 

### Subtyping for Fixed-Size Array Types {#Subtyping for Fixed-Size Array Types}

If a fixed-size array contains elements of reference types (see
`Reference Types`{.interpreted-text role="ref"}), then the subtyping of elements is based on the
subtyping of element types. It is formally described as follows:

`FixedSize<B> <: FixedSize<A>` if `B <: A`.

The situation is represented in the following example:

``` {.typescript}
let x: FixedArray<string> = ["aa", "bb", "cc"]
let y: FixedArray<Object> = x // OK, as string <: Object
x = y // Compile-time error
```

The subtyping allows array assignments that can cause an `ArrayStoreError`
at runtime if a value of a type that is not a subtype of the element type of
one array is put into that array by using a subtype of the element type of
another array. Type safety is ensured by runtime checks performed by the runtime
system as represented in the example below:

::: {.index}
type
subtype
subtyping
fixed-size array
fixed-size array type
array element
parameter type
runtime check
array
array element type
type safety
runtime system
:::

``` {.typescript}
class C {}
class D extends C {}

function foo (ca: FixedArray<C>) {
  ca[0] = new C() // ArrayStoreError if ca refers to FixedArray<D>
}

let da: FixedArray<D> = [new D()]

foo(da) // leads to runtime error in 'foo'
```

| 

### Subtyping for Intersection Types {#Subtyping for Intersection Types}

Intersection type `I` defined as (`I`~1~ `& ... & I`~n~)
is a subtype of type `T` if `I`~i~ is a subtype of `T`
for some *i*.

Type `T` is a subtype of intersection type
(`I`~1~ `& ... & I`~n~) if `T` is a subtype of each
`I`~i~.

::: {.index}
subtype
subtyping
intersection type
:::

| 

### Subtyping for Difference Types {#Subtyping for Difference Types}

Difference type `A - B` is a subtype of `T` if `A` is
a subtype of `T`.

Type `T` is a subtype of the difference type `A - B` if `T` is
a subtype of `A`, and no value belongs both to `T` and `B`
(i.e., `T & B = never`).

::: {.index}
subtype
subtyping
difference type
:::

| 

## Type Identity {#Type Identity}

*Identity* relation between two types means that the types are
indistinguishable. Identity relation is symmetric and transitive.
Identity relation for types `A` and `B` is defined as follows:

-   Array types `A` = `T1[]` and `B` = `Array<T2>` are identical
    if `T1` and `T2` are identical.
-   Tuple types `A` = \[`T`~1~, `T`~2~, `...`, `T`~n~\] and
    `B` = \[`U`~1~, `U`~2~, `...`, `U`~m~\]
    are identical on condition that:
    -   `n` is equal to `m`, i.e., the types have the same number of elements;
    -   Every *T*~i~ is identical to *U*~i~ for any *i* in `1 .. n`.
-   Union types `A` = `T`~1~ \| `T`~2~ \| `...` \| `T`~n~ and
    `B` = `U`~1~ \| `U`~2~ \| `...` \| `U`~m~
    are identical on condition that:
    -   `n` is equal to `m`, i.e., the types have the same number of elements;
    -   *U*~i~ in `U` undergoes a permutation after which every *T*~i~
        is identical to *U*~i~ for any *i* in `1 .. n`.
-   Types `A` and `B` are identical if `A` is a subtype of `B` (`A<:B`),
    and `B` is at the same time a subtype of `A` (`A:>B`).

::: {.note}
::: {.title}
Note
:::

`Type Alias Declaration`{.interpreted-text role="ref"} creates no new type but only a new name for
the existing type. An alias is indistinguishable from its base type.
:::

::: {.note}
::: {.title}
Note
:::

If a generic class or an interface has a type parameter `T` while its
method has its own type parameter `T`, then the two types are different
and unrelated.

``` {.typescript}
class A<T> {
   data: T
   constructor (p: T) { this.data = p } // OK, as here 'T' is a class type parameter
   method <T>(p: T) {
       this.data = p // Compile-time error as 'T' of the class is different from 'T' of the method
   }
}
```
:::

::: {.index}
type identity
identity
indistinguishable type
permutation
array type
tuple type
union type
subtype
type
type alias
type alias declaration
declaration
base type
:::

| 

## Assignability {#Assignability}

Type `T`~1~ is assignable to type `T`~2~ if:

-   `T`~1~ is a subtype of `T`~2~ (see `Subtyping`{.interpreted-text role="ref"}); or
-   *Implicit conversion* (see `Implicit Conversions`{.interpreted-text role="ref"}) is present that
    allows converting a value of type `T`~1~ to type `T`~2~.

*Assignability* relationship is asymmetric, i.e., that `T`~1~
is assignable to `T`~2~ does not imply that `T`~2~ is
assignable to type `T`~1~.

::: {.index}
assignability
assignment
type
type identity
subtyping
conversion
implicit conversion
asymmetric relationship
value
:::

| 

## Invariance, Covariance and Contravariance {#Invariance, Covariance and Contravariance}

*Variance* is how subtyping between types relates to subtyping between
derived types, including generic types (See `Generics`{.interpreted-text role="ref"}), member
signatures of generic types (type of parameters, return type),
and overriding entities (See `Override-Compatible Signatures`{.interpreted-text role="ref"}).
Variance can be of three kinds:

-   Covariance,
-   Contravariance, and
-   Invariance.

::: {.index}
variance
subtyping
type
subtyping
derived type
generic type
generic
signature
type parameter
overriding entity
override-compatible signature
parameter
variance
invariance
covariance
contravariance
:::

*Covariance* means it is possible to use a type which is more specific than
originally specified.

::: {.index}
covariance
type
:::

*Contravariance* means it is possible to use a type which is more general than
originally specified.

::: {.index}
contravariance
type
:::

*Invariance* means it is only possible to use the original type, i.e., there is
no subtyping for derived types.

::: {.index}
invariance
type
subtyping
derived type
:::

Valid and invalid usages of variance are represented in the examples below.
If class `Base` is defined as follows:

::: {.index}
variance
base class
:::

``` {.typescript}
class Base {
   method_one(p: Base): Base {}
   method_two(p: Derived): Base {}
   method_three(p: Derived): Derived {}
}
```

\-\--then the code below is valid:

``` {.typescript}
class Derived extends Base {
   // invariance: parameter type and return type are unchanged
   override method_one(p: Base): Base {}

   // covariance for the return type: Derived is a subtype of Base
   override method_two(p: Derived): Derived {}

   // contravariance for parameter types: Base is a supertype for Derived
   override method_three(p: Base): Derived {}
}
```

::: {.index}
variance
parameter type
invariance
covariance
contravariance
subtype
supertype
override method
base
overriding
method
:::

On the contrary, the following code causes compile-time errors:

``` {.typescript}
class Derived extends Base {

   // covariance for parameter types is prohibited
   override method_one(p: Derived): Base {}

   // contravariance for the return type is prohibited
   override method_three(p: Derived): Base {}
}
```

| 

## Compatibility of Call Arguments {#Compatibility of Call Arguments}

The following semantic checks must be performed to arguments from the left to
the right when checking the validity of any function, method, constructor, or
lambda call:

**Step 1**: All arguments in the form of a spread expression (see
`Spread Expression`{.interpreted-text role="ref"}) that spreads an array literal (see
`Array Literal`{.interpreted-text role="ref"}) are to be linearized recursively to ensure
that no spread expression of that form remains at the call site.

**Step 2**: The following checks are performed on all arguments from left to
right, starting from `arg_pos` = 1 and `par_pos` = 1:

> if parameter at position `par_pos` is of non-rest form then
>
> > if ~T~[arg\_pos]{.title-ref} \<: ~T~[par\_pos]{.title-ref} then increment `arg_pos` and `par_pos`
> > else a `compile-time error`{.interpreted-text role="index"} occurs, exit Step 2
>
> else // parameter is of rest form (see `Rest Parameter`{.interpreted-text role="ref"})
>
> > if parameter is of rest\_array\_form then
> >
> > > if argument is a spread expression of an array of some type [U]{.title-ref} and
> > > \'U\' \<: ~T~[rest\_array\_type]{.title-ref} then increment `arg_pos`
> > > else if ~T~[arg\_pos]{.title-ref} \<: ~T~[rest\_array\_type]{.title-ref} then increment `arg_pos`
> > > else increment `par_pos`
> >
> > else // parameter is of rest\_tuple\_form
> >
> > > for [rest\_tuple\_pos]{.title-ref} in 1 .. rest\_tuple\_types.count do
> > >
> > > > if ~T~[arg\_pos]{.title-ref} \<: ~T~[rest\_tuple\_pos]{.title-ref} then increment `arg_pos` and [rest\_tuple\_pos]{.title-ref}
> > > > else if rest\_tuple\_pos \< rest\_tuple\_types.count then increment `rest_tuple_pos`
> > > > else a `compile-time error`{.interpreted-text role="index"} occurs, exit Step 2
> > >
> > > end
> > > increment `par_pos`
> >
> > end
>
> end

::: {.index}
assignability
call argument
compatibility
semantic check
function call
method call
constructor call
function
method
constructor
rest parameter
parameter
spread operator
spread expression
array
tuple
argument type
expression
operator
assignable type
increment
array type
rest parameter
check
:::

The checks are represented in the examples below:

``` {.typescript}
function call (...p: Object[]) {}
call (...[1, "str", true], ...[ 123])  // Initial call form
call (1, "str", true, 123)             // To be unfolded into the form with
                                       // no spread expressions

let arr: number[] = [1, 2, 3]
tricky_call (...arr)  // Type 'number' is assignable to 'Object', and a new
                     // array of type 'Object[]' is created from elements
                     // of the array of numbers

function tricky_call (...p: Object[]) {
  p[0] = true
  console.log ("Initial array: ", arr)
  console.log ("Parameter array: ", p)
}

function foo1 (p: Object) {}
foo1 (1)  // Type of '1' must be assignable to 'Object'
          // p becomes 1

function foo2 (...p: Object[]) {}
foo2 (1, "111")  // Types of '1' and "111" must be assignable to 'Object'
          // p becomes array [1, "111"]

function foo31 (...p: (number|string)[]) {}
foo31 (...[1, "111"])  // Type of array literal [1, "111"] must be assignable to (number|string)[]
          // p becomes array [1, "111"]

function foo32 (...p: [number, string]) {}
foo32 (...[1, "111"])  // Types of '1' and "111" must be assignable to 'number' and 'string' accordingly
          // p becomes tuple [1, "111"]

function foo4 (...p: number[]) {}
foo4 (1, ...[2, 3])  //
          // p becomes array [1, 2, 3]
```

::: {.index}
check
assignable type
Object
string
array
:::

| 

## Type Inference {#Type Inference}

supports strong typing but allows not to burden a programmer with the
task of specifying type annotations everywhere. A smart compiler can infer
types of some entities and expressions from the surrounding context.
This technique called *type inference* allows keeping type safety and
program code readability, doing less typing, and focusing on business logic.
Type inference is applied by the compiler in the following contexts:

-   `Type Inference for Constant Expressions`{.interpreted-text role="ref"};
-   Variable and constant declarations (see `Type Inference from Initializer`{.interpreted-text role="ref"});
-   Implicit generic instantiations (see `Implicit Generic Instantiations`{.interpreted-text role="ref"});
-   Function, method or lambda return type (see `Return Type Inference`{.interpreted-text role="ref"});
-   Lambda expression parameter type (see `Lambda Signature`{.interpreted-text role="ref"});
-   Array literal type inference (see `Array Literal Type Inference from Context`{.interpreted-text role="ref"},
    and `Array Type Inference from Types of Elements`{.interpreted-text role="ref"});
-   Object literal type inference (see `Object Literal`{.interpreted-text role="ref"});
-   Smart casts (see `Smart Casts and Smart Types`{.interpreted-text role="ref"}).

::: {.index}
strong typing
type annotation
annotation
smart compiler
type inference
inferred type
expression
entity
surrounding context
code readability
type safety
context
numeric constant expression
initializer
variable declaration
constant declaration
generic instantiation
function return type
function
method return type
method
lambda
lambda return type
return type
lambda expression
parameter type
array literal
Object literal
smart type
smart cast
:::

| 

### Type Inference for Constant Expressions {#Type Inference for Constant Expressions}

The type of a constant expression (see `Constant Expressions`{.interpreted-text role="ref"}) is first
inferred from the context, if the context allows.
The following contexts allow inference:

-   `Assignment-like Contexts`{.interpreted-text role="ref"};
-   `Cast Expression`{.interpreted-text role="ref"} context;
-   `Numeric Operator Contexts`{.interpreted-text role="ref"}.

If context does not allow to to infer type, the *value default type* is set as follows:

-   `int` for a constant expression of a *big integer type*
    (see `Specifics of Constant Expressions Evaluation`{.interpreted-text role="ref"}) if its value
    can be represented by a 32-bit number;
-   `long` for a constant expression of a *big integer type*
    (see `Specifics of Constant Expressions Evaluation`{.interpreted-text role="ref"}) if its value
    can be represented by a 64-bit number;
-   `double` or `float` for a floating-point constant expression
    (see `Specifics of Constant Expressions Evaluation`{.interpreted-text role="ref"}).

Type inference is used only where the *target type* is one of the following:

-   Case 1: *Numeric type* (see `Numeric Types`{.interpreted-text role="ref"}); or
-   Case 2: Union type (see `Union Types`{.interpreted-text role="ref"}) containing at least one
    *numeric type*.

**Case 1: Target type is a numeric type**

Where a *target type* is numeric, the type of a constant expression is inferred
from the *target type* and the value of the const expression,
if one of following conditions is met:

1.  *Target type* is equal to or larger than the value default type; or
2.  Value is an *integer value* that fitting into the range
    of the *target type*.

::: {.note}
::: {.title}
Note
:::

A *floating-point suffix* if present declares a `floating-point literal`,
and no type inference occurs.
:::

If none of the conditions above is met, then the *target type* is not a
valid type for the constant expression, and a `compile-time error`{.interpreted-text role="index"} occurs.

Type inference for a numeric *target type* is represented in the examples below:

``` {.typescript}
let l: long = 1     // OK, target type is larger than literal default type
let b: byte = 127   // OK, integer value fits type 'byte'
let f: float = 123f // OK, target type is the same as literal default type
let g: double = 11  // OK, target type is larger than literal default type

b = 63 + 64           // OK, integer value fits type 'byte'
b = 1 as short        // OK, integer value fits type 'byte'
let s: short = -32767 // OK, integer value fits type 'short'

l = 1.0    // Compile-time error, 'double' cannot be assigned to 'long'
b = 128    // Compile-time error, value is out of range
f = 3.14   // Compile-time error, 'double' cannot be assigned to 'float'
```

**Case 2: Target type is a union type containing at least one numeric type**

In the case the *target type* is a union type
(`N`~1~ `| ... | N`~k~ `| ... | U`~n~), where `k`
$\geq$ `1` and `N`~i~ is a numeric type, then the inferred
literal type is determined as follows:

1.  If no `N`~i~ suits the value, then the default type is used;
2.  If only a single `N`~i~ suits the value, then `N`~i~ is the
    inferred type;
3.  If several `N` types suit the value, then the following checks are
    performed:
    -   If the value is an integer value, and only one suitable *integer*
        `N`~i~ is present, then this `N`~i~ is the inferred type.

Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs due to type inference ambiguity.

Type inference for a union target type is represented in the examples below:

``` {.typescript}
let b: byte | Object = 127 // inferred type for 127 is 'byte'
b = 128 /* inferred type for 128 is 'int' (default literal type),
           which is a subtype of Object
        */

let c: byte | string = 127 // inferred type for 127 is 'byte'
c = 128 /* inferred type for 128 is 'int' (default literal type),
           compile-time error as no type in a union is a supertype for
           'int'
        */

let d: int | double = 1.0 // inferred type for 1.0 is 'double'
d = 1 // inferred type for 1 is 'int'

let e: byte | long = 128 // inferred type for 128 is 'long'
e = 127 // Compile-time error, type inference ambiguity for 127

let f: float | double = 3.14 // inferred type is 'double'
f = 2f                       // inferred type is 'float'

let g: float | double = 3.4e39 // inferred type is 'double'
g = 1 // Compile-time error, type inference ambiguity for 1
```

::: {.index}
numeric type
inferred type
target type
integer type
context
type
union type
value
:::

::: {.note}
::: {.title}
Note
:::

If *target type* is a union type that contains no numeric type, then the
default type of the literal is used. The following code is valid as
numeric types are subtypes of \'Object\':

``` {.typescript}
let x: Object | string = 1 // OK, instance of type 'int' is assigned to 'x'

x = 1.0 // OK, instance of type 'double' is assigned to 'x'
```
:::

| 

### Return Type Inference {#Return Type Inference}

A missing function, method, getter, or lambda return type can be inferred from
the function, method, getter, or lambda body. A `compile-time error`{.interpreted-text role="index"}
occurs if return type is missing from a native function (see
`Native Functions`{.interpreted-text role="ref"}).

The current version of allows inferring return types at least under
the following conditions:

-   If there is no return statement, or if all return statements have no
    expressions, then the return type is `void` (see
    `Type void or undefined`{.interpreted-text role="ref"}). It effectively implies that a call to a
    function, method, or lambda returns the value `undefined`.
-   If there are *k* return statements (where *k* is 1 or more) with
    the same type expression *R*, then `R` is the return type.
-   If there are *k* return statements (where *k* is 2 or more) with
    expressions of types `T`~1~, `...`, `T`~k~, then `R` is the
    *union type* (see `Union Types`{.interpreted-text role="ref"}) of these types (`T`~1~ \| \... \|
    `T`~k~), and its normalized version (see `Union Types Normalization`{.interpreted-text role="ref"})
    is the return type. If at least one of return statements has no expression, then
    type `undefined` is added to the return type union.
-   If a lambda body contains no return statement but at least one throw statement
    (see `Throw Statements`{.interpreted-text role="ref"}), then the lambda return type is `never` (see
    `Type never`{.interpreted-text role="ref"}).
-   If a function, a method, or a lambda is `async` (see
    `Asynchronous execution`{.interpreted-text role="ref"}), a return type is inferred by applying
    the above rules, and the return type `T` is not `Promise`, then the return
    type is assumed to be `Promise<T>`.

Return type inference is represented in the example below:

::: {.index}
return type
function
method
getter
lambda
value
getter return type
lambda return type
function return type
method return type
native function
void type
type inference
inferred type
method body
void type
return statement
normalization
expression type
expression
function
implementation
compiler
union type
never type
async type
lambda body
:::

``` {.typescript}
// Explicit return type
function foo(): string { return "foo" }

// Implicit return type inferred as string
function goo() { return "goo" }

class Base {}
class Derived1 extends Base {}
class Derived2 extends Base {}

function bar (condition: boolean) {
    if (condition)
        return new Derived1()
    else
        return new Derived2()
}
// Return type of bar will be Derived1|Derived2 union type

function boo (condition: boolean) {
    if (condition) return 1
}
// That is a compile-time error as there is an execution path with no return
```

*Smart types* can appear in the process of return type inference
(see `Smart Casts and Smart Types`{.interpreted-text role="ref"}).
A `compile-time error`{.interpreted-text role="index"} occurs if an inferred return type is a `Type Expression`{.interpreted-text role="ref"}
that cannot be expressed in :

``` {.typescript}
class C{}
interface I {}
class D extends C implements I {}

function foo(c: C) {
    return c instanceof I ? c : new D() // Compile-time error, inferred type is C & I
}
```

::: {.index}
union type
type inference
inferred type
smart type
function
return type
execution path
smart cast
:::

| 

## Smart Casts and Smart Types {#Smart Casts and Smart Types}

uses the concept of *smart casts*, meaning that
in some cases the compiler can implicitly cast
a value of a variable to a type which is more specific than
the declared type of the variable.
The more specific type is called *smart type*.
*Smart casts* allow keeping type safety, require less typing from
programmer and improve performance.

Smart casts are applied to local variables
(see `Variable and Constant Declarations`{.interpreted-text role="ref"}) and parameters
(see `Parameter List`{.interpreted-text role="ref"}), except those that are captured and
modified in lambdas.
Further in the text term *variable* is used for both local variables
and parameters.

::: {.index}
smart cast
smart type
cast
value
variable
type
declared type
type safety
performance
local variable
parameter
lambda
:::

::: {.note}
::: {.title}
Note
:::

Smart casts are not applied to global variables and class fields, as it is
difficult to track their values.
:::

A variable has a single declared type, and can have different *smart
types* in different contexts. A *smart type* of variable is always
a subtype of its declared type.

*Smart type* is used by the compiler each time the value of a variable is read.
It is never used when a variable value is changed.

The usage and benefits of a *smart type* are represented in the example below:

``` {.typescript}
class C {}
class D extends C {
    foo() {}
}

function bar(c: C) {
    if (c instanceof D) {
        c.foo() // OK, here smart type of 'c' is 'D', 'foo' is safely called
    }
    c.foo() // Compile-time error, 'c' does not have method 'foo'
    (c as D).foo() // no compile-time error, can throw runtime error
}
```

::: {.index}
smart cast
smart type
global variable
variable
value
declared type
context
subtype
runtime
runtime error
call
:::

The compiler uses data-flow analysis based on `Control-flow Graph`{.interpreted-text role="ref"} to
compute *smart types* (see `Computing Smart Types`{.interpreted-text role="ref"}). The following
language features influence the computation:

-   Variable declarations;

-   Variable assignments (a variable initialization is handled as a variable
    declaration combined with an assignment);

-   `instanceof Expression`{.interpreted-text role="ref"} with variables;

-   Conditional statements and conditional expressions that include:

    > -   `Equality Expressions`{.interpreted-text role="ref"} of a variable and an expression that
    >     process string literals, `null` value, and `undefined` value in
    >     a specific way.
    > -   `Equality Expressions`{.interpreted-text role="ref"} of `typeof v` and a string literal, where
    >     `v` is a variable.
    > -   `Extended Conditional Expressions`{.interpreted-text role="ref"}.

-   `Loop Statements`{.interpreted-text role="ref"}.

A *smart type* usually takes the form of a `Type Expression`{.interpreted-text role="ref"} that can
contain types not otherwise represented in , namely:

-   `Intersection Types`{.interpreted-text role="ref"};
-   `Difference Types`{.interpreted-text role="ref"}.

::: {.index}
smart type
data-flow analysis
control-flow graph
variable
variable declaration
variable assignment
variable initialization
assignment
conditional statement
conditional expression
equality expression
null
expression
undefined
string literal
loop statement
extended conditional expression
intersection type
difference type
:::

| 

### Type Expression {#Type Expression}

The *type* of an entity is conventionally defined as the set of values
an entity (e.g., a variable) can take, and the set of operators
applicable to that entity. Two types with equal sets of values
and operators are considered equal irrespective of a syntactic form used to
denote the types.

However, in some cases it is useful to distinguish between equal types with
different representation or syntactic form. For example, types `Object` and
`Object|C` are equal but they behave in different ways as a context of
an `Object Literal`{.interpreted-text role="ref"}:

``` {.typescript}
class C {
    num = 1
}
function foo(x: Object|C) {}
function bar(x: Object) {}

foo({num: 42}} // OK, object literal is of type 'C'
bar({num: 42}} // Compile-time error, Object does not have field 'num'
```

::: {.index}
type expression
type
entity
value
variable
operator
set of values
syntactic form
equal type
context
object
object literal
field
:::

The term *type expression* is used below as notation that consists of type
names and operators on types, namely:

-   `'|'` for union operator;
-   `'&'` for intersection operator (see `Intersection Types`{.interpreted-text role="ref"});
-   `'-'` for difference operator (see `Difference Types`{.interpreted-text role="ref"}).

Computing *smart types* is the process of creating, evaluating, and simplifying
*type expressions*.

::: {.note}
::: {.title}
Note
:::

*Intersection types* and *difference types* are semantic (not syntactic
notions) that cannot be represented in .
:::

::: {.index}
type expression
entity
value
variable
operator
syntax
context
object literal
field
type expression
notation
type name
operator
type
intersection type
difference type
union operator
intersection operator
difference operator
semantic notion
syntactic notion
:::

| 

### Intersection Types {#Intersection Types}

An *intersection type* is a type created from other types by using the
intersection operator `'&'`.
The values of intersection type `A & B` are all values that belong
to both `A` and `B`. The same applies to the set of operations.

Intersection types cannot be expressed directly in . Instead, they appear
as *smart types* of variables in the process of `Computing Smart Types`{.interpreted-text role="ref"} as
represented below:

``` {.typescript}
class C {
    foo() {}
}
interface I {
    bar(): void
}

function test(i: I) {
    if (i instanceof C) {
        // smart type of 'i' here is of some subtype of 'C' that implements 'I'
        // type expression for this type is I & subtype of C
        i.foo() // OK
        i.bar() // OK
    }
}
```

More details are provided in `Subtyping for Intersection Types`{.interpreted-text role="ref"}.

::: {.index}
intersection type
intersection operator
value
set of operators
operation
variable
type
subtype
implementation
subtyping
:::

| 

### Difference Types {#Difference Types}

A *difference type* is a type created from two other types by a subtraction
operation, i.e., by using the operator `'-'`.
The values of the difference type `A - B` are all values that belong to type
`A` but not to type `B`. The same applies to the set of operations.

Difference types in cannot be expressed directly. They appear as
*smart types* of variables in the process of `Computing Smart Types`{.interpreted-text role="ref"}:

``` {.typescript}
function foo(x: string | undefined): number {
    if (x == undefined) {
        return 0
    } else {
        // smart type of 'x' here is (string | undefined - undefined) = string,
        // hence, string property can be applied to 'x'
        return x.length
    }
}
```

This is discussed in detail in `Subtyping for Difference Types`{.interpreted-text role="ref"}.

::: {.index}
difference type
difference operator
subtraction operation
operator
value
set of operators
smart type
variable
type
string
property
:::

| 

### Computing Smart Types {#Computing Smart Types}

Computing smart types is based on *must-alias sets*. A *must-alias set* is a set of
variables known to have the same value in a given context.

Two maps are used to specify a context `(l, s)`, where:

-   *l: V* $\rightarrow$ *L*, map from variables *V* to must-alias sets *L*;
-   *s: L* $\rightarrow$ *T*, map from must-alias sets to smart types *T*
    ascribed to those sets.

Contexts are computed in relation to nodes of `Control-flow Graph`{.interpreted-text role="ref"}.
Control-flow graph (CFG) contains the following kinds of nodes:

-   Nodes for expressions that have results assigned to variables,
    including temporary variables;
-   *Branching nodes* that have true and false branches;
-   *Assuming nodes* that have an assumed condition specified;
-   *Backedge nodes* that mark the transfer of control from the end
    point of a loop to its start point.

::: {.index}
smart type
must-alias set
set of variables
context
value
map
variable
node
control-flow graph (CFG)
expression
branching node
assuming node
backedge node
control
control transfer
loop
start point
branch
true branch
false branch
:::

The way maps *(l, s*) are changed when processing specific nodes is described
below.

The notation $N(x)$ is used to denote a union of type `x` and all types
to which type `x` can be converted, namely:

> -   If `x` is a numeric type, then a larger numeric type;
> -   If `x` is an enumeration type, then *enumeration base type*.

The notation $x'$ is used to denote a map that replaces any previous map
during node evaluation.

At a **variable declaration** `let v: T`:

-   `l(v):={v}`;
-   `s(l(v)):={T}`, where `T` is a the declared type of `v`,
    that is either set explicitly, or inferred from an initializer expression.

In an **assignment to the variable** `v`: `v = e`:

-   If *e* is a variable, and no implicit conversions are performed, then:

    > -   `l'(v):={v}` $\cup$ `l(e)`;
    > -   `l'(u):={v}` $\cup$ `l(e)` for each `u` $\in$ `l(e)`;
    > -   `l'(u):=l(v)-{v}` for each `u` $\in$ `l(v)-{v}`;
    > -   `s'(l'(v)):=s(l(e))`;
    > -   `s'(l(v)-{v}):=s(l(v))`.

-   Otherwise:

    > -   `l'(v):={v}`;
    > -   `l'(u):=l(v)-{v}` for each `u` $\in$ `l(v)-{v}`;
    > -   `s'(l'(v)):=N(T(e)`, where `T(e)` is the smart type of `e`.

Maps evaluation at an *assumption node* are summarized in the
following table:

::: {.index}
map
node
notation
node evaluation
conversion
variable
smart type
type
numeric type
enumeration base type
context
assumption node
:::

+--------------------+------------------------+------------------------+
| Branching on       | Positive Branch        | Negative Branch        |
+====================+========================+========================+
| *v* `instanceof`   | Assuming *v*           | Assuming !(*v*         |
| `A`                | `instanceof` `A`:      | `instanceof` `A`):     |
|                    |                        |                        |
|                    | `s'(l(v)):=s(l(v))&A`  | `s'(l(v)):=s(l(v))-A`, |
+--------------------+------------------------+------------------------+
| *v* `===` *str*    | `s'(l(v)):=str`        | `                      |
| (string literal)   |                        | s'(l(v)):=s(l(v))-str` |
+--------------------+------------------------+------------------------+
| *v* `===`          | `s'(l(v)):=undefined`  | `s'(l(v                |
| `undefined`        |                        | )):=s(l(v))-undefined` |
+--------------------+------------------------+------------------------+
| *v* `===` `null`   | `s'(l(v)):=null`       | `s                     |
|                    |                        | '(l(v)):=s(l(v))-null` |
+--------------------+------------------------+------------------------+
| *v* `==`           | `s'(                   | `s'(l(v)):= s          |
| `undefined`        | l(v)):=undefined|null` | (l(v))-undefined-null` |
+--------------------+------------------------+------------------------+
| *v* `==` `null`    | `s'(                   | `s'(l(v)):= s          |
|                    | l(v)):=null|undefined` | (l(v))-undefined-null` |
+--------------------+------------------------+------------------------+
| *v* `===` *ec*,    | `s'(l(v)):=N(ec)`      | `s'(l(v)):=s(l(v))`    |
| where *ec* is an   |                        |                        |
| `enum` constant    |                        |                        |
+--------------------+------------------------+------------------------+
| `typeof` *v* `===` | `s'(l(v)):= s(l(v))&T` | `                      |
| *str*              |                        | s'(l(v)) := s(l(v))-T` |
|                    |                        |                        |
| See **Note 2**     |                        |                        |
| below for          |                        |                        |
| evaluation of type |                        |                        |
| *T*.               |                        |                        |
+--------------------+------------------------+------------------------+
| *v* `===` *e*,     | If *e* is the variable | No change              |
| where *e* is any   | *w*, no implicit       |                        |
| expression         | conversion occurs,     |                        |
|                    | and no consideration   |                        |
|                    | is given to            |                        |
|                    | `null == undefined`,   |                        |
|                    | then:                  |                        |
|                    |                        |                        |
|                    | `l'(                   |                        |
|                    | v):=l'(w):=l(v)`$\cup$ |                        |
|                    | `l(w)`                 |                        |
|                    |                        |                        |
|                    | Otherwise,             |                        |
|                    |                        |                        |
|                    | `s'(l                  |                        |
|                    | '(v))=s(l(v))&N(T(e))` |                        |
|                    |                        |                        |
|                    | The definitions of `T` |                        |
|                    | and `N` are as in the  |                        |
|                    | assignment clause.     |                        |
+--------------------+------------------------+------------------------+
| *v* (truthiness    | `s'(l(v)):=s(l(v))     | `s'(l(v)):=s(l(v))&T`, |
| check)             | - (null|undefined|"")` |                        |
|                    |                        | where `T` is union of  |
|                    |                        | all types the contain  |
|                    |                        | at least one value     |
|                    |                        | considered as `false`  |
|                    |                        | in                     |
|                    |                        | `Extende               |
|                    |                        | d Conditional Expressi |
|                    |                        | ons`{.interpreted-text |
|                    |                        | role="ref"}.           |
+--------------------+------------------------+------------------------+

::: {.index}
positive branch
negative branch
string literal
branching
conversion
expression
value
truthiness check
union
type
:::

::: {.note}
::: {.title}
Note
:::

1.  In the table above the operator `'==='` can be replaced for `'=='`
    except where the separate case for `'=='` is listed explicitly.
2.  For branching on `typeof` *v* `===` *str*, type *T* is
    evaluated in accordance with the value of *str* as follows:

  ----------------------------------------------------------------------------------------------------
  Value of *str*             Type of *T*
  -------------------------- -------------------------------------------------------------------------
  `"boolean"`                `boolean`

  `"string"`                 `string`

  `"bigint"`                 `bigint`

  `"char"`                   `char`

  `"undefined"`              `undefined`

  A name of a numeric type   The same numeric type

  `"object"`                 `(Object - all types for which typeof is not equal to "object") | null`
  ----------------------------------------------------------------------------------------------------
:::

At a **node that joins two CFG branches**, namely
`C`~1~ `= ( l`~1~, `s`~1~ `)`, and
`C`~2~ `= ( l`~2~, `s`~2~ `)`,
the following is performed for each variable `v`:

-   `l'(v):=l`~1~ `(v)`$\cap$ `l`~2~ `(v)`; and
-   `s'(l'(v)):=s`~1~ `(l`~1~ `(v))|s`~2~ `(l`~2~ `(v))`.

At each **backedge node**, the following updates are performed for each variable `m`
modified in the loop body:

-   `l'(u):=l(m)-{m}` for each `u` $\in$ `l(m)-{m}`;
-   `l'(m):={m}`;
-   `s'(l'(m)):={T}`, where `T` is the declared type of `m`.

::: {.index}
value
node
branch
variable
declared type
control-flow graph (CFG)
:::

| 

### Control-flow Graph {#Control-flow Graph}

Computing smart types based on *control-flow graph* that describes
the possible evaluation paths of a function body
(graphs are intraprocedural).

See `Computing Smart Types`{.interpreted-text role="ref"} for a list of CFG nodes that influences
computation.

TBD: Describe how each language construct is translated to a CFG fragment.

::: {.index}
control-flow graph (CFG)
smart type
evaluation path
function body
:::

| 

### Type Expression Simplification {#Type Expression Simplification}

The following table summarizes the contexts for *type expression simplification*
transformations to be performed at each node of the CFG:

  -------------------------------------------------------------------------------------
  Transformation                          Initial expression    Simplified expression
  --------------------------------------- --------------------- -----------------------
  Associativity of `'&'`                  `(A&B)&C`             `A&(B&C)`

  Commutativity of `'&'`                  `A&B`                 `B&A`

  In case of subtyping `A<:B` and `'&'`   `A&B`                 `A`

                                          `A&never`             `never`

                                          `A&Any`               `A`

  Associativity of `'|'`                  `(A|B)C`              `A|(B|C)`

  Commutativity of `'|'`                  `A|B`                 `B|A`

  In case of subtyping `A<:B` and `'|'`   `A|B`                 `B`

                                          `A|never`             `A`

                                          `A|Any`               `Any`

  Difference with `never`                 `A-never`             `A`

  In case of subtyping `A<:B` and `'-'`   `A-B`                 `never`

                                          `A-Any`               `never`

                                          `(B-A)|A`             `B`

                                          `(A-B)&B`             `never`

  Other transformations                   `(A&B)-C`             `(A-C)&(B-C)`

                                          `(A|B)&C`             `(A&C)|(B&C)`

                                          `(A|B)-C`             `(A-C)|(B-C)`

                                          `(A-B)-C`             `(A-(B|C)`
  -------------------------------------------------------------------------------------

::: {.index}
control-flow graph (CFG)
type expression
type
expression
node
commutativity
associativity
subtyping
simplification transformation
:::

The following simplifications for object types are also taken into account:

1.  If `A` and `B` are classes and neither transitively extends the other,
    then `A&B = never`, `A-B = A`.
2.  If `A` is a final class that does not implement the interface *I*, then
    `A&I = never`, `A-I = A`.
3.  If `A` is a class or interface, and *U* is `never` or `undefined`, then
    `A&U = never`, `A-U = A`.

The following normalization procedure is performed for every *smart type* at
every node of CFG where possible:

1.  Push *difference types* inside *intersection types* and unions, and
    simplify the difference.
2.  Push *intersection types* inside unions, and simplify the intersections.
3.  Simplify the resultant union types.

After a simplification, *smart types* undergo approximation with *difference
types* `A-B` recursively replaced by `A`.

::: {.index}
control-flow graph (CFG)
intersection type
smart type
difference type
union
union type
implementation
:::

| 

### Smart Cast Examples {#Smart Cast Examples}

By using variable initializers or an assignment the compiler can narrow
(smart cast) a declared type to a more precise subtype (smart type). It
allows operations that are specific to the subtype:

``` {.typescript}
function boo() {
    let a: number | string = 42
    a++ /* Smart type of 'a' is number and number-specific
       operations are type-safe */
}

class Base {}
class Derived extends Base { method () {} }
function goo() {
   let b: Base = new Derived
   b.method () /* Smart type of 'b' is Derived and Derived-specific
       operations can be applied in type-safe way */
}
```

::: {.index}
assignment
compiler
subtype
type safety
interface type
:::

Other examples are explicit calls to `instanceof` or checks against `undefined`
(see `Equality Expressions`{.interpreted-text role="ref"}) as parts of `if` statements
(see `if Statements`{.interpreted-text role="ref"}) or ternary conditional expressions
(see `Ternary Conditional Expressions`{.interpreted-text role="ref"}):

``` {.typescript}
class Base { method() { console.log("Base")}; }
class Derived extends Base { method() { console.log("Derived")};  }

function foo (b: Base|null, d: Derived|undefined) {
   if (b instanceof Base) {
      b.method()
   }
   if (d != undefined) {
      d.method()
   }
}

console.log('call with (Base, Derived)')
foo( new Base(), new Derived())
console.log('call with (null, undefined)')
foo(null, undefined)
/* Output is:
   call with (Base, Derived)
   Base
   Derived
   call with (null, undefined)
*/
```

| 

::: {.index}
call
instanceof
null
if statement
ternary conditional expression
expression
method
:::

In like cases, a smart compiler requires no additional checks or casts (see
`Cast Expression`{.interpreted-text role="ref"}) to deduce a smart type of an entity.

`Overloading`{.interpreted-text role="ref"} can cause tricky situations
when a smart type results in calling an entity that suits the smart type
rather than a declared type of an argument (see
`Overload Resolution`{.interpreted-text role="ref"}):

``` {.typescript}
class Base {b = 1}
class Derived extends Base{d = 2}

function fooBase (p: Base) {}
function fooDerived (p: Derived) {}

overload foo { fooDerived, fooBase }

function too() {
    let a: Base = new Base
    foo (a) // fooBase will be called
    let b: Base = new Derived
    foo (b) // as smart type of 'b' is Derived, fooDerived will be called
}
```

::: {.index}
smart compiler
check
smart type
entity
cast expression
check
overloading
type
type argument
function
overload resolution
compiler
:::

| 

## Overriding {#Overriding}

*Method overriding* is the language feature closely connected with inheritance.
It allows a subclass or a subinterface to offer a specific
implementation of a method already defined in its supertype optionally
with modified signature.

The actual method to be called is determined at runtime based on object type.
Thus, overriding is related to *runtime polymorphism*.

::: {.note}
::: {.title}
Note
:::

*Overriding* does not apply to constructors.
:::

uses the *override-compatibility* rule to check the correctness of
overriding. The *overriding* is correct if method signature in a subtype
(subclass or subinterface) is *override-compatible* with the method defined
in a supertype (see `Override-Compatible Signatures`{.interpreted-text role="ref"}).

An implementation is forced to `Make a Bridge Method for Overriding Method`{.interpreted-text role="ref"}
in some cases of *method overriding*.

::: {.index}
overriding
method overriding
subclass
subinterface
supertype
signature
method signature
runtime polymorphism
inheritance
parent class
object type
runtime
override-compatibility
override-compatible signature
implementation
bridge method
method overriding
:::

| 

### Overriding in Classes {#Overriding in Classes}

::: {.note}
::: {.title}
Note
:::

Only accessible (see `Accessible`{.interpreted-text role="ref"}) methods are subjected to overriding.
The same rule applies to accessors in case of overriding.
:::

An overriding method can retain access modifier of a method from a superclass
or a superinterface, or change [protected]{.title-ref} for [public]{.title-ref}
(see `Access Modifiers`{.interpreted-text role="ref"}).
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
overloading
class
inheritance
overriding
class
constructor
accessibility
access
private method
method
subclass
accessor
superclass
access modifier
implementation
superinterface
:::

``` {.typescript}
class Base {
   public public_member() {}
   protected protected_member() {}
   private private_member() {}
}

interface Interface {
   public_member()             // All members are public in interfaces
   private private_member() {} // Except private methods with default implementation
}

class Derived extends Base implements Interface {
   public override public_member() {}
      // Public member can be overridden and/or implemented by the public one
   public override protected_member() {}
      // Protected member can be overridden by the protected or public one
   override private_member() {}
      // A compile-time error occurs as private methods of a superclass or
      // a superinterface are not accessible in the derived class, and such
      // a declaration attempt has nothing to override. 
   private_member() {}
      // Will be a correct method declaration which is not related to 
      // private methods with the same name and signature from a supoer class
      // or superinterfaces
}
```

If an *instance method* is defined or inherited by a subclass with the same name as the
*instance method* in a superclass or superinterface, then the following semantic rules are
applied:

-   If signatures are not *override-compatible* (see
    `Override-Compatible Signatures`{.interpreted-text role="ref"}), and
    if signatures formed by using *effective
    signature types* of original signatures
    are *override-compatible* after type erasure,
    then a `compile-time error`{.interpreted-text role="index"} occurs.
-   If signatures are *override-compatible* (see
    `Override-Compatible Signatures`{.interpreted-text role="ref"}), then the method of subinterface overrides
    the method of superinterface *in* the subinterface.
-   Otherwise, `Implicit Method Overloading`{.interpreted-text role="ref"} is used.

::: {.index}
context
semantic check
instance method
subclass
superclass
override-compatible signature
overriding
override-compatibility
:::

Overriding methods from a superclass is represented in the example below:

``` {.typescript}
class Base {
   method_1() {}
   method_2(p: number) {}
}
class Derived extends Base {
   override method_1() {} // overriding
   override method_2(p: string) {} // Compile-time error, not override-compatible
}
```

Overriding a method from a superinterface by a method from a superclass is represented in the example below:

``` {.typescript}
interface I {
   m(): void
}

class Base {
   m() { }
}
class Derived extends Base implements I {
   // method 'm' inherited from 'Base' overrides 'm' defined in 'I'
}
```

A single method in a subclass can override several methods of a superclass:

``` {.typescript}
class B {}
class C {
    foo(a: A) {}
    foo(b: B) {}
}
class D extends C {
    foo(o: Object) { console.log("foo in D")}
}

let c: C = new D()
c.foo(new A()) // output: foo in D
c.foo(new B()) // output: foo in D
```

If more than one method of the subclass overrides the same method of the
superclass a `compile-time error`{.interpreted-text role="index"} occurs:

``` {.typescript}
class I{
   foo (p: C) {}
}
class C extends I { // More than one method of class C overrides the same method
   foo (p: C) {}
   foo (p: I) {}
}
```

| 

### Overriding in Interfaces {#Overriding in Interfaces}

If a method is defined in a subinterface with the same name as an accessible
method in the superinterface, then the following semantic rules apply:

-   If signatures are not *override-compatible* (see
    `Override-Compatible Signatures`{.interpreted-text role="ref"}), and
    if signatures formed by using *effective
    signature types* of original signatures
    are *override-compatible* after type erasure,
    then a `compile-time error`{.interpreted-text role="index"} occurs.
-   If signatures are *override-compatible* (see
    `Override-Compatible Signatures`{.interpreted-text role="ref"}), then the method of subinterface overrides
    the method of superinterface *in* the subinterface.
-   Otherwise, `Implicit Method Overloading`{.interpreted-text role="ref"} is used.

``` {.typescript}
interface Base {
   m(p: string): void
   m(p: number): void
}
interface Derived extends Base {
   m(p: object): void  // m overrides both Base.m(string) and Base.m(number)
}
```

::: {.note}
::: {.title}
Note
:::

Several methods of superinterface can be overridden by a single method in
a subinterface.
:::

::: {.index}
overriding
interface
subinterface
name
method
superinterface
signature
override-compatible signature
override-compatibility
overriding
subinterface
private method
:::

``` {.typescript}
interface Base {
   method_1()
   method_2(p: number)
   method_3(): string
   method_4(a: Array<string>)
   private foo() {} // private method with implementation body
}
interface Derived extends Base {
   method_1()           // overriding
   method_2(p: string)  // overloading
   method_3(): number // Compile-time error, bad overriding, return type mismatch
   method_4(a: Array<number>)  // Compile-time error, original signatures are
                               // not override-compatible, but effective
                               // signatures after type erasure are compatible.
   foo(p: number): void // it is just a new method declaration
                        // Base.foo() is not accessible here at all
}
```

If more than one method of the subinterface overrides the same method of the
superinterface a `compile-time error`{.interpreted-text role="index"} occurs.

``` {.typescript}
interface I{
   foo (p: C): void
}
interface C extends I { // More than one method of interface C overrides the same method
   foo (p: C): void
   foo (p: I): void
}
```

| 

### Override-Compatible Signatures {#Override-Compatible Signatures}

Let\'s consider classes `Derived` and `Base` for which:

-   `Derived` is a subclass of `Base`
-   both classes declare method `foo`
-   in `Base`, `foo()` has a signature `S`~1~
    \<`V`~1~ `, ... V`~k~\>
    (`U`~1~ `, ..., U`~n~) `:U`~n+1~,
-   in `Derived`, `foo()` has a signature `S`~2~
    \<`W`~1~ `, ... W`~j~\>
    (`T`~1~ `, ..., T`~m~) `:T`~m+1~

as in the example below:

::: {.index}
override-compatible signature
override-compatibility
class
base class
derived class
signature
:::

``` {.typescript}
class Base {
   foo <V1, ... Vk> (p1: U1, ... pn: Un): Un+1
}
class Derived extends Base {
   override foo <W1, ... Wj> (p1: T1, ... pm: Tm): Tm+1
}
```

The signature `S`~2~ is override-compatible with `S`~1~
only if **all** of the following conditions are met:

1.  Number of parameters of both methods is the same, i.e., `n = m`.
2.  Each parameter type `T`~i~ is a supertype of `U`~i~
    for `i` in `1..n` (contravariance).
3.  If return type `T`~m+1~ is `this`, then `U`~n+1~ is `this`,
    or any of superinterfaces or superclass of the current type.
4.  If return type `T`~m+1~ is not `this`, then it must be a subtype
    of `U`~n+1~ (covariance).
5.  Number of type parameters of either method is the same, i.e., `k = j`.
6.  Constraints of `W`~1~, \... `W`~j~ are to be contravariant
    (see `Invariance, Covariance and Contravariance`{.interpreted-text role="ref"}) to the appropriate
    constraints of `V`~1~, \... `V`~k~.

::: {.index}
signature
override-compatible signature
override compatibility
class
signature
method
parameter
superinterface
superclass
return type
type
contravariant
covariance
invariance
constraint
type parameter
:::

The following rule applies to generics:

> -   Derived class must have type parameter constraints to be subtypes
>     (see `Subtyping`{.interpreted-text role="ref"}) of respective type parameter constraints
>     in the base type;
> -   Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
generic
derived class
subtyping
subtype
type parameter
base type
:::

``` {.typescript}
class Base {}
class Derived extends Base {}
class A1 <CovariantTypeParameter extends Base> {}
class B1 <CovariantTypeParameter extends Derived> extends A1<CovariantTypeParameter> {}
    // OK, derived class may have type compatible constraint of type parameters

class A2 <ContravariantTypeParameter extends Derived> {}
class B2 <ContravariantTypeParameter extends Base> extends A2<ContravariantTypeParameter> {}
    // Compile-time error, derived class cannot have non-compatible constraints of type parameters
```

The semantics is represented in the examples below:

1.  **Class/Interface Types**

``` {.typescript}
interface Base {
    param(p: Derived): void
    ret(): Base
}

interface Derived extends Base {
    param(p: Base): void    // Contravariant parameter
    ret(): Derived          // Covariant return type
}
```

::: {.index}
class type
semantics
interface type
contravariant parameter
covariant return type
:::

2.  **Function Types**

``` {.typescript}
interface Base {
    param(p: (q: Base)=>Derived): void
    ret(): (q: Derived)=> Base
}

interface Derived extends Base {
    param(p: (q: Derived)=>Base): void  // Covariant parameter type, contravariant return type
    ret(): (q: Base)=> Derived          // Contravariant parameter type, covariant return type
}
```

::: {.index}
function type
covariant parameter type
contravariant return type
contravariant parameter type
covariant return type
:::

3.  **Union Types**

``` {.typescript}
interface BaseSuperType {}
interface Base extends BaseSuperType {
   // Overriding for parameters
   param<T extends Derived, U extends Base>(p: T | U): void

   // Overriding for return type
   ret<T extends Derived, U extends Base>(): T | U
}

interface Derived extends Base {
   // Overriding kinds for parameters, Derived <: Base
   param<T extends Base, U extends Object>(
      p: Base | BaseSuperType // contravariant parameter type:  Derived | Base <: Base | BaseSuperType
   ): void
   // Overriding kinds for return type
   ret<T extends Base, U extends BaseSuperType>(): T | U
}
```

::: {.index}
union type
return type
parameter
overriding
:::

4.  **Type Parameter Constraint**

``` {.typescript}
interface Base {
    param<T extends Derived>(p: T): void
    ret<T extends Derived>(): T
}

interface Derived extends Base {
    param<T extends Base>(p: T): void       // Contravariance for constraints of type parameters
    ret<T extends Base>(): T                // Contravariance for constraints of the return type
}
```

Override compatibility with `Object` is represented in the example below:

::: {.index}
contravariance
constraint
return type
type parameter
override compatibility
:::

``` {.typescript}
enum E  { One, Two }
interface Base {
   kinds_of_parameters<T extends Derived, U extends Base>(
      // It represents all possible kinds of parameter type
      p01: Derived,
      p02: (q: Base)=>Derived,
      p03: number,
      p04: T | U,
      p05: E,
      p06: Base[],
      p07: [Base, Base]
   ): void
   kinds_of_return_type(): Object // It can be overridden by all subtypes of Object
}
interface Derived extends Base {
   kinds_of_parameters( // Object is a supertype for all class types
      p1: Object,
      p2: Object,
      p3: Object,
      p4: Object,
      p5: Object,
      p6: Object,
      p7: Object
   ): void
}

interface Derived1 extends Base {
   kinds_of_return_type(): Base // Valid overriding
}
interface Derived2 extends Base {
   kinds_of_return_type(): (q: Derived)=> Base // Valid overriding
}
interface Derived3 extends Base {
   kinds_of_return_type(): number // Valid overriding
}
interface Derived4 extends Base {
   kinds_of_return_type(): number | string // Valid overriding
}
interface Derived5 extends Base {
   kinds_of_return_type(): E // Valid overriding
}
interface Derived6 extends Base {
   kinds_of_return_type(): Base[] // Valid overriding
}
interface Derived7 extends Base {
   kinds_of_return_type(): [Base, Base] // Valid overriding
}
```

::: {.index}
parameter type
overriding
subtype
supertype
overriding
compatibility
:::

| 

## Overloading {#Overloading}

*Overloading* is the language feature that allows using the same name to
call several functions, methods, or constructors with different signatures.

The actual function, method, or constructor to be called is determined at
compile time. Thus, *overloading* is compile-time *polymorphism by name*.

supports the following two *overloading* mechanisms:

-   *Implicit overloading*, where a set of overloaded entities for functions and
    methods is determined by their names, or includes all constructors;
    and
-   *Explicit overloading* (see `Explicit Overload Declarations`{.interpreted-text role="ref"}) that allows
    a developer to specify a set of overloaded entities explicitly.

::: {.index}
overloading
name
context
entity
function
constructor
method
signature
compile-time polymorphism
polymorphism by name
explicit overload declaration
:::

In either case, an ordered set of overloaded entities is built at compile time,
and used by `Overload Resolution`{.interpreted-text role="ref"} to select one entity to call from within
the set. *Overload resolution* uses the first-match algorithm to streamline
the resolution process, i.e., only the first appropriate entity is called, while
all other entities are not considered.

If signatures of *implicitly overloaded entities* are
*overload-equivalent*, then a `compile-time error`{.interpreted-text role="index"} occurs (see
`Overload-Equivalent Signatures`{.interpreted-text role="ref"}). *Explicitly overloaded entities* are
never checked for overload equivalence. *Explicitly overloaded entities*
with separate names never cause a `compile-time error`{.interpreted-text role="index"}.

Overloading for the module scope name *main* is prohibited, and causes a
`compile-time error`{.interpreted-text role="index"} if attempted:

``` {.typescript}
function main() {}
function main(p: string[]) {}
// Such declarations lead to a compile-time error
```

| 

### Implicit Function Overloading {#Implicit Function Overloading}

Two or more functions declared with the same name in the same
declaration scope are *implicitly overloaded*.

::: {.note}
::: {.title}
Note
:::

Same-name functions declared in different scopes cannot be *implicitly
overloaded* (see `Declaration Distinguishable by Signatures`{.interpreted-text role="ref"}).
A `compile-time error`{.interpreted-text role="index"} occurs if the names of an imported function
and of a function declared in the current module are the same.
:::

When calling an overloaded function (see `Function Call Expression`{.interpreted-text role="ref"}),
`Overload Resolution`{.interpreted-text role="ref"} is used to determine exactly which function must be
called.

::: {.index}
implicit function overloading
declaration scope
signature
name
overload-equivalence
overload-equivalent signature
overloaded function
function call
:::

``` {.typescript}
function foo(p: number) {} // #1
function foo(p: string) {} // #2

foo(5)   // function marked #1 is called
foo("5") // function marked #2 is called
```

::: {.index}
overload set
call
:::

If signatures of two implicitly overloaded non-generic functions are
overload-equivalent (see `Overload-Equivalent Signatures`{.interpreted-text role="ref"}), then a
`compile-time error`{.interpreted-text role="index"} occurs. However, an implicit overload with
instantiation of a generic and overload-equivalent non-generic
function causes no compile-time error, and the textually first function is
used:

``` {.typescript}
function goo(x: int): void {}
function goo(x: int): void {}  // Compile-time error, overload-equivalent
                               // non-generic functions

function foo<T>(x: T) {}
function foo(x: number) {}

foo(1)   // OK, instance of foo<T>() with T=number called

function bar(x: number) {}
function bar<T>(x: T) {}

bar(1)   // OK, plain bar() called
```

| 

### Implicit Method Overloading {#Implicit Method Overloading}

Two or more methods within a class or an interface are implicitly overloaded
if:

-   All have the same name;
-   All are either `static` or non-`static`.

A `compile-time error`{.interpreted-text role="index"} occurs if signatures of two implicitly overloaded
methods are *overload-equivalent* (see `Overload-Equivalent Signatures`{.interpreted-text role="ref"}).

::: {.index}
implicit method overloading
class
signature
overload-equivalent signature
overload equivalence
overloaded method
method
instantiation
interface
:::

Implicit overload can be caused by method declaration or inheritance:

``` {.typescript}
class Base{
    foo(p: number) {} // #1
}

class Derived extends Base {
    foo(p: string) {} // #2
}

let d = new Derived()

d.foo(5)   // method marked #1 is called
d.foo("5") // method marked #2 is called
```

When calling an overloaded method (see `Method Call Expression`{.interpreted-text role="ref"}),
`Overload Resolution`{.interpreted-text role="ref"} is used to determine exactly which method is to be
called.

::: {.index}
implicit method overloading
overload-equivalence
overload-equivalent signature
overloaded function
method call
:::

``` {.typescript}
class C{
    foo(p: number) {} // #1
    foo(p: string) {} // #2
}

let c = new C()

c.foo(5)   // method marked #1 is called
c.foo("5") // method marked #2 is called
```

If an instantiation of a generic class or a generic interface leads to an
*overload-equivalent* method, then the textually first method is called:

``` {.typescript}
class Template<T> {
   foo (p: T) { console.log("generic foo") }
   foo (p: number) { console.log("plain foo") }
   bar (p: number) { console.log("plain bar") }
   bar (p: T) { console.log("generic bar") }
}

// This instantiation leads to two *overload-equivalent* methods
let instantiation: Template<number> = new Template<number>

instantiation.foo(1)  // prints 'generic foo'
instantiation.bar(1)  // prints 'plain bar'
```

| 

### Implicit Constructor Overloading {#Implicit Constructor Overloading}

Two or more constructors within a class are *implicitly overloaded*. If
signatures of two overloaded constructors are *overload-equivalent* (see
`Overload-Equivalent Signatures`{.interpreted-text role="ref"}), then a `compile-time error`{.interpreted-text role="index"}
occurs.

`Overload Resolution`{.interpreted-text role="ref"} is used to determine exactly which one constructor is
to be called in a class instance creation expression (see `New Expressions`{.interpreted-text role="ref"}).

::: {.index}
constructor overloading
constructor
class instance
instance creation expression
compile time
:::

``` {.typescript}
class BigFloat {
    /*other code*/
    constructor (n: number) {/*body1*/} // #1
    constructor (s: string) {/*body2*/} // #2
}

new BigFloat(1)      // constructor, marked #1,  is used
new BigFloat("3.14") // constructor, marked #2,  is used
```

| 

### Overload-Equivalent Signatures {#Overload-Equivalent Signatures}

Signatures *S1* and *S2* are *overload-equivalent* if:

-   Both have the same number of parameters;
-   *Effective signature types* (see `Type Erasure`{.interpreted-text role="ref"}) of each parameter type in *S1*
    and *S2* are equal.

Return types of *S1* and *S2* do not affect *overload-equivalence*.

The following code causes a `compile-time error`{.interpreted-text role="index"} as function signatures
are *overload-equivalent*:

``` {.typescript}
function foo(x: Array<string>): string {}
function foo(x: Array<number>): number {} // Compile-time error
```

::: {.index}
overload-equivalent signature
signature
overload equivalence
:::

| 

## Overload Resolution {#Overload Resolution}

*Overload resolution* is used to select one entity to call from an *ordered
set of overloaded entities* (called in short *overload set*) in a function
call or a method call or a constructor call, where the constructor call is
a part of a new expression (see `New Expressions`{.interpreted-text role="ref"}).

An *overload set* for each overloaded name is formed while processing
declarations. The process (see `Forming an Overload Set`{.interpreted-text role="ref"}) takes into
account the following:

-   Textual order of implicitly overloaded entities;
-   Listing order of explicit overload declarations; and
-   Inheritance.

The *overload resolution* process is rather straightforward. The process takes
overloaded entities one after another from an *overload set*, and checks the call
of each entity to be valid for the arguments given. The first entity for which
the call is valid is the selected entity. Other entities are not checked
after the first valid entity is found.

A `compile-time`{.interpreted-text role="index"} occurs if a call is invalid for any overload entities.

A call of an entity is valid if:

-   Each required parameter has an argument;
-   There is no excess argument that fails to correspond to a parameter,
    including to an optional parameter or to a rest parameter;
-   Each argument is assignable to a corresponding parameter type, or
    to a corresponding element type of a rest parameter.

Return types of overload entities are not considered by *overload resolution*,
it means that the selected entity can lead to a `compile-time`{.interpreted-text role="index"} error,
like in the following example:

``` {.typescript}
function foo(n: number): number {}
function foo(s: string): string {}

let x: number = foo("1") // Compile-time error
```

| 

### Forming an Overload Set {#Forming an Overload Set}

Only a single *overload set* is created for each overloaded name in a scope.
An overload set combines entities that are overloaded implicitly and explicitly.
If an entity is not overloaded, then an *overload set* contains the very entity
for the entity name. The order of an *overload set* is determined as follows:

1.  If an overload set is formed from *implicit overloads* only, then
    the order of the *overload set* corresponds to the textual order of
    entity declaration;
2.  If an overload set is formed from *explicit overloads* only, then
    the order of the *overload set* is the same as the order of the entities
    listed.
3.  If an overload set is a combination of implicitly and explicitly overloaded
    entities, then:
    -   An *explicit overload* list must contain the name of an implicitly
        overloaded entity. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.
    -   The order is based on the order of the *explicit overload* list as an
        *explicit overload* has a higher priority.
        All implicitly overloaded entities are listed in the textual order of
        declaration, and are included into the *explicit overload* list at the
        position of the overloaded name.

The textual position of an *explicit overload* does not influence
the order in the *overload set*. An *explicit overload* is effectively processed
at the end of the scope.

An overload set for interface and instance class methods can contain methods
from superinterfaces and superclasses. Methods defined in an interface or in a
class are added to the *overload set* before any inherited method, i.e., more
specific entities have a higher priority. Further details are discussed in
`Overload Set for Interface Methods`{.interpreted-text role="ref"} and
`Overload Set for Class Instance Methods`{.interpreted-text role="ref"}.

| 

### Overload Set for Functions {#Overload Set for Functions}

For a given function name, the overload set is formed from
implicitly overloaded functions (see `Implicit Function Overloading`{.interpreted-text role="ref"})
and from functions listed in `Explicit Function Overload`{.interpreted-text role="ref"} (see
`Forming an Overload Set`{.interpreted-text role="ref"}).

The example below illustrates how *overload set* is formed and used
by *overload resolution*:

``` {.typescript}
function fooN(n: number) {}

function foo() {}           // implicitly overloaded foo#1
function foo(b: boolean) {} // implicitly overloaded foo#2

function fooX(x?: number) {}

overload foo {fooN, foo, fooX}
// The overload set for 'foo' is {fooN, foo#1, foo#2, fooX}

overload bar {fooX, foo}
// The overload set for 'bar' is {fooX, foo#1, foo#2}

foo(1) // fooN is called
bar(1) // fooX is called

foo()  // foo#1 is called
bar()  // fooX is called

foo(true) // foo#2 is called
bar(true) // foo#2 is called
```

| 

### Overload Set for Interface Methods {#Overload Set for Interface Methods}

An overload set for a given interface is formed from the following:

-   Implicitly overloaded methods (see `Implicit Method Overloading`{.interpreted-text role="ref"});
-   Explicitly overloaded methods listed in
    `Explicit Interface Method Overload`{.interpreted-text role="ref"};
-   Overload sets from superinterfaces, if any.

The following steps are taken to form an overload set:

1.  Explicitly and implicitly overloaded methods defined
    in a given interface are added into the overload set in the order
    described in `Forming an Overload Set`{.interpreted-text role="ref"}.
2.  Overload sets from each direct superinterface are added at the end of an
    overload set in the order of the `implements` clauses. A method that is
    already added to the overload set is not added again.

::: {.note}
::: {.title}
Note
:::

Overload sets from non-direct superinterfaces are not considered as they are
already accounted for in direct superinterfaces.
:::

Forming an *overload set* for an interface that has no superinterface is
represented in the example below:

``` {.typescript}
interface I {
    foo(x: number) // #1
    foo(s: string) // #2
    // The overload set for 'foo' is {foo#1, foo#2}
}

interface J {
    foo(x: number) // #1
    foo(s: string) // #2
    fooOpt(x?: number)
    overload foo { foo, fooOpt}
    // The overload set for 'foo' is {foo#1, foo#2, fooOpt}
}
```

Overload sets for an interface with superinterfaces is represented in the
example below:

``` {.typescript}
interface I1 {
    foo(x: number)  // #1
}
interface I2 {
    foo(s: string)  // #2
    foo(b: boolean) // #3
}
interface J extends I1, I2 { // the order in extends list is used
    foo() // #4
    /* The overload set is {foo#4, foo#1, foo#2, foo#3}
       Formed as: set(J)={foo#4} append set(I1)={foo#1} append set(I2)={foo#2, foo#3}
    */
}
```

That overridden methods occur only once in a list (`I` and `I2` as defined
above) is represented in the example below:

``` {.typescript}
interface K extends I1, I2 {
    foo(s: string) // #2 as it overrides I2.foo
    /* The overload set is {foo#2, foo#1, foo#3}
       Formed as: set(K)={foo#2} append set(I1)={foo#1} append set(I2)={foo#2, foo#3}
       Second occurrence of foo#2 is skipped.
    */
}
```

Combining implicit and explicit overloads is represented in the example below:

``` {.typescript}
interface I {
    foo(s: string)  // #1
    fooOpt(x?: number)
    overload foo {fooOpt, foo}
    // The overload set is {fooOpt, foo#1}
}

interface J1 extends I {
    foo(b: boolean) // #2
    /* The overload set is {foo#2, fooOpt, foo#1}
       Formed as: {foo#2} append set(I)={fooOpt, foo#1}
    */
}

interface J2 extends I {
    foo(b: boolean) // #2
    overload foo {foo, fooOpt}
    /* The overload set is {foo#2, fooOpt, foo#1}
       Formed as: {foo#2, fooOpt} append set(A)={fooOpt, foo#1}
       Second occurrence of fooOpt is skipped.
    */
}
```

| 

### Overload Set for Class Static Methods {#Overload Set for Class Static Methods}

An overload set of static methods for a given class is formed from implicitly
overloaded methods (see `Implicit Method Overloading`{.interpreted-text role="ref"}), and from the
methods listed in `Explicit Class Method Overload`{.interpreted-text role="ref"}.

The algorithm that defines the order of an *overload set* considers only the
static methods defined directly in a class scope (see
`Forming an Overload Set`{.interpreted-text role="ref"}) because static methods are not inherited.

The formation and the use of an *overload set* by the *overload resolution* is
represented in the example below:

``` {.typescript}
class C {

    static foo() {}           // implicitly overloaded foo#1
    static foo(b: boolean) {} // implicitly overloaded foo#2
    static fooX(x?: number) {}

    static overload foo {foo, fooX}
    // The overload set for 'foo' is {foo#1, foo#2, fooX}
}

C.foo(1)    // fooX is called
C.foo()     // foo#1 is called
C.foo(true) // foo#2 is called
```

| 

### Overload Set for Class Instance Methods {#Overload Set for Class Instance Methods}

An overload set for class instance methods of a given class is formed from
the following:

-   Implicitly overloaded methods (see `Implicit Method Overloading`{.interpreted-text role="ref"});
-   Explicitly overloaded methods listed in `Explicit Class Method Overload`{.interpreted-text role="ref"};
-   Methods from a direct superclass, if any.

The following steps are taken to form an overload set:

1.  Explicitly and implicitly overloaded methods defined
    in a given class are added into an overload set in the order
    described in `Forming an Overload Set`{.interpreted-text role="ref"}, including the
    methods that override or implement methods from supertypes.
2.  Overload set from a direct superclass (if any) is added at the end of an
    overload set. A method that is already added to the overload set is not
    added again.
3.  Overload sets from each superinterface are added at the end of an overload
    set in the order of the `implements` clauses. A method that is already
    added to the overload set is not added again.

::: {.note}
::: {.title}
Note
:::

Overload sets from non-direct supertypes are not considered.
:::

Forming an *overload set* for a class that has neither a superclass nor a
superinterface is represented in the example below:

``` {.typescript}
class C {
    foo(x: number) {} // #1
    foo(s: string) {} // #2
    // The overload set for 'foo' is {foo#1, foo#2}
}

class D {
    foo(x: number) {} // #1
    foo(s: string) {} // #2
    fooOpt(x?: number) {}
    overload foo { foo, fooOpt}
    // The overload set for 'foo' is {foo#1, foo#2, fooOpt}
}
```

An overload set for a class with a superclass and a superinterface is represented
in the example below:

``` {.typescript}
interface I {
    foo(x: number)  // #1
}

class C {
    foo(s: string) {} // #2
}

class D extends C implements I{
    foo(x: number) {}  // overrides #1
    foo(x: boolean) {} // #3
    /* The overload set is {foo#1, foo#3, foo#2}
       Formed as: set(D)={foo#1, foo#3} append set(C)={foo#2} append set(I)={foo#1}
       Second occurrence of foo#1 is skipped.
    */
}
```

Only direct supertypes are considered for overload sets. It is represented in
the example below:

``` {.typescript}
interface I{
    foo(x: number) {} // #1
}
class C implement I{
    foo(x: A)      // #2
    // Note: foo in I has default body, no need to implement it in C
    // The overload set is {foo#2, foo#1}
}
class D extends C {
    foo(s: string) {}   // #3
    foo(x: A | undefined) {} // overrides #2
    /* The overload set is {foo#3, foo#2, foo#1}
       Formed as: set(D)={foo#3, foo#2} append set(C)={foo#2, foo#1}
       Second occurrence of foo#2 from set(C) is skipped.
    */
}
class E extends D {
    foo(x: number) {} // overrides #1
    /* The overload set is {foo#1, foo#3, foo#2}
       Formed as: set(E)={foo#1} append set(D)={foo#3, foo#2, foo#1}
       Second occurrence of foo#1 from set(D) is skipped.
    */
}
```

More details are provided in `Overloading and Overriding`{.interpreted-text role="ref"}.

| 

### Overload Set for Constructors {#Overload Set for Constructors}

For a given class, the overload set for constructors is formed from
implicitly overloaded constructors
(see `Implicit Constructor Overloading`{.interpreted-text role="ref"}).
The order of constructors in the overload set is textual order
of constructor declarations.

The example below illustrates how *overload set* is formed by
*overload resolution*:

``` {.typescript}
class C {
    constructor () {}       // ctor#1
    constructor (s: string) {} // ctor#2
}
/* The overload set of constructors for class 'C' is
   {ctor#1, ctor#2} */

new C()     // ctor#1 is used
new C("aa") // ctor#2 is used
```

| 

### Overload Set Warning {#Overload Set Warning}

A `compile-time warning`{.interpreted-text role="index"} is issued if the order of entities in an
overload set implies that some overloaded entity can never be
selected for a call:

``` {.typescript}
function f1 (p: number) {}
function f2 (p: number|string) {}
function f3 (p: string) {}
overload foo {f1, f2, f3}  // warning: f3 will never be called as foo()

foo (5)                    // f1() is called
foo ("5")                  // f2() is called
```

::: {.index}
overload set
call
:::

| 

### Overload Set at Method Call {#Overload Set at Method Call}

Additional processing of an *overload set* is used at
`Method Call Expression`{.interpreted-text role="ref"} because an identifier at the call site can denote
both *instance methods* and `Functions with Receiver`{.interpreted-text role="ref"}.

If the identifier at the call expression denotes *functions with receiver*
only, then `Overload Set for Functions`{.interpreted-text role="ref"} is used. However, only *functions
with receiver* (not ordinary functions) are considered for *overload resolution*:

``` {.typescript}
class C {}

function foo(this: C) {}            // #1
function foo(this: C, s: string) {} // #2
function foo(c: C, n: number) {}    // #3

let c = new C()
c.foo() // only function #1, #2, but not #3 are considered here

foo(c) // all three functions are considered here
```

If the identifier denotes both instance methods and *functions with receiver*,
then the overload set for methods is used for *overload resolution*, i.e.,
no function with receiver is called. Otherwise, a
`compile-time warning`{.interpreted-text role="index"} is issued as represented in the example below:

``` {.typescript}
// File1
export class C {
    bar() {}
}
export function foo(this: C) {}

// File2
import {C, foo as bar} from "File1"

new C().bar() // C.bar is called, warning is issued
```

::: {.note}
::: {.title}
Note
:::

If a function with receiver is declared, and the name of the function is the
same as the name of an accessible instance method or field of the receiver
type, then a `compile-time error`{.interpreted-text role="index"} occurs in most cases (see the
example in `Functions with Receiver`{.interpreted-text role="ref"}). A warning is issued where no such
error is reported.
:::

| 

### Overloading and Overriding {#Overloading and Overriding}

When calling an overloaded method (class instance method or interface method),
both `Overloading`{.interpreted-text role="ref"} and `Overriding`{.interpreted-text role="ref"} influence the actual method
to call. As *compile-time* polymorphism, *overload resolution* selects the
method to call from a class type or an interface type known at compile time.
However, the method can be overridden in subtypes, and the actual method is
called in accordance with the *runtime type* of the object from which the method
is called.

::: {.note}
::: {.title}
Note
:::

Overriding does not influence forming of overload sets by itself despite
any method declared in a class\-\--both new or overridden\-\--is placed in the
overload set before any inherited method.
:::

The manner *overloading* and *overriding* influence the method to call is
represented in the example below:

``` {.typescript}
class C1 {}
class C2 extends C1 {}

class A {
    foo(c: C2) { console.log("A.C2") }
    foo(c: C1) { console.log("A.C1") }
}

class B extends A {
    override foo(c: C2) { console.log("B.C2") }
}

let a: A = new B()
a.foo(new C2()) // 1st call output: B.C2
a.foo(new C1()) // 2nd call output: A.C1
```

The details of the first call are as follows:

-   Static type of `a` is `A`, and only this type is considered for
    overload resolution;
-   First overloaded `foo` can be called, and is selected;
-   Runtime type of `a` is `B`, `foo(c: C2)` is overridden in `B`, and
    then the method from `B` is called.

The details of the second call are as follows:

-   `foo(c: C1)` is selected to call;
-   `foo(c: C1)` is not overridden, and the original method from `A` is called.

The situation where a single method in a subclass overrides several methods of
a superclass is represented in the example below:

``` {.typescript}
class C1 {}
class C2 extends C1 {}

class A {
    foo(c: C2) { console.log("A.C2") }
    foo(c: C1) { console.log("A.C1") }
}

class D extends A {
    foo(c: C1) { console.log("D.C1") }
}

let a: A = new D()
a.foo(new C2()) // 1st call output: D.C1
a.foo(new C1()) // 2nd call output: D.C1
```

In the example above, `foo` in `D` overrides both `A` methods (see
`Override-Compatible Signatures`{.interpreted-text role="ref"}). As a result, the same method is called
despite different methods are selected at compile time for the first and the
second calls.

| 

### Dynamic resolution of method calls {#Dynamic resolution of method calls}

The actual method to be invoked during the `Method Call Expression`{.interpreted-text role="ref"} evaluation is
determined in the runtime with respect to the method statically resolved
during the compile time (see `Overload Set at Method Call`{.interpreted-text role="ref"}) and the actual
*type* of the `objectReference`.

The resolution depends on the form of the call expression:

-   For *static method calls*, overriding is not used and the statically
    determined method is the one to be invoked
-   For *super calls*, overriding is not used and the statically resolved
    method of superclass is the one to be invoked
-   For *instance method calls*, the actual type of the `objectReference`
    referred to as *T* is used to determine the method to be invoked.

For the statically resolved method *M* defined in the type *D*, let the type *C* be

-   *D* if the method *M* is found in the type *D* during the execution.
-   The *closest* superclass of *C* that defines the method of the signature of *M*.
-   The *closest* superinterface of *C* that defines the method of the signature of *M*.

Note: For the set of programs compiled without source code updates *C* is always *D*

Type *T* (which is always a class) and the statically
determined method *M* defined in the type *C* (where *T* is necessarily a subtype of
*C*) are used to perform the resolution, which is defined as follows:

-   If *T* is *C*, the result of the resolution is *M*.

-   If *T* has a superclass and the resolution of the method *M*
    for the superclass of *T* succeeds and the resolved method is defined in
    class, let *Ms* be the result of the resolution:

    -   If the type *T* defines several method declarations that override the method *Ms*
        in *T*:
        -   If the set of such methods contains exactly one method, this method is the
            result of the resolution.
        -   Otherwise, the method resolution fails for type *T*.
    -   Otherwise, *Ms* is the result of the resolution.

-   Otherwise, the set of the *superinterfaces* of *T* is searched for a matching method:

    -   Each considered method should be declared in the superinterface of *T*
        and should override the method *M* in *C*.
    -   For each considered method *Mi*, there should be no other method *Mio*
        satisfying the previous criterion that overrides *Mi* in the interface
        that defines *Mio*.

    Note: That means, all considered method belong to subinterfaces of
    the declaring interface of *M*.

    If the set contains exactly one default method, this method is the result of
    the resolution. Otherwise, the set either

    -   has multiple default methods
    -   has no default methods

    In these cases, the resolution fails for type *T*.

If the method resolution fails, then a `runtime error`{.interpreted-text role="index"} occurs.

Note: For the set of programs compiled without source code updates
the resolution always results in method resolved and does never throw.

| 

## Type Erasure {#Type Erasure}

*Type erasure* is the concept that refers to a special handling of some language
*types*, primarily `Generics`{.interpreted-text role="ref"}, as members of a smaller subset of the language
*type system* when considering certain parts of the language semantics.
The subset defined via type mapping is referred to as *effective type*.
*Effective type* mapping satisfies the following properties:

-   For arbitrary types `A` and `B`, if `A` is a subtype of `B`, then an
    `EffectiveType(A)` is a subtype of `EffectiveType(B)`
-   For arbitrary types `A` and `B`, `EffectiveType(A | B)` is identical to
    `EffectiveType(A) | EffectiveType(B)`
-   For an arbitrary type `A`, `A | undefined` is a subtype of `EffectiveType(A | undefined)`
    -   In particular, for an arbitrary type `A`, `undefined` is a subtype of `EffectiveType(A)`

An original type and an *effective type* can have relationships of two kinds:

-   If *Effective type* of `T` is identical to `T`, then type `T` is *preserved by type erasure*;
-   Otherwise, the type is considered as *affected by type erasure*.

If `T | undefined` is *preserved by type erasure*, then type `T` is *preserved
up to undefined*.

This property limits the possible applications of type-checking expressions:

-   `instanceof Expression`{.interpreted-text role="ref"};
-   `Cast Expression`{.interpreted-text role="ref"}.

::: {.index}
type erasure
instanceof expression
cast expression
execution
operation
type
generic
semantics
effective type
type mapping
supertype
:::

Type mapping determines *effective types* as follows (the `undefined` union
member is excluded in the right-hand-side column for brevity):

+-------------------------------+--------------------------------------+
| **Original Type**             | **Effective Type (undefined member   |
|                               | excluded)**                          |
+===============================+======================================+
| `Any`                         | `Any`                                |
+-------------------------------+--------------------------------------+
| `never`                       | `never`                              |
+-------------------------------+--------------------------------------+
| `undefined`                   | `undefined`                          |
+-------------------------------+--------------------------------------+
| `null`                        | `null`                               |
+-------------------------------+--------------------------------------+
| *Generic types* (see          | Instantiation of the same generic    |
| `Generics`{.interpreted-text  | type                                 |
| role="ref"})                  | (see                                 |
|                               | `Explicit Gener                      |
|                               | ic Instantiations`{.interpreted-text |
|                               | role="ref"}) with type arguments     |
|                               | selected                             |
|                               | in accordance with                   |
|                               | `Type P                              |
|                               | arameter Variance`{.interpreted-text |
|                               | role="ref"}:                         |
|                               |                                      |
|                               | -   *Covariant* type parameters are  |
|                               |     instantiated with the constraint |
|                               |     type;                            |
|                               | -   *Contravariant* type parameters  |
|                               |     are instantiated with type       |
|                               |     `never`;                         |
+-------------------------------+--------------------------------------+
| `Type                         | `Type Par                            |
| Parameters`{.interpreted-text | ameter Constraint`{.interpreted-text |
| role="ref"}                   | role="ref"}                          |
+-------------------------------+--------------------------------------+
| `U                            | Union of effective types of each     |
| nion Types`{.interpreted-text | constituent type of `T1 ... Tn`.     |
| role="ref"} in the form       |                                      |
| `T1 | T2 ... Tn`              |                                      |
+-------------------------------+--------------------------------------+
| `A                            | Same as for a generic type           |
| rray Types`{.interpreted-text | `Array<T>`.                          |
| role="ref"} in the form `T[]` |                                      |
+-------------------------------+--------------------------------------+
| `Fixed-Size A                 | Instantiations of `FixedArray<T>`    |
| rray Types`{.interpreted-text | (i.e., the effective type of type    |
| role="ref"} (`FixedArray<T>`) | argument `T` is preserved).          |
+-------------------------------+--------------------------------------+
| `Func                         | Instantiation of an internal generic |
| tion Types`{.interpreted-text | *function* type with respect to the  |
| role="ref"} in the form       | number of parameter types *n*.       |
| `(P1, P2, Pn) => R`           | Parameter                            |
|                               | types `P1, P2 ... Pn` are            |
|                               | instantiated with `Any`. Return type |
|                               | `R`                                  |
|                               | is instantiated with type `never`.   |
+-------------------------------+--------------------------------------+
| `Func                         | Instantiation of an internal generic |
| tion Types`{.interpreted-text | *rest-parametrized function* type    |
| role="ref"} in the form       | with respect to the number of        |
| `(P1, P2, Pn, ...PR) => R`    | parameter types *n*.                 |
|                               | Internal generic *rest-parametrized  |
|                               | function* of *n* parameters is a     |
|                               | supertype                            |
|                               | of the internal generic *function*   |
|                               | type of *n* parameters. Parameter    |
|                               | types `P1, P2 ... Pn` and rest       |
|                               | parameter type `PR` are instantiated |
|                               | with `Any`. Return type `R` is       |
|                               | instantiated with type `never`.      |
+-------------------------------+--------------------------------------+
| `T                            | Instantiation of an internal generic |
| uple Types`{.interpreted-text | tuple type with respect to the       |
| role="ref"} in the form       | number of element types *n*.         |
| `[T1, T2 ..., Tn]`            |                                      |
+-------------------------------+--------------------------------------+
| `String Lit                   | `string`                             |
| eral Types`{.interpreted-text |                                      |
| role="ref"}                   |                                      |
+-------------------------------+--------------------------------------+
| Awaited\<T\>                  | -   If `T` is neither a type         |
|                               |     parameter nor a subtype of       |
|                               |     `Promise`, then                  |
|                               |     the Effective type               |
|                               |     (Awaited\<T\>) is the Effective  |
|                               |     type (T);                        |
|                               | -   If `T` is a `Promise<U>`, then   |
|                               |     the Effective type               |
|                               |     (Awaited\<T\>)                   |
|                               |     is the Effective type (U);       |
|                               | -   If `T` is a type parameter with  |
|                               |     `in` variance, then the          |
|                               |     Effective                        |
|                               |     type (Awaited\<T\>) is `never`;  |
|                               | -   If `T` is a type parameter with  |
|                               |     `out` variance or no variance    |
|                               |     specified, then the Effective    |
|                               |     type (Awaited\<T\>) is the       |
|                               |     Effective type                   |
|                               |     (upper-bound(T)).                |
+-------------------------------+--------------------------------------+
| NonNullable\<T\>              | Effective type (T) - `null`          |
+-------------------------------+--------------------------------------+
| Partial\<T\>                  | Special runtime partial class        |
+-------------------------------+--------------------------------------+
| Required\<T\>                 | `Effective type (T)`                 |
+-------------------------------+--------------------------------------+
| Readonly\<T\>                 | `Effective type (T)`                 |
+-------------------------------+--------------------------------------+
| Record\<K, V\>                | `Map <Effe                           |
|                               | ctive type (K), Effective type (V)>` |
+-------------------------------+--------------------------------------+
| ReturnType\<F\>               | `Effective type (return type of F)`  |
+-------------------------------+--------------------------------------+

Additional type mapping defines an *effective signature type*, i.e.,
an *effective type* of a corresponding type except the following:

  -----------------------------------------------------------------------
  **Original Type**               **Effective signature type**
  ------------------------------- ---------------------------------------
  Return type `never`             `never`

  -----------------------------------------------------------------------

Otherwise, the original type is *preserved*.

::: {.index}
type erasure
type mapping
generic type
type parameter
constraint
effective type
instantiation
type argument
covariant type parameter
type parameter
contravariant type parameter
type
generic tuple
tuple type
string
literal type
enumeration base type
enumeration
invariant type parameter
parameter type
type preservation
:::

A program that uses types not *preserved* by erasure, and relies
on certain cast expressions (see `Cast Expression`{.interpreted-text role="ref"}) which narrow
values to types not *preserved up to undefined*,
can cause `ClassCastError` thrown during the evaluation of
`Field Access Expression`{.interpreted-text role="ref"}, `Method Call Expression`{.interpreted-text role="ref"},
or `Function Call Expression`{.interpreted-text role="ref"}. Checks that cause any `runtime error`{.interpreted-text role="index"}
mentioned above ensure type safety of program execution:

``` {.typescript}
class A<T> {
  field: T

  constructor(value: T) {
    this.field = value
  }
}

function unsafe(p: Object): A<number> {
  return p as A<number>  // OK, but check is performed against type A<>, but not against A<number>
                         // thus it can cause exception later during execution
}

let a: A<number> = unsafe(new A<string>("a")) // A<string> resides in A<number>

let n = a.field // An exception is raised as the expected type is number but the actual type is string
```

::: {.index}
access
type erasure
field access
function call
method call
target type
cast expression
:::

| 

## Static Initialization {#Static Initialization}

*Static initialization* is a routine performed once for each class (see
`Classes`{.interpreted-text role="ref"}), namespace (see `Namespace Declarations`{.interpreted-text role="ref"}), or
module (see `Namespaces and Modules`{.interpreted-text role="ref"}).

*Static initialization* presumes executing the following:

-   *Initializers* of *variables* or *static fields*;
-   *Top-level statements* for modules and namespaces;
-   Code inside a *static block* for classes.

::: {.index}
static initialization
routine
class
namespace
namespace declaration
module
initializer
variable
static field
top-level statement
static block
:::

*Static initialization* is performed before one of the following operations is
executed for the first time:

-   Calling a class static method (see `Method Call Expression`{.interpreted-text role="ref"}),
    accessing a class static field (see `Accessing Static Fields`{.interpreted-text role="ref"}), and
    creating a new class instance (see `New Expressions`{.interpreted-text role="ref"}) or a
    *static initialization* of a direct subclass;
-   Calling a function or accessing a variable of a namespace or a module.

::: {.note}
::: {.title}
Note
:::

None of the operations above invokes a *static initialization* of the same
entity recursively if it is not completed.

The code in a static block of a namespace is executed only if namespace
members are used in a program (an example is provided in
`Namespace Declarations`{.interpreted-text role="ref"}).
:::

An initialization is not complete if the execution of a *static
initialization* is terminated due to an exception thrown. A repeated attempt to
execute the *static initialization* can throw an exception again.

If a *static initialization* invokes a concurrent execution (see
`Execution model`{.interpreted-text role="ref"}), then all that try to invoke it
are synchronized. The synchronization is to ensure that the initialization
is performed only once, and that the operations requiring the *static
initialization* to be performed are executed after the initialization completes.

If *static initialization* routines of two concurrently initialized classes are
circularly dependent, then a deadlock can occur.

::: {.index}
static initialization
entity
scope
static field
variable
access
direct subclass
subclass
class
interface
operation
exception
invocation
concurrent execution
synchronization
deadlock
:::

| 

### Static Initialization Safety {#Static Initialization Safety}

A compile-time error occurs if a *named reference* refers to a not yet
initialized *entity*, including one of the following:

-   Variable (see `Variable and Constant Declarations`{.interpreted-text role="ref"}) of a module or
    namespace (see `Namespace Declarations`{.interpreted-text role="ref"});
-   Static field of a class (see `Static and Instance Fields`{.interpreted-text role="ref"}).

If detecting an access to a not yet initialized *entity* is not possible, then
runtime evaluation is performed as follows:

-   Default value is produced if the type of an entity has a default value;
-   Otherwise, `NullPointerError` is thrown.

::: {.index}
static initialization
safety
named reference
initialization
entity
variable
module
namespace
static field
class
access
runtime evaluation
default value
value
type
:::

| 

## Compatibility Features {#Compatibility Features}

Some features are added to in order to support smooth compatibility.
Using these features while doing the programming is not recommended in
most cases.

::: {.index}
compatibility
:::

| 

### Extended Conditional Expressions {#Extended Conditional Expressions}

provides extended semantics for conditional expressions
to ensure better alignment. It affects the semantics of the following:

-   `Ternary Conditional Expressions`{.interpreted-text role="ref"};
-   `Conditional-And Expression`{.interpreted-text role="ref"};
-   `Conditional-Or Expression`{.interpreted-text role="ref"};
-   `Logical Complement`{.interpreted-text role="ref"};
-   `While Statements and Do Statements`{.interpreted-text role="ref"};
-   `For Statements`{.interpreted-text role="ref"};
-   `if Statements`{.interpreted-text role="ref"}.

::: {.note}
::: {.title}
Note
:::

The extended semantics is to be deprecated in one of the future versions of
.
:::

The extended semantics approach is based on the concept of *truthiness* that
extends the boolean logic to operands of non-boolean types.

Depending on the kind of a valid expression\'s type, the value of the valid
expression can be handled as `true` or `false` as described in the table
below:

::: {.index}
extended conditional expression
ternary conditional expression
expression
alignment
semantics
conditional-and expression
conditional-or expression
logical complement
while statement
do statement
for statement
if statement
truthiness
non-boolean type
expression type
extended semantics
boolean logic
boolean type
non-boolean type
:::

+-----------------+-----------------+-----------------+-----------------+
| Value Type Kind | When `false`    | When `true`     | Code Example to |
|                 |                 |                 | Check           |
+=================+=================+=================+=================+
| `string`        | empty string    | non-empty       | `s.length == 0` |
|                 |                 | string          |                 |
+-----------------+-----------------+-----------------+-----------------+
| `boolean`       | `false`         | `true`          | `x`             |
+-----------------+-----------------+-----------------+-----------------+
| `char`          | `c'\u0000'`     | `any value ex   | `x`             |
|                 |                 | cept c'\u0000'` |                 |
+-----------------+-----------------+-----------------+-----------------+
| `enum`          | `enum` constant | `enum` constant | `x.valueOf()`   |
|                 | handled as      | handled as      |                 |
|                 | `false`         | `true`          |                 |
+-----------------+-----------------+-----------------+-----------------+
| `number`        | `0` or `NaN`    | any other       | `n !=           |
| (`d             |                 | number          | 0 && !isNaN(n)` |
| ouble`/`float`) |                 |                 |                 |
+-----------------+-----------------+-----------------+-----------------+
| any integer     | `== 0`          | `!= 0`          | `i != 0`        |
| type            |                 |                 |                 |
+-----------------+-----------------+-----------------+-----------------+
| `bigint`        | `== 0n`         | `!= 0n`         | `i != 0n`       |
+-----------------+-----------------+-----------------+-----------------+
| `null` or       | `always`        | `never`         | `x != null` or  |
| `undefined`     |                 |                 |                 |
|                 |                 |                 | `               |
|                 |                 |                 | x != undefined` |
+-----------------+-----------------+-----------------+-----------------+
| Union types     | When value is   | When value is   | `x != null` or  |
|                 | `false`         | `true`          |                 |
|                 | according to    | according to    | `               |
|                 | this column     | this column     | x != undefined` |
|                 |                 |                 | for union types |
|                 |                 |                 | with nullish    |
|                 |                 |                 | types           |
+-----------------+-----------------+-----------------+-----------------+
| Any other       | `never`         | `always`        | `new So         |
| nonNullish type |                 |                 | meType != null` |
+-----------------+-----------------+-----------------+-----------------+

::: {.index}
value type
integer type
union type
nullish type
empty string
non-empty string
string
number
nonzero
:::

Extended semantics of `Conditional-And Expression`{.interpreted-text role="ref"} and
`Conditional-Or Expression`{.interpreted-text role="ref"} affects the resultant type of expressions
as follows:

-   For *conditional-and* expression `A && B`:
    -   If the value of `A` is known at compile time, then the type of an
        expression is the type of `B` when `A` is handled as `true`, and the
        type of `A` otherwise.
    -   If the value of `A` is unknown at compile time, then the type of an
        expression is union `A | B`.
-   For *conditional-or* expression `A || B`:
    -   If the value of `A` is known at compile time, then the type of an
        expression is the type of `B` when `A` is handled as `false`, and the
        type of `A` otherwise.
    -   If the value of `A` is unknown at compile time, then the type of an
        expression is union `A | B`.

The way this approach works in practice is represented in the example below.
Any `nonzero` number is handled as `true`. The loop continues until it
becomes `zero` that is handled as `false`:

``` {.typescript}
console.log(typeof (false || 1) )
console.log(typeof (true || 1) )
for (let i = 10; i; i--) {
   console.log (i)
}
/* And the output will be
     int
     boolean
     10
     9
     8
     7
     6
     5
     4
     3
     2
     1
 */
```

::: {.index}
NaN
nullish expression
numeric expression
semantics
conditional-and expression
conditional-or expression
loop
:::

```{=pdf}
PageBreak
```
