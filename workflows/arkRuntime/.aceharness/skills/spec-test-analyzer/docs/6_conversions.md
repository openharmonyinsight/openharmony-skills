# Contexts and Conversions {#Contexts and Conversions}

This Chapter defines expression contexts and conversions that can be applied
to expressions in different contexts.

Contexts can be of the following kinds:

-   `Assignment-like Contexts`{.interpreted-text role="ref"};
-   `String Operator Contexts`{.interpreted-text role="ref"} with `string` concatenation (operator `'+'`);
-   `Numeric Operator Contexts`{.interpreted-text role="ref"} with all numeric operators (`'+'`, `'-'`, etc.).

::: {.index}
context
conversion
expression
string
assignment-like context
numeric operator
concatenation
:::

| 

## Assignment-like Contexts {#Assignment-like Contexts}

*Assignment-like contexts* include the following:

-   *Declaration contexts* that allow setting an initial value to a variable
    (see `Variable Declarations`{.interpreted-text role="ref"}), a constant (see
    `Constant Declarations`{.interpreted-text role="ref"}), or a field (see `Field Declarations`{.interpreted-text role="ref"})
    with an explicit type annotation;
-   *Assignment contexts* that allow assigning (see `Assignment`{.interpreted-text role="ref"}) an
    expression value to a variable;
-   *Call contexts* that allow assigning an argument value to a corresponding
    formal parameter of a function, method, constructor or lambda call (see
    `Function Call Expression`{.interpreted-text role="ref"}, `Method Call Expression`{.interpreted-text role="ref"},
    `Explicit Constructor Call`{.interpreted-text role="ref"}, and `New Expressions`{.interpreted-text role="ref"});
-   *Return contexts* (see `return Statements`{.interpreted-text role="ref"}) the allow specifying
    a resultant value of a function, method or lambda call;
-   *Composite literal contexts* that allow setting an expression value to an
    array element (see `Array Literal Type Inference from Context`{.interpreted-text role="ref"}),
    a class, or an interface field (see `Object Literal`{.interpreted-text role="ref"});

::: {.index}
assignment
assignment-like context
assignment context
call context
variable declaration
constant declaration
constant
field
field declaration
assignment
assignment context
expression value
expression
conversion
function call
constructor call
lambda call
method call
call context
type
type inference
interface field
formal parameter
array literal
object literal
initial value
value
variable
constant
composite literal context
function
method
constructor
expression value
array element
:::

The examples are presented below:

``` {.typescript}
// declaration contexts:
let x: number = 1
const str: string = "done"
class C {
  f: string = "aa"
}

// assignment contexts:
x = str.length
new C().f = "bb"
function foo<T1, T2> (p1: T1, p2: T2) {
  let t1: T1 = p1
  let t2: T2 = p2
}

// call contexts:
function foo(s: string) {}
foo("hello")

// composite literal contexts:
let a: number[] = [str.length, 11]
```

In all these cases, the expression type must be *assignable* to the *target
type* (see `Assignability`{.interpreted-text role="ref"}).
*Assignability* allows using of one of `Implicit Conversions`{.interpreted-text role="ref"}.
If there is no applicable conversion, then a `compile-time error`{.interpreted-text role="index"}
occurs.

::: {.index}
expression type
expression
target type
assignability
conversion
:::

| 

## String Operator Contexts {#String Operator Contexts}

*String context* applies only to a non-*string* operand of the binary operator
`'+'` if the other operand is `string`.

*String conversion* for a non-`string` operand is evaluated as follows:

-   An operand of an integer type (see `Integer Types and Operations`{.interpreted-text role="ref"})
    is converted to type `string` with a value that represents the operand in
    the decimal form.

-   An operand of a floating-point type (see `Floating-Point Types and Operations`{.interpreted-text role="ref"})
    is converted to type `string` with a value that represents the operand in
    the decimal form without the loss of information.

-   An operand of type `boolean` is converted to type `string` with the
    values `true` or `false`.

-   An operand of enumeration type (see `Enumerations`{.interpreted-text role="ref"}) is converted to
    type `string` with the value of the corresponding enumeration member
    if values of enumeration are of type `string`.

