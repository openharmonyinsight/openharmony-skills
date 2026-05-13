Overview
********

Runtime specification presents complete information on the structure of the
ArkTS runtime system with the detailed description of its binary file
structure, type system and public interfaces.
Fully Qualified Name
********************

*Fully qualified name* is used to create unique identifiers for different types
and entities at runtime and in binary files. A *Fully qualified name* of an
entity is generated from its *unqualified name* by a build system, and
specific rules vary from one build system to another. However, the ArkTS
runtime expects concrete *fully qualified name* for some predefined types.
Such cases are described in
:ref:`Language Representation In Binary File <RT Language Representation In Binary File>`.
Binary File Format
******************

The ArkTS binary file format is designed with the following goals in mind:

- Compactness,
- Fast information access,
- Low memory footprint,
- Extensibility, and
- Compatibility.

**Compactness**. Many mobile applications use numerous types, methods,
and fields. The number is very large, and does not fit into a 16-bit
unsigned integer. As a result, an application developer creates several
files, and some data cannot be deduplicated.

Current binary file format must extend these limits to conform to modern
requirements. It is achieved by making all direct references in a binary
file 4 bytes long to allow 4Gb addressing.

16-bit indices are used to refer to classes, methods and fields in
bytecode and metadata for greater compactness. A file can contain multiple
indices, each covering a part of a file as described in :ref:`RegionHeader <RT RegionHeader>`.

A file format uses :ref:`TaggedValue <RT TaggedValue>` to enable compact value storage to
store only the information available and avoid zero offset to any missing
Alignment
=========

Most entities have the 4-byte alignment in order to improve the speed of
data access. All exceptions are specified explicitly in appropriate descriptions
below.

Endianness
==========

All multibyte values are little-endian as most target architectures are.

Offsets
=======

Unless specified otherwise, all offsets are calculated from the beginning
of the file.

An offset cannot contain values in the range ``[0; sizeof(Header))``,
except in certain cases specifically mentioned.

Data Types
==========

Integer Types
-------------

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Type
     - Description

   * - ``uint8_t``
     - 8-bit unsigned integer value

   * - ``uint16_t``
     - 16-bit unsigned integer value

   * - ``uint32_t``
     - 32-bit little-endian unsigned integer value

   * - ``uleb128``
     - Unsigned integer value in leb128 encoding

   * - ``sleb128``
     - Signed integer value in leb128 encoding

String Format
-------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``utf16_length``
     - ``uleb128``
     -  ``len << 1 | is_ascii`` where ``len`` is the length of the string in 
        UTF-16 code units

   * - ``data``
     - ``uint8_t[]``
     -  ``\0`` terminated character sequence in MUTF-8 (Modified UTF-8)
        encoding
TaggedValue Format
------------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``tag_value``
     - ``uint8_t``
     -  Tag that determines the encoding of ``data``.

   * - ``data``
     - ``uint8_t[]``
     -  Optional payload

Source Language
---------------

Source language can be specified for classes and methods. Default language for
methods is that of the class. A file can be emitted from the sources written
in the following languages:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Source
     - Encoding
   * - ``Ark Assembly``
     - ``0x01``

Values ``0x00``, ``0x02`` - ``0x0f`` are reserved.

File Layout
===========

A binary file begins with the :ref:`Header <RT Header>` located at offset ``0``.
Any other data can be reached from the header.

Header Format
-------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 25 15 60
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``magic``
     - ``uint8_t[8]``
     - Magic string - 'PANDA\0\0\0'.

   * - ``checksum``
     - ``uint8_t[4]``
     - ``adler32`` checksum of the file except magic and checksum fields.

   * - ``version``
     - ``uint8_t[4]``
ClassIndex Format
-----------------

``ClassIndex`` entities are designed to allow to quickly find a type definition
by name at runtime. It is organized as an array of offsets to a
:ref:`Class <RT Class>` or to a :ref:`ForeignClass <RT ForeignClass>`.
All offsets are sorted by the corresponding class names.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``offsets``
     - ``uint32_t[]``
     - Sorted array of offsets to a :ref:`Class <RT Class>` or to a
       :ref:`ForeignClass <RT ForeignClass>`.
LineNumberProgramIndex Format
-----------------------------

``LineNumberProgramIndex`` entities are designed to allow using more compact
references to :ref:`Line Number Program <RT Line Number Program>`. It is organized
as an array of offsets to a :ref:`Line Number Program <RT Line Number Program>`

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``offsets``
     - ``uint32_t[]``
     - Array of offsets to a :ref:`Line Number Program <RT Line Number Program>`.

LiteralArrayIndex Format
------------------------

``LiteralArrayIndex`` entities are designed to allow to find a
:ref:`LiteralArray <RT LiteralArray>` definition by index at runtime.
It is organized as an array of offsets to a :ref:`LiteralArray <RT LiteralArray>`.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``offsets``
     - ``uint32_t[]``
     - Sorted array of offsets to a :ref:`LiteralArray <RT LiteralArray>`.

RegionIndex Format
------------------

``RegionIndex`` entities are designed to allow finding the index
that covers a specified offset in the file at runtime. It is organized as
sorted array of a :ref:`RegionHeader <RT RegionHeader>`.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``region_headers``
     - ``RegionHeader[]``
     - File regions sorted by the start offset of the region. Each element
       must have the :ref:`RegionHeader <RT RegionHeader>` format.

**Constraint**: Two different regions must not overlap with each other.
RegionHeader Format
-------------------

To address file entities by using 16-bit indices, a binary file is split
into regions. The information on each region is stored in the ``RegionHeader`` format.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``start_off``
     - ``uint32_t``
     - Start offset of the region.

   * - ``end_off``
     - ``uint32_t``
     - End offset of the region.
ClassRegionIndex Format
-----------------------

