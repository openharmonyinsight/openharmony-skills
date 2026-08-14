# Experimental Features {#Experimental Features}

This Chapter introduces the features that are considered parts of
the language, but have no counterpart in , and are therefore not
recommended to those who seek a single source code for and .

Some features introduced in this Chapter are still under discussion. They can
be removed from the final version of the specification. Once a feature
introduced in this Chapter is approved and/or implemented, the corresponding
section is moved to the body of the specification as appropriate.

The *array creation* feature introduced in
`Resizable Array Creation Expressions`{.interpreted-text role="ref"} enables programmers to create
objects of the array type at runtime by providing the following as arguments:

-   Array size;
-   One element to fill the array with, or a lambda to generate a set of elements
    to fill the array with.

This addition is useful to other array-related features of the language, such
as array literals. This feature can also be used to create arrays of arrays.

Overloading functions, methods, or constructors is a practical and convenient
way to write program actions that are similar in logic but different in
implementation. uses `Explicit Overload Declarations`{.interpreted-text role="ref"} as an innovative
form of *managed overloading*.

::: {.index}
implementation
array creation
runtime expression
array
array literal
constructor
function
method
array type
runtime
array size
function overloading
method overloading
implementation
constructor overloading
overload declaration
:::

Section `Native Functions and Methods`{.interpreted-text role="ref"} introduces practically important
and useful mechanisms for the inclusion of components written in other languages
into a program written in .

Sections `Final Classes`{.interpreted-text role="ref"} and `Final Methods`{.interpreted-text role="ref"}
discuss the well-known feature that
in many OOP languages provides a way to restrict class inheritance and method
overriding. Making a class *final* prohibits defining classes derived from it,
whereas making a method *final* prevents it from overriding in derived classes.

Section `Adding Functionality to Existing Types`{.interpreted-text role="ref"} discusses the way to
add new functionality to an already defined type.

::: {.index}
native function
native method
function overloading
method overloading
final class
final method
object-oriented programming (OOP)
OOP (object-oriented programming)
inheritance
:::

| 

## Type `char` {#Type char}

Values of `char` type are 16-bit Unicode code units.
Any Unicode code point can be encoded with one or two `char` values.

  ---------------------------------------------------------------------------
  Type               Type\'s Set of Values
  ------------------ --------------------------------------------------------
  `char` (16-bits)   Symbols (code units) with codes from U+0000 to U+FFFF

  ---------------------------------------------------------------------------

Predefined constructors, methods, and constants for `char` type are
parts of the `Standard Library`{.interpreted-text role="ref"}.

Type `char` is a class type that is a part of the
`Standard Library`{.interpreted-text role="ref"}. It means that type `char` is a subtype of
`Object`, and that it can be used at any place where a class name is
expected.

``` {.typescript}
let a_char: char = c'a'
console.log (a_char)
// Output is: a
let o: Object = a_char // OK
```

::: {.index}
char type
Unicode code point
set of values
predefined constructor
predefined method
predefined constant
char type
:::

| 

### `char` Literals {#char Literals}

*Char literal* represents a 16-bit Unicode code unit that can be written as
a single UTF-16 symbol or a single escape sequence preceded by the characters
*single quote* (U+0027) and \'*c*\' (U+0063), and followed by a *single quote*.

The syntax of *character literal* is represented below:

``` {.abnf}
CharLiteral:
    'c\'' SingleQuoteCharacter '\''
    ;

SingleQuoteCharacter:
    ~['\\\r\n]
    | '\\' EscapeSequence
    ;
```

The examples are presented below:

``` {.typescript}
c'a'
c'\n'
c'\x7F'
c'\u0000'
```

If a literal cannot be represented by an unsigned 16-bit value, then a
`compile-time`{.interpreted-text role="index"} occurs:

``` {.typescript}
c'\u{FFFFF}' // Compile-time error
```

*Char literals* are of type `char`.

::: {.index}
char literal
value
character
syntax
escape sequence
single quote
type char
value
:::

| 

### `char` Operations {#char Operations}

Equality operators (see `Equality Expressions`{.interpreted-text role="ref"}) and relational operators
`Relational Expressions`{.interpreted-text role="ref"}) can be used if:

-   both operands are of `char` type; or
-   one operand is of `char` type and other is of a numeric type
    (see `char Conversions for Relational and Equality Operands`{.interpreted-text role="ref"});
-   otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

In first case, the operation is performed as an integer comparison of two unsigned 16-bit values.
In the second case, the operation is performed as an integer comparison of the correspondent
numeric type.

``` {.typescript}
let c: char = c'A'
let c1 = new char
c1 = c'A'

// The following lines both print true as values are equal
console.log(c == c1)  // true
console.log(c === c1) // true

console.log(c == 0x41) // true

c1 = c'B'
console.log(c < c1)  // true
console.log(c < 0x41)  // false

console.log(c > 3.14)  // true
```

| 

## Fixed-Size Array Types {#Fixed-Size Array Types}

*Fixed-size array type*, written as `FixedArray<T>`, is the built-in type
characterized by the following:

-   Any instance of array type contains elements. The number of elements is known
    as *array length*, and can be accessed by using the property `length`.
-   Array length is a non-negative integer number.
-   Array length is set once at runtime and cannot be changed later.
-   Array element is accessed by its index. *Index* is an integer number
    starting from *0* to *array length minus 1*.
-   Accessing an element by its index is a constant-time operation.
-   If passed to a non- environment, an array is represented as a contiguous
    memory location.
-   Type of each array element is assignable to the element\'s type specified
    in the array declaration (see `Assignability`{.interpreted-text role="ref"}).

*Fixed-size arrays* differ from *resizable arrays* as follows:

-   Fixed-size array length is set once to achieve better performance;
-   Fixed-size arrays preserve the element type during the `Type Erasure`{.interpreted-text role="ref"};
-   Fixed-size arrays have no methods defined;
-   Fixed-size arrays have several constructors (see
    `Fixed-Size Array Creation`{.interpreted-text role="ref"});
-   Fixed-size arrays are not compatible with *resizable arrays*.

Incompatibility between a resizable array and a fixed-size array is represented
by the example below:

``` {.typescript}
function foo(a: FixedArray<number>, b: Array<number>) {
    a = b // Compile-time error
    b = a // Compile-time error
}
```

::: {.index}
resizable array
fixed-size array
fixed-size array type
built-in type
instance
array type
length property
array length
index
runtime
access
index
integer number
constant-time operation
memory location
assign
assignability
array declaration
compatibility
incompatibility
:::

| 

### Fixed-Size Array Creation {#Fixed-Size Array Creation}

*Fixed-size array* can be created by using `Array Literal`{.interpreted-text role="ref"} or
constructors defined for type `FixedArray<T>`, where `T` must be a
type *preserved* by `Type Erasure`{.interpreted-text role="ref"}.

The use of an *array literal* to create an array is represented in following
examples:

``` {.typescript}
let a : FixedArray<number> = [1, 2, 3]
  /* create array with 3 elements of type number */
a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
let y = a[2] /* get the last element of array 'a' */
let count = a.length // get the number of array elements
y = a[3] // Will cause a runtime error - attempt to access non-existing array element
```

``` {.typescript}
function foo<T>(v: T): FixedArray<T | number> {
  return [v] // Compile-time error, T | number is not preserved by type erasure
}
let arr: FixedArray<string | number> = foo("a")
```

::: {.index}
fixed-size array type
array length
array literal
constructor
fixed-size array
integer
array element
access
assignability
resizable array
runtime error
:::

The following constructor creates an instance of `FixedArray<T>`
of the specified length, filled with a single value `elem`:

-   `constructor(len: int, elem: T)`

``` {.typescript}
let a = new FixedArray<string>(3, "a") // creates array ["a", "a", "a"]
```

::: {.index}
constructor
array instance
:::

| 

## Value Array Types {#Value Array Types}

*Value array type* is the built-in type written as
`ValueArray<T>` and characterized by the following:

-   Any instance of array type contains elements of type `T`. `T` must be
    a *value type* (see `Value Types`{.interpreted-text role="ref"}).
-   The number of elements is known as *array length*, and can be accessed
    by using the property `length`.
-   Array length is a non-negative integer number.
-   Array length is set once at runtime and cannot be changed later.
-   Array element is accessed by its index. *Index* is an integer number
    starting from *0* to *array length minus 1*.
-   Accessing an element by its index is a constant-time operation.
-   If passed to a non- environment, an array is represented as a contiguous
    memory location, filled by the primitive values (not references).
-   Type of each array element is equal to the element\'s type specified
    in the array declaration.
-   No subtyping relation holds between two `ValueArray` types, except where
    their type arguments are identical.

::: {.note}
::: {.title}
Note
:::

-   `ValueArray<T>` is not a generic type, despite using
    notation identical to generics.
-   Limitations imposed by `ValueArray` subtyping make it more performant
    compared to `Fixed-Size Array Types`{.interpreted-text role="ref"}.
:::

::: {.index}
value array type
built-in type
length property
array length
index
runtime
access
index
integer number
constant-time operation
:::

*Value array* can be created by using `Array Literal`{.interpreted-text role="ref"} or
constructors defined for type `ValueArray<T>` (see below).

The use of an *array literal* to create an array is represented in following
examples:

``` {.typescript}
let a : ValueArray<int> = [1, 2, 3]
  /* create array with 3 elements of type int */
a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
let y = a[2] /* get the last element of array 'a' */
let count = a.length // get the number of array elements
y = a[3] // runtime error, attempt to access non-existing array element
```

