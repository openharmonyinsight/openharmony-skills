# std.reflect

## 功能介绍

`reflect` 包提供了反射功能，使得程序在运行时能够获取到各种实例的类型信息，并进行各种读写和调用操作。

本包暂不支持 macOS 平台。

> **注意：**
>
> - 对于全局信息仓颉的反射功能只能访问可见性为 `public` 的全局变量和全局函数。
> - 对于当前所在包，仓颉的反射功能可以访问所有全局定义的类型，而对于外部导入的包或动态加载的模块，则只能访问其中可见性为 `public` 的全局定义的类型。
> - 对于成员信息仓颉的反射功能只能访问类型内的可见性为 `public` 的成员（实例/静态成员变量/属性/函数），使用非 `public` 修饰符修饰的或缺省修饰符的成员均是不可见的。
> - 目前，仓颉的反射功能尚不支持函数类型、元组类型、`enum` 类型。

## API 列表

### 函数

|              函数名          |           功能           |
| --------------------------- | ------------------------ |
| [parseParameterTypes(String)](./reflect_package_api/reflect_package_funcs.md#func-parseparametertypesstring) | 将字符串转换为包含具体类型信息的函数签名，以便 `getStaticFunction` 等函数使用。 |

### 类型别名

| 类型别名                                                       | 功能                          |
| ------------------------------------------------------------ | ----------------------------- |
| [Annotation](./reflect_package_api/reflect_package_types.md#type-annotation--object)| [Object](../core/core_package_api/core_package_classes.md#class-object) 的别名。|

### 类

|                 类名              | 功能                                     |
| --------------------------------- |----------------------------------------|
| [ClassTypeInfo](./reflect_package_api/reflect_package_classes.md#class-classtypeinfo) | 描述`class`类型的类型信息。                      |
| [ConstructorInfo](./reflect_package_api/reflect_package_classes.md#class-constructorinfo)| 描述构造函数信息。           |
| [GenericTypeInfo](./reflect_package_api/reflect_package_classes.md#class-generictypeinfo) | 描述泛型信息。|
| [GlobalFunctionInfo](./reflect_package_api/reflect_package_classes.md#class-globalfunctioninfo) | 描述全局函数信息。                              |
| [GlobalVariableInfo](./reflect_package_api/reflect_package_classes.md#class-globalvariableinfo) | 描述全局变量信息。                              |
| [InstanceFunctionInfo](./reflect_package_api/reflect_package_classes.md#class-instancefunctioninfo) | 描述实例成员函数信息。                            |
| [InstancePropertyInfo](./reflect_package_api/reflect_package_classes.md#class-instancepropertyinfo) | 描述实例成员属性信息。                            |
| [InstanceVariableInfo](./reflect_package_api/reflect_package_classes.md#class-instancevariableinfo) | 描述实例成员变量信息。                            |
| [InterfaceTypeInfo](./reflect_package_api/reflect_package_classes.md#class-interfacetypeinfo) | 描述`interface`类型的类型信息。                  |
| [PackageInfo](./reflect_package_api/reflect_package_classes.md#class-packageinfo) | 描述包信息。                                 |
| [ParameterInfo](./reflect_package_api/reflect_package_classes.md#class-parameterinfo) | 描述函数形参信息。                              |
| [PrimitiveTypeInfo](./reflect_package_api/reflect_package_classes.md#class-primitivetypeinfo) | 描述原始数据类型的类型信息。                         |
| [StaticFunctionInfo](./reflect_package_api/reflect_package_classes.md#class-staticfunctioninfo) | 描述静态成员函数信息。                            |
| [StaticPropertyInfo](./reflect_package_api/reflect_package_classes.md#class-staticpropertyinfo) | 描述静态成员属性信息。                            |
| [StaticVariableInfo](./reflect_package_api/reflect_package_classes.md#class-staticvariableinfo) | 描述静态成员变量信息。                            |
| [StructTypeInfo](./reflect_package_api/reflect_package_classes.md#class-structtypeinfo) | 描述`struct`类型的类型信息。                     |
| [TypeInfo](./reflect_package_api/reflect_package_classes.md#class-typeinfo) | `TypeInfo`提供了所有数据类型通用的操作接口，支持用户进行反射操作。 |

### 枚举

| 枚举名                                                                                                                                           |           功能           |
|-----------------------------------------------------------------------------------------------------------------------------------------------| ------------------------ |
| [ModifierInfo](./reflect_package_api/reflect_package_enums.md#enum-modifierinfo) | 描述修饰符信息。 |

### 异常类

| 异常类名                                                                                                                      | 功能                                                |
|---------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------|
| [IllegalSetException](./reflect_package_api/reflect_package_exceptions.md#class-illegalsetexception)             | 表示对不可变类型进行更改异常。   |
| [IllegalTypeException](./reflect_package_api/reflect_package_exceptions.md#class-illegaltypeexception)           | 表示类型不匹配异常。       |
| [InfoNotFoundException](./reflect_package_api/reflect_package_exceptions.md#class-infonotfoundexception)         | 表示无法找到对应信息异常。                                     |
| [InvocationTargetException](./reflect_package_api/reflect_package_exceptions.md#class-invocationtargetexception) | 表示调用函数包装异常。 |
| [MisMatchException](./reflect_package_api/reflect_package_exceptions.md#class-mismatchexception)                 | 表示调用对应函数抛出异常。       |
| [ReflectException](./reflect_package_api/reflect_package_exceptions.md#class-reflectexception)                   | `ReflectException` 为 Reflect 包的基异常类。   |
