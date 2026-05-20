---
keyword: option
synonyms: [Option, Some, None, 可选类型, optional type, 空值安全, null safety, ?., ??]
related: [enum, pattern-match, null, 空值]
category: language-feature
---

# Option 类型 (Option Type)

## 中文描述
Option<T> 是仓颉的可选类型,用于表示可能存在或不存在的值。通过 Some 和 None 两个枚举值实现空值安全,避免空指针异常。支持 ?. 和 ?? 操作符。

## English Description
Option<T> is Cangjie's optional type, used to represent values that may or may not exist. Implements null safety through Some and None enum values, avoiding null pointer exceptions. Supports ?. and ?? operators.

## 使用场景
- 表示可能为空的值
- 空值安全编程
- 可选链操作(?.)
- 空值合并操作(??)

## 相关实现
- Option 类型处理在 Sema 模块
- ?. 和 ?? 操作符在 Sema/TypeCheckExpr/
- 关键类: OptionType, OptionalChainingExpr

## 代码示例

### 示例 1: IsCoreOptionType
文件: `include/cangjie/AST/Types.h:179`

```cpp
bool IsCoreOptionType() const;
    /** Return whether a ty is class.
     * U: Sema.
     */
    bool IsClass() const;
    /** Return whether a ty is interface.
     * U: Sema.
     */
    bool IsInterface() const;
    /** Return whether a ty is intersection.
     * U: Sema.
     */
    bool IsIntersection() const;
    /** Return whether a ty is union.
     * U: Sema.
     */
    bool IsUnion() const;
    /** Return whether a ty is nominal.
     * U: Sema.
     */
```

### 示例 2: IsOption
文件: `include/cangjie/CHIR/IR/Type/Type.h:829`

```cpp
bool IsOption() const;

    std::vector<EnumCtorInfo> GetConstructorInfos(CHIRBuilder& builder) const;

    std::string ToString() const override;

    /**
     * @brief whether this EnumType is boxed, boxed Enum Type is used to break the ring of types.
     *
     * e.g.      *
     * struct S {
     *     let x:Option<S> = None
     * }
     *
     * the type of S's member x above is boxed EnumType, otherwise as struct and enum are both value type,
     * S will contain Option<S>, Option<S> contains S, S contains Option<S> again,
     * and infinite recursion of inclusion continues.
     */
    bool IsBoxed(CHIRBuilder& builder);
```

### 示例 3: CheckSancovOption
文件: `include/cangjie/CHIR/Transformation/SanitizerCoverage.h:41`

```cpp
bool CheckSancovOption(DiagAdapter& diag) const;

    // entry for different sanitizer coverage option
    void InjectTraceForCmp(BinaryExpression& binary, bool isDebug);
    void InjectTraceForSwitch(MultiBranch& mb, bool isDebug);
    void InsertCoverageAheadBlock(Block& block, bool isDebug);
    void InjectTraceMemCmp(Expression& expr, bool isDebug);
    // for switch trace
    RawArrayAllocate* CreateArrayForSwitchCaseList(MultiBranch& multiBranch);
    Intrinsic* CreateRawDataAcquire(const Expression& dataList, Type& elementType) const;

    // for memory compare IR generator
    std::vector<Value*> GenerateCStringMemCmp(const std::string& fuzzName, Value& oper1, Value& oper2, Apply& apply);
    std::vector<Value*> GenerateStringMemCmp(const std::string& fuzzName, Value& oper1, Value& oper2, Apply& apply);
    std::vector<Value*> GenerateArrayCmp(const std::string& fuzzName, Value& oper1, Value& oper2, Apply& apply);
    std::pair<Value*, Value*> CastArrayListToArray(Value& oper1, Value& oper2, Apply& apply);
    Expression* CreateOneCPointFromList(Value& array, Apply& apply, Type& elementType, Type& startType);
    std::pair<std::string, std::vector<Value*>> GetMemFuncSymbols(Value& oper1, Value& oper2, Apply& apply);

    Expression* CreateMemCmpFunc(const std::string& intrinsicName, Type& paramsType, const std::vector<Value*>& params,
```

## 概念关系图谱

- **同义词**: Option, Some, None, 可选类型, optional type, 空值安全, null safety, ?., ??
- **相关概念**: enum, pattern-match, null, 空值
- **相关模块**: codegen, driver, frontend, include, option, sema, unittests

## 常见问题

### option 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 option？

请参考下面的代码示例部分。

### option 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

