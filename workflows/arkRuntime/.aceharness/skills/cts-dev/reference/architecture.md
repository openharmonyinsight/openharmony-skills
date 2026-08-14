# ets2panda 编译器模块架构

## 整体编译流水线

```
Lexer → Parser → VarBinder → Checker → Lowering → Compiler/Core
          ↓          ↓          ↓          ↓
        AST构建    符号绑定   类型检查   AST变换(降级)
```

## 仓库级规则

- **Spec-first**: 行为以最新技术预览规范为准，测试/遗留行为不能作为与spec冲突的理由
- **审查阻断**: 无测试、实现spec外功能、移除assertion的patch均被阻断
- **调试辅助**: `node->DumpEtsSrc()`（AST dump）、`type->ToString()`（类型dump）、`sig->ToString()`（签名dump）
- **Phase调试**: `--dump-ets-src-after-phases=<PhaseName>` 查看phase后的AST

---

## Checker模块

### 职责

对绑定后的AST执行语义分析：类型检查、类型推断、类型转换和类型关系，以及ETS特有语义（可达性、赋值、装箱等），报告语义错误和警告。

### 修改范围

- **仅ETSChecker**: 实际修改仅涉及ETSChecker；TSChecker/JSChecker/ASchecker不在范围内
- **仅ETS语义**: 语义和类型相关变更仅适用于ETS路径

### 硬性约束：不改AST树

- **Checker不得变换AST树**（不能add/remove/replace/reparent节点）
- **Checker不得分配新AST节点**
- Checker更新限于语义元数据：设置节点类型信息和已解析的变量引用
- 遗留代码中变换AST树的已排期重构/移除

### 类型检查规则

- 使用`TypeRelation` API（`IsSupertypeOf`、`IsIdenticalTo`等）做子类型/兼容性/转换逻辑
- 不硬编码类型名（如`"escompat.Record"`），不用指针比较类型
- 涉及子类型语义时避免`Is<SomeType>`检查，通过`TypeRelation`表达规则
- 不引入新的checker状态标志作为变通逻辑
- spec和实现/测试分歧时，报告不一致并保持spec-first

### 目录结构

```
checker/
├── ETSchecker.*                    # ETS checker入口
├── ETSAnalyzer.cpp, ETSAnalyzer.h  # 每节点Check()入口
├── ETSAnalyzerHelpers.*            # ETSAnalyzer辅助
├── ETSAnalyzerUnreachable.cpp      # 不可达代码分析
├── ets/                            # ETS特有子模块
│   ├── function.cpp                # 函数调用、重载/签名选择
│   ├── arithmetic.*                # 算术表达式
│   ├── assignAnalyzer.*            # 赋值语义和活跃性
│   ├── aliveAnalyzer.*             # 活跃性/可达性
│   ├── boxingConverter.* / unboxingConverter.* / wideningConverter.*  # 装箱/拆箱/宽化
│   ├── typeConverter.* / conversion.* / typeCreation.*  # 类型转换和创建
│   ├── castingContext.* / typeRelationContext.*  # 转型和类型关系上下文
│   ├── object.cpp                  # 对象类型/字面量检查
│   ├── etsWarningAnalyzer.*        # ETS警告分析
│   ├── helpers.cpp / typeCheckingHelpers.cpp / validateHelpers.cpp  # 辅助函数
│   └── utilityTypeHandlers.cpp     # 工具类型(Partial, ReturnType等)
├── types/                          # 类型表示和关系
│   ├── ets/                        # ETS类型（原始、对象、联合、元组、函数等）
│   └── globalTypesHolder.* / signature.*
├── checkerContext.*                 # 共享checker上下文
├── typeChecker/                    # 类型检查核心
└── checker.*                       # 基类
```

### 扩展方式

- **新ETS类型**: 在`types/ets/`下添加类型类，接入`typeRelation`和ETSChecker
- **新ETS检查规则**: 在ETSAnalyzer/ETSChecker或`ets/`访问器中添加分支并报告诊断信息
- **新AST节点**: 在ETSAnalyzer.h通过`AST_NODE_MAPPING`声明`Check(ir::NodeType *node)`

---

## Parser模块

### 职责

将token流解析为AST，维护解析上下文和程序根节点。仅做语法解析，不做类型检查或符号解析。

### 修改范围

- **仅ETSParser和ETS解析逻辑**: TSParser/JSParser/ASParser不在范围内
- 新语法和功能首先在Parser中添加解析

### 类层次