``ClassRegionIndex`` entities are designed to allow finding a type
definition by index at runtime. It is organized as an array of offsets to a
:ref:`Class <RT Class>` or to a :ref:`ForeignClass <RT ForeignClass>`.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``types``
     - ``uint32_t[]``
     - Offsets to a :ref:`Class <RT Class>` or to a :ref:`ForeignClass <RT ForeignClass>`.

MethodRegionIndex Format
------------------------

``MethodRegionIndex`` entities are designed to allow finding a method
definition by index at runtime. It is organized as an array of offsets
to a :ref:`Method <RT Method>` or to a :ref:`ForeignMethod <RT ForeignMethod>`.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``methods``
     - ``uint32_t[]``
     - Array of offsets to a :ref:`Method <RT Method>` or to a :ref:`ForeignMethod <RT ForeignMethod>`.

FieldRegionIndex Format
-----------------------

``FieldRegionIndex`` entities are designed to allow finding a field
definition by index at runtime. It is organized as an array of offsets
to a :ref:`Field <RT Field>` or to a :ref:`ForeignField <RT ForeignField>`.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``fields``
     - ``uint32_t[]``
     - Array of offsets to a :ref:`Field <RT Field>` or to a :ref:`ForeignField <RT ForeignField>`.

ProtoRegionIndex Format
-----------------------

``ProtoRegionIndex`` entities are designed to allow finding a proto
definition by index at runtime.

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``protos``
     - ``uint32_t[]``
     - Array of offsets to a :ref:`Proto <RT Proto>`.

ExportData Format
-----------------

``ExportData`` region provides information about exported declarations,
to be able to import the binary file from another source file and resolve to its declarations at compile-time.
This information is mandatory if the binary file is distributed as a library without available sources.
The information is read by the compiler front-end and used when resolving and checking references to the imported file.

It is organized as two subsections according to two existing mechanisms of import resolution to the binary file.

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``metadataEnabled``
     - ``uint32_t``
     - A flag of whether metadata was emitted for the file.
ForeignField Format
-------------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 10 75
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``class_idx``
     - ``uint16_t``
     - Index of a declaring class in the corresponding :ref:`ClassRegionIndex <RT ClassRegionIndex>`.
       The corresponding index entry must be an offset to a :ref:`Class <RT Class>` or to a
       :ref:`ForeignClass <RT ForeignClass>`.

   * - ``type_idx``
     - ``uint16_t``
     - Index of the field type in the corresponding :ref:`ClassRegionIndex <RT ClassRegionIndex>`.
Field Format
------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 20 65
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``class_idx``
     - ``uint16_t``
     - Index of a declaring class in the corresponding :ref:`ClassRegionIndex <RT ClassRegionIndex>`.
       The corresponding index entry must be an offset to a :ref:`Class <RT Class>` or to a
       :ref:`ForeignClass <RT ForeignClass>`.

   * - ``type_idx``
     - ``uint16_t``
     - Index of the field type in the corresponding :ref:`ClassRegionIndex <RT ClassRegionIndex>`.
FieldType
---------

Any offset in the range ``[0; sizeof(Header))`` is invalid because the first
bytes of the file contain the header. The ``FieldType`` encoding uses this fact to
encode primitive types of the field in the low 4 bits. The value of a
non-primitive type is an offset to a :ref:`Class <RT Class>` or to a :ref:`ForeignClass <RT ForeignClass>`.
In either case, :ref:`FieldType <RT FieldType>` is ``uint32_t``. Primitive types are encoded
as follows:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Type
     - Encoding

   * - ``u1``
     - ``0x00``

   * - ``i8``
     - ``0x01``

   * - ``u8``
Field Access Flags
------------------

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``ACC_PUBLIC``
     - ``0x0001``
     - Declared public.

   * - ``ACC_PRIVATE``
     - ``0x0002``
     - Declared private.

   * - ``ACC_PROTECTED``
     - ``0x0004``
     - Declared protected.

   * - ``ACC_STATIC``
Field Tags
----------

.. list-table::
   :width: 100%
   :align: left
   :widths: 30 10 10 15 35
   :header-rows: 1

   * - Name
     - Tag
     - Quantity
     - Data Format
     - Description

   * - ``NOTHING``
     - ``0x00``
     - ``1``
     - ``none``
     - No more values. The value with this tag must be the last.

   * - ``INT_VALUE``
     - ``0x01``
     - ``0-1``
ForeignMethod Format
--------------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 10 75
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``class_idx``
     - ``uint16_t``
     - Index of a declaring class in the corresponding :ref:`ClassRegionIndex <RT ClassRegionIndex>`.
       The corresponding index entry must be an offset to a :ref:`Class <RT Class>` or to a
       :ref:`ForeignClass <RT ForeignClass>`.

   * - ``proto_idx``
     - ``uint16_t``
     - Index of a method prototype in the corresponding :ref:`ProtoRegionIndex <RT ProtoRegionIndex>`.
Method Format
-------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 20 65
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``class_idx``
     - ``uint16_t``
     - Index of a declaring class in the corresponding :ref:`ClassRegionIndex <RT ClassRegionIndex>`.
       The corresponding index entry must be an offset to a :ref:`Class <RT Class>` or to a
       :ref:`ForeignClass <RT ForeignClass>`.

   * - ``proto_idx``
     - ``uint16_t``
     - Index of a method prototype in the corresponding :ref:`ProtoRegionIndex <RT ProtoRegionIndex>`.
Proto Format
------------

**Alignment**: 2 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 20 15 65
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``shorty``
     - ``uint16_t[]``
     - Short representation of a prototype. Syntax is described in
       :ref:`Shorty <RT Shorty>`.

   * - ``reference_types``
     - ``uint16_t[]``
     - Array of indices of the non-primitive types in a method signature.
       Each ``ref`` type in a ``shorty`` has a corresponding element
Shorty Syntax
-------------

``Shorty`` is a short description of a method signature without detailed
information on reference types. A ``shorty`` begins with a return type
followed by method arguments, and ends with ``0x0``.

