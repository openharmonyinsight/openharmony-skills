# ArkTS Lexical Structure Reference

## Identifiers

```typescript
myVariable
_privateVar
$special
\u0041nicode  // Starts with Unicode letter
```

**Rules:**
- Must start with `$`, `_`, or Unicode letter
- Can contain letters, digits, `$`, `_`, ZWJ, ZWNJ
- Cannot be a keyword

---

## Keywords

### Hard Keywords (cannot be identifiers)

```
abstract, as, async, await, break, case, catch, class, const, constructor
continue, default, do, else, enum, extends, final, false, for, function
if, implements, import, in, instanceof, interface, let, new, null
override, private, protected, public, return, static, super, switch
this, throw, true, try, typeof, undefined, void, while
```

### Type Keywords

```
Any, bigint, BigInt, boolean, Boolean, byte, Byte, char, Char
double, Double, float, Float, int, Int, long, Long, number, Number
Object, object, short, Short, string, String, void
```

### Soft Keywords (contextual)

```
catch, declare, finally, from, get, keyof, namespace, of, out
readonly, set, type
```

---

## Literals

### Numeric Literals

```typescript
42             // Decimal int
0xFF           // Hexadecimal
0o755          // Octal
0b1010         // Binary
1_000_000      // Underscore separator
3.14           // Double
3.14f          // Float
1.5e10         // Exponent
123n           // BigInt
```

### String Literals

```typescript
"double quotes"
'single quotes'
`multiline
string`
```

### Escape Sequences

```
\"  Double quote
\'  Single quote
\\  Backslash
\n  Newline
\r  Carriage return
\t  Tab
\b  Backspace
\f  Form feed
\v  Vertical tab
\0  Null character
\xHH Hex escape
\uHHHH Unicode escape
\u{HHHHHH} Extended Unicode
```

### Boolean Literals

```typescript
true
false
```

### Null/Undefined Literals

```typescript
null
undefined
```

---

## Comments

```typescript
// Single-line comment

/*
  Multi-line comment
*/

/**
  Documentation comment
*/
```

---

## Semicolons

Semicolons are optional but recommended:

```typescript
let x: number = 1    // Semicolon inferred
let y: number = 2;   // Explicit semicolon

// Need semicolon to avoid ambiguity
a = b + c
(d + e).print()     // Without semicolon, looks like function call
```
