# ArkTS 静态语法生成约束

> **模块信息**
> - 层级：L2_Generation
> - 子模块：generator/
> - 用途：定义 ArkTS-Sta 静态项目测试代码生成时必须遵循的 ArkTS 静态语法约束
> - 来源：提取自 arkts-static-spec 技能
> - 适用条件：仅当目标语法类型为 ArkTS-Sta（静态项目）时加载

---

ArkTS 静态语法与动态语法有本质区别，生成的测试代码必须遵循以下约束，否则无法通过编译。详细的语法规范参考见 `arkts-static-spec` 技能，本文件只列出与测试代码生成直接相关的约束。

---

## 1. 类型强制要求

### 1.1 禁止 `any` 和 `unknown`

所有变量、参数、返回值必须有显式类型声明，禁止使用 `any` 或 `unknown`。（ArkTS-Sta 编译器会拒绝包含 any/unknown 的代码，直接报编译错误 `Type 'any' is not allowed`，无法生成 HAP）

```typescript
let player: media.AVPlayer | null = null
let fd: number = -1
let result: string = await someFunction()
```

```typescript
let player: any = null
let result = await someFunction()
```

### 1.2 禁止隐式类型推断的边界场景

虽然 ArkTS 支持类型推断，但在测试代码中建议显式标注类型，避免推断歧义。

### 1.3 catch 参数必须标注类型

```typescript
try {
    await player.play()
} catch (error) {
    expect(error.code).assertEqual(5400102)
}
```

注意：当前 ArkTS 静态编译器对 catch 参数类型推断较为宽松，但建议保持与动态语法一致的写法。

---

## 2. 变量声明

### 2.1 禁止 `var`，只使用 `let` 和 `const`

```typescript
let count: number = 0
const TAG: string = 'AVPlayerTest'
```

```typescript
var count = 0
```

### 2.2 字段必须初始化

所有成员变量在声明时必须赋初值。

```typescript
let avPlayer: media.AVPlayer | null = null
let fd: number = -1
let isPrepared: boolean = false
```

```typescript
let avPlayer: media.AVPlayer
let fd: number
```

---

## 3. 不支持的语法特性

### 3.1 禁止对象解构

```typescript
let width: number = rect.width
let height: number = rect.height
```

```typescript
let { width, height } = rect
```

### 3.2 禁止 `in` 运算符

```typescript
if (obj instanceof MyClass) { ... }
```

```typescript
if ("property" in obj) { ... }
```

### 3.3 禁止 `Symbol()`、私有 `#` 标识符

不使用 `Symbol()` 和 `#privateField` 语法。

### 3.4 禁止 `require`

```typescript
import media from '@ohos.multimedia.media'
```

```typescript
const media = require('@ohos.multimedia.media')
```

### 3.5 禁止 `as` 类型断言（除 `as any` 外的其他类型断言也应注意）

```typescript
// ✅ 正确：使用类型守卫
let item = container.get(0)
if (typeof item === 'string') {
  expect(item).assertEqual('expected')
}
```

```typescript
// ❌ 反模式：用 as 强制类型转换
let result = api.method() as MyCustomType

// ❌ 反模式：双重 as 断言（等同于 as any）
let value = data as unknown as TargetType
```

### 3.6 禁止计算属性名

```typescript
obj.propertyName = value
```

```typescript
let key: string = 'propertyName'
obj[key] = value  // ArkTS 静态模式不支持动态属性访问
```

### 3.7 禁止 `arguments` 对象

```typescript
function testHelper(...args: string[]) {
  for (let i = 0; i < args.length; i++) {
    console.log(args[i])
  }
}
```

```typescript
function testHelper() {
  let args = arguments  // ArkTS 静态模式不支持
}
```

### 3.8 禁止 `for...in` 循环

```typescript
let keys = Object.keys(obj)
for (let i = 0; i < keys.length; i++) {
  console.log(keys[i])
}
```

```typescript
for (let key in obj) {  // 禁止：与 3.2 节 in 运算符禁用规则一致
  console.log(key)
}
```

---

## 4. 类型不匹配是编译错误（非运行时错误）

这是静态项目测试生成的**最重要区别**：

- **动态语法**：传入错误类型的参数 → 运行时抛出 401 错误码
- **静态语法**：传入错误类型的参数 → **编译失败**，无法生成 HAP

**因此：静态项目不生成 ERROR_401（参数类型错误）测试用例——因为类型错误在静态编译时已由编译器拦截，运行时永远不会触发 401，生成此类测试必然失败。**

应该测试的内容：
- 有效类型范围内的边界值
- 类型兼容的显式转换
- 运行时逻辑错误码（如 5400102 操作不支持、801 能力未启用等）

```typescript
it('playbackRateBoundaryTest001', ..., async (done) => {
    await prepareAndPlay(avPlayer)
    avPlayer.rate = media.PlaybackSpeed.SPEED_FORWARD_2_00_X
    expect(avPlayer.rate).assertEqual(media.PlaybackSpeed.SPEED_FORWARD_2_00_X)
    done()
})
```

```typescript
it('invalidTypeErrorTest001', ..., async (done) => {
    avPlayer.rate = "invalid" as any
    expect(error.code).assertEqual(401)
    done()
})
```

---

## 5. 数值语义注意

ArkTS 静态语法中整数除法结果为整数：

```typescript
let result: number = 1 / 2  // 结果为 0，不是 0.5
```

在测试边界值时注意此差异。

---

## 6. 导入和模块

使用标准 ES6 import/export，不使用 `export =` 或 `import m = require()`。

```typescript
import { describe, it, expect } from '@ohos/hypium'
import media from '@ohos.multimedia.media'
import { BusinessError } from '@kit.BasicServicesKit'
import fileIO from '@ohos.fileio'
```

---

## 7. 访问修饰符

测试代码中不需要使用访问修饰符（`private`/`protected`），保持简洁即可。辅助函数使用顶层函数声明。
