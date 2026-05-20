# 异常类

## class ASTException

```cangjie
public class ASTException <: Exception {
    public init()
    public init(message: String)
}
```

功能：ast 库的异常类，在 ast 库调用过程中发生异常时使用。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ASTException](ast_package_exceptions.md#class-astexception) 对象。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [ASTException](ast_package_exceptions.md#class-astexception) 对象。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

## class MacroContextException

```cangjie
public class MacroContextException <: Exception {
    public init()
    public init(message: String)
}
```

功能：ast 库的上下文宏异常类，在上下文宏的相关接口中发生异常时使用。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MacroContextException](ast_package_exceptions.md#class-macrocontextexception) 对象。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [MacroContextException](ast_package_exceptions.md#class-macrocontextexception) 对象。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

## class ParseASTException

```cangjie
public class ParseASTException <: Exception {
    public init()
    public init(message: String)
}
```

功能：ast 库的解析异常类，在节点解析过程中发生异常时使用。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ParseASTException](ast_package_exceptions.md#class-parseastexception) 对象。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [ParseASTException](ast_package_exceptions.md#class-parseastexception) 对象。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。