The ``shorty`` syntax is as follows:

``Type`` encoding:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Type
     - Encoding

   * - ``void``
     - ``0x01``

   * - ``u1``
     - ``0x02``

   * - ``i8``
     - ``0x03``
Method Access Flags
-------------------

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``ACC_PUBLIC``
     - ``0x0001``
     - Declared public.

   * - ``ACC_PRIVATE``
     - ``0x0002``
     - Declared private.

   * - ``ACC_PROTECTED``
     - ``0x0004``
     - Declared protected.

   * - ``ACC_STATIC``
Method Tags
-----------

.. list-table::
   :width: 100%
   :align: left
   :widths: 30 10 10 15 35
   :header-rows: 1

   * - Name
     - Tag
     - Quantity
     - Data Format
     - Description

   * - ``NOTHING``
     - ``0x00``
     - ``1``
     - ``none``
     - No more values. The value with this tag must be the last.

   * - ``CODE``
     - ``0x01``
     - ``0-1``
Code Format
-----------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``num_vregs``
     - ``uleb128``
     - Number of registers (without argument registers).

   * - ``num_args``
     - ``uleb128``
     - Number of arguments.

   * - ``code_size``
     - ``uleb128``
TryBlock Format
---------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 15 70
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``start_pc``
     - ``uleb128``
     - Start ``pc`` of a ``TryBlock``. This ``pc`` points to the first
       instruction covered by a ``TryBlock``.

   * - ``length``
     - ``uleb128``
     - Number of instructions covered by a ``TryBlock``.

   * - ``num_catches``
CatchBlock Format
-----------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 10 75
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``type_idx``
     - ``uleb128``
     - Index + 1 of the exception type handled by a
       :ref:`CatchBlock <RT CatchBlock>`, or ``0`` in case of a *catch all* block.
       The corresponding index entry must be an offset to a :ref:`ForeignClass <RT ForeignClass>`
       or to a :ref:`Class <RT Class>`. If the index is 0, then it is a *catch all* block
       that catches all exceptions.

   * - ``handler_pc``
ParamAnnotations Format
-----------------------

**Alignment**: 8 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 20 65
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``count``
     - ``uint32_t``
     - Number of parameters that a method has. This number includes synthetic
       and mandated parameters.

   * - ``annotations``
     - ``AnnotationArray[]``
     - Array of annotation lists for each parameter. The array has ``count``
       elements. Each element must have the :ref:`AnnotationArray <RT AnnotationArray>` format.
AnnotationArray Format
----------------------

**Alignment**: 8 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 10 15 75
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``count``
     - ``uint32_t``
     - Number of elements in the array.

   * - ``offsets``
     - ``uint32_t[]``
     - Array of offsets to parameter annotations. Each offset must refer to
       an :ref:`Annotation <RT Annotation>`. The array has ``count`` elements.

ForeignClass Format
-------------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``name``
     - ``String``
     - Name of a foreign type. The name must conform to
       :ref:`Type Descriptor <RT Type Descriptor>` syntax.

Class Format
------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``name``
     - ``String``
     - Name of a type. The name must conform to :ref:`Type Descriptor <RT Type Descriptor>`
       syntax.

   * - ``super_class_off``
     - ``uint8_t[4]``
     - Offset to the name of a super class or ``0`` for root object class.
       A non-zero offset must point at a :ref:`ForeignClass <RT ForeignClass>`
Type Descriptor
---------------

Type descriptors in a binary file have the following syntax:

``RefTypeName`` is a :ref:`Fully Qualified Name <RT Fully Qualified Name>` of the type with all dots (``'.''``) replaced for slashes (``'/''``).

``PrimitiveType`` encoding:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Type
     - Encoding
     - Description

   * - ``u1``
     - ``Z``
     - 1-bit unsigned integer

   * - ``i8``
     - ``B``
     - 8-bit signed integer

   * - ``u8``
Class Access Flags
------------------

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``ACC_PUBLIC``
     - ``0x0001``
     - Declared public.

   * - ``ACC_FINAL``
     - ``0x0010``
     - Declared final.

   * - ``ACC_SUPER``
     - ``0x0020``
     - No special meaning. Added for compatibility only

   * - ``ACC_INTERFACE``
Class Tags
----------

.. list-table::
   :width: 100%
   :align: left
   :widths: 30 10 10 15 35
   :header-rows: 1

   * - Name
     - Tag
     - Quantity
     - Data Format
     - Description

   * - ``NOTHING``
     - ``0x00``
     - ``1``
     - ``none``
     - No more values. The value with this tag must be the last.

   * - ``INTERFACES``
     - ``0x01``
     - ``0-1``
Annotation Format
-----------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 25 60
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``class_idx``
     - ``uint16_t``
     - Index of a declaring class in the :ref:`ClassRegionIndex <RT ClassRegionIndex>` format.
       The corresponding index entry must be an offset to a :ref:`Class <RT Class>` or to a
       :ref:`ForeignClass <RT ForeignClass>`.

   * - ``count``
     - ``uint16_t``
     - The number of name-value pairs in the annotation
Annotation Element Type
-----------------------

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Type
     - Tag

   * - ``u1``
     - ``1``

   * - ``i8``
     - ``2``

   * - ``u8``
     - ``3``

   * - ``i16``
     - ``4``

   * - ``u16``
     - ``5``

   * - ``i32``
AnnotationElement Format
------------------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 15 15 70
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``name_off``
     - ``uint32_t``
     - Offset to the element name. The offset must point at a :ref:`String <RT String>`.

   * - ``value``
     - ``uint32_t``
     - Value of the element. If the type of an annotation element is ``boolean``,
       ``byte``, ``short``, ``char``, ``int``, or ``float``, then the field
       ``value`` contains the value itself in the corresponding :ref:`Value <RT Value>`
Value Format
------------

There are different value encodings depending on the value type.

ByteValue Format
----------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t``
     - Signed 1-byte integer value.

