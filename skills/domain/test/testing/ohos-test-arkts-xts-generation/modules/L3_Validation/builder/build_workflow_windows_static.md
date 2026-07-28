# Windows 静态编译工作流

> **动态编译**: `build_workflow_windows_compile.md`
> **完整 Windows 工作流**: `build_workflow_windows.md`

---

## 十、ArkTS 静态 XTS 编译流程（arkts-sta）

> **本章适用场景**：当用户明确提到"arkts-sta"、"arkts静态"、"ArkTS静态"、"静态xts"等关键词，或者工程配置了 `arkTSVersion: "1.2"` 时使用本章流程。

### 10.1 静态编译模式概述

ArkTS 静态 XTS 编译模式是针对 ArkTS 静态强类型语法的编译流程，具有以下特点：

- **严格类型检查**：所有变量和函数必须有明确的类型注解
- **静态规范约束**：遵守 ArkTS 静态语言规范（禁止 any、禁止对象解构等）
- **Java 环境依赖**：需要配置 JAVA_HOME 环境变量
- **特殊编译参数**：使用静态模式特定的编译参数

### 10.2 环境准备

#### 10.2.1 检查工程类型

首先确认工程是否为静态模式：

```powershell
# 检查 build-profile.json5 中的 arkTSVersion 配置
Get-Content "build-profile.json5" | Select-String "arkTSVersion"
```

**静态工程特征**：
- `build-profile.json5` 中包含 `"arkTSVersion": "1.2"` 或更高版本
- 工程使用 ArkTS 静态语法规范
- 编译时会进行严格的静态类型检查

#### 10.2.2 Java 环境配置（必需）

静态编译必须配置 Java 环境：

```powershell
# 方法1：临时设置（当前 PowerShell 会话）
$env:JAVA_HOME = "{deveco_studio_path}\jbr"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH

# 验证 Java 安装
java -version

# 预期输出示例：
# openjdk version "11.0.15" 2022-04-19
# OpenJDK Runtime Environment (build 11.0.15+10)
```

**⚠️ 重要**：静态编译过程中，hvigorw 需要调用 Java 编译器，如果 JAVA_HOME 未配置会导致 `spawn java ENOENT` 错误。

#### 10.2.3 Node.js 环境配置

```powershell
# 检查 Node.js 版本
node --version

# 预期输出：v14.x 或更高
```

### 10.3 静态编译流程

#### 10.3.1 直接使用 hvigorw 命令

```powershell
# 进入项目目录，设置 JAVA_HOME（同 10.2.2），然后执行
cd C:\Users\{username}\Desktop\xts_demo_1
"{hvigor_path}\hvigorw.bat" assembleHap --mode module -p module=entry -p product=default
```

### 10.4 编译输出示例

**成功输出**：

```
> hvigor UP-TO-DATE :entry:default@PreBuild...
> hvigor Finished :entry:default@CompileResource... after 378 ms
> hvigor Finished :entry:default@CompileArkTSEvolution... after 15 s 234 ms
> hvigor Finished :entry:default@SignHap... after 209 ms
> hvigor BUILD SUCCESSFUL in 18 s 451 ms
```

**关键差异**：
- 静态编译通常比动态编译慢（需要额外的类型检查）
- `CompileArkTSEvolution` 阶段耗时更长（静态类型检查）
- 静态测试套使用 `default` target 而非 `ohosTest`

### 10.5 静态类型检查

静态编译会自动执行以下类型检查：

#### 10.5.1 类型注解完整性检查

```typescript
// ✅️ 正确 - 显式类型注解
function add(a: number, b: number): number {
  return a + b;
}

// ❌ 错误 - 缺少类型注解（静态模式下会报错）
function add(a, b) {
  return a + b;
}
```

#### 10.5.2 禁止 any 类型检查

```typescript
// ❌ 错误 - 静态模式禁止使用 any
let data: any = getSomeData();

// ✅️ 正确 - 使用具体类型（静态模式也禁止 unknown，必须使用具体类型）
let data: string = getSomeData();
// 或使用联合类型
let data: string | null = getSomeData();
```

#### 10.5.3 字段初始化检查

```typescript
// ✅️ 正确 - 所有字段都初始化
class Person {
  name: string = "";
  age: number = 0;
}

// ❌ 错误 - 字段未初始化
class Person {
  name: string;
  age: number;
}
```

