# ArkUI 子系统通用配置

> **子系统信息**
> - 名称: ArkUI
> - Kit包: @kit.ArkUI
> - 测试路径: test/xts/acts/arkui/
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、子系统通用配置

### 1.1 API Kit 映射

```typescript
// ArkUI 组件导入
import {Component} from '@kit.ArkUI';
import {Column, Row, Text, Button} from '@kit.ArkUI';
```

### 1.2 测试路径规范

```
测试用例目录: test/xts/acts/arkui/test/
历史用例参考: ${OH_ROOT}/test/xts/acts/arkui/
文档资料: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-arkui/
```

### 1.3 子系统通用测试规则

#### 1.3.1 组件测试规则

1. **组件属性测试**：
   - 需要验证属性绑定和更新
   - 测试属性的类型校验
   - 验证属性的默认值

2. **组件事件测试**：
   - 验证事件触发机制
   - 测试事件回调函数
   - 验证事件参数传递

3. **组件生命周期测试**：
   - 测试 aboutToAppear
   - 测试 aboutToDisappear
   - 测试其他生命周期钩子

4. **辅助工程要求**：
   - ArkUI 组件测试需要辅助工程提供 UI 界面
   - 辅助工程命名：`{测试套名}Scene`
   - 测试工程需要依赖辅助 HAP 包

#### 1.3.2 状态管理测试规则

1. **State 测试**：
   - 测试状态变量的响应式更新
   - 验证状态变化触发 UI 更新

2. **Prop 测试**：
   - 测试父组件向子组件传递数据
   - 验证 props 的单向数据流

3. **Link 测试**：
   - 测试双向数据绑定
   - 验证父子组件数据同步

### 1.4 模块映射配置

ArkUI 子系统包含多个模块，每个模块对应一个或多个 API 声明文件：

| 模块名称 | API 声明文件 | 主要 API | 说明 |
|---------|-------------|---------|------|
| **Component** | @ohos.arkui.d.ts | Component, Column, Row, Text, Button 等 | 基础组件和容器 |
| **Animator** | @ohos.animator.d.ts | animateTo, animateXXX, getAnimator 等 | 动画接口 |
| **Router** | @ohos.router.d.ts | pushUrl, replaceUrl, back, clear 等 | 路由导航 |
| **UIEngine** | @ohos.uiEngine.d.ts | createUIEngine, getUIEngine 等 | UI 引擎 |
| **Window** | @ohos.window.d.ts | getWindow, createWindow 等 | 窗口管理 |
| **Display** | @ohos.display.d.ts | getDefaultDisplay, getCutoutInfo 等 | 显示管理 |

**模块解析说明**：
- **模块级解析**：可以解析某个模块的所有 API（如解析 Animator 模块的所有方法）
- **API 级解析**：可以解析单个 API（如 Component.onClick）
- **批量解析**：可以解析整个子系统的所有模块和 API

### 1.5 子系统通用代码模板

#### 1.5.1 组件属性测试模板

```typescript
/**
 * @tc.name ArkUI Component Attribute Test
 * @tc.number SUB_ARKUI_COMPONENT_XXX_ATTRIBUTE_001
 * @tc.desc 测试 ArkUI 组件属性功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testComponentAttribute001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建组件实例
  let component = new ComponentName();

  // 2. 设置属性值
  component.attributeName = attributeValue;

  // 3. 验证属性值
  expect(component.attributeName).assertEqual(attributeValue);

  // 4. 验证UI更新（如需要）
});
```

#### 1.5.2 组件事件测试模板

```typescript
/**
 * @tc.name ArkUI Component Event Test
 * @tc.number SUB_ARKUI_COMPONENT_XXX_EVENT_001
 * @tc.desc 测试 ArkUI 组件事件功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testComponentEvent001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建组件实例
  let component = new ComponentName();
  let eventTriggered = false;

  // 2. 注册事件回调
  component.onEvent(() => {
    eventTriggered = true;
  });

  // 3. 触发事件
  component.triggerEvent();

  // 4. 验证事件被触发
  expect(eventTriggered).assertTrue();
});
```

## 二、已知问题和注意事项

### 2.1 组件测试限制

1. **UI依赖**：
   - 组件测试需要实际的 UI 环境支持
   - 单元测试无法完全模拟用户交互
   - 需要辅助工程提供测试界面

2. **异步渲染**：
   - 组件渲染是异步的
   - 需要等待渲染完成后再验证
   - 使用 setTimeout 或 waitFor 机制

3. **性能测试**：
   - 性能测试需要在真实设备上进行
   - 模拟器测试结果仅供参考
   - 注意测试环境的稳定性

### 2.2 辅助工程配置

1. **命名规范**：
   - 辅助工程目录：`{测试套名}Scene`
   - 例如：`arkuiTest` → `arkuiTestScene`

2. **BUILD.gn 配置**：
   ```gni
   # 辅助工程
   ohos_app_assist_suite("ArkUITestEntry") {
     testonly = true
     subsystem_name = "arkui"
     part_name = "arkui_test"
     certificate_profile = "./signature/auto_ohos_default_com.arkui.test.p7b"
     hap_name = "ArkUITestEntry"
   }

   # 测试工程
   ohos_js_app_suite("ArkUITest") {
     test_hap = true
     testonly = true
     certificate_profile = "./signature/auto_ohos_default_com.arkui.test.p7b"
     hap_name = "ArkUITest"
     part_name = "arkui_test"
     subsystem_name = "arkui"
     deps = [
       ":ArkUITestEntry",  # 依赖辅助工程
     ]
   }
   ```

3. **辅助工程内容**：
   - 包含被测试的 UI 界面和组件
   - 提供测试目标（按钮、文本、输入框等）
   - 配置 module.json5 和 build-profile.json5

### 2.3 测试注意事项

1. **状态变量测试**：
   - 状态变量需要用 `@State` 装饰
   - 状态变化会触发组件重新渲染
   - 需要验证渲染后的结果

2. **父子组件测试**：
   - 父组件向子组件传递 props
   - 子组件通过事件向父组件通信
   - 需要创建父子组件关系进行测试

3. **列表渲染测试**：
   - LazyForEach 需要实现数据源接口
   - 需要测试滚动性能
   - 需要测试列表项的复用机制

## 三、参考示例

### 3.1 历史用例参考

```
${OH_ROOT}/test/xts/acts/arkui/test/
```

### 3.2 辅助工程参考

```
测试工程: ${OH_ROOT}/test/xts/acts/arkui/uitest
辅助工程: ${OH_ROOT}/test/xts/acts/arkui/uitestScene
```

## 四、版本历史

- **v1.0.0** (2025-01-31): 初始版本，定义 ArkUI 子系统通用配置