ShortValue Format
-----------------

**Alignment**: 2 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[2]``
     - Signed 2-byte integer value.

IntegerValue Format
-------------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[4]``
     - Signed 4-byte integer value.

LongValue Format
----------------

**Alignment**: 8 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[8]``
     - Signed 8-byte integer value.

FloatValue Format
-----------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[4]``
     - 4-byte bit pattern, zero-extended to the right, and interpreted as an
       IEEE754 32-bit floating point value.

DoubleValue Format
------------------

**Alignment**: 8 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[8]``
     - 8-byte bit pattern, zero-extended to the right, and interpreted as an
       IEEE754 64-bit floating point value.

StringValue Format
------------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint32_t``
     - The value represents an offset to a :ref:`String <RT String>`.

EnumValue Format
----------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint32_t``
     - The value represents an offset to an enum field. An offset must
       point at a :ref:`Field <RT Field>` or at a :ref:`ForeignField <RT ForeignField>`.

ClassValue Format
-----------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint32_t``
     - The value represents an offset to a :ref:`Class <RT Class>` or to a :ref:`ForeignClass <RT ForeignClass>`.

AnnotationValue Format
----------------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint32_t``
     - The value represents an offset to a :ref:`Annotation <RT Annotation>`.

MethodValue Format
------------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint32_t``
     - The value represents an offset to a :ref:`Method <RT Method>` or to a :ref:`ForeignMethod <RT ForeignMethod>`.

MethodHandleValue Format
------------------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint32_t``
     - The value represents an offset to a :ref:`MethodHandle <RT MethodHandle>`.

MethodTypeValue Format
----------------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint32_t``
     - The value represents an offset to a :ref:`Proto <RT Proto>`.

ArrayValue Format
-----------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``count``
     - ``uleb128``
     - Number of elements in the array.

   * - ``value``
     - ``uint32_t``
     - Unaligned array of :ref:`Value <RT Value>` entities. The array has ``count`` elements.
       Format depends on the ``tag_value`` field.

LiteralArray Format
-------------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 20 15 65
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``num_literals``
     - ``uint32_t``
     - Interpreted differently for different :ref:`Literal Tags <RT Literal Tags>`.
       If ``literals`` have an ``ARRAY_*`` ``tag``, then ``num_literals``
       equals to the number of elements in an array. For other tags ``num_literals``
       equals to the number of elements in ``literals`` array times 2 (since each ``tag``
       can be interpreted as separate :ref:`Literal <RT Literal>`).

   * - ``literals``
Literal Tags
------------

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Tag
     - Value
     - ``data`` encoding

   * - ``TAGVALUE``
     - ``0x00``
     - :ref:`ByteOne <RT ByteOne>`

   * - ``BOOL``
     - ``0x01``
     - :ref:`ByteOne <RT ByteOne>`

   * - ``INTEGER``
     - ``0x02``
     - :ref:`ByteFour <RT ByteFour>`

   * - ``FLOAT``
Literal Format
--------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 10 15 75
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``tag``
     - ``uint8_t``
     - Tag of a literal. A tag of a literal instructs how to interpret
       ``num_literals`` and ``data`` fields. A tag of a literal must be one of
       :ref:`Literal Tags <RT Literal Tags>`.

   * - ``data``
     - ``uint8_t[]``
     - Elements of a literal array. The number of elements is ``num_literals``.
ByteOne Format
--------------

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t``
     - 1-byte value.

ByteTwo Format
--------------

**Alignment**: 2 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[2]``
     - 2-byte value.

ByteFour Format
---------------

**Alignment**: 4 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[4]``
     - 4-byte value.

ByteEight Format
----------------

**Alignment**: 8 bytes

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``value``
     - ``uint8_t[8]``
     - 8-byte value.

InstDebugInfo Format
--------------------

Debug information contains mapping between program counter of a method,
line numbers in source code, and information about local variables. The format
is derived from the DWARF Debugging Information Format, Version 3 (see subsection 6.2).
The mapping and local variable information are encoded in
the line number program, which is interpreted by the :ref:`State Machine <RT State Machine>`.
All constants the program refers to are moved into the :ref:`Constant Pool <RT Constant Pool>`
in order to deduplicate identical line number programs of different methods.

**Alignment**: None

**Format**:

.. list-table::
   :width: 100%
   :align: left
   :widths: 30 15 55
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``line_start``
Constant Pool
-------------

Many methods have similar line number programs that differ in
variable names, variable types, and file names only. In order to deduplicate such
programs, all constants the program refers to are stored in the constant pool.
During program interpretation, the :ref:`State Machine <RT State Machine>` tracks a pointer to
the constant pool. When the :ref:`State Machine <RT State Machine>` interprets an instruction
that requires a constant argument, the machine reads memory for the value pointed to by
the constant pool pointer, and then increments the pointer. Thus,
a program has no explicit reference to constants, and can be deduplicated.

State Machine
-------------

The aim of the state machine is to generate mapping between the program
counter, line numbers, and local variable information. The machine has
the following registers:

.. list-table::
   :width: 100%
   :align: left
   :widths: 22 20 58
   :header-rows: 1

   * - Name
     - Initial value
     - Description

   * - ``address``
     - 0
     - Program counter (refers to method instructions).
       Must always increase monotonically.

   * - ``line``
     - ``line_start`` from :ref:`InstDebugInfo <RT InstDebugInfo>`.
     - Unsigned integer which corresponds to a line number in source code.
Line Number Program Format
--------------------------

A line number program consists of instructions. Each instruction has one
byte opcode and optional arguments. Depending on opcode, an argument
value can be encoded into the instruction. Otherwise, the instruction
requires the value to be read from the constant pool.

.. list-table::
   :width: 100%
   :align: left
   :widths: 25 10 10 10 45
   :header-rows: 1

   * - Opcode
     - Value
     - Instruction Format
     - Constant Pool Args
     - Description

   * - ``END_SEQUENCE``
     - ``0x00``
     - 
     - 
