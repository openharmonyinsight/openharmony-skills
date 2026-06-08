# 格式化和规范验证

> **模块信息**
> - 层级：L3_Validation
> - 子模块：validator/
> - 优先级：必须加载（Phase 7 不可跳过）
> - 依赖：references/conventions/, L2_Generation/generator/

---

## 一、模块概述

本模块负责 Phase 7 步骤 A 的**生成上下文检查**——验证生成阶段特有的质量项。

代码质量深度检查（@tc 格式、命名规范、断言方法等 17 条规则）由 `ohos-test-xts-code-quality` 技能在 Phase 7 步骤 B 中执行，不在本模块中重复。

### 1.1 核心职责

1. **许可证头验证**: 确保包含 Apache 2.0 许可证头
2. **导入语句验证**: 确保 hypium 和被测模块导入正确
3. **资源释放验证**: 确保 afterEach/afterAll 正确释放资源
4. **类型安全验证**: 确保不使用 `as any`
5. **设计文档验证**: 确保每个测试用例都有对应的设计文档
6. **done() 完整性验证**: 确保异步测试所有分支都调用了 done()
7. **分支断言覆盖验证**: 确保所有代码分支都有断言
8. **空 describe 块验证**: 确保所有 describe 块至少包含一个 it()

---

## 二、许可证头验证

文件顶部必须包含 Apache 2.0 许可证头：

```typescript
/*
 * Copyright (C) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

---

## 三、导入语句验证

### 3.1 hypium 导入验证

```typescript
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level } from '@ohos/hypium';
```

确认导入了实际使用的符号（如未使用 `beforeAll` 则不必导入，但 `describe`、`it`、`expect` 必须导入）。

### 3.2 被测模块导入验证

确认导入了正确的被测模块，与 Phase 3 解析的 API 来源一致。常见格式：

```typescript
import media from '@ohos.multimedia.media';
import { BusinessError } from '@kit.BasicServicesKit';
```

### 3.3 未使用的导入

检查是否存在导入但未使用的符号。

---

## 四、资源释放验证

### 4.1 afterEach 资源释放

（未释放的资源会在后续用例中累积：播放器占用硬件解码器导致新用例无法创建播放器，文件描述符耗尽导致系统级错误，设备最终需要重启才能恢复）

- 播放器等对象在 afterEach 中调用 `release()`
- 文件描述符在 afterEach 中调用 `closeSync()`
- 释放逻辑使用 try-catch 包裹
- 资源变量初始值设为 null/-1，释放后重置

```typescript
afterEach(() => {
    if (avPlayer !== null) {
        try {
            avPlayer.release();
        } catch (e) {
            console.error(TAG + ` release error: ${e}`);
        }
        avPlayer = null;
    }
    if (fd > 0) {
        try {
            fileIO.closeSync(fd);
        } catch (e) {
            console.error(TAG + ` close fd error: ${e}`);
        }
        fd = -1;
    }
});
```

### 4.1.1 资源释放分级原则

> **afterEach vs afterAll 分级释放**：
> - **afterEach**：释放每个用例独立创建的资源（播放器实例、文件描述符、数据库连接）
> - **afterAll**：释放整个套件共享的资源（Driver 实例、全局数据库）
>
> 禁止在 `it()` 内部释放资源（异常时不会执行），禁止所有资源都在 `afterAll` 释放（用例间泄漏）。

```typescript
// ❌ 反模式1：在 it() 内部释放（异常时不执行）
it('testPlay001', Level.LEVEL1, async (done: Function) => {
  let player = await media.createAVPlayer();
  await player.play();
  await player.release();  // 如果 play() 抛异常，release 不会执行
  done();
});

// ❌ 反模式2：afterEach 中释放 afterAll 级别资源
afterEach(() => {
  if (driver !== null) {
    // Driver 使用完成后自动销毁，无需手动关闭
    driver = null;
  }
});
```

### 4.2 null/undefined 安全检查

- 对象使用前先创建/初始化
- 文件描述符关闭前检查有效性（fd > 0）

---

## 五、类型安全验证

### 5.1 禁止 as any

不使用 `as any` 绕过类型检查。null 和 undefined 可以直接传入，不需要类型转换。

```typescript
// 禁止
let player = await media.createAVPlayer() as any;
```

### 5.2 deprecated API 处理

不使用已废弃的 API（如 AudioPlayer、VideoPlayer），使用推荐的替代 API（如 AVPlayer）。

---

## 六、设计文档验证

### 6.1 一一对应关系

每个测试用例都有对应的测试设计文档条目（`{测试文件名}.design.md`）。

### 6.2 内容一致性

设计文档中的测试步骤、预期结果与代码实现一致。

---

## 七、done() 完整性验证

### 7.1 异步测试 done() 检查

- 所有 `async (done: Function)` 的 `.then` 和 `.catch` 分支都调用了 `done()`
- `done()` 没有被多次调用
- 回调风格 API 的 `done()` 在回调内部调用（不是外部）

### 7.2 分支断言覆盖检查

- 每个 try-catch 块的 try 分支包含 `expect().assertFail()`
- if-else 分支中所有路径都有断言
- 没有"空"代码路径（既无断言也无 assertFail）

### 7.3 空 describe 块检查

- 所有 `describe` 块至少包含一个 `it()` 调用
- 不存在只有注释没有实际用例的 `describe` 块

## 八、验证报告格式

```markdown
# 验证报告

## 步骤 A: 生成上下文检查

- [ ] Apache 2.0 许可证头
- [ ] @ohos/hypium 导入正确
- [ ] 被测模块导入正确
- [ ] 无未使用的导入
- [ ] afterEach/afterAll 资源释放完整
- [ ] null/undefined 安全检查
- [ ] 无 as any 类型断言
- [ ] 无 deprecated API
- [ ] 设计文档一一对应
- [ ] ArkTS 语法规范
- [ ] 异步测试 done() 各分支完整
- [ ] try-catch 分支断言覆盖完整
- [ ] 无空 describe 块

## 步骤 B: ohos-test-xts-code-quality 深度扫描

- 扫描规则: R002,R003,R004,R008,R009,R013,R015,R016,R018,R022,R023,R024,R025,R026,R027,R028,R029
- 扫描结果: {通过/失败} ({issue数} issues)
```

---

**更新日期**: 2026-04-21
**版本**: 2.0.0 - 精简为生成上下文检查，代码质量扫描委托给 ohos-test-xts-code-quality