If `ValueArray` is used with non-value type argument,
then a `compile-time error`{.interpreted-text role="index"} occurs as follows:

``` {.typescript}
let x: ValueArray<string> = ["aa"]   // Compile-time error
type A = ValueArray<int | undefined> // Compile-time error
```

The following constructor creates an instance of `ValueArray<T>`
of the specified length, filled with a single value `elem`:

-   `constructor(len: int, elem: T)`

``` {.typescript}
let a = new ValueArray<double>(3, 7.) // creates array [7., 7., 7.]
```

::: {.index}
constructor
array instance
:::

| 

## Resizable Array Creation Expressions {#Resizable Array Creation Expressions}

*Array creation expression* creates new objects that are instances of *resizable
arrays* (see `Resizable Array Types`{.interpreted-text role="ref"}). An array instance can be created
alternatively by using `Array literal`{.interpreted-text role="ref"}.

The syntax of *array creation expression* is presented below:

``` {.abnf}
newArrayInstance:
    'new' arrayElementType dimensionExpression '(' arrayElement ')'
    ;

arrayElementType:
    typeReference
    | '(' type ')'
    ;

dimensionExpression:
    '[' expression ']'
    ;

arrayElement: 
  expression
;
```

``` {.typescript}
let x = new number[3] (7) // create array instance: [7, 7, 7]
```

::: {.index}
resizable array
array creation expression
object
instance
array
array instance
array literal
syntax
expression
:::

*Array creation expression* creates an object that is a new array with the
elements of the type specified by `arrayElementType`.

The type of the *dimension expression* must be assignable (see
`Assignability`{.interpreted-text role="ref"}) to an `int` type. Otherwise,
a `compile-time error`{.interpreted-text role="index"} occurs.

A `compile-time error`{.interpreted-text role="index"} occurs if the *dimension expression* is a
constant expression that is evaluated to a negative integer value at compile
time.

::: {.index}
array creation expression
array
type
dimension expression
assignment
conversion
integer
integer type
negative integer value
int type
assignability
type
integer value
type int
constant expression
compile time
:::

Type of `arrayElement` `expression` must be be assignable (see
`Assignability`{.interpreted-text role="ref"}) to `arrayElementType`.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
dimension expression
floating-point type
compile-time error
runtime error
expression
array element
array dimension
:::

``` {.typescript}
let x = new number[-3] (0) // Compile-time error

let y = new number[3.14] (0) // Compile-time error

function foo (length: int) {
   let y = new number[length] (0)  // runtime error
}
foo (-3)
```

::: {.index}
class
accessibility
access
parameterless constructor
constructor
parameter
optional parameter
default value
:::

A `compile-time error`{.interpreted-text role="index"} occurs if `arrayElementType` is a type
parameter:

``` {.typescript}
class A<T> {
   foo(element: T) {
      new T[2] (element) // Compile-time error, 'T' is a type parameter
   }
}
```

::: {.index}
compile-time error
constructor
type parameter
array
:::

The creation of an array with a known number of elements is presented below:

``` {.typescript}
class A {
  constructor (x: number) {}
}

let array_size = 5

let array = new A[array_size] (new A(1))
   /* Create array of 'array_size' elements and all of them will have
      initial value equal to an object created by new A expression */
```

The creation of exotic arrays with different kinds of element types is presented
below:

::: {.index}
array
array creation
parameterless constructor
default value
type
lambda function
index
:::

``` {.typescript}
let array_of_union = new (Object|undefined) [5] (undefined) // filled with undefined

type Functor = () => void
let array_of_functor = new Functor[5] ( (): void => {}) // filled with lambda    

type Arr = number []
let array_of_array = new Arr [5] ( [3.14] ) // filled with array literal
```

| 

### Runtime Evaluation of Array Creation Expressions {#Runtime Evaluation of Array Creation Expressions}

The evaluation of an array creation expression at runtime is performed
as follows:

1.  The dimension expression is evaluated. If the dimension expression
    evaluation completes abruptly, then *array creation expression* also does
    so.
2.  The value of dimension expression is checked. If its value is less than
    zero, then `NegativeArraySizeError` is thrown.
3.  Space for the new array is allocated. If the available space is not
    sufficient to allocate the array, then `OutOfMemoryError` is thrown,
    and the evaluation of the array creation expression completes abruptly.
4.  Then, a one-dimensional array is created. Each element of this array is
    initialized either with the value passed or by calls to the lambda
    generating a set of values.

::: {.index}
runtime evaluation
array
array creation
array creation expression
evaluation
dimension expression
constructor
abrupt completion
expression
space allocation
class type
runtime
runtime evaluation
evaluation
initialization
:::

| 

## Indexable Types {#Indexable Types}

If a class or an interface declares one or two functions with names `$_get`
and `$_set`, and signatures *(index: Type1): Type2* and *(index: Type1,
value: Type2)* respectively, then an indexing expression (see
`Indexing Expressions`{.interpreted-text role="ref"}) can be applied to variables of such types:

``` {.typescript}
class SomeClass {
   $_get (index: number): SomeClass { return this }
   $_set (index: number, value: SomeClass) { }
}
let x = new SomeClass
x = x[1] // This notation implies a call: x = x.$_get (1)
x[1] = x // This notation implies a call: x.$_set (1, x)
```

If only one function is present, then only the appropriate form of indexing
expression (see `Indexing Expressions`{.interpreted-text role="ref"}) is available:

::: {.index}
indexable type
interface
class
declaration
function name
function
signature
indexing expression
variable
type
:::

``` {.typescript}
class ClassWithGet {
   $_get (index: number): ClassWithGet { return this }
}
let getClass = new ClassWithGet
getClass = getClass[0]
getClass[0] = getClass // Error - no $_set function available

class ClassWithSet {
   $_set (index: number, value: ClassWithSet) { }
}
let setClass = new ClassWithSet
setClass = setClass[0] // Error - no $_get function available
setClass[0] = setClass
```

Type `string` can be used as a type of the index parameter:

::: {.index}
function
indexing expression
string
string type
type
index parameter
:::

``` {.typescript}
class SomeClass {
   $_get (index: string): SomeClass { return this }
   $_set (index: string, value: SomeClass) { }
}
let x = new SomeClass
x = x["index string"]
   // This notation implies a call: x = x.$_get ("index string")
x["index string"] = x
   // This notation implies a call: x.$_set ("index string", x)
```

Functions `$_get` and `$_set` are ordinary functions with compiler-known
signatures. The functions can be used like any other function.
The functions can be abstract, or defined in an interface and implemented later.
The functions can be overridden and provide a dynamic dispatch for the indexing
expression evaluation (see `Indexing Expressions`{.interpreted-text role="ref"}). The functions can be
used in generic classes and interfaces for better flexibility. A
`compile-time error`{.interpreted-text role="index"} occurs if these functions are marked as `async`.

::: {.index}
function
ordinary function
compiler
compiler-known signature
abstract function
signature
overriding
interface
implementation
dynamic dispatch
implementation
indexing expression
indexing expression evaluation
generic class
generic interface
evaluation
flexibility
async function
:::

``` {.typescript}
interface ReadonlyIndexable<K, V> {
   $_get (index: K): V
}

interface Indexable<K, V> extends ReadonlyIndexable<K, V> {
   $_set (index: K, value: V)
}

class IndexableByNumber<V> implements Indexable<number, V> {
   private data: V[] = []
   $_get (index: number): V { return this.data [index] }
   $_set (index: number, value: V) { this.data[index] = value }
}

class IndexableByString<V> implements Indexable<string, V> {
   private data = new Map<string, V>
   $_get (index: string): V { return this.data [index] }
   $_set (index: string, value: V) { this.data[index] = value }
}

class BadClass extends IndexableByNumber<boolean> {
   override $_set (index: number, value: boolean) { index / 0 }
}

let x: IndexableByNumber<boolean> = new BadClass
x[42] = true // This will be dispatched at runtime to the overridden
   // version of the $_set method
x.$_get (15)  // $_get and $_set can be called as ordinary
   // methods
```

| 

## Iterable Types {#Iterable Types}

A class or an interface is *iterable* if it implements the interface `Iterable`
defined in the `Standard Library`{.interpreted-text role="ref"}, and thus has an accessible parameterless
method with the name `$_iterator` and a return type that is a subtype (see
`Subtyping`{.interpreted-text role="ref"}) of type `Iterator` as defined in the `Standard Library`{.interpreted-text role="ref"}.
It guarantees that an object returned by the `$_iterator` method is of the
type which implements `Iterator`, and thus allows traversing an object of the
*iterable* type.

A union of iterable types is also *iterable*. It means that instances of such
types can be used in `for-of` statements (see `For-Of Statements`{.interpreted-text role="ref"}).

Array (see `Array Types`{.interpreted-text role="ref"}) and string (see `Type string`{.interpreted-text role="ref"}) types are
iterable.

An *iterable* class `C` is represented in the example below:

::: {.index}
iterable class
class
iterable interface
interface
parameterless method
access
accessibility
subtyping
subtype
iterator
instance
for-of statement
return type
traversing
assignability
type Iterator
implementation
iterable type
union
for-of statement
object
:::