-   The operand of a nullish type that has a nullish value is converted as
    follows:

    > -   Operand `null` is converted to string `null`.
    > -   Operand `undefined` is converted to string `undefined`.

-   An operand of a reference type or an `enum` type with non-*string* values
    is converted by applying the method call `toString()`.

If there is no applicable conversion, then a `compile-time error`{.interpreted-text role="index"} occurs.

The target type in this context is always `string`:

::: {.index}
string context
non-string operand
binary operator
string operand
string conversion
conversion
reference type
integer type
operand
floating-point type
loss of information
enumeration type
string type
nullish type
boolean
decimal
string conversion
operand null
operator undefined
method call
context
:::

``` {.typescript}
console.log("" + null) // prints "null"
console.log("value is " + 123) // prints "value is 123"
console.log("BigInt is " + 123n) // prints "BigInt is 123"
console.log(15 + " steps") // prints "15 steps"
let x: string | null | undefined = null
console.log("string is " + x) // prints "string is null"
x = undefined
console.log("string is " + x) // prints "string is undefined"
```

| 

## Numeric Operator Contexts {#Numeric Operator Contexts}

Numeric contexts apply to the operands of an arithmetic operator.
Numeric contexts use numeric types conversions
(see `Widening Numeric Conversions`{.interpreted-text role="ref"}), and ensure that each argument
expression can be converted to target type `T` while the arithmetic
operation for the values of type `T` is being defined.

An operand of enumeration type (see `Enumerations`{.interpreted-text role="ref"}) can be used in
a numeric context if enumeration
base type is a numeric type. The type of this operand is assumed to be the same
as the enumeration base type.

::: {.index}
numeric context
arithmetic operator
predefined type
numeric type
conversion
argument expression
target type
string conversion
string context
type int
:::

Numeric contexts take the following forms:

-   `Unary Expressions`{.interpreted-text role="ref"};
-   `Exponentiation expression`{.interpreted-text role="ref"};
-   `Multiplicative Expressions`{.interpreted-text role="ref"};
-   `Additive Expressions`{.interpreted-text role="ref"};
-   `Shift Expressions`{.interpreted-text role="ref"};
-   `Relational Expressions`{.interpreted-text role="ref"};
-   `Equality Expressions`{.interpreted-text role="ref"};
-   `Bitwise and Logical Expressions`{.interpreted-text role="ref"};
-   `Conditional-And Expression`{.interpreted-text role="ref"};
-   `Conditional-Or Expression`{.interpreted-text role="ref"}.

::: {.index}
numeric context
expression
unary expression
multiplicative expression
additive expression
shift expression
relational expression
equality expression
bitwise expression
logical expression
conditional-and expression
conditional-or expression
:::

| 

### Numeric Conversions for Relational and Equality Operands {#Numeric Conversions for Relational and Equality Operands}

Relational and equality operators (see `Relational Expressions`{.interpreted-text role="ref"} and
`Equality Expressions`{.interpreted-text role="ref"}) allow *implicit conversion* of numeric type
operands of different sizes (see `Widening numeric conversions`{.interpreted-text role="ref"}).
Specific details of such conversions are discussed in
`Specifics of Numeric Operator Contexts`{.interpreted-text role="ref"}.

The situation for the relational operator `'<'` is represented in the example
below:

``` {.typescript}
let a: int = 1
let b: long = 0

if (b<a) { // 'a' converted to 'long' prior to comparison
   ;
}
```

::: {.index}
numeric conversion
numeric types conversion
widening numeric conversion
operand
numeric type
conversion
:::

| 

### `char` Conversions for Relational and Equality Operands {#char Conversions for Relational and Equality Operands}

Relational and equality operators (see `Relational Expressions`{.interpreted-text role="ref"} and
`Equality Expressions`{.interpreted-text role="ref"}) allow *implicit conversion* of type `char` operand
if other operand is of a numeric type.

A `char` type operand is widened to one of the following:

-   Type `int` if the other operand is of types `byte`, `char` or `int`; or
-   Type of the other operand.

The situation for the relational operator `'<'` is represented in the example
below:

