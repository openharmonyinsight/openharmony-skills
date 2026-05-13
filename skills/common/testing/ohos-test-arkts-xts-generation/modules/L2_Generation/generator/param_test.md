# 参数/返回值/边界值测试规则与示例

> **模块信息**
> - 层级：L2_Generation/generator
> - 优先级：按需加载
> - 适用范围：参数测试、返回值测试、边界值测试
> - 父模块：`test_generator.md`

---

## 一、参数测试规则

### 1.1 参数类型测试规则表

| 参数类型 | 必须测试的场景 | 生成的测试用例数 |
|---------|---------------|----------------|
| **string** | 正常值、空字符串、null、undefined、超长字符串 | 5-6 个 |
| **number** | 正数、负数、0、null、undefined、边界值 | 6-7 个 |
| **boolean** | true、false、null、undefined | 4 个 |
| **枚举** | 每个枚举值、null、undefined、无效值 | 枚举值+2 个 |
| **数组** | 空数组、非空数组、null、undefined、边界长度 | 5-6 个 |
| **对象** | 正常对象、null、undefined、缺少属性、类型错误 | 5-6 个 |

### 1.2 字符串参数格式测试

字符串参数除常规场景外，还应根据参数含义测试特定格式（API 文档或参数名可推断格式类型）：

| 格式 | 示例 |
|------|------|
| URI | `"file://xxx"` |
| URL | `"https://xxx"` |
| 颜色 | `"#AARRGGBB"` |
| MAC | `"00:11:22:33:44:55"` |
| 日期 | `"yyyy-mm-dd"` |
| Email | 标准格式 |
| UUID | 标准格式 |

### 1.3 数值参数边界策略

- **有范围 [m, n]**：测试 m-1, m, m+1, n-1, n, n+1
- **无范围**：测试 0, 正数, 负数, Infinity, -Infinity
- **特殊值**：null, undefined 需单独测试

### 1.4 布尔参数测试

必须覆盖 true、false、null/undefined 三种情况：

```typescript
customScan.setAutoZoomEnabled(true)
customScan.setAutoZoomEnabled(false)
customScan.setAutoZoomEnabled(null)  // 可能 crash，需验证
```

### 1.5 数组/集合参数测试

- 空数组测试：`addAll([])` → 返回 false
- 边界：0 个元素、1 个元素、最大值
- null/undefined 单独测试

### 1.6 联合类型参数测试

必须覆盖所有类型分支：

```typescript
// 参数类型: number | Record<number, number>
setBlur(0.3)                // number 分支
setBlur({5: 0.1, 10: 0.4}) // Record<number, number> 分支
```

---

## 二、参数测试模板

### 2.1 通用模板

```typescript
/**
 * @tc.name {MethodName}{ParamType}{Scenario}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_{PARAM}_{SCENARIO}_0001
 * @tc.desc 测试 {API} 的 {method} 方法 - {scenario}场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}{ParamType}{Scenario}0001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
  let apiObject = new APIName();
  let paramValue = /* 根据场景设置 */;

  let result = apiObject.methodName(paramValue);

  expect(result).assertEqual(expectedValue);
});
```

### 2.2 string 类型示例

```typescript
// 正常值
it('testAddStringNormal001', Level.LEVEL1, () => {
  let treeSet = new TreeSet<string>();
  let result = treeSet.add("hello");
  expect(result).assertTrue();
});

// 空字符串
it('testAddStringEmpty002', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  let result = treeSet.add("");
  expect(result).assertTrue();
});

// null - 必须根据 API 的 @throws 标记确定实际的错误码
it('testAddStringNull003', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  try {
    treeSet.add(null);  // ✅ 直接传入 null，不使用 as any
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual({actualErrorCode});  // 从 @throws 标记中提取
  }
});

// undefined
it('testAddStringUndefined004', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  try {
    treeSet.add(undefined);  // ✅ 直接传入 undefined，不使用 as any
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual({actualErrorCode});  // 从 @throws 标记中提取
  }
});
```

### 2.3 number 类型示例

```typescript
// 正常值
it('testAddNumberNormal001', Level.LEVEL1, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(100);
  expect(result).assertTrue();
});

// 零值
it('testAddNumberZero002', Level.LEVEL1, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(0);
  expect(result).assertTrue();
});

// 负数
it('testAddNumberNegative003', Level.LEVEL1, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(-100);
  expect(result).assertTrue();
});

// 边界值
it('testAddNumberBoundary004', Level.LEVEL2, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(Number.MAX_SAFE_INTEGER);
  expect(result).assertTrue();
});
```

---

## 三、返回值测试

### 3.1 返回值类型验证模板

```typescript
// 基础类型
it('test{MethodName}Return001', Level.LEVEL1, () => {
  let apiObject = new APIName();
  let result = apiObject.methodName();

  expect(typeof result).assertEqual('string');
  expect(result).assertEqual(expectedValue);
});

// 联合类型
it('test{MethodName}Return002', Level.LEVEL1, () => {
  let apiObject = new APIName();
  let result = apiObject.methodName();

  if (result !== null && result !== undefined) {
    expect(typeof result).assertEqual('string');
    expect(result.length).assertLarger(0);
  }
});

// Promise 类型
it('test{MethodName}Return003', Level.LEVEL1, async (done: Function) => {
  let apiObject = new APIName();

  apiObject.methodName()
    .then((result) => {
      expect(result).assertEqual(expectedValue);
      done();
    })
    .catch((error: BusinessError) => {
      expect().assertFail();
      done();
    });
});
```