``` {.typescript}
class C implements Iterable<string> {
  data: string[] = ['a', 'b', 'c']
  $_iterator() { // Return type is inferred from the method body
    return new CIterator(this)
  }
}

class CIterator implements Iterator<string> {
  index = 0
  base: C
  constructor (base: C) {
    this.base = base
  }
  next(): IteratorResult<string> {
    return {
      done: this.index >= this.base.data.length,
      value: this.index >= this.base.data.length ? "" : this.base.data[this.index++]
    }
  }
}

let c = new C()
for (let x of c) {
      console.log(x)
}
```

In the example above, class `C` method `$_iterator` returns
`CIterator<string>` that implements `Iterator<string>`. If executed,
this code prints out the following:

``` {.typescript}
"a"
"b"
"c"
```

The method `$_iterator` is an ordinary method with a compiler-known
signature. This method can be used like any other method. It can be
abstract or defined in an interface to be implemented later. A
`compile-time error`{.interpreted-text role="index"} occurs if this method is marked as `async`.

::: {.index}
type inference
inferred type
method
method body
ordinary method
class
iterator
compiler-known signature
compiler
signature
implementation
async method
:::

::: {.note}
::: {.title}
Note
:::

To support the code compatible with , the name of the method
`$_iterator` can be written as `[Symbol.iterator]`. In this case, the
class `C` from the example above looks as follows:

``` {.typescript}
class C implements Iterable<string>  {
  data: string[] = ['a', 'b', 'c'];
  [Symbol.iterator]() {
    return new CIterator(this)
  }
}
```
:::

The use of the name `[Symbol.iterator]` is considered deprecated.
It can be removed in the future versions of the language.

::: {.index}
compatibility
compatible code
name
class
method
iterator
iterable class
:::

| 

## Callable Types {#Callable Types}

A type is *callable* if the name of the type can be used in a call expression.
A call expression that uses the name of a type is called a *type call
expression*. Only class type can be callable. To make a type
callable, a static method either with the name `$_invoke` or with the name
`$_instantiate` must be defined:

``` {.typescript}
class C {
    static $_invoke() { console.log("invoked") }
}
C() // prints: invoked
C.$_invoke() // also prints: invoked
```

In the above example, `C()` is a *type call expression*. It is the short
form of the normal method call `C.$_invoke()`. Using an explicit call is
always valid for the methods `$_invoke` and `$_instantiate`.

A class can define either the method `$_invoke()` or the method `$_instantiate`
but not both. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs. However, a class
can define several implementations of the methods `$_invoke` or `$_instantiate`
with different signatures:

``` {.typescript}
// Compile-time error, both $_invoke and $_instantiate defined
class A {
    static $_invoke(i: int): int { return i; }
    static $_instantiate(factory: () => A): A { return factory(); }
}

// OK, two $_invoke with different signatures
class B {
    static $_invoke(p: int): int { return p; }
    static $_invoke(): string { return "hello"; }
}
```

Static methods have no access to type parameters of generic in . It means
that the method `$_instantiate` cannot be declared for a generic type. The
method `$_invoke` can be declared, but the *type call expression* or explicit
call of `$_invoke()` must not use a type parameter.

::: {.index}
callable type
call expression
type name
expression
instantiation
invocation
type call expression
callable class type
callable type
class type
type call expression
method call
inheritance
static method
normal method call
call
explicit call
method
:::

::: {.note}
::: {.title}
Note
:::

Only a constructor\-\--not the methods `$_invoke` or `$_instantiate`\-\--is
called in a *new expression*:

``` {.typescript}
class C {
    static $_invoke() { console.log("invoked") }
    constructor() { console.log("constructed") }
}
let x = new C() // constructor is called
```
:::

The methods `$_invoke` and `$_instantiate` are similar but have differences
as discussed below.

::: {.index}
constructor
method
instantiation
invocation
call
new expression
callable type
:::

| 

### Callable Types with `$_invoke` Method {#Callable Types with $_invoke Method}

The static method `$_invoke` can have an arbitrary signature. The method
is either called implicitly in a *type call expression*, or called explicitly.
The class can have several `$_invoke` methods with different signatures. If
the signature has parameters, then the call must contain corresponding arguments.

``` {.typescript}
class Add {
    static $_invoke(a: number, b: number): number {
        return a + b
    }
    static $_invoke(a: string, b: string): string {
        return a + b
    }
}
console.log(Add(2, 2)) // prints: 4
console.log(Add.$_invoke(2, 2)) // prints: 4
console.log(Add("Number ", "one")) // prints "Number one"
```

A class can declare an instance method `$_invoke`
but the method does not make the class *callable*.

::: {.index}
static method
invocation
callable type
arbitrary signature
signature
parameter
method
type call expression
argument
instance method
type
:::

| 

### Callable Types with `$_instantiate` Method {#Callable Types with $_instantiate Method}

The static method `$_instantiate` can have an arbitrary signature by itself.
If it is to be used in a *type call expression*, then
its first parameter must be a *factory* defined as
a parameterless function type returning the class
type in which the method `$_instantiate` is declared. The method can have or
not have other parameters which can be arbitrary. The return type of the method
`$_instantiate` is typically the same as the return type of the factory,
but can be arbitrary instead. A class can contain several static
`$_instantiate` methods with different sets of parameters. If a class declares
two `$_instantiate` methods that have the same parameter set but different
return types, then a `compile-time error`{.interpreted-text role="index"} occurs.

In a *type call expression*, the argument corresponding to the `factory`
parameter is passed implicitly:

``` {.typescript}
class C {
    // #1, parameterless
    static $_instantiate(factory: () => C): C {
        return factory()
    }

    // #2. As #1, but with another return type
    // If uncommented, then a compile-time error occurs
    // static $_instantiate(factory: () => C): int {
    //     return 1
    // }

    // #3, with string parameter
    static $_instantiate(factory: () => C, s: string): string {
        return "hello " + s
    }
}

let x = C() // #1 called, factory is passed implicitly

// Explicit call of #1 requires explicit 'factory':
let y = C.$_instantiate(() => { return new C()})

let s: string = C("world") // #3 called, factory is passed implicitly
```

::: {.index}
static method
callable type
method
instantiation
signature
arbitrary signature
type call expression
parameter
factory parameter
parameterless function type
class type
type call expression
:::

If the method `$_instantiate` has additional parameters, then the call must
contain corresponding arguments:

``` {.typescript}
class C {
    name = ""
    static $_instantiate(factory: () => C, name: string): C {
        let x = factory()
        x.name = name
        return x
    }
}
let x = C("Bob") // factory is passed implicitly
```

A `compile-time error`{.interpreted-text role="index"} occurs in a *type call expression* with type `T`,
if:

-   `T` has neither method `$_invoke` nor method `$_instantiate`; or
-   `T` has the method `$_instantiate` but its first parameter is not
    a `factory`.

``` {.typescript}
class C {
    static $_instantiate(factory: string): C {
        return factory()
    }
}
let x = C() // Compile-time error, wrong '$_instantiate' 1st parameter
```

Where the method `$_instantiate` is used implicitly
in the *type call expression*:

-   If the method `$_instantiate` does not declare
    `factory` as an *optional parameter*, then a `factory`
    implementation is generated automatically.
-   If the method `$_instantiate` declares `factory`
    as an *optional parameter* (see `Optional Parameters`{.interpreted-text role="ref"}), then the default
    implementation is used for `factory`.

``` {.typescript}
class A {
    static $_instantiate(
        factory: () => A): A { return factory() }
}
class B {
    static $_instantiate(
        factory: () => B = () =>{
            console.log("default factory");
            return new B; } ): B
        { return factory() }
}

A() // Automatically generated factory is used
B() // Default implementation is used for factory
```

A *type call expression* passes no arguments
to the `factory` function, and the latter uses
a parameterless class constructor. If a class has
no parameterless class constructor, then a
`compile-time error`{.interpreted-text role="index"} occurs:

``` {.typescript}
class A {
    constructor(p: int) {}
    static $_instantiate(factory: () => A): A { return factory() }
}

A() // Compile-time error, no parameterless constructor
```

::: {.note}
::: {.title}
Note
:::

Calling the method `$_instantiate` explicitly
with such a class, or supplying the default
implementation for the factory that uses
a constructor with parameters, is still
possible though useless:

``` {.typescript}
class A {
    constructor(p: int) {}
    static $_instantiate(
        factory: () => A = () => { return new A(1); }
        ): A { return factory() }
}

A() // OK, default is used for the optional factory
A.$_instantiate(() => { return new A(1); }) // OK, explicit call
```
:::

A class can declare an instance method `$_instantiate`
but the method does not make the class *callable*.

::: {.index}
method
call
factory
type call expression
instantiation
invocation
parameter
callable type
instance method
instance
:::

| 

## Statements {#Statements Experimental}

| 

### For-of Explicit Type Annotation {#For-of Explicit Type Annotation}

An explicit type annotation is allowed for a *ForVariable*
(see `For-Of Statements`{.interpreted-text role="ref"}):

``` {.typescript}
// explicit type is used for a new variable,
let x: string[] = ["aaa", "bbb", "ccc"]
for (let str: string of x) {
  console.log(str)
}
```

