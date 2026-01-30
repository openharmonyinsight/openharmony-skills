# Header & Scope Management

## Header Files
*   **Header Guards:** Use standard `#ifndef ... #define` guards.
    *   **Strict Rule:** Do NOT use `#pragma once`.
*   **Includes:** Use `#include` to ensure dependency visibility.
    *   *Note:* OpenHarmony prefers `#include` over forward declarations to avoid hidden dependencies.

## Namespaces & Scope
*   **Encapsulation:** Use namespaces or `static` to encapsulate internal implementation details.
*   **Global Pollution:** **Never** use `using namespace` in header files.
