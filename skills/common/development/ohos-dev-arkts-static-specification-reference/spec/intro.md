Introduction
############

This document presents complete information on the new common-purpose,
multi-paradigm programming language called ArkTS.

Overall Description
*******************

The ArkTS language combines and supports features that have already proven
helpful and powerful in many well-known programming languages.

ArkTS supports imperative, object-oriented, functional, and generic
programming paradigms, and combines them safely and consistently.

At the same time, ArkTS does not support features that allow software
developers to write dangerous, unsafe, or inefficient code. In particular,
the language uses the strong static typing principle. Object types are
determined by their declarations, and no dynamic type change is allowed.
The semantic correctness is checked at compile time.

ArkTS is designed as a part of the modern language manifold. To provide an
efficient and safely executable code, the language takes flexibility and
power from |TS| and its predecessor |JS|, and the static
typing principle from Java and Kotlin. Overall design keeps the ArkTS
syntax style similar to that of those languages, and some of its important
constructs are almost identical to theirs on purpose.

In other words, ArkTS has a significant *common subset* of features with
|TS|, |JS|, Java, and Kotlin. Consequently, the ArkTS style and constructs
are no puzzle for the |TS| and Java users who can intuitively sense the
Lexical and Syntactic Notation
******************************

This section introduces the notation known as *context-free grammar*. The
notation is used throughout this specification to define the lexical and
syntactic structure of a program.

The ArkTS lexical notation defines a set of rules, or productions that specify
the structure of the elementary language  parts called *tokens*. All tokens are
defined in :ref:`Lexical Elements`. The set of tokens (identifiers, keywords,
numbers/numeric literals, operator signs, delimiters), special characters
(white spaces and line separators), and comments comprises the language's
*alphabet*.

The tokens defined by the lexical grammar are terminal symbols of syntactic
notation. Syntactic notation defines a set of productions starting from the
goal symbol *moduleDeclaration* (see :ref:`Module Declarations`). It is a
sentence that consists of a single distinguished nonterminal, and describes how
sequences of tokens can form syntactically correct programs.

Lexical and syntactic grammars are defined as a range of productions, and each
production is comprised of the following:

- Abstract symbol (*nonterminal*) as its left-hand side,
- Sequence of one or more *nonterminal* and *terminal* symbols as its
Terms and Definitions
*********************

This section contains the alphabetical list of important terms found in the
Specification, and their ArkTS-specific definitions. Such definitions are
not generic and can differ significantly from the definitions of the same terms
as used in other languages, application areas, or industries.

.. glossary::
   :sorted:

   compile-time error
     -- a text message displayed by the compiler if an error is identified
     in a program code that prevents the code to be generated.

   compile-time warning
     -- a text message displayed by the compiler if a program code is found
     to have some logical inconsistencies that require reconsidering design
     and actual coding.

   expression
     -- a formula for calculating values. The syntactic form of an expression
     is a combination of operators and parentheses, where the parentheses are
     used to change the order of calculation. The default order of calculation
     is determined by operator preferences.