### 10.6 常见编译错误及解决方案

#### 错误1：spawn java ENOENT

**症状**：
```
Error: spawn java ENOENT
```

**原因**：Java 不在 PATH 环境变量中

**解决方案**：按 10.2.2 配置 JAVA_HOME，或使用 10.3.1 的 PowerShell 脚本（已内含环境配置）。

#### 错误2：类型检查错误

**症状**：
```
Type 'any' is not allowed in ArkTS static mode
Type 'string' is not assignable to type 'number'
```

**原因**：违反 ArkTS 静态类型规范

**解决方案**：
1. 检查是否使用了 `any` 类型
2. 确保所有函数参数和返回值都有类型注解
3. 验证类型兼容性
4. 参考：`ohos-dev-arkts-static-specification-reference` 技能目录下的规范文档

#### 错误3：字段未初始化

**症状**：
```
Property 'xxx' has no initializer and is not definitely assigned
```

**解决方案**：
```typescript
// 添加默认值或使用构造函数初始化
class MyClass {
  // 方法1：添加默认值
  field: string = "";

  // 方法2：构造函数初始化
  constructor() {
    this.field = "";
  }
}
```

### 10.7 测试执行

静态编译成功后，测试执行流程与动态模式相同。

### 10.8 完整自动化脚本

创建 `build_and_test_static.ps1`：

```powershell
<#
.SYNOPSIS
    ArkTS 静态 XTS 测试完整自动化脚本
.DESCRIPTION
    包含静态编译的完整流程
#>

param(
    [string]$ProjectPath = (Get-Location).Path,
    [string]$BundleName = "com.example.myapplication"
)

# 1. 配置环境
Write-Host "`n[环境准备] 配置 Java 和 Node.js 环境..." -ForegroundColor Yellow
$env:JAVA_HOME = "{deveco_studio_path}\jbr"
$env:PATH = "$env:JAVA_HOME\bin;{deveco_studio_path}\tools\node;" + $env:PATH

# 2. 静态编译
Write-Host "`n[1/2] 执行 ArkTS 静态编译..." -ForegroundColor Yellow
Set-Location $ProjectPath

& "{deveco_studio_path}\tools\node\node.exe" "{hvigor_path}\hvigorw.js" `
  assembleHap `
  --mode module `
  -p module=entry `
  -p product=default `
  --analyze=normal `
  --parallel `
  --incremental `
  --no-daemon

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 编译失败" -ForegroundColor Red
    exit 1
}

Write-Host "`n[2/2] 验证编译产物..." -ForegroundColor Yellow
$TestHap = Get-ChildItem "entry\build\default\outputs" -Recurse -Filter "*.hap" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($TestHap) {
    Write-Host "✓ Test HAP 已生成: $($TestHap.Name)" -ForegroundColor Green
} else {
    Write-Host "✗ Test HAP 未找到" -ForegroundColor Red
    exit 1
}

Write-Host "`n✓ ArkTS 静态编译完成" -ForegroundColor Green
```

### 10.9 静态与动态编译对比

| 特性 | 动态模式 | 静态模式 |
|------|---------|---------|
| **类型检查** | 运行时检查 | 编译时严格检查 |
| **any 类型** | 允许 | **禁止** |
| **类型注解** | 可选 | **必需** |
| **字段初始化** | 可延迟 | **必须初始化** |
| **编译速度** | 较快 | 稍慢（额外类型检查） |
| **代码安全性** | 中等 | **高** |
| **Java 环境** | 可选 | **必需** |
| **适用场景** | 快速开发、原型 | 生产代码、严格规范 |

### 10.10 最佳实践

#### 10.10.1 开发流程

```
1. 编写测试代码
   ↓
2. 本地类型检查（IDE 实时提示）
   ↓
3. 静态编译验证
   ↓
4. 修复类型错误（如有）
```

#### 10.10.2 代码规范

1. **始终使用显式类型注解**
2. **禁止使用 `any` 和 `unknown`**，必须使用具体类型或联合类型
3. **初始化所有字段**
4. **使用类型守卫**进行类型收窄
5. **遵循 ArkTS 静态规范**

#### 10.10.3 性能优化

- **增量编译**：使用 `--incremental` 参数加速重复编译
- **并行编译**：使用 `--parallel` 参数利用多核
- **缓存优化**：避免频繁清理构建产物