MethodHandle Format
-------------------

Alignment: none

Format:

.. list-table::
   :width: 100%
   :align: left
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``type``
     - ``uint8_t``
     - Type of a handle. Must be one of :ref:`Type Of MethodHandle <RT Type Of MethodHandle>`.

   * - ``offset``
     - ``uleb128``
     - Offset to an entity of a corresponding type. Type of an entity is
       determined depending on the handle type (see
       :ref:`Type of MethodHandle <RT Type of MethodHandle>`).
Type of MethodHandle
---------------------

The types available for a method handle are as follows:

.. list-table::
   :width: 100%
   :align: left
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``PUT_STATIC``
     - ``0x00``
     - Method handle refers to a static setter. Offset in
       :ref:`MethodHandle <RT MethodHandle>` must point at a :ref:`Field <RT Field>` or at a
       :ref:`ForeignField <RT ForeignField>`.

   * - ``GET_STATIC``
     - ``0x01``
     - Method handle refers to a static getter. Offset in
       :ref:`MethodHandle <RT MethodHandle>` must point at a :ref:`Field <RT Field>` or at a
Argument Types
--------------

A bootstrap method can accept static arguments of the following types:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Name
     - Format
     - Description

   * - ``Integer``
     - ``0x00``
     - Corresponding argument has the :ref:`IntegerValue <RT IntegerValue>` encoding.

   * - ``Long``
     - ``0x01``
     - Corresponding argument has the :ref:`LongValue <RT LongValue>` encoding.

   * - ``Float``
     - ``0x02``
     - Corresponding argument has the :ref:`FloatValue <RT FloatValue>` encoding.
Runtime Type System
*******************

The ArkTS runtime operates upon the following types:

- *Primitive types* : ``void``, ``u1``, ``i8``, ``u8``, ``i16``,
  ``u16``, ``i32``, ``u32``, ``f32``, ``f64``, ``i64``, ``u64``,
  ``any``.
- *Reference types* : All other types. All *reference types* have
  corresponding :ref:`ForeignClass <RT ForeignClass>` or :ref:`Class <RT Class>` in a binary file.

The ArkTS runtime additionally distinguishes between the above *reference type* groups as follows:

- ``Any`` : Top type of the runtime type system. Correspondent to the 
  :ref:`Class <RT Class>` with the :ref:`Type Descriptor <RT Type Descriptor>` that matches ``RefType`` with a
  :ref:`Fully Qualified Name <RT Fully Qualified Name>` ``Y``. **NOTE:** NOT the same as ``any``
  in *primitive types*.
- ``never`` : Bottom type of the runtime type system. Correspondent to the
  :ref:`Class <RT Class>` with the :ref:`Type Descriptor <RT Type Descriptor>` that matches ``RefType`` with a
  :ref:`Fully Qualified Name <RT Fully Qualified Name>` ``N``.
- *Array types* : Types that represent arrays of some *component type*.
  Correspondent to a :ref:`Class <RT Class>` with the :ref:`Type Descriptor <RT Type Descriptor>` that matches
  ``ArrayType``.
- *Union types* : Types that represent unions of their *component types*.
Subtyping
=========

*Reference types* and *Primitive types* form the type hierarchy described
below:

::

                         Any
               __________/ \__________
              /                       \
   *Primitive types*                Object
             |                ________/ \________
             |               /                   \
             |        *Array types*      *User-defined types*        *Union types*
             |               \___                 |                   ___/
             |                   \                |                  /
             |                   +-----------------------------------+
             |                   | language reference type hierarchy |
             |                   +-----------------------------------+
              \__________   _____________________/
                         \ /
                        never
Runtime Name
************

The ArkTS runtime (e.g. standard library reflection, and class loading APIs)
and build time (build system, compiler, bytecode manipulation tools) use
*runtime name* to work with modules, classes, and other entities.
The syntax of a *runtime name* is presented below:

``RefTypeName`` is the :ref:`Fully Qualified Name <RT Fully Qualified Name>` of the type.

**Constraint**: ``UnionType`` must be canonicalized. Canonicalization
presumes sorting ``RuntimeName`` s of all *constituent types* alphabetically.
Language Representation in Binary File
**************************************

This chapter describes how the ArkTS compiler translates different language
types and constructs into bytecode.

.. note::
   The ArkTS *type erasure* rules take precedence over the translation
   rules discussed in this chapter. It means that the *type erasure* rules are
   applied first for any ArkTS type ``T``, and then the *effective type* of ``T``
   is translated into the binary representation in accordance with the rules below.

Value Types
===========

The ArkTS *value types* can be represented in a binary file in **one** of the following two forms depending on the context:

- ``PrimitiveType`` in :ref:`Type Descriptor <RT Type Descriptor>`, :ref:`FieldType <RT FieldType>`, or :ref:`Shorty <RT Shorty>`; or
- Corresponding predefined *reference type*.

The :ref:`Type Descriptor <RT Type Descriptor>` of a *reference type* type matches ``RefType``.
Mapping between the ArkTS type, *primitive type* and :ref:`Fully Qualified Name <RT Fully Qualified Name>`
of a *reference type* is presented in the table below:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Type
     - Primitive
     - Reference
   * - boolean
     - ``u1``
     - ``std.core.Boolean``
   * - char
Selecting Between Primitive And Reference
-----------------------------------------

Each time one of *value types* is used, the ArkTS compiler tries
to lower it to its corresponding *primitive type* representation by default.
However, *reference type* representation is required in some cases.
A comprehensive list of such scenarios is presented below:

- *Component types* of a *union type* must be *reference types*, i.e., any
  *value type* in a *union type* is represented as a *reference type* in a binary
  file.
- If a *value type* is used as a constraint of a generic parameter, then it is also
  represented as a *reference type* in a binary file.