Type of elements in a `for-of` expression must be assignable
(see `Assignability`{.interpreted-text role="ref"}) to the type of the variable. Otherwise, a
`compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
type annotation
annotation
for-variable
expression
assignability
variable
for-of type statement
:::

| 

## Explicit Overload Declarations {#Explicit Overload Declarations}

supports conventional overloading for functions, methods, and
constructors (i.e. implicit overloading of same-name entities), and an
innovative form of explicit overload declarations that allows
a developer to specify a set of overloaded entities explicitly and to control
the overload resolution process.

Regardless of implicit or explicit overloading being used, the actual entity
to be called is determined at compile time. As a result, *overloading* is
related to *compile-time polymorphism by name*. The semantic details are
discussed in `Overloading`{.interpreted-text role="ref"}.

::: {.index}
polymorphism
polymorphism by name
entity
overloading
overloaded entity
compile time
compatibility
semantics
:::

An *explicit overload declaration* can be used for:

-   Functions (see `Explicit Function Overload`{.interpreted-text role="ref"}), including functions in
    namespaces;
-   Class or interface methods (see `Explicit Class Method Overload`{.interpreted-text role="ref"} and
    `Explicit Interface Method Overload`{.interpreted-text role="ref"}).

An *overload declaration* starts with the keyword `overload` and
declares an *ordered overload set*. The exact syntax of the declaration
is presented in the appropriate subsections.

::: {.index}
overload declaration
overloaded entity
entity
function
method
constructor
overload declaration
namespace
class method
interface method
method declaration
overload keyword
overload set
entity
:::

The use of an explicit overload declaration is represented in the example below:

``` {.typescript}
function max2(a: number, b: number): number {
    return  a > b ? a : b
}
function maxN(...a: number[]): number {
    // return max element
}

// declare 'max' as an ordered set of functions max2 and maxN
overload max { max2, maxN }

max(1, 2)     // max2 is called
max(3, 2, 4)  // maxN is called
max("a", "b") // Compile-time error, no function to call
```

The semantics of an entity included into an *overload set* does not change.
Such entities follow the ordinary accessibility rules, and can be called
explicitly as follows:

``` {.typescript}
maxN(1, 2) // maxN is explicitly called
max2(2, 3) // max2 is explicitly called
```

When calling an *explicit overload*, entities from an *overload set* are checked
in the listed order, and the first entity with an appropriate signature is
called (see `Overload resolution`{.interpreted-text role="ref"} for detail).
A `compile-time error`{.interpreted-text role="index"} occurs if no entity with an appropriate signature
is available:

::: {.index}
function
semantics
entity
overload
accessibility
overload set
overload resolution
signature
:::

``` {.typescript}
max(1)    // maxN is called
max(1, 2) // max2 is called, as is the first appropriate in the set

max("a", "b") // Compile-time error, no function to call
```

A name in an *overload set* can be the name of an implicitly overloaded entity.
In this case, `Overload Resolution`{.interpreted-text role="ref"} checks each implicitly overloaded
entity for this name, and not a single entity only. The implicitly overloaded
entities are checked in the order of declaration.

The use of a combination of explicit and implicit overloads is represented
in the example below:

``` {.typescript}
// Implicitly overloaded functions:
function minimum(a: number, b: number): number {/*body*/}
function minimum(...a: number[]): number {/*body*/}

// Function with the distinct name:
function minInt(a: int, b: int): int {/*body*/}

// overload set contains 'minInt' and two functions named 'minimum'
overload min {minInt, minimum}

// Overload resolution selects first appropriate function:
min(1, 2)    // minInt is called
min(3.14, 2) // min(a: number, b: number) is called
min(1, 2, 3) // min(...a: number[]) is called
```

An overloaded entity in an *explicit overload declaration* can be *generic*
(see `Generics`{.interpreted-text role="ref"}).

If type arguments are provided explicitly in a call of an overloaded entity
(see `Explicit Generic Instantiations`{.interpreted-text role="ref"}), then only the entities that have
the number of type arguments compatible with the number of mandatory and
optional type parameters (i.e., entities with optional type parameters are the
entities that have type parameter default) are considered during
`Overload Resolution`{.interpreted-text role="ref"}:

``` {.typescript}
// Resolution with explicit type arguments
function one<T>() { console.log("one") }
function two<T, U=string>() { console.log("two") }
function three<T, U=string, V=number>() { console.log("three") }

overload numbers { one, two, three }

numbers<string, number, int>() // Only 'three` considered

numbers<string, number>() // 'two' and 'three; considered as both
                          // allow 2 type arguments

numbers<int>()  // 'one', 'two' and 'three; considered as all
                // allow 1 type argument
```

If *type arguments* are not provided explicitly (see
`Implicit Generic Instantiations`{.interpreted-text role="ref"}), then consideration is given to all
entities as represented in the example below:

::: {.index}
entity
call
call site
function call
overloaded entity
overload declaration
generic
generic instantiation
type argument
type parameter
overload resolution
:::

``` {.typescript}
function foo1(s: string) {}
function foo2<T>(x: T) {}

overload foo { foo1, foo2 }

foo("aa")   // foo1 is called
foo(1) // foo2 is called, implicit generic instantiation
foo<string>("aa") // foo2 is called
```

An entity can be listed in several *explicit overload declarations*:

``` {.typescript}
function max2i(a: int, b: int): int {
    return  a > b ? a : b
}
function maxNi(...a: int[]): int {
    // return max element
}
function maxN(...a: number[]): number {
    // return max element
}

overload maxi { max2i, maxNi }
overload max { max2i, maxNi, maxN }
```

::: {.index}
entity
function
overload declaration
generic instantiation
:::

| 

### Explicit Function Overload {#Explicit Function Overload}

*Explicit function overload* allows declaring a name for a set of functions
(see `Function Declarations`{.interpreted-text role="ref"}). The syntax is presented below:

``` {.abnf}
explicitFunctionOverload:
    'overload' identifier overloadList
    ;
overloadList:
    '{' identifier (',' identifier)* ','? '}'
    ;
```

::: {.index}
explicit function overload
set of functions
function declaration
function
syntax
qualified name
:::

A `compile-time error`{.interpreted-text role="index"} occurs if an *identifier* in the list refers
to no accessible function.

All overloaded functions must be in the same module or namespace scope (see
`Scopes`{.interpreted-text role="ref"}). Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs. The erroneous
overload declarations are represented in the example below:

``` {.typescript}
import {foo1} from "something"

function foo2() {}
overload foo {foo1, foo2} // Compile-time error

namespace N {
    export function fooN() {}
    namespace M {
        export function fooM() {}
    }
    overload goo {M.fooM, fooN} // Compile-time error
}
overload bar {foo2, N.fooN} // Compile-time error
```

::: {.index}
overloaded function
module
namespace
namespace scope
scope
overload declaration
import
:::

A name of an *explicit function overload* can be the same as the name of a
function or implicitly overloaded functions in the same scope,
but the name must be used in the overloaded list, otherwise
a `compile-time`{.interpreted-text role="index"} occurs.
This situation is represented in the following example:

``` {.typescript}
function foo(n: number): number {/*body1*/}
function fooString(s: string): string {/*body2*/}

overload foo {foo, fooString} // valid overload

foo(1)    // function 'foo' is called
foo("aa") // function 'fooString' is called

function bar(): void {}

// Invalid overload, as 'bar' does not appear in the list:
overload bar {foo, fooString} // Compile-time error

let name: string = "abc"

// Invalid overload, as 'name' refers to a variable:
overload name {foo, fooString, name} // Compile-time error
```

Using the name of a function as the name of an explicit overload causes no
ambiguity for it is considered at the call site only, i.e., a name of an
*explicit overload* is **not** considered in the following situations:

-   List of the overloaded entities;
-   `Function Reference`{.interpreted-text role="ref"}.

::: {.index}
name
overloaded function
function
entity
function reference
:::

``` {.typescript}
function foo(n: number): number {/*body1*/}
function fooString(s: string): string {/*body2*/}
overload foo {foo, fooString}

let func1 = foo // 'foo' refers to function, not to explicit overload
```

A `compile-time error`{.interpreted-text role="index"} occurs, if an *explicit overload* is exported
but an overloaded function is not:

``` {.typescript}
export function foo1(p: string) {}
function foo2(p: number) {}
export overload foo { foo1, foo2 } // Compile-time error, 'foo2' is not exported
overload bar { foo1, foo2 } // OK, as 'bar' is not exported
```

If an *explicit overload* is called like a function with receiver, i.e., syntax
of method call is used (see `Functions with Receiver`{.interpreted-text role="ref"}), then a
`compile-time error`{.interpreted-text role="index"} occurs:

``` {.typescript}
function bar1(this: string) {}
function bar2(this: number) {}

overload bar { bar1, bar2 }

let s: string = "";
let n: number = 1;

bar(s) // OK
bar(n) // OK
s.bar()  // Compile-time error
n.bar()  // Compile-time error
```

| 

### Explicit Class Method Overload {#Explicit Class Method Overload}

*Explicit class method overload* allows declaring a name
for a set of class methods (see `Method Declarations`{.interpreted-text role="ref"}).
The syntax is presented below:

``` {.abnf}
explicitClassMethodOverload:
    explicitClassMethodOverloadModifier*
    'overload' identifier overloadList
    ;

explicitClassMethodOverloadModifier: 'static' | 'async';
```

The use of an *explicit class method overload* is represented in the example
below:

::: {.index}
class method
class member
static method
instance method
method
explicit class method overload
syntax
set of methods
identifier
:::

``` {.typescript}
class Processor {
    overload process { processNumber, processString }
    processNumber(n: number) {/*body*/}
    processString(s: string) {/*body*/}
}

