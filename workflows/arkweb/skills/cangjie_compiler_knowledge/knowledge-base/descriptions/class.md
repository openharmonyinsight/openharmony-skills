---
keyword: class
synonyms: [类, 类定义, class definition, 面向对象, OOP, 继承, inheritance, 多态, polymorphism]
related: [struct, interface, extend, generic, constructor, 构造函数]
category: language-feature
---

# 类 (Class)

## 中文描述
类是仓颉语言中的引用类型,支持继承、多态、访问控制等面向对象特性。类可以包含属性、方法、构造函数,支持单继承和多接口实现。

## English Description
Class is a reference type in Cangjie language, supporting inheritance, polymorphism, access control and other object-oriented features. Classes can contain properties, methods, constructors, and support single inheritance and multiple interface implementation.

## 使用场景
- 定义引用类型的数据结构
- 实现继承和多态
- 封装数据和行为
- 访问控制(public, private, protected)

## 相关实现
- 类声明解析在 Parse/ParseDecl.cpp
- 类型检查在 Sema/TypeCheckClassLike.cpp
- 继承关系验证在 Sema/InheritanceChecker/
- 关键类: ClassDecl, ClassType, InheritanceChecker

## 代码示例

### 示例 1: DemangleClassType
文件: `demangler/Demangler.h:213`

```cpp
T DemangleClassType();

    /**
     * @brief Get demangled qualified name.
     *
     * @return T The qualified name.
     */
    T DemangleQualifiedName();

    /**
     * @brief Get scope resolution.
     *
     * @return T The scope resolution.
     */
    T ScopeResolution() const { return scopeResolution; };
#ifdef BUILD_LIB_CANGJIE_DEMANGLE
    /**
     * @brief Set generic vector.
     *
     * @param vec The generic vector.
```

### 示例 2: DemangleClass
文件: `demangler/Demangler.h:253`

```cpp
DemangleInfo<T> DemangleClass(TypeKind typeKind);
    DemangleInfo<T> DemangleCFuncType();
    DemangleInfo<T> DemangleTuple();
    DemangleInfo<T> DemangleCommonDecl(bool isClass = false);
    DemangleInfo<T> DemangleDecl();
    DemangleInfo<T> DemangleRawArray();
    DemangleInfo<T> DemangleVArray();
    DemangleInfo<T> DemangleCPointer();
    DemangleInfo<T> DemangleFunction();
    DemangleInfo<T> DemanglePrimitive();
    DemangleInfo<T> DemangleCStringType();
    DemangleInfo<T> DemangleGenericType();
    DemangleInfo<T> DemangleDefaultParamFunction();
    DemangleInfo<T> DemangleInnerFunction();
    DemangleInfo<T> DemangleType();
    DemangleInfo<T> DemangleGenericTypes();
    DemangleInfo<T> DemangleFunctionParameterTypes();
    DemangleInfo<T> DemangleGlobalInit();
    DemangleInfo<T> DemangleParamInit();
    DemangleInfo<T> DemangleWrappedFunction();
```

### 示例 3: DemangleClass
文件: `demangler/Demangler.cpp:1430`

```cpp
return DemangleClass(TypeKind::CLASS);
        case 'R':
            return DemangleClass(TypeKind::STRUCT);
        case 'F':
            if (currentIndex + MANGLE_CHAR_LEN < mangledName.Length()) {
                // The F0 and FC is the function type prefix.
                if (mangledName[currentIndex + MANGLE_CHAR_LEN] == '0') {
                    return DemangleFunction();
                } else if (mangledName[currentIndex + MANGLE_CHAR_LEN] == 'C') {
                    return DemangleCFuncType();
                } else {
                    break;
                }
            } else {
                break;
            }
        case 'N':
            return DemangleClass(TypeKind::ENUM);
        case 'T':
            return DemangleTuple();
```

## 概念关系图谱

- **同义词**: 类, 类定义, class definition, 面向对象, OOP, 继承, inheritance, 多态, polymorphism
- **相关概念**: struct, interface, extend, generic, constructor, 构造函数
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, demangler, driver, frontend, frontendtool, include, incrementalcompilation, lex, macro, modules, parse, sema, unittests, utils

## 常见问题

### class 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 class？

请参考下面的代码示例部分。

### class 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