``` {.typescript}
function foo(c: char, b: byte, i: int, l: long, d: double) {
    c < b // 'c' and 'b' are converted to 'int' prior to comparison
    c < i // 'c' is converted to 'int' prior to comparison
    c < l // 'c' is converted to 'long' prior to comparison
    c < d // 'c' is converted to 'double' prior to comparison
}
```

::: {.index}
char conversion
widening numeric conversion
operand
numeric type
conversion
:::

| 

## Implicit Conversions {#Implicit Conversions}

This section describes all implicit conversions that are allowed. Each
conversion is allowed in a particular context (e.g., if an expression
that initializes a local variable is subject to `Assignment-like Contexts`{.interpreted-text role="ref"},
then the rules of this context define what specific conversion is implicitly
chosen for the expression).

::: {.index}
identity conversion
conversion
context
local variable
assignment
assignment-like context
conversion
expression
variable
:::

| 

### Widening Numeric Conversions {#Widening Numeric Conversions}

*Widening numeric conversion* converts a value of a numeric type
(see `Numeric Types`{.interpreted-text role="ref"}) to one of the following:

-   Larger numeric type; or
-   Union type (see `Widening Numeric to a Union Type`{.interpreted-text role="ref"}).

This conversion never causes a `runtime error`{.interpreted-text role="index"}.

``` {.typescript}
function foo(l: long) {}
function bar(d: double) {}

let b: byte = 1
let s: short = 2
let i: int = 3

foo(b) // byte to long conversion
foo(s) // short to long conversion
foo(i) // int to long conversion

let f: float = 3.14f

bar(i) // int to double conversion
bar(f) // float to double conversion
```

::: {.index}
widening
numeric conversion
conversion
numeric type
value
byte
short
int
long
float
integer type
:::

All *widening numeric conversions* are presented in the following table:

  -----------------------------------------------------------------------
  From Type          To Type
  ------------------ ----------------------------------------------------
  `byte`             `short`, `int`, `long`, `float`, `double`

  `short`            `int`, `long`, `float`, `double`

  `int`              `long`, `float`, or `double`

  `long`             `float` or `double`

  `float`            `double`
  -----------------------------------------------------------------------

The above conversions cause no loss of information about the overall magnitude
of a numeric value. Some least significant bits of the value can be lost only
in conversions from an integer type to a floating-point type if the IEEE 754
*round-to-nearest* mode is used correctly. The resultant floating-point value
is properly rounded to the integer value.

::: {.index}
conversion
numeric value
floating-point type
integer type
conversion
round-to-nearest mode
runtime error
IEEE 754
widening
numeric conversion
rounding
:::

| 

### Widening Numeric to a Union Type {#Widening Numeric to a Union Type}

A numeric value `v` is converted to `U`~i~ of union type
(`U`~1~ `| ... | U`~n~), if `U`~i~
is a single numeric type in the union that is larger than the value type.
Otherwise, a `compile-time error`{.interpreted-text role="index"} occurs.

::: {.note}
::: {.title}
Note
:::

*Before* widening to a union type, the following semantic rules are applied
in most cases:

-   `Type Inference for Constant Expressions`{.interpreted-text role="ref"} if `v` is
    a numeric literal; or
-   `Subtyping for Union Types`{.interpreted-text role="ref"} if `U`~i~ is equal
    to the value type.

If one of these rules applies successfully, then no widening conversion is
required.
:::

All cases are represented in the following example:

``` {.typescript}
let s: short = 1
let i: int = 2

let u: byte | int = 256 // OK, type inference for numeric literal
console.log(u instanceof int) // output: true

u = i // OK, subtyping
console.log(u instanceof int) // output: true

u = s // OK, widening to union type, short => int conversion
console.log(u instanceof int) // output: true
```

| 

### Enumeration to Numeric Type Conversion {#Enumeration to Numeric Type Conversion}

If *enumeration base type* is a numeric type, then a value of the enumeration
type is converted to one of the following:

-   Numeric type equal to or larger than the *enumeration base type*; or
-   Union type considering the *enumeration base type* (see
    `Widening Numeric to a Union Type`{.interpreted-text role="ref"}).