let c = new C()
c.process(42) // calls processNumber
c.process("aa") // calls processString
```

The name of an *explicit method overload* can be the same as the name of a
method in the same class (see `Explicit Overload Name Same As Method Name`{.interpreted-text role="ref"}
for details).

*Static explicit overload* is represented in the example below:

``` {.typescript}
class C {
    static one(n: number) {/*body*/}
    static two(s: string) {/*body*/}
    static overload foo { one, two }
}
```

A `compile-time error`{.interpreted-text role="index"} occurs if:

-   Method modifier is used more than once in an explicit method overload;

-   *Identifier* in the overloaded method list refers to no accessible
    method (either declared or inherited) of the current class;

-   *Explicit overload* is:

    > -   *Static* but the overloaded method is *non-static*;
    > -   *Non-static* but the overloaded method is *static*;
    > -   Marked `async` but the overloaded method is not; or
    > -   Not `async` but the overloaded method is.

::: {.index}
method modifier
explicit method overload
identifier
accessible method
declaration
inheritance
overloaded method
:::

An *explicit overload* and the overloaded methods can have different access
modifiers. A `compile-time error`{.interpreted-text role="index"} occurs if an *explicit overload* is:

-   `public` but at least one overloaded method is not `public`;
-   `protected` but at least one overloaded method is `private`.

Valid and invalid explicit overloads are represented in the example below:

::: {.index}
overloaded method
explicit overload
access modifier
public
protected
private
:::

``` {.typescript}
class C {
    private foo1(x: number) {/*body*/}
    protected foo2(x: string) {/*body*/}
    public foo3(x: boolean) {/*body*/}
    foo4() {/*body*/} // implicitly public

    public overload foo { foo3, foo4 } // OK
    protected overload bar { foo2, foo3 } // OK
    private overload goo { foo1, foo2, foo3 } // OK

    public overload err1 {foo2, foo3} // Compile-time error, foo2 is not public
    protected overload err2 {foo2, foo1} // Compile-time error, foo1 is private
}
```

Some or all overloaded functions can be `native` as follows:

``` {.typescript}
class C {
    native foo1(x: number)
    foo2(x: string) {/*body*/}
    overload foo { foo1, foo2 }
}
```

::: {.index}
public
overload
private
overloaded function
native
:::

If a superclass has an *explicit overload*, then this declaration can be
overridden in a subclass. If a subclass does not override an
*explicit overload*, then the overload from the superclass is inherited.

If a subclass overrides an *explicit overload*, then this declaration must
list all methods of the *explicit overload* in a superclass, otherwise, a
`compile-time error`{.interpreted-text role="index"} occurs.

In addition, overriding an *explicit overload* in a subclass can include
new methods and change the order of methods.

An *explicit overload* is used like an ordinary class method except that it is
replaced in a call at compile time for one of overloaded methods that use the
type of *object reference*. An *explicit overload* in subtypes is
represented in the example below:

::: {.index}
superclass
overload declaration
overriding
subclass
inheritance
declaration
superclass
overloaded method
object reference
method
:::

``` {.typescript}
class Base {
    overload process { processNumber, processString }
    processNumber(n: number) {/*body*/}
    processString(s: string) {/*body*/}
}

class D1 extends Base {
    // method is overridden
    override processNumber(n: number) {/*body*/}
    // overload declaration is inherited
}

class D2 extends Base {
    // method is added:
    processInt(n: int) {/*body*/}
    // new order for overloaded methods is specified:
    overload process { processInt, processNumber, processString }
}

new D1().process(1)   // calls processNumber from D1

new D2().process(1)   // calls processInt from D2 (as it is listed earlier)
new D2().process(1.0) // calls processNumber from Base (first appropriate)
```

Methods with special names (see `Indexable Types`{.interpreted-text role="ref"}, `Iterable Types`{.interpreted-text role="ref"},
and `Callable Types`{.interpreted-text role="ref"}) can be overloaded like ordinary methods:

::: {.index}
overloaded method
overriding
method
name
iterable type
callable type
inheritance
ordinary method
name
:::

``` {.typescript}
class C {
    getByNumber(n: number): string {...}
    getByString(s: string): string {...}
    overload $_get { getByNumber, getByString }
}

let c = new C()

c[1]     // getByNumber is used
c["abc"] // getByString is used
```

If a class implements some interfaces with an *explicit overload* of the
same name, then a new *explicit overload* must include all overloaded
methods. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
overloaded method
class
interface
overload declaration
alias
:::

``` {.typescript}
interface I1 {
    overload foo {f1, f2}
    // f1 and f2 are declared in I1
}
interface I2 {
    overload foo {f3, f4}
    // f3 and f4 are declared in I2
}
class C implements I1, I2 {
   // Compile-time error as no new overload is defined
}
class D implements I1, I2 {
    overload foo { f2, f3, f1, f4 } // OK, as new overload is defined
}
class E implements I1, I2 {
    overload foo { f2, f4 } // Compile-time error as not all methods are used
}

const i1: I1 = new D
i1.foo(<arguments>) // call is valid if arguments fit first signature of {f1, f2} set

const i2: I2 = new D
i2.foo(<arguments>) // call is valid if arguments fit first signature of {f3, f4} set

const d: D = new D
d.foo(<arguments>) // call is valid if arguments fit first signature of {f2, f3, f1, f4} set
```

::: {.index}
overloaded interface
declaration
method
argument
signature
:::

| 

### Explicit Interface Method Overload {#Explicit Interface Method Overload}

*Explicit interface method overload* allows declaring a name
for a set of interface methods (see `Interface Method Declarations`{.interpreted-text role="ref"}).
The syntax is presented below:

``` {.abnf}
explicitInterfaceMethodOverload:
    'overload' identifier overloadList
    ;
```

The use of an *explicit interface method overload* is represented in the
example below:

``` {.typescript}
interface I {
    foo(): void
    bar(n?: string): void
    overload goo { foo, bar }
}

function example(i: I) {
    i.goo()        // calls i.foo()
    i.goo("hello") // calls i.bar("hello")
    i.bar()        // explicit call: i.bar(undefined)
}
```

::: {.index}
interface method
explicit overload
interface
:::

The name of an *explicit method overload* can be the same as the name of a
method in the same interface (see
`Explicit Overload Name Same As Method Name`{.interpreted-text role="ref"} for details).

An *explicit overload* is used like an ordinary interface method, except that
one of the overloaded methods replaces it in a call at compile time by using
the type of *object reference*.

An *explicit interface overload* can be overridden in a class. In that case,
an *explicit overload* in a class must contain all the methods overloaded in the
interface. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

``` {.typescript}
class D implements I {
     foo(): void {/*body*/}
     bar(n?: string): void {/*body*/}
     overload goo( bar, foo) // order is changes
}

let d = new D()
d.goo() // d.bar(undefined) is used, as it is the first appropriate method
```

If a class does not override an *explicit overload* declared in an interface,
then it inherits the overload:

``` {.typescript}
// Using interface overload declaration
class C implements I {
     foo(): void {/*body*/}
     bar(n?: string): void {/*body*/}
}

let c = new C()
c.goo() // calls c.foo()
```

::: {.index}
ordinary method
interface method
call
compile time
overloaded method
object reference
type
class
implementation
:::

An *explicit overload* defined in a superinterface can be overridden in a
subinterface. In this case, the *overload declaration* of the subinterface
must contain all methods overloaded in superinterface. Otherwise, a
`compile-time error`{.interpreted-text role="index"} occurs.

An *explicit overload* defined in a superinterface must be overridden in a
subinterface if several *explicit overloads* of the same name are inherited
in the interface. Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.index}
interface
class
explicit overload
superinterface
method
subinterface
overloaded method
interface
override
inheritance
:::

``` {.typescript}
interface I1 {
    overload foo {f1, f2}
    // f1 and f2 are declared in I1
}
interface I2 {
    overload foo {f3, f4}
    // f3 and f4 are declared in I2
}
interface I3 extends I1, I2 {
   // Compile-time error as no new overload for 'foo' is defined
}
interface I4 extends I1, I2 {
    overload foo { f4, f1, f3, f2 } // OK, as new overload is defined
}
interface I5 extends I1, I2 {
    overload foo { f1, f3 } // Compile-time error as not all methods are included
}
```

| 

### Explicit Overload Name Same As Method Name {#Explicit Overload Name Same As Method Name}

The name of an *explicit overload* of a class or an interface can be the same
as the name of the overloaded method. For example, a method defined in a
superclass can be used as one of the overloaded methods in an *explicit
overload* of the same-name subclass. This important case is represented in the
following example:

``` {.typescript}
class C {
    foo(n: number): number {/*body*/}
}
class D extends C {
    fooString(s: string): string {/*body*/}

    overload foo {
        foo, // method 'foo' from C
        fooString
    }
}

let d = new D()
let c: C = d

d.foo(1)    // 'foo' from C is called
d.foo("aa") // 'fooString' from D is called
c.foo(1)    // method 'foo' from is called (no overload)
```

::: {.index}
method name
explicit overload
overloaded method
superclass
subclass
:::

If names of a method and of an *explicit overload* are the same, then the method
can be overridden as usual:

``` {.typescript}
class C {
    foo(n: number): number {/*body*/}
}
class D extends C {
    foo(n: number): number {/*body*/} // method is overridden
    fooString(s: string): string {/*body*/}

    overload foo { foo, fooString }
}
```

This feature is also valid in interfaces, or in an interface and a class that
implements the interface:

::: {.index}
method
name
method name
overriding
overridden method
interface
class
implementation
:::

``` {.typescript}
interface I {
    foo(n: number): number {/*body*/}
}
interface J extends I {
    fooString(s: string): string
    overload foo { foo, fooString }
}

