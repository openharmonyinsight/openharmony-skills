# Class & Function Design

## Class Design
*   **Initialization:** Explicitly initialize all member variables (in declaration or constructor list).
*   **Constructors:**
    *   Use `explicit` for single-argument constructors to prevent implicit conversion.
    *   **Rule of All or None:** If you define one copy/move constructor or assignment operator, define (or delete) ALL of them.
    *   **No Virtual Calls:** Never call virtual functions in constructors or destructors.
*   **Inheritance:**
    *   Base class destructors must be `virtual` if intended for polymorphic use.
    *   Use `override` for derived virtual functions.
    *   Do not redefine inherited non-virtual functions.

## Function Design
*   **Size:** Functions should be short (< 50 lines). Inline functions should be tiny (< 10 lines).
*   **Parameters:**
    *   Max 5 parameters per function.
    *   Use references (`const T&`) instead of pointers for object parameters where possible.
    *   **Strong typing:** Avoid `void*`.

## Modern C++ Best Practices
*   Use `nullptr` instead of `NULL`.
*   Use `const` and `constexpr` for constants instead of `#define`.
*   Use `static_cast` instead of C-style casts. Avoid `reinterpret_cast` and `const_cast`.