### 3.2 返回值测试场景

| 返回值类型 | 测试场景 |
|-----------|---------|
| string | 返回空字符串、返回非空字符串、返回特定格式 |
| number | 返回0、返回正数、返回负数、返回边界值 |
| boolean | 返回 true、返回 false |
| 数组 | 返回空数组、返回单元素数组、返回多元素数组 |
| 对象 | 返回 null、返回包含所有属性的对象、返回部分属性的对象 |
| T \| undefined | 返回有效值、返回 undefined |

### 3.3 异步模式选择（先选模式，再看反模式避坑）

根据 API 的 `.d.ts` 签名直接确定测试写法：

| API 特征 | 识别方式 | 测试模式 | done() 要求 |
|----------|---------|---------|-------------|
| 返回 `Promise<T>` | 返回类型含 Promise | `async/await`（推荐） | 不需要 done 参数 |
| 接受 callback 参数 | 参数列表含函数类型 `(result: T) => void` | callback + done() | done() 在 callback 内部调用 |
| 事件监听 | 方法名含 `on`/`subscribe`，或参数是 `Callback<T>` | 事件回调 + done() | done() 在事件回调内部调用 |
| 同步方法 | 返回非 Promise 类型，无 callback 参数 | 同步 | 不使用 done，不使用 async |

```typescript
// 模式 A：返回 Promise<T> → async/await，无 done
it('testPromise001', Level.LEVEL1, async () => {
  let result = await api.asyncMethod(param);
  expect(result).assertEqual(expected);
});

// 模式 B：接受 callback → done() 在 callback 内部
it('testCallback001', Level.LEVEL1, async (done: Function) => {
  api.method(param, (result) => {
    expect(result).assertEqual(expected);
    done();
  });
});

// 模式 C：事件监听 → done() 在事件回调内部
it('testEvent001', Level.LEVEL1, async (done: Function) => {
  emitter.on('event', (data) => {
    expect(data).assertEqual(expected);
    done();
  });
  emitter.emit('event', testData);
});

// 模式 D：同步 → 不用 async，不用 done
it('testSync001', Level.LEVEL1, () => {
  let result = api.syncMethod(param);
  expect(result).assertEqual(expected);
});
```

> **不确定时**：按 `.d.ts` 返回类型判断——含 `Promise` 按异步处理，否则按同步处理。

### 3.4 异步测试 done() 使用反模式（重要！）

> **Hypium 框架的 `done()` 必须在每个异步分支中恰好调用一次。**
> （缺少 `done()` 的分支会导致测试无限挂起直到超时，测试运行器资源被占用，且超时错误掩盖了真实的测试意图）

```typescript
// ❌ 反模式1：catch 分支忘记 done()，Promise reject 时测试超时
it('testAsync001', Level.LEVEL1, async (done: Function) => {
  api.method(param)
    .then((result) => {
      expect(result).assertEqual(expected);
      done();
    })
    .catch((error: BusinessError) => {
      expect(error.code).assertEqual(401);
      // 忘记 done()！测试将超时挂起
    });
});

// ❌ 反模式2：done() 被多次调用
it('testAsync002', Level.LEVEL1, async (done: Function) => {
  api.method(param)
    .then((result) => {
      expect(result).assertEqual(expected);
      done();
      done();  // 重复调用，框架报错
    });
});

// ❌ 反模式3：回调 API 中 done() 在回调外部调用
it('testCallback001', Level.LEVEL1, async (done: Function) => {
  emitter.on('event', (data) => {
    expect(data).assertEqual(expected);
  });
  done();  // ❌ 太早！回调可能还没触发就结束了测试
});

// ✅ 正确：回调 API 的 done() 在回调内部调用
it('testCallback001', Level.LEVEL1, async (done: Function) => {
  emitter.on('event', (data) => {
    expect(data).assertEqual(expected);
    done();  // 在回调内部调用 done()
  });
  emitter.emit('event', expectedData);
});

// ❌ 反模式4：在同步 it() 中使用 done 参数（导致并发问题）
it('testSync001', Level.LEVEL1, (done: Function) => {
  let result = api.syncMethod();
  expect(result).assertEqual(expected);
  done();  // 多余！同步测试不需要 done，可能导致并发问题
});

// ✅ 正确：同步 it() 不使用 done 参数
it('testSync001', Level.LEVEL1, () => {
  let result = api.syncMethod();
  expect(result).assertEqual(expected);
});
```

---

## 四、边界值测试

### 4.1 边界值识别

| 参数类型 | 边界值 |
|---------|-------|
| number | Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER, 0, -1, 1 |
| string | 空字符串、最大长度、特殊字符 |
| 数组 | 空数组、单元素、最大长度 |
| 集合 | 空集合、单元素、最大容量 |

### 4.2 边界值测试模板

```typescript
/**
 * @tc.name test{MethodName}Boundary001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_BOUNDARY_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 最小边界值
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Boundary001', Level.LEVEL2, () => {
  let minValue = /* 计算最小边界值 */;
  let apiObject = new APIName();
  let result = apiObject.methodName(minValue);
  expect(result).assertEqual(expectedValue);
});
```
