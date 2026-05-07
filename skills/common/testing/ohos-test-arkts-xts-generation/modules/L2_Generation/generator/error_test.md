# 错误码测试规则与示例

> **模块信息**
> - 层级：L2_Generation/generator
> - 优先级：按需加载
> - 适用范围：错误码测试用例生成
> - 父模块：`test_generator.md`

---

## 一、错误码速查表

### 1.1 通用错误码

| 错误码 | 含义 | 典型场景 | 可触发 |
|--------|------|---------|--------|
| 201 | 权限拒绝 | 无权限或权限被撤销 | ❌ 通常不可触发（XTS 已配置权限） |
| 202 | 方法不存在 | 非系统应用调用系统 API | ❌ 通常不可触发（XTS 是系统应用） |
| 301 | 重定向 | ExtensionAbility | 视情况 |
| 401 | 参数错误 | 参数校验失败 | ✅ 通常可触发（传 null/undefined/无效类型） |
| 501 | 业务错误 | API 特定业务逻辑 | 视情况 |
| 801 | 能力不支持 | L1 级 API、设备不支持 | ⚠️ 需特定设备能力 |
| 804 | 设备差异 | 特定设备特有行为 | ⚠️ 需特定设备 |
| 901 | 跨平台不支持 | ArkUI-X 跨平台限制 | 视情况 |

### 1.2 错误码范围分类

| 范围 | 类别 |
|------|------|
| 2XX | 成功/处理中 |
| 3XX | 重定向 |
| 4XX | 客户端错误 |
| 5XX | 服务端错误 |
| 8XX | 特性不支持 |
| 9XX | 跨平台/特殊场景 |

---

## 二、错误码提取原则

> **重要**：必须从 API 的 `@throws` 标记中提取**实际的错误码**，而不是假设所有参数错误都抛出 401。（假设错误码会导致断言值与实际运行时错误码不匹配，测试必然 fail 且无法通过修改测试代码解决——必须使用正确的错误码）

从 `@throws` 标记中提取错误码及其触发条件：

```typescript
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types.
 * @throws { BusinessError } 10200010 - Container is empty.
 * @throws { BusinessError } 8300001 - Invalid parameter value.
 */
method(param: ParamType): ReturnType;
```

**解析原则**：
1. 读取 `.d.ts` 文件中该 API 的 `@throws` 标记
2. 提取所有声明的错误码及其触发条件
3. 根据触发条件设计测试场景
4. 每个错误码生成对应的测试用例

> **重要：使用正确的 hypium 断言方法**
> - 断言规范详见 `references/conventions/hypium_framework.md` 第九章
> - 核心规则：使用 `assertEqual` 明确断言错误码，禁止使用不存在的 `assertLessThanOrEqual`

**错误码参考**：
- **通用错误码**：`docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`
- **子系统特有错误码**：`docs/zh-cn/application-dev/reference/apis-xxx/errorcode-xxx.md`

---

## 三、错误码测试模板

```typescript
/**
 * @tc.name test{MethodName}Error{Code}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{CODE}_0001
 * @tc.desc 测试 {API} 的 {method} 方法 - 错误码 {code}：{触发条件}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Error{Code}0001', Level.LEVEL2, () => {
  let errCode{CodeName} = {Code};
  try {
    let apiObject = new APIName();
    // 设置会触发错误码的状态或参数（根据 @throws 中的触发条件）
    apiObject.methodName(invalidParam);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(errCode{CodeName});
  }
});
```

---

## 四、错误码测试示例

### 4.1 参数错误 (401)

```typescript
/**
 * API 声明：
 * @throws { BusinessError } 401 - Parameter error.
 */
function popFirst(): T;

/**
 * @tc.name testPopFirstError401001
 * @tc.number SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_001
 * @tc.desc 测试 TreeSet 的 popFirst 方法 - 容器为空时抛出 401
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testPopFirstError401001', Level.LEVEL2, () => {
  let treeSet = new TreeSet<number>();
  let errCodeParamError = 401;

  try {
    let result = treeSet.popFirst();
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(errCodeParamError);
  }
});
```

### 4.2 子系统特有错误码

```typescript
/**
 * API 声明：
 * @throws { BusinessError } 10200010 - Container is empty.
 */
function popLast(): T;

/**
 * @tc.name testPopLastError10200010001
 * @tc.number SUB_UTILS_UTIL_TREESET_POPLAST_ERROR_10200010_001
 * @tc.desc 测试 TreeSet 的 popLast 方法 - 容器为空时抛出 10200010
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testPopLastError10200010001', Level.LEVEL2, () => {
  let treeSet = new TreeSet<number>();
  let errCodeContainerEmpty = 10200010;

  try {
    let result = treeSet.popLast();
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(errCodeContainerEmpty);
  }
});
```

### 4.3 多种错误码

```typescript
/**
 * API 声明：
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 2100001 - Invalid parameter value.
 */
function createNetConnection(): void;

it('testCreateNetConnectionError401001', Level.LEVEL2, () => {
  let errCodeParamError = 401;
  try {
    let connection = connection.createNetConnection(invalidParam);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(errCodeParamError);
  }
});
```

---

## 五、参数测试中的错误码处理

对于 null/undefined 等异常参数，**必须根据 API 的 @throws 标记确定实际的错误码**：

```typescript
// ✅ 正确：从 @throws 提取错误码，使用 assertEqual 明确断言
/**
 * API 声明：
 * @throws { BusinessError } 401 - Parameter error.
 */
it('testAddStringNull003', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  let errCodeParamError = 401;
  try {
    treeSet.add(null);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(errCodeParamError);
  }
});
```

---

## 六、错误码测试反模式（重要！）

> **以下模式会导致无效测试，严格禁止**：

```typescript
// ❌ 反模式1：try 块中忘记 expect().assertFail()
// 如果 api.method 没有抛异常，测试会静默通过（无效测试）
it('testError401', Level.LEVEL2, () => {
  try {
    api.method(invalidParam);
    // 缺少 expect().assertFail()！异常未抛出时测试静默通过
  } catch (error) {
    expect(error.code).assertEqual(401);
  }
});

// ❌ 反模式2：catch 块为空或只有 console.log（吞掉异常）
it('testError401', Level.LEVEL2, () => {
  try {
    api.method(invalidParam);
    expect().assertFail();
  } catch (error) {
    console.log('error: ' + error);  // 不是断言！测试永远"通过"
  }
});

// ❌ 反模式3：生成无法触发的错误码测试
// 错误码 201 在 XTS 测试环境中通常已配置权限，无法触发
it('testError201', Level.LEVEL2, () => {
  try {
    api.method();
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(201);  // XTS 环境已有权限，永远不会执行到这里
  }
});
```

> **错误码可触发性判断**：
> - 401（参数错误）：通常可触发（传 null/undefined/无效类型）
> - 201（权限被拒绝）：XTS 测试通常已配置权限，**通常不可触发**
> - 202（非系统应用调用系统API）：XTS 测试通常是系统应用，**通常不可触发**
> - 801（API 不支持）：需要特定设备能力，**视情况可触发**
> - 子系统特有错误码：需要具体分析触发条件是否可在测试环境构造

> 完整的错误码断言规范（包括正确/错误示例）见 `references/conventions/hypium_framework.md` 第九章。