- If a default value for a parameter of a method or a function is of a *value type*,
  then the type of that parameter is represented with *reference type*
  in a binary file.
- When a field of a class is inherited as an instantiation of a field
  of a generic class whose type is a type parameter, that field is
  represented with *reference* type.
- If a method is inherited from a generic class or interface without overriding,
  its parameters whose type in the original definition
  is a type parameter are represented with *reference* type. The same
Type ``Any``
============

The ArkTS type ``Any`` is represented in a binary file with the predefined
:ref:`Class <RT Class>`. The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
:ref:`Fully Qualified Name <RT Fully Qualified Name>` ``Y``.

Type ``Object``
===============

The ArkTS type ``Object`` is represented in a binary file with the predefined
:ref:`Class <RT Class>`. The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
:ref:`Fully Qualified Name <RT Fully Qualified Name>` ``std.core.Object``.

Type ``never``
==============

The ArkTS type ``never`` is represented in a binary file with the predefined
:ref:`Class <RT Class>`. The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
:ref:`Fully Qualified Name <RT Fully Qualified Name>` ``N``.

Type ``void``
=============

The ArkTS type ``void`` is represented in a binary file as the primitive type ``void``
in the :ref:`Shorty <RT Shorty>`.

Type ``null``
=============

The ArkTS type ``null`` is represented in a binary file with the predefined
:ref:`Class <RT Class>`. The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
:ref:`Fully Qualified Name <RT Fully Qualified Name>` ``std.core.Null``.

Type ``string``
===============

The ArkTS type ``string`` is represented in a binary file with the predefined
:ref:`Class <RT Class>`. The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
:ref:`Fully Qualified Name <RT Fully Qualified Name>` ``std.core.String``.

Type ``bigint``
===============

The ArkTS type ``bigint`` is represented in a binary file with the predefined
:ref:`Class <RT Class>`. The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
:ref:`Fully Qualified Name <RT Fully Qualified Name>` ``std.core.BigInt``.

Array types
===========

Resizable Array Types
---------------------

The ArkTS *resizable array types* are represented in a binary file by the
predefined :ref:`Class <RT Class>`. The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches
``RefType`` with :ref:`Fully Qualified Name <RT Fully Qualified Name>` ``std.core.Array``.

Fixed-Size Array Types
----------------------

The ArkTS *fixed-size array types* are represented in a binary file by a predefined :ref:`Class <RT Class>`.
Each distinct *fixed-size array type* has a unique correspondent predefined :ref:`Class <RT Class>`.
The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``ArrayType``.
:ref:`Fully Qualified Name <RT Fully Qualified Name>` of the component type and of the *component type* of a
*fixed-size array type* are the same.

Tuple Types
===========

The ArkTS *tuple types* are represented in a binary file by a
predefined :ref:`Class <RT Class>`. :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches
``RefType`` with :ref:`Fully Qualified Name <RT Fully Qualified Name>` ``std.core.Tuple1``,
``std.core.Tuple2``, ..., ``std.core.Tuple16``, or ``std.core.TupleN``
that depends on the number of constituent types of a *tuple type*.

**Constraint**: As shown above, the ArkTS runtime does not distinguish between tuple
types with a number of constituent types greater than ``16``.

Functional Types
================

The ArkTS *functional types* are represented in a binary file by a
predefined :ref:`Class <RT Class>` that depends on the number of parameters of the *functional type*
and on the presence of a *rest parameter* in the signature.
The :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` for *functional types* without a
*rest parameter* matches ``RefType`` with the :ref:`Fully Qualified Name <RT Fully Qualified Name>`
``std.core.Function0``, ``std.core.Function1``, ..., ``std.core.Function16``, or ``std.core.FunctionN``.
The exact :ref:`Type Descriptor <RT Type Descriptor>` depends on the number of parameters of the *functional type*.
However, the :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` for *functional types* with a
*rest parameter* matches ``RefType`` with the :ref:`Fully Qualified Name <RT Fully Qualified Name>`
``std.core.FunctionR0``, ``std.core.FunctionR1``, ..., ``std.core.FunctionR15``, or ``std.core.FunctionR16``.
The exact :ref:`Type Descriptor <RT Type Descriptor>` depends on the number of parameters of the *functional type*.

Functional Objects
------------------

The ArkTS *functional objects* are represented in a binary file by a predefined
:ref:`Class <RT Class>`. Each *functional object* has a unique correspondent predefined :ref:`Class <RT Class>`.
``fields`` of this :ref:`Class <RT Class>`
contain references captured by the *functional object*.
``methods`` of this :ref:`Class <RT Class>` contain auxiliary functions needed to invoke the
*functional object*. The :ref:`Method <RT Method>` that contains the body of the *functional object*
is added to the ``methods`` of the enclosing class of the
*functional object*. It is to allow the body of the *functional object* to access private members of the enclosing class.

Union Types
===========

The ArkTS *union types* are represented in a binary file by a predefined :ref:`Class <RT Class>`.
Each *union type* has a unique correspondent predefined :ref:`Class <RT Class>`.
:ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``UnionType``
with *qualified names* of the *component types*
being the *qualified names* of the *component types* of the *union type*.

Utility Types
=============

Awaited
-------

The ArkTS type ``Awaited`` is fully expanded at compile time, and does not appear
at runtime.

NonNullable
-----------

The ArkTS type ``NonNullable`` is fully expanded at compile time, and does not
appear at runtime.

Partial
-------

The ArkTS type ``Partial`` is represented in a binary file by a predefined :ref:`Class <RT Class>`.
Each ``Partial`` type has a unique correspondent predefined :ref:`Class <RT Class>`.
:ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
the *unqualified name* ``%%partial-typeName``, where ``typeName`` is
an *unqualified name* of the ``Partial``'s type argument.

Required
--------

The ArkTS type ``Required`` is fully expanded at compile time, and does not appear
at runtime.

Readonly
--------

The ArkTS type ``Readonly`` is fully expanded at compile time, and does not appear
at runtime.

