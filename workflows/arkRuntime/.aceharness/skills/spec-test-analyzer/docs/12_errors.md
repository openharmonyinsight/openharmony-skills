# Error Handling {#Error Handling}

is designed to provide first-class support in responding to, and
recovering from different error situations in a program. Normal program
execution can be interrupted by the occurrence of situations of two kinds:

-   Runtime errors (e.g., null pointer dereferencing, array bounds
    checking, or division by zero);
-   Operation completion failures (e.g., the task of reading
    and processing data from a file on disk can fail if the file does
    not exist on a specified path, read permissions are not available,
    or else).

The term *error* in this Specification denotes all kinds of error situations.

::: {.index}
execution
null pointer dereferencing
runtime error
array bounds checking
completion
normal execution
normal completion
completion failure
path
read permission
error
:::

| 

## Errors {#Errors}

*Error* is the base class of all error situations. Defining a new
error class is normally not required because essential error classes for
various cases (e.g., `RangeError`) are defined in the
standard library (see `Standard Library`{.interpreted-text role="ref"}).

However, a developer can handle a new error situation by using `Error`
class itself, or by a subclass of `Error`. An example of error
handling is provided below:

::: {.index}
error
base class
class
error handling
derived class
standard library
:::

``` {.typescript}
class UnknownError extends Error { // user-defined error class 
   error: Error
   constructor (error: Error) {
      super()
      this.error = error
   }
 }

 function get_array_element<T>(array: T[], index: int): T|undefined {
     try {
       return array[index] // RangeError if index < 0 or index >= array.length
     }
     catch (error) {
       if (error instanceof RangeError) // invalid index detected
          return undefined
       throw new UnknownError (error) // unknown error occurred
     }
 }

 let arr = [1, 2, 3]
 let val = get_array_element(arr, -3) // RangeError: index -3 < 0

console.log(val) // Output: undefined
```

In most cases, errors are raised by the runtime system, or by the
standard library (see `Standard Library`{.interpreted-text role="ref"}) code.

New error situations can be created and raised by `throw` statements (see
`Throw Statements`{.interpreted-text role="ref"}) .

Errors are handled by using `try` statements (see `Try Statements`{.interpreted-text role="ref"}).

::: {.note}
::: {.title}
Note
:::

Some errors cannot be recovered.
:::

::: {.index}
runtime system
standard library
generic class
subclass
error situation
throw statement
error
try statement
:::

``` {.typescript}
function handleAll(
  actions : () => void,
  handling_actions : () => void)
{
  try {
    actions()
  }
  catch (x) { // Type of x is Error
      handling_actions()
  }
}
```

```{=pdf}
PageBreak
```
