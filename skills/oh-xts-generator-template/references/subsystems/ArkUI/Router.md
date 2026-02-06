# Router 模块配置

> **模块信息**
> - 所属子系统: ArkUI
> - 模块名称: Router
> - API 声明文件: @ohos.router.d.ts
> - 主要 API: pushUrl, replaceUrl, back, clear 等
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、模块特有配置

### 1.1 模块概述

Router 模块提供页面路由导航功能，包括页面跳转、返回、清空等操作。

### 1.2 API 声明文件

```
API声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.router.d.ts
```

### 1.3 通用配置继承

本模块继承 ArkUI 子系统通用配置：

- **测试路径规范**: 见 `ArkUI/_common.md` 第 1.2 节
- **组件测试规则**: 见 `ArkUI/_common.md` 第 1.3.1 节
- **辅助工程配置**: 见 `ArkUI/_common.md` 第 2.2 节

## 二、模块特有 API 列表

### 2.1 路由导航API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| pushUrl | 跳转到新页面 | LEVEL0 | URL、参数、模式 |
| replaceUrl | 替换当前页面 | LEVEL0 | URL、参数 |
| back | 返回上一页 | LEVEL0 | 返回层级、结果 |
| clear | 清空栈 | LEVEL1 | 清空后行为 |

### 2.2 路由状态API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| getLength | 获取栈长度 | LEVEL1 | 栈状态 |
| getState | 获取路由状态 | LEVEL1 | 当前页面信息 |
| getParams | 获取页面参数 | LEVEL2 | 参数传递 |

## 三、模块特有测试规则

### 3.1 页面跳转测试规则

1. **pushUrl 测试**：
   - 测试基本跳转
   - 测试带参数跳转
   - 测试跳转模式（Standard、Single）
   - 测试跳转失败场景

2. **replaceUrl 测试**：
   - 测试替换当前页面
   - 测试带参数替换
   - 测试替换后栈状态

### 3.2 页面返回测试规则

1. **back 测试**：
   - 测试返回上一页
   - 测试返回多级
   - 测试返回带结果
   - 测试栈底返回

2. **clear 测试**：
   - 测试清空路由栈
   - 测试清空后跳转
   - 测试清空失败场景

### 3.3 参数传递测试规则

1. **参数传递**：
   - 测试基本类型参数
   - 测试对象参数
   - 测试参数解析

2. **参数接收**：
   - 测试 onReady 接收参数
   - 测试参数类型验证
   - 测试参数缺失场景

## 四、模块特有代码模板

### 4.1 pushUrl 测试模板

```typescript
/**
 * @tc.name ArkUI Router pushUrl Test
 * @tc.number SUB_ARKUI_ROUTER_PUSH_URL_001
 * @tc.desc 测试 Router pushUrl 功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testRouterPushUrl001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  // 1. 准备跳转参数
  let url = 'pages/SecondPage';
  let params = {
    key: 'value',
    number: 123
  };

  // 2. 执行跳转
  try {
    await router.pushUrl({
      url: url,
      params: params
    });

    // 3. 验证跳转成功
    // (需要验证页面栈状态)
    expect().assertTrue();

  } catch (error) {
    expect().assertFail();
  }
});
```

### 4.2 back 测试模板

```typescript
/**
 * @tc.name ArkUI Router back Test
 * @tc.number SUB_ARKUI_ROUTER_BACK_001
 * @tc.desc 测试 Router back 功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testRouterBack001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 获取当前栈长度
  let lengthBefore = router.getLength();

  // 2. 执行返回
  router.back();

  // 3. 验证栈长度减少
  let lengthAfter = router.getLength();
  expect(lengthAfter).assertEqual(lengthBefore - 1);
});
```

## 五、测试注意事项

1. **页面栈管理**：
   - 测试前需要准备页面栈
   - 测试后需要清理页面栈
   - 避免页面栈溢出

2. **异步操作**：
   - 路由操作是异步的
   - 需要使用 async/await
   - 需要等待页面加载完成

3. **辅助页面**：
   - 需要准备测试用页面
   - 页面需要配置在 route_map.json
   - 页面需要支持参数传递

4. **异常场景**：
   - 测试无效 URL
   - 测试页面栈溢出
   - 测试重复跳转

## 六、辅助工程要求

### 6.1 页面配置

测试工程需要配置测试页面：

```json5
{
  "routerMap": [
    {
      "name": "TestPage1",
      "pageSourceFile": "src/main/ets/pages/TestPage1.ets",
      "buildFunction": "TestPage1Builder"
    },
    {
      "name": "TestPage2",
      "pageSourceFile": "src/main/ets/pages/TestPage2.ets",
      "buildFunction": "TestPage2Builder"
    }
  ]
}
```

### 6.2 页面文件

每个测试页面需要：
- 实现 @Builder 装饰的构建函数
- 实现参数接收逻辑
- 实现页面生命周期

## 七、版本历史

- **v1.0.0** (2025-01-31): 初始版本，定义 Router 模块配置