class K implements I {
    foo(n: number): number {/*body*/}
    fooString(s: string): string {/*body*/}

    overload foo { foo, fooString }
}
```

The use of an *explicit overload* causes no ambiguity for it is considered
at the call site only. An *explicit overload* name is **not** considered
in the following situations:

-   `Overriding`{.interpreted-text role="ref"};
-   List of the overloaded entities (see `Explicit Class Method Overload`{.interpreted-text role="ref"}
    and `Explicit Interface Method Overload`{.interpreted-text role="ref"});
-   `Method Reference`{.interpreted-text role="ref"}.

::: {.index}
number
interface
string
overload
call site
overriding
overloaded entity
method reference
class method overload declaration
method reference
:::

``` {.typescript}
class C {
    foo(n: number): number {/*body*/}
}

class D extends C {
    fooString(s: string): string {/*body*/}

    overload foo { foo, fooString }
}

let d = new D()
let c: C = d

let func1 = c.foo // method 'foo' is used
let func2 = d.foo // method 'foo' is used
```

A `compile-time error`{.interpreted-text role="index"} occurs if the name of an *explicit overload*
is the same as the name of a method (with the same static or non-static
modifier) that is not listed as an overloaded method as follows:

``` {.typescript}
class C {
    foo(n: number) {/*body*/}
    fooString(s: string) {/*body*/}
    fooBoolean(b: boolean) {/*body*/}

    overload foo { // Compile-time error
        fooBoolean, fooString
    }
}
```

::: {.index}
number
string
method
static modifier
non-static modifier
overloaded method
:::

| 

## Native Functions and Methods {#Native Functions and Methods}

### Native Functions {#Native Functions}

*Native function* is a function marked with the keyword `native` (see
`Function Declarations`{.interpreted-text role="ref"}).

*Native function* implemented in a platform-dependent code is typically written
in another programming language (e.g., *C*). A `compile-time error`{.interpreted-text role="index"}
occurs if a native function has a body.

::: {.index}
native keyword
function
native function
native method
function body
:::

| 

### Native Methods {#Native Methods Experimental}

*Native method* is a method marked with the keyword `native` (see
`Method Declarations`{.interpreted-text role="ref"}).

*Native methods* are the methods implemented in a platform-dependent code
written in another programming language (e.g., *C*).

A `compile-time error`{.interpreted-text role="index"} occurs if:

-   Method declaration contains the keyword `abstract` along with the
    keyword `native`.
-   *Native method* has a body (see `Method Body`{.interpreted-text role="ref"}) that is a block
    instead of a simple semicolon or empty body.

::: {.index}
native method
method
implementation
platform-dependent code
native keyword
method body
block
method declaration
abstract keyword
semicolon
empty body
:::

| 

### Native Constructors {#Native Constructors}

*Native constructor* is a constructor marked with the keyword `native` (see
`Constructor Declaration`{.interpreted-text role="ref"}).

*Native constructors* are the constructors implemented in a platform-dependent
code written in another programming language (e.g., *C*).

A `compile-time error`{.interpreted-text role="index"} occurs if a *native constructor* has a non-empty
body (see `Constructor Body`{.interpreted-text role="ref"}).

::: {.index}
native constructor
constructor
constructor declaration
platform-dependent code
native keyword
implementation
non-empty body
:::

| 

## Classes Experimental {#Classes Experimental}

### Final Classes {#Final Classes}

A class can be declared `final` to prevent extension, i.e., a class declared
`final` can have no subclasses. No method of a `final` class can be
overridden.

If a class type `F` expression is declared *final*, then only a class `F`
object can be its value.

A `compile-time error`{.interpreted-text role="index"} occurs if the `extends` clause of a class
declaration contains another class that is `final`.

::: {.index}
final class
class
class type
subclass
object
extension
method
overriding
class
class extension
extends clause
class declaration
:::

| 

### Final Methods {#Final Methods}

A method can be declared `final` to prevent it from being overridden (see
`Overriding Methods`{.interpreted-text role="ref"}) in subclasses.

A `compile-time error`{.interpreted-text role="index"} occurs if:

-   The method declaration contains the keyword `abstract` or `static`
    along with the keyword `final`.
-   A method declared `final` is overridden.

::: {.index}
final method
overriding
instance method
final method
overridden method
subclass
method declaration
abstract keyword
static keyword
final keyword
:::

| 

## Default Interface Method Declarations {#Default Interface Method Declarations}

The syntax of *interface default method* is presented below:

``` {.abnf}
interfaceDefaultMethodDeclaration:
    'private'? identifier signature block
    ;
```

A default method can be explicitly declared `private` in an interface body.

A block of code that represents the body of a default method in an interface
provides a default implementation for any class if such a class does not
override the method that implements the interface.

::: {.index}
method declaration
interface method declaration
default method
private method
implementation
interface
block
class
method body
interface body
default implementation
overriding
syntax
:::

| 

## Adding Functionality to Existing Types {#Adding Functionality to Existing Types}

supports adding functions and accessors to already defined types. The
usage of functions so added looks the same as if they are methods and accessors
of such types. The mechanism is called `Functions with Receiver`{.interpreted-text role="ref"}. This
feature is often used to add new functionality to a class or an interface
without having to inherit from the class or to implement the interface.
However, it can be used not only for classes and interfaces but also for other
types.

Moreover, `Function Types with Receiver`{.interpreted-text role="ref"} and
`Lambda Expressions with Receiver`{.interpreted-text role="ref"} can be defined and used to make the
code more flexible.

::: {.index}
functionality
function
type
accessor
method
function with receiver
interface
inheritance
class
implementation
function type
lambda expression
lambda expression with receiver
flexibility
:::

| 

### Functions with Receiver {#Functions with Receiver}

*Function with receiver* declaration is a top-level declaration
(see `Top-Level Declarations`{.interpreted-text role="ref"}) that looks almost the same as
`Function Declarations`{.interpreted-text role="ref"}, except that the first mandatory parameter uses
keyword `this` as its name.

The syntax of *function with receiver* is presented below:

``` {.abnf}
functionWithReceiverDeclaration:
    'function' identifier typeParameters? signatureWithReceiver block
    ;

signatureWithReceiver:
    '(' receiverParameter (', ' parameterList)? ')' returnType?
    ;

receiverParameter:
    annotationUsage? 'this' ':' type
    ;
```

::: {.index}
function with receiver
function with receiver declaration
declaration
top-level declaration
function declaration
parameter
this keyword
:::

*Function with receiver* can be called in the following two ways by making:

-   Ordinary function call (see `Function Call Expression`{.interpreted-text role="ref"}) when the first
    argument is the receiver object;
-   Method call (see `Method Call Expression`{.interpreted-text role="ref"}) when the receiver is an
    `objectReference` before the function name passed as the first argument
    of the call.

All other arguments are handled in an ordinary manner.

::: {.index}
function with receiver
function call
expression
parameter
method call
method call expression
derived class
derived interface
argument
object reference
receiver
function name
:::

The keyword `this` must be used in the parameter list for the first parameter
only. If it is used for other parameters, then a `compile-time error`{.interpreted-text role="index"}
occurs.

The keyword `this` can be used inside a *function with receiver* where
it corresponds to the first parameter. The type of parameter `this` is called
*receiver type* (see `Receiver Type`{.interpreted-text role="ref"}):

``` {.typescript}
class A {
  num: number = 1
  foo(): void { console.log(this.num); }
}
function bar(this: A) {
  this.num = 5
}
let a = new A()
a.foo() // method is called
a.bar() // Function with receiver is called
a.foo() // method is called
```

The first parameter named `this` is readonly.

If the *receiver type* is a class or interface type, then `private` or
`protected` members are not accessible (see `Accessible`{.interpreted-text role="ref"}) within the
body of a *function with receiver*. Only `public` members can be accessed:

::: {.index}
this keyword
function with receiver
receiver type
type parameter
call
interface type
public member
private member
protected member
access
accessibility
parameter
:::

``` {.typescript}
class A {
    foo () { ... this.bar() ... }
                 // function bar() is accessible here
    protected member_1 ...
    private member_2 ...
}
function bar(this: A) { ...
   this.foo() // Method foo() is accessible as it is public
   this.member_1 // Compile-time error as member_1 is not accessible
   this.member_2 // Compile-time error as member_2 is not accessible
   ...
}
let a = new A()
a.foo() // Ordinary class method is called
a.bar() // Function with receiver is called
```

Derived classes or interfaces can be used as receivers:

``` {.typescript}
class C {}

function foo(this: C) {}
function bar(this: C, n: number): void {}

let c = new C()

// as a function call:
foo(c)
bar(c, 1)

// as a method call:
c.foo()
c.bar(1)

interface D {}
function foo1(this: D) {}
function bar1(this: D, n: number): void {}

function demo (d: D) {
   // as a function call:
   foo1(d)
   bar1(d, 1)

   // as a method call:
   d.foo1()
   d.bar1(1)
}

class E implements D {}
const e = new E

// derived class is used as a receiver for a method call:
e.foo1()
e.bar1(1)

// the same as a function call:
foo1(e)
bar1(e, 1)
```

*Function with receiver* can be generic as in the following example:

::: {.index}
function with receiver
access
accessibility
instance method
derived class
name
method
receiver type
generic function
:::

``` {.typescript}
class G<T> {}

function foo<T>(this: G<T>, p: T) {
    console.log (p)
}

class C {}