Record
------

The ArkTS type ``Record`` is represented in a binary file by a predefined
:ref:`Class <RT Class>`. :ref:`Type Descriptor <RT Type Descriptor>` of this :ref:`Class <RT Class>` matches ``RefType`` with
*qualified name* ``std.core.Record``.

ReturnType
----------

The ArkTS type ``ReturnType`` is fully expanded at compile time, and does not
appear at runtime.

Class Types
===========

Class Declaration
-----------------

Each *class declaration* is lowered to a :ref:`Class <RT Class>` with an *unqualified name*
equal to the *class* name in the source code. ``fields`` of this :ref:`Class <RT Class>`
correspond to all *class field declarations* of the *class*. ``methods`` of this
:ref:`Class <RT Class>` correspond to all *class method declarations* and
*class accessor declarations* of the *class*. Additionally, for each
*constructor declaration* of the *class* a method is generated with the name
``<ctor>`` and for all *static block* in *class* the single *static method*
is generated with the name ``<cctor>``.

A :ref:`Method <RT Method>` with the name ``<ctor>`` is generated for each
*constructor declaration* of the *class*.
A *static* (``access_flags | ACC_STATIC == 1``) :ref:`Method <RT Method>` with the name ``<cctor>`` is generated for each
*static block* in the *class*.

Class Extension Clause
----------------------

*Direct superclass* of the *class* is stored in the ``super_class_off`` field
of the :ref:`Class <RT Class>`.

Class Implementation Clause
---------------------------

*Direct superinterfaces* of the *class* stored in the field ``class_data`` of
the :ref:`Class <RT Class>`. The tag ``INTERFACES`` is used to store *direct superinterfaces*.

Class Field
-----------

Each *class field declaration* is lowered to a :ref:`Field <RT Field>` with the name
equal to the *field* name in the source code. Access modifiers of the
*field* are represented by the corresponding :ref:`Field Access Flags <RT Field Access Flags>`:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Modifier
     - Access Flag
   * - ``private``
     - ``ACC_PRIVATE``
   * - ``public``
     - ``ACC_PUBLIC``
   * - ``protected``
     - ``ACC_PROTECTED``
   * - ``static``
     - ``ACC_STATIC``
Class Method
------------

Each *class method declaration* is lowered to a :ref:`Method <RT Method>` with the
name equal to the *method* name in the source code. Modifiers of the
*method* are represented by the corresponding :ref:`Method Access Flags <RT Method Access Flags>`:

.. list-table::
   :width: 100%
   :align: left
   :widths: auto
   :header-rows: 1

   * - Modifier
     - Access Flag
   * - ``private``
     - ``ACC_PRIVATE``
   * - ``public``
     - ``ACC_PUBLIC``
   * - ``protected``
     - ``ACC_PROTECTED``
   * - ``abstract``
     - ``ACC_ABSTRACT``
Class Accessor
--------------

Each *class accessor declaration* is lowered to a :ref:`Method <RT Method>`.
The :ref:`Method <RT Method>` name of a getter for the property ``propName``
is ``%%get-propName``.
The :ref:`Method <RT Method>` name of a setter for the property ``propName``
is ``%%set-propName``.

Interface Types
===============

Interface Declaration
---------------------

Each *interface declaration* is lowered to a :ref:`Class <RT Class>` with
an *unqualified name* equal to the *interface* name in the source code.
This :ref:`Class <RT Class>` is an *interface*
(``access_flags | ACC_INTERFACE == 1``, ``access_flags | ACC_ABSTRACT == 1``).
``fields`` of this :ref:`Class <RT Class>` must be empty. ``methods`` of this :ref:`Class <RT Class>`
correspond to all *interface properties* and *interface method declarations* of
the *interface*.

Superinterfaces And Subinterfaces
---------------------------------

The representation of *direct superinterfaces* of an *interface* and of
:ref:`Class Implementation Clause <RT Class Implementation Clause>` is the same.

Interface Property
------------------

The representation of an interface accessor and of the :ref:`Class Accessor <RT Class Accessor>` is the same.

Interface Method
----------------

Each *interface method declaration* is lowered to a :ref:`Method <RT Method>` with the
name equal to the *method* name in the source code. This :ref:`Method <RT Method>` is an
*abstract method*.

Enumeration Types
=================

Each *enumeration declaration* is lowered to a :ref:`Class <RT Class>` with
an *unqualified name* equal to the *enumeration type* name in the source code.
``fields`` of this :ref:`Class <RT Class>` correspond to all
*enum constants* of the *enumeration type*.
``methods`` of this class correspond to the *enumeration methods* of the *enumeration type*.
A single *static method* with the name ``<cctor>`` is generated additionally for this
:ref:`Class <RT Class>`. This *static method* corresponds to the *enumeration type* static constructor.
This :ref:`Class <RT Class>` extends the :ref:`Class <RT Class>` with
:ref:`Fully Qualified Name <RT Fully Qualified Name>` ``std.core.BaseEnum``.

Namespaces And Modules
======================

Each *namespace declaration* is lowered to a :ref:`Class <RT Class>` with an
*unqualified name* equal to the *namespace* name in the source code. This
:ref:`Class <RT Class>` is *abstract* (``access_flags | ACC_ABSTRACT == 1``), and has
an :ref:`Annotation <RT Annotation>` with the :ref:`Fully Qualified Name <RT Fully Qualified Name>` ``ets.annotation.Module``.
``fields`` of this :ref:`Class <RT Class>` correspond to all *variable declarations* and
*constant declarations* of the *namespace*. ``methods`` of this :ref:`Class <RT Class>`
correspond to all *function declarations*, *accessor declarations*,
*function with receiver declarations*, and *accessor with receiver declarations*
of the *namespace*. Additionally, each *namespace* has a generated
*static method* with the name ``<cctor>``. It corresponds to the static
initializer of the *namespace*. A name for *top-level* namespace is chosen by the
*build system*, while the binary representation remains.