This conversion never causes a `runtime error`{.interpreted-text role="index"}.

``` {.typescript}
enum IntegerEnum {a, b, c}
let int_enum: IntegerEnum = IntegerEnum.b
let int_value: int = int_enum // int_value will get the value 1
let number_value: number = int_enum
   /* number_value will get the value 1 as a result of conversion
      to a larger numeric type */

enum DoubleEnum: double {a = 1.0, b = 2.0, c = 3.141592653589}
let d_enum: DoubleEnum = DoubleEnum.a
let d_value: double = d_enum // d_value will get the value 1.0
```

::: {.index}
enumeration type
numeric base type
base type
conversion
integer type
constant
type int
:::

| 

### Enumeration to `string` Type Conversion {#Enumeration to string Type Conversion}

A value of *enumeration* with `string` base type is converted to type
`string` or to a union type (see `Union Types`{.interpreted-text role="ref"}) that contains type `string`.
This conversion never causes a `runtime error`{.interpreted-text role="index"}.

``` {.typescript}
enum StringEnum {a = "a", b = "b", c = "c"}
let s_enum: StringEnum = StringEnum.a
let s: string = s_enum // 's' will get the value of "a"

let u: string | number = s_enum // 'u' will get the value of "a"
```

::: {.index}
enumeration type
string type
conversion
constant
runtime error
:::

| 

## Numeric Casting Conversions {#Numeric Casting Conversions}

A *numeric casting conversion* occurs if the *target type* and the expression
type are both `numeric`.
The context for a *numeric casting conversion* is where conversion methods
are used as defined in the standard library (see `Standard Library`{.interpreted-text role="ref"}).

The explicit use of methods for *numeric cast conversions* is represented in
the following example:

``` {.typescript}
function process_int(an_int: int) { /* ... */ }

let pi = 3.14
process_int(pi.toInt())
```

A numeric casting conversion never causes a `runtime error`{.interpreted-text role="index"}.

Numeric casting conversion of an operand of type `double` to target type
`float` is performed in compliance with the IEEE 754 rounding rules. This
conversion can lose precision or range, resulting in the following:

-   Float zero from a nonzero double; and
-   Float infinity from a finite double.

Double `NaN` is converted to float `NaN`.

Double infinity is converted to the same-signed floating-point infinity.

::: {.index}
numeric casting conversion
target type
expression type
numeric type
double type
float type
compliance
rounding rule
float zero
nonzero double
float infinity
infinity double
floating-point infinity
double infinity
double NaN
Nan
float NaN
IEEE 754
rounding rule
conversion
infinity
:::

A numeric conversion of a floating-point type operand to target types `long`
or `int` is performed by the following rules:

-   If the operand is `NaN`, then the result is 0 (zero).
-   If the operand is positive infinity, or if the operand is too large for the
    target type, then the result is the largest representable value of the target
    type.
-   If the operand is negative infinity, or if the operand is too small for
    the target type, then the result is the smallest representable value of
    the target type.
-   Otherwise, the result is the value that rounds toward zero by using IEEE 754
    *round-toward-zero* mode.

A numeric casting conversion of a floating-point type operand to types
`byte` or `short` is performed in two steps as follows:

-   The casting conversion to `int` is performed first (see above);
-   Then, the `int` operand is cast to the target type.

::: {.index}
target type
floating-point operand
floating-point type
long type
int type
NaN
numeric conversion
byte
short
positive infinity
negative infinity
casting conversion
runtime error
operand
compliance
IEEE 754
NaN
floating-point type
floating-point infinity
rounding rules
round-toward-zero
:::

A numeric casting conversion from an integer type to a smaller integer
type `I` discards all bits except the *N* lowest ones, where *N* is
the number of bits used to represent type `I`. This conversion can lose the
information on the magnitude of the numeric value. The sign of the resulting
value can differ from that of the original value.

::: {.index}
IEEE 754
floating-point type
numeric casting conversion
operand
conversion
positive infinity
target type
negative infinity
casting conversion
integer type
conversion
rounding rule
numeric value
:::

| 

```{=pdf}
PageBreak
```
