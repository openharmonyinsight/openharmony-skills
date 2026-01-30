# Secure Coding & Error Handling

## Input Validation (CRITICAL)
*   **Strict Validation:** Strictly validate **ALL** data from external sources (network, user, files).
*   **Checks:** Verify lengths, ranges, and types **before** using them as array indices, loop conditions, or allocation sizes.

## Integer Safety
*   **Overflow/Underflow:** Prevent integer overflow/underflow (especially with `size_t` subtractions).
*   **Division:** explicit checks to avoid divide-by-zero errors.
*   **Bitwise Operations:** ONLY perform on **unsigned** integers.

## Memory Management
*   **Allocation:** Validate memory size before allocation (avoid 0 or excessive sizes).
*   **Null Checks:** Check for `nullptr` after allocation if not using throwing `new`.
*   **Dangling Pointers:** Set pointers to `nullptr` **immediately** after `delete`/`free`.
*   **Pairing:** Ensure `new`/`delete` and `new[]`/`delete[]` are paired correctly.

## String Safety
*   **Null Termination:** Ensure C-strings are null-terminated.
*   **Pointer Lifetime:** Do not hold onto `std::string::c_str()` pointers longer than the string object's life.
*   **Sensitive Data:** Do not store sensitive info (passwords) in `std::string` (memory cannot be securely cleared).

## System & Process
*   **Command Injection:** Avoid `system()` or `popen()` with external data. Use safer API alternatives.
*   **Format Strings:** Use format string constants (e.g., `printf("%s", str)` not `printf(str)`).

## Error Handling
*   **Exceptions:** Throw objects by value, catch by reference.
*   **Destructors:** Never throw exceptions from a destructor.
