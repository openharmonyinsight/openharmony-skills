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

.. _Error Handling:

Error Handling
##############

.. meta:
    frontend_status: Done

|LANG| is designed to provide first-class support in responding to, and
recovering from different error situations in a program. Normal program
execution can be interrupted by the occurrence of situations of two kinds:

-  Runtime errors (e.g., null pointer dereferencing, array bounds
   checking, or division by zero);

-  Operation completion failures (e.g., the task of reading
   and processing data from a file on disk can fail if the file does
   not exist on a specified path, read permissions are not available,
   or else).

The term *error* in this Specification denotes all kinds of error situations.

.. index::
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

|

.. _Errors:

Errors
******

.. meta:
    frontend_status: Done

*Error* is the base class of all error situations. Defining a new
error class is normally not required because essential error classes for
various cases (e.g., ``RangeError``) are defined in the
standard library (see :ref:`Standard Library`).

However, a developer can handle a new error situation by using ``Error``
class itself, or by a subclass of ``Error``. An example of error
handling is provided below:

.. index::
   error
   base class
   class
   error handling
   derived class
   standard library


.. code-block:: typescript
   :linenos:

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


In most cases, errors are raised by the |LANG| runtime system, or by the
standard library (see :ref:`Standard Library`) code.

New error situations can be created and raised by ``throw`` statements (see
:ref:`Throw Statements`) .

Errors are handled by using ``try`` statements (see :ref:`Try Statements`).

.. note::
   Some errors cannot be recovered.

.. index::
   runtime system
   standard library
   generic class
   subclass
   error situation
   throw statement
   error
   try statement

.. code-block:: typescript
   :linenos:

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

.. raw:: pdf

   PageBreak