let g = new G<C>
g.foo(new C)    // implicit instantiation
g.foo<C>(new C) // explicit instantiation
```

When the receiver type contains an accessible
instance method (see `Accessible`{.interpreted-text role="ref"}) with the same name as the
function with receiver, the instance method has a priority
over the implicitly called function with receiver. The function with receiver
still can be called explicitly:

``` {.typescript}
class A {
    foo (): int { return 1; }
}

function foo(this: A): int { return 2; }

console.log((new A).foo())  // instance method called, prints '1'
console.log(foo(new A)) // explicit call of a receiver function, prints '2'
```

*Functions with receiver* are dispatched statically. What function is being
called is known at compile time based on the receiver type specified in the
declaration. A *function with receiver* can be applied to the receiver of any
derived class until it is overridden within the derived class:

``` {.typescript}
class Base { ... }
class Derived extends Base { ... }

function foo(this: Base) { console.log ("Base.foo is called") }

let b: Base = new Base()
b.foo() // `Base.foo is called` to be printed
b = new Derived()
b.foo() // `Base.foo is called` to be printed
```

A *function with receiver* can be defined in a module other than the one that
defines the receiver type. This is represented in the following example:

::: {.index}
function with receiver
static dispatch
function call
compile time
receiver type
declaration
receiver
derived class
class
module
:::

``` {.typescript}
// file a.ets
class A {
    foo() { ... }
}

// file ext.ets
import {A} from "a.ets" // name 'A' is imported
function bar(this: A) () {
   this.foo() // Method foo() is called
}
```

A *function with receiver* can be defined in a namespace (see
`Namespace Declarations`{.interpreted-text role="ref"}). A *function with receiver* cannot be called by
using the *method call* syntax outside the namespace, though, because an entity
exported from a namespace can be accessed in the form of a `qualifiedName`
only.

This situation is represented in the following example:

``` {.typescript}
namespace NS {
    export function foo(this: int) {}
    function bar(i: int) {
        i.foo() // OK, method call is used
    }
}

let i = 1
NS.foo(i)  // OK, function call is used
i.foo()    // Compile-time error, 'foo' is not resolved
i.NS.foo() // Compile-time error, 'NS' is not defined for 'int'
```

::: {.note}
::: {.title}
Note
:::

While a function with receiver can be used in an explicit overload list,
such an overload cannot be called by using the method access syntax as
in the example provided in `Explicit Function Overload`{.interpreted-text role="ref"}.
:::

| 

### Receiver Type {#Receiver Type}

*Receiver type* is the type of the *receiver parameter* in a function,
function type, and lambda with receiver. A *receiver type* can be
an interface type, a class type, or an array type.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

Using array type as a *receiver type* is presented in the example below:

``` {.typescript}
function addElements(this: number[], ...s: number[]) {
 ...
}

let x: number[] = [1, 2]
x.addElements(3, 4)
```

::: {.index}
receiver type
receiver parameter
type
function
function type
lambda with receiver
interface type
class type
array type
type parameter
array type
:::

| 

### Function Types with Receiver {#Function Types with Receiver}

*Function type with receiver* specifies the signature of a function or lambda
with receiver. It is almost the same as *function type* (see `Function Types`{.interpreted-text role="ref"}),
except that the first parameter is mandatory, and the keyword `this` is used
as its name:

The syntax of *function type with receiver* is presented below:

``` {.abnf}
functionTypeWithReceiver:
    '(' receiverParameter (',' ftParameterList)? ')' ftReturnType
    ;
```

The type of a *receiver parameter* is called the *receiver type* (see
`Receiver Type`{.interpreted-text role="ref"}).

::: {.index}
function type with receiver
signature
function
lambda
function with receiver
lambda with receiver
function type
this keyword
syntax
parameter
receiver type
receiver parameter
:::

``` {.typescript}
class A {...}

type FA = (this: A) => boolean
type FN = (this: number[], max: number) => number
```

*Function type with receiver* can be generic as in the following example:

``` {.typescript}
class B<T> {...}

type FB<T> = (this: B<T>, x: T): void
type FBS = (this: B<string>, x: string): void
```

The usual rule of function type compatibility (see
`Subtyping for Function Types`{.interpreted-text role="ref"}) is applied to
*function type with receiver*, and parameter names are ignored.

::: {.index}
function type with receiver
generic
function type
compatibility
subtyping
parameter name
:::

``` {.typescript}
class A {...}

type F1 = (this: A) => boolean
type F2 = (a: A) => boolean

function foo(this: A): boolean {}
function goo(a: A): boolean {}

let f1: F1 = foo // OK
f1 = goo // OK

let f2: F2 = goo // OK
f2 = foo // OK
f1 = f2 // OK
```

The sole difference is that only an entity of *function type with receiver*
nut not an entity of a compatible *function type* can be used in
`Method Call Expression`{.interpreted-text role="ref"}.

``` {.typescript}
let a = new A()
a.f1() // OK, function type with receiver
f1(a)  // OK

a.f2() // Compile-time error
f2(a) // OK
```

::: {.index}
entity
function type with receiver
method call
expression
compile-time error
:::

::: {.note}
::: {.title}
Note
:::

The limitation of the method call syntax can be easily bypassed by assigning
an ordinary function to a compatible *function type with receiver*.
A snippet of code illustrative of parameter type with receiver is
represented by the example below.
:::

Function type with receiver can be used as a parameter type. Using parameter
type with receiver is represented by the example below:

``` {.typescript}
function foo(p: number, f: (this: number)=> number) {
    console.log(p.f(), f(p))
}

function goo(this: number) { return this - 1 }
function bar(this: number) { return this + 1 }
function compat(n: number) { return n }

let n: number = 1
foo(n, goo)  // prints `0 0`
foo(n, bar)  // prints `2 2`
foo(n, compat)  // prints `1 1`
```

The method call syntax cannot be used when assigning the actual entity to a
variable of *function type with receiver*. Attempting to do so causes a
`compile-time error`{.interpreted-text role="index"}:

``` {.typescript}
function foo<T extends Object>(this: T, functor: (this: T)=> void): void {
   // following two calls are equivalent
   functor(this)
   this.functor()
}

function bar<T>(this: T): void {
   console.log(this)
}

let x = 5
x.foo(bar<int>) // OK
let y = bar<int> // OK
x.foo(y) // OK

// compile time error - can not assign entity with method call syntax
// to a function type
x.foo(x.bar)
x.foo(x.bar<int>)
let z = x.bar
let y = x.bar<int>
```

| 

### Lambda Expressions with Receiver {#Lambda Expressions with Receiver}

*Lambda expression with receiver* defines an instance of a *function type with
receiver* (see `Function Types with Receiver`{.interpreted-text role="ref"}). It looks almost the same
as an ordinary lambda expression (see `Lambda Expressions`{.interpreted-text role="ref"}), except that
the first parameter is mandatory, and the keyword `this` is used as its name:

The syntax of *lambda expression with receiver* is presented below:

``` {.abnf}
lambdaExpressionWithReceiver:
    annotationUsage?
    '(' receiverParameter (',' lambdaParameterList)? ')'
    returnType? '=>' lambdaBody
    ;
```

The use of annotations is discussed in `Using Annotations`{.interpreted-text role="ref"}.

The keyword `this` can be used inside a *lambda expression with receiver*,
It corresponds to the first parameter:

::: {.index}
lambda expression with receiver
lambda expression
instance
function type with receiver
lambda expression
parameter
this keyword
annotation
:::

``` {.typescript}
class A { name = "Bob" }

let show = (this: A): void {
    console.log(this.name)
}
```

Lambda can be called in two syntactical ways represented by the example below:

``` {.typescript}
class A {
  name: string
  constructor (n: string) {
      this.name = n
  }
}

function foo(aa: A[], f: (this: A) => void) {
  for (let a of aa) {
      a.f() // first way
      f (a) // second way
  }
}

let aa: A[] = [new A("aa"), new A("bb")]
foo(aa, (this: A) => { console.log(this.name)} ) // output: "aa" "bb"
```

::: {.index}
lambda
syntax
constructor
function
class
:::

::: {.note}
::: {.title}
Note
:::

If *lambda expression with receiver* is declared in a class or interface,
then `this` use in the lambda body refers to the first lambda parameter and
not to the surrounding class or interface. Any lambda call outside a class
has to use the ordinary syntax of arguments as represented by the example
below:

``` {.typescript}
class B {
  foo() { console.log ("foo() from B is called") }
}
class A {
  foo() { console.log ("foo() from A is called") }
  bar() {
      let lambda1 = (this: B): void => { this.foo() } // local lambda
      new B().lambda1()
  }
  lambda2 = (this: B): void => { this.foo() } // class field lambda
}
new A().bar() // Output is 'foo() from B is called'
new A().lambda2 (new B) // Argument is to be provided in its usual place

interface I {
   lambda: (this: B) => void // Property of the function type
}
function foo (i: I) {
   i.lambda(new B) // Argument is to be provided in its usual place
}
```
:::

::: {.index}
lambda expression with receiver
class
interface
this keyword
lambda body
lambda parameter
surrounding class
surrounding interface
syntax
argument
function type
:::

| 

## Trailing Lambdas {#Trailing Lambdas}

The *trailing lambda* is a special form of notation for function
or method call when the last parameter of a function or a method is of
function type, and the argument is passed as a lambda using the
`Block`{.interpreted-text role="ref"} notation. The *trailing lambda* syntactically looks as follows:

``` {.abnf}
trailingLambda:
    'async'? block
    ;