```
ParserImpl                    # 基类；parserImpl.*被所有解析器共享
├── JSParser                  # JS
└── TypedParser               # 类型标注解析（共享）
    ├── ETSParser (final)     # ETS [主要修改目标]
    └── ThrowingTypedParser   # 解析失败时抛出异常
        ├── TSParser          # TS
        └── ASParser          # AS
```

- `parserImpl.cpp`的变更影响所有语言，修改时需考虑回归

### 错误类型

- **仅语法错误**: 无效token、语法违规、括号不匹配等
- **不报告语义错误**: 类型不匹配、未定义变量等由checker阶段报告

### 目录结构

```
parser/
├── ETSParser*.cpp              # [范围内] ETS表达式/语句/类型/类/枚举/命名空间/注解
├── *Parser*.cpp, *.h           # 各语言解析器入口
├── context/                    # 解析上下文
├── program/                    # 程序根、声明缓存
├── expressionParser.cpp        # 共享表达式解析
├── statementParser.cpp         # 共享语句解析
└── parserImpl.*                # 共享实现；修改影响所有语言
```

### Spec和AST耦合规则

- 解析器行为必须匹配最新技术预览规范的形式语法
- 语法存在但无对应AST节点、或有AST节点但无语法基础，需与前端owner确认
- 若parser bug导致无效AST通过验证，同步更新`ast_verifier/`

---

## Lowering模块

### 职责

将高级语法变换为低级语法（AST→AST）。解语法糖（lambda、语法糖等）在此实现。分为pre-checker和post-checker阶段。

### 目录结构

```
compiler/lowering/
├── phase.* / checkerPhase.* / plugin_phase.*  # Phase框架和插件
├── resolveIdentifiers.* / scopesInit/         # 标识符解析和作用域初始化
├── util.* / util-inl.h / phase_id.h           # 工具和Phase ID
└── ets/                         # ETS特有lowering
    ├── *Lowering.cpp/h          # 字面量/lambda/枚举/optional/rest/spread/装箱等
    ├── *Phase.cpp/h             # CFG构建/解构/声明生成/原始类型转换等
    └── topLevelStmts/           # 顶层语句处理
```

### 创建AST节点方式

| 方式 | 说明 | 典型用途 |
|------|------|----------|
| `ArenaAllocator::New<T>(...)` | 静态分配器分配节点 | Identifier、OpaqueTypeNode |
| `ctx->AllocNode<T>(...)` | 通过Context/Checker分配器分配 | arrayLiteralLowering等 |
| `parser->CreateFormattedExpression(str, nodes)` | 模板字符串→AST | 完整语句/表达式生成 |
| `Gensym(allocator)` | 唯一临时标识符节点 | 配合CreateFormatted*使用 |

### Re-bind和Re-check

Post-checker阶段创建新AST节点后，必须执行scope setup、标识符绑定和类型检查：

| 方法 | 使用场景 |
|------|----------|
| `CheckLoweredNode(varBinder, checker, node)` | 全新子树：完整bind+check |
| `BindLoweredNode(varBinder, node)` | 仅绑定，不类型检查 |
| `Rebind(phaseManager, varBinder, node)` | 已有节点：清除后重新绑定 |
| `Recheck(phaseManager, varBinder, checker, node)` | 已有节点：完整re-bind+re-check |

### Phase分类

1. **Core**: TopLevelStatements, InitScopesPhaseETS, ResolveIdentifiers, CheckerPhase
2. **Desugaring**: DefaultParametersLowering, OptionalLowering, SpreadConstructionPhase, RestArgsLowering等
3. **Code injection**: UnboxPhase, BoxingForLocals, ArrayLiteralLowering, ObjectLiteralLowering, UnionLowering
4. **Restructuring**: LambdaConversionPhase, AsyncMethodLowering, EnumLoweringPhase, GenericBridgesPhase
5. **Special**: ConstantExpressionLowering, DynamicImport, RelaxedAnyLoweringPhase等
6. **Language features**: ObjectIndexLowering, ObjectIteratorLowering, LateInitializationConvert

### Phase放置规则

- **Before checker**: 仅限不需要推断类型的语法脱糖和结构简化
- **After checker**: 用于依赖类型的变换；创建/重写的子树需re-bind/re-check
- 若lowering仅重写函数体不改外部声明，优先body-only策略（`PhaseForBodies`）

## 模块依赖关系

```
Lexer → Parser → VarBinder → Checker → Lowering → Compiler/Core
                    ↑           ↑          ↑
                  parser/ir    varbinder  checker
                               parser/ir  varbinder
                                          ir/util
```