Annotations
===========

Annotation Declaration
----------------------

Each *annotation declaration* is lowered to a :ref:`Class <RT Class>` with
an *unqualified name* equal to the *annotation* name in the source code. This
:ref:`Class <RT Class>` is an *annotation* (``access_flags | ACC_ANNOTATION == 1``,
``access_flags | ACC_ABSTRACT == 1``). ``fields`` of this :ref:`Class <RT Class>`
correspond to all *annotation fields* of the *annotation*. ``methods`` of
this :ref:`Class <RT Class>` must be empty.

Annotation Field
----------------

The representation of each *annotation field* and :ref:`Class field <RT Class field>` in bytecode is the same.
Verification
************

Even though the ArkTS compiler ensures that user program is structurally correct and does not violate ArkTS type system, and it produces
only binary files that satisfy all the static and structural constraints of the :ref:`Binary File Format <RT Binary File Format>`,
the ArkTS runtime has no guarantee that the loaded binary file was generated by such compiler or is properly formed.

.. note::
   An additional problem with compile-time checking is the potential conflict between different versions of the binary files.
   Suppose that the module ``A`` that depends on the module ``B`` was successfully compiled. Since the time ``A`` was compiled,
   the definition of the module ``B`` might have changed in a way that breaks the binary compatibility
   (see :ref:`Binary Compatibility <Binary Compatibility>`). Such conflict can only be detected at runtime by the process of verification.

Because of the aforementioned problems, ArkTS runtime requires all loaded binary files to be verified,
and rejects all non-verified binary files with a runtime error.

Verification ensures that the binary representation of the program is structurally correct and that the ArkTS type system is not violated in any way.
For example, verification checks that no final class is later extended; that called method parameter types and count matches this method's definition;
and that none of the instructions violate the ArkTS type system.

If an error occurs during verification, then an error will be thrown at the point in the program that caused the verification to start.

Verification Process
====================

Depending on the implementation, the verification process may happen:

- At runtime - on :ref:`Class <RT Class>` loading.
- Statically - if a program linkage sequence is known prior to it's execution.

For both of these options the verification consists of these main steps:

- Verification of the dependent entities (see :ref:`Dependent Entity Verification <RT Dependent Entity Verification>`).
- Verification of the type system (see :ref:`Type System Verification <RT Type System Verification>`)
- Verification of the control flow of the program (see :ref:`Control Flow Verification <RT Control Flow Verification>`).
- Abstract interpretation of the program (see :ref:`Abstract Interpretation <RT Abstract Interpretation>`).

For the :ref:`Dependent Entity Verification <RT Dependent Entity Verification>` and the :ref:`Type System Verification <RT Type System Verification>`.
the unit of verification is a :ref:`Class <RT Class>`.
For the :ref:`Abstract Interpretation <RT Abstract Interpretation>` and the :ref:`Control Flow Verification <RT Control Flow Verification>`,
the unit of verification is a :ref:`Method <RT Method>`.

.. note::
   The code for each :ref:`Method <RT Method>` is verified independently of each other.

Dependent Entity Verification
=============================

This step verifies that all dependent entities of the :ref:`Class <RT Class>` can be resolved an
produce no error on verification. If any of the dependent entities can not be resolved or fails
the verification, an error is thrown.

Type System Verification
========================

This step verifies that the :ref:`Class <RT Class>` declaration does not violate the existing static type system that
consists of both ArkTS types and other user-defined types. This step includes, but is not limited to the following checks:

- Check that the :ref:`Class <RT Class>` does not extend *final* :ref:`Class <RT Class>`.
- Check that the :ref:`Class <RT Class>` has access to the :ref:`Class <RT Class>` it extends.
- etc.

If any of the checks performed at this step fail, an error is thrown.

Control Flow Verification
=========================

This step verifies that the control flow of the :ref:`Method <RT Method>` is consistent.
This step includes, but is not limited to the following checks:

- The targets of all control flow instructions are each the start of an instruction.
- Control flow of a :ref:`Method <RT Method>` can not reach outside of it.
- Control flow can only reach the body of an exception handler via dedicated instructions.
- Control flow of a :ref:`Method <RT Method>` end must terminate with any of the proper instructions.
- etc.

If any of the checks performed at this step fail, an error is thrown.

Abstract Interpretation
=======================

This step checks the :ref:`Method <RT Method>` instructions for type consistency.
Abstract interpretation goes instruction by instruction maintaining the actual
state with the inferred types in the :ref:`Method <RT Method>` dataflow. Abstract interpretation takes into
account how each instruction affects the types in the :ref:`Method <RT Method>` dataflow and correctly handles
the convergence of different data flows in a given instruction.

This step includes, but is not limited to the following checks:

- Check that each accessed :ref:`Field <RT Field>` / :ref:`Class <RT Class>` / :ref:`Method <RT Method>` has corresponding access rights.
- Check that types expected as instruction input / method argument are correctly related via subtyping with actual types.
- Check that type of the value returned from the :ref:`Method <RT Method>` matches the it's signature.
- Check correctness of exception handlers.
- etc.

If any of the checks performed at this step fail, an error is thrown.

Verifier Type System
--------------------------------

Below is listed the type hierarchy of the builtin types of the verifier.

Subtyping of the *user-defined types* is mandated by the :ref:`Runtime Type System <RT Runtime Type System>`.

::

                                                Top
                                  ______________/ \___________
                                 /                            \
                            Primitive                      Reference
            ___________________/ \______________               |
           /                                    \              |
        bits32                                 bits64        Object
       __/ \____                             ___/ \___         |
      /         \                           /         \        |
  Float32        |                      Float64        |   FixedArray
     |           |                         |           |       |
    f32          |                        f64          |       |
     |       Integral32                    |       Integral64  |
     |      ____/|\_______                 |       ___/ \___   |
     |     /     |        \                |      /         \  |