```

::: {.index}
trailing lambda
notation
function call
method call
parameter
function type
method
parameter
lambda
block notation
:::

The modifier `async` is used optionally to mark `Async Lambdas`{.interpreted-text role="ref"}.

The use of a trailing lambda is represented in the example below:

``` {.typescript}
class A {
    foo (f: ()=>void) { ... }
}

let a = new A()
a.foo() { console.log ("method lambda argument is activated") }
// method foo receives last argument as the trailing lambda
```

Currently, no parameter can be specified for the type of a trailing lambda,
except a receiver parameter (see `Lambda Expressions with Receiver`{.interpreted-text role="ref"}).
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

A block immediately after a call is always handled as *trailing lambda*.
A `compile-time error`{.interpreted-text role="index"} occurs if the last parameter of the called entity
is not of a function type.

The semicolon `';'` separator can be used between a call and a block to
indicate that the block does not define a *trailing lambda*. When calling an
entity with the last optional parameter (see `Optional Parameters`{.interpreted-text role="ref"}), it
means that the call must use the default value of the parameter.

::: {.index}
trailing lambda
syntax
parameter
receiver parameter
optional parameter
lambda expression with receiver
block
function type
lambda
semicolon
separator
default value
call
:::

``` {.typescript}
function foo (f: ()=>void) { ... }

foo() { console.log ("trailing lambda") }
// 'foo' receives last argument as the trailing lambda

function bar(f?: ()=>void) { ... }

bar() { console.log ("trailing lambda") }
// function 'bar' receives last argument as the trailing lambda,
bar(); { console.log ("that is the block code") }
// function 'bar' is called with parameter 'f' set to 'undefined'

function goo(n: number) { ... }

goo() { console.log("aa") } // Compile-time error as goo() requires an argument
goo(); { console.log("aa") } // Compile-time error as goo() requires an argument
```

If there are optional parameters in front of an optional function type parameter,
then calling such a function or method can skip optional arguments and keep the
trailing lambda only. This implies that the value of all skipped arguments is
`undefined`.

``` {.typescript}
function foo (p1?: number, p2?: string, f?: ()=>string) {
    console.log (p1, p2, f?.())
}

foo()                           // undefined undefined undefined
foo() { return "lambda" }       // undefined undefined lambda
foo(1) { return "lambda" }      // 1 undefined lambda
foo(1, "a") { return "lambda" } // 1 a lambda
```

::: {.index}
optional parameter
optional argument
trailing lambda
argument
operational function
function
function type
parameter
method
function call
method call
string
lambda
:::

| 

## Accessor Declarations {#Accessor Declarations}

Accessor is either a top-level declaration (see
`Top-level Declarations`{.interpreted-text role="ref"}) or a declaration inside a namespace
(see `Namespace Declarations`{.interpreted-text role="ref"}) that declares a getter, a setter, or
functions with predefined signatures. The syntatic form of accessor usage
mimics code patterns used to work with variables, i.e., getting or setting a
variable value.

The syntax of *accessor declarations* is presented below:

``` {.abnf}
accessorDeclaration:
    'native'?
    ( 'get' identifier '(' ')' returnType? block?
    | 'set' identifier '(' requiredParameter ')' block?
    )
    ;
```

::: {.index}
accessor
accessor declaration
top-level declaration
variable
control
getter
setter
value
:::

The modifier `native` indicates that the accessor is a *native accessor*
(similarly to `Native Functions`{.interpreted-text role="ref"}).

A non-native accessor must have a body. A `compile-time error`{.interpreted-text role="index"} occurs if:

-   Native accessor has a body; or
-   Non-native accessor has no body.

A *get-accessor* (*getter*) must have an explicit return type and no parameters,
or no return type at all on condition the type can be inferred from the getter
body (see `Return Type Inference`{.interpreted-text role="ref"}).
A *set-accessor* (*setter*) must have a single parameter and no return type.

::: {.note}
::: {.title}
Note
:::

If an *accessor* is an entity of a namespace, then the same rules apply to
it when exporting and using qualified names as the rules that apply to other
namespace entities (see `Namespace Declarations`{.interpreted-text role="ref"}).
:::

A `compile-time error`{.interpreted-text role="index"} occurs if:

-   Getter or setter is used in a call expression (like a function);
-   Getter return type cannot be inferred from the getter body; or
-   *Set-accessor* (*setter*) has an optional parameter (see
    `Optional Parameters`{.interpreted-text role="ref"}):

::: {.index}
native modifier
accessor
native accessor
native function
non-native accessor
get-accessor
set-accessor
getter
setter
return type
accessor declaration
top-level declaration
parameter
type inference
:::

The typical use of an accessor to control value setting is represented in the
following example:

``` {.typescript}
let saved_age = 0

export get age(): number { return saved_age }
export set age(a: number) {
    if (a < 0) { throw new Error("wrong age") }
    saved_age = a
}
```

Which accessor (getter or setter) is to be called is defined by the place of
use:

``` {.typescript}
get name(): string { return "" }
set name(x: string) { }

console.log (name) // Getter is called
name = "some string" // Setter is called
```

::: {.index}
accessor
value setting
control
getter
setter
function
:::

However, an accessor declaration must be distinguishable from other entities,
and a `compile-time error`{.interpreted-text role="index"} occurs if:

-   Accessor name is the same as that of another entity in a scope;
-   Names of two getters or two setters in a scope are the same.

``` {.typescript}
let name = "Bob"
get name(): string { return "Alice" } // Compile-time error
```

No additional restrictions are imposed on signatures of getters and
setters that have the same name.

``` {.typescript}
set hashCode(x: string) {/*body*/}
get hashCode(): long {/*body*/} // OK

hashCode = "some string"
const l: long = hashCode
```

::: {.index}
accessor declaration
accessor
entity
scope
getter
setter
name
restriction
signature
:::

The use of getters and setters looks identical to the use of variables.
A `compile-time error`{.interpreted-text role="index"} occurs if:

-   Getter is used in the position of a *left-hand-side expression* in an
    `Assignment`{.interpreted-text role="ref"};
-   Setter is used to get a value.

``` {.typescript}
get magicNumber(): number { return 42 }
set randomSeed(a: number) {}

console.log(magicNumber) // OK, getter is used
magicNumber = 15 // Compile-time error, setter is not defined

randomSeed = 42 // OK, setter is used
console.log(randomSeed) // Compile-time error, getter is not defined
```

::: {.index}
getter
setter
variable
expression
assignment
value
:::

Accessors can be declared at all places where `Top-Level Declarations`{.interpreted-text role="ref"}
including namespaces can be used:

``` {.typescript}
namespace N {
    let saved_age = 0

    export get age(): number { return saved_age }
    export set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        saved_age = a
    }
}

N.age = 18
console.log(N.age)
```

::: {.index}
accessor
declaration
top-level declaration
:::

| 

## Pattern Matching {#Pattern Matching}

*Pattern Matching* is a set of powerful features supported by most modern
programming languages. *Pattern matching* generally allows checking a value
against a pattern, and executing a corresponding action after a match is
successful. A successful match can also deconstruct a value into its constituent
parts.

The current version of supports a simple *pattern matching* feature
called *destructuring assignment*. Other features are to be added in the
forthcoming revisions of this specification.

| 

### Destructuring Assignment {#Destructuring Assignment}

*Destructuring assignment* allows extracting values from arrays or tuples, and
assigning them to distinct variables.

The syntax of a *destructuring assignment* is as follows:

``` {.abnf}
destructuringAssignment:
    '[' lhsExpression? (',' lhsExpression?)* ']' '=' rhsExpression
    ;
```

The definitions of `lhsExpression` and `rhsExpression` are provided in
`Assignment`{.interpreted-text role="ref"}.

`rhsExpression` must be of array type or tuple type. Otherwise, a
`compile-time error`{.interpreted-text role="index"} occurs.

*Destructuring assignment* can be considered a compact form of a set of
assignments (see `Simple Assignment Operator`{.interpreted-text role="ref"}).
Items in a *left-hand-side* expression (whether `lhsExpression` or none)
correspond to the sequence of elements in `rhsExpression` staring from the
first element (i.e., the element with the index `0`) of an array or a tuple:

``` {.typescript}
function foo(x: string[]) {
    let a = ""
    let b = "";
    [a, , b] = x
    // this line works the same as the previous line:
    a = x[0]; b = x[2]
}
```

In the example above, `a` takes the value `x[0]`, and `b` takes the
value `x[2]`. If an attempt is made to have an array element with an index
greater than or equal to the length of the array, then *RangeError* is thrown
in exactly the same way as in `Array Indexing Expression`{.interpreted-text role="ref"}.

If `lhsExpression` is missing, then the corresponding element of an array or
of a tuple is ignored.

A `compile-time error`{.interpreted-text role="index"} occurs if:

-   Type of an array element or of a tuple element is not assignable to the type
    of a corresponding `lhsExpression` (see `Assignability`{.interpreted-text role="ref"});
-   `rhsExpression` is of a tuple type, and `lhsExpression` corresponds to
    the missing tuple element.

Valid and erroneous destructuring is represented in the following example:

``` {.typescript}
function foo(x: [string, number, string]) {
    let a: string
    let b: number
    [a] = x; // OK
    [, b, a] = x; // OK
    [, b, a,,,,] = x; // OK
    [b] = x; // Compile-type error, x[0] is not assignable to 'b'
    [, b] = x; // OK
    [,,,b] = x; // Compile-time error, there is no element for variable 'b'
}
```

```{=pdf}
PageBreak
```
