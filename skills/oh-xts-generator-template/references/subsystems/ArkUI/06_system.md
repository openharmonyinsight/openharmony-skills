# 06. 系统能力接口测试指南

> 六、系统与能力接口（System & Ability APIs）- 和系统打交道

---

## 接口说明

系统与能力接口用来**和系统打交道**，通常来自 `@ohos.*` 模块，非 UI 组件接口。

### 常见能力分类

| 类型 | 模块 | 示例 |
|------|------|------|
| 页面路由 | `@ohos.router` | `pushUrl()`、`replaceUrl()`、`back()` |
| 生命周期 | `@ohos.ability.UIAbility` | `onCreate()`、`onDestroy()`、`onForeground()` |
| 媒体能力 | `@ohos.multimedia.media` | 播放器、录制器 |
| 设备能力 | `@ohos.deviceInfo` | 获取设备信息 |
| 网络能力 | `@ohos.net.http` | HTTP 请求 |
| 数据存储 | `@ohos.data.preferences` | 首选项存储 |
| 通知能力 | `@ohos.notificationManager` | 发送通知 |

---

## 测试重点

### 1. Router 路由测试

**测试目的**：验证页面路由是否正确工作。

#### 页面侧

```typescript
import router from '@ohos.router';

@Entry
@Component
struct RouterTest {
  build() {
    Column({ space: 20 }) {
      Button('Push URL')
        .id('button_push_url')
        .onClick(() => {
          router.pushUrl({
            url: 'pages/DestinationPage'
          });
        })

      Button('Replace URL')
        .id('button_replace_url')
        .onClick(() => {
          router.replaceUrl({
            url: 'pages/DestinationPage'
          });
        })

      Button('Back')
        .id('button_back')
        .onClick(() => {
          router.back();
        })
    }
    .width('100%')
    .height('100%')
    .padding(20)
    .backgroundColor('#F5F5F5')
  }
}
```

#### 测试侧

```typescript
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, Level } from '@ohos/hypium';
import { hilog } from '@kit.PerformanceAnalysisKit';
import { destoryAbility, sleep, startPage } from '../../../uiutils/commonUtils';
import { UiComponent, Driver, ON } from '@ohos.UiTest';

export default function RouterTest() {
  describe('RouterTest', () => {
    beforeAll(async () => {
      hilog.info(0x0000, 'RouterTest', 'beforeAll: start test page');
      await startPage('pages/router/RouterTest');
      await sleep(1000);
    });

    /**
     * @tc.name   routerPushUrl_0100
     * @tc.number SUB_ARKUI_ROUTER_PUSH_URL_0100
     * @tc.desc   测试 router.pushUrl 路由跳转功能
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL1
     */
    it('routerPushUrl_0100', Level.LEVEL1, async () => {
      let driver: Driver = await Driver.create();
      let button = await driver.findComponent(ON.id('button_push_url'));

      await button.click();
      await sleep(1000);  // 等待页面跳转

      // 验证是否跳转到目标页面
      try {
        let targetComponent = await driver.findComponent(ON.id('destination_page_id'));
        expect(targetComponent).notBeNull();
      } catch (e) {
        // 页面跳转失败
        expect(true).assertFalse();
      }
    });

    /**
     * @tc.name   routerBack_0100
     * @tc.number SUB_ARKUI_ROUTER_BACK_0100
     * @tc.desc   测试 router.back 返回功能
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL1
     */
    it('routerBack_0100', Level.LEVEL1, async () => {
      let driver: Driver = await Driver.create();
      let pushButton = await driver.findComponent(ON.id('button_push_url'));
      await pushButton.click();
      await sleep(1000);

      // 返回上一页
      let backButton = await driver.findComponent(ON.id('button_back'));
      await backButton.click();
      await sleep(1000);

      // 验证返回到原页面
      let originalButton = await driver.findComponent(ON.id('button_push_url'));
      expect(originalButton).notBeNull();
    });
  });
}
```

### 2. DeviceInfo 设备信息测试

**测试目的**：验证获取设备信息的能力。

#### 测试侧（无需页面）

```typescript
import { describe, it, expect, Level } from '@ohos/hypium';
import deviceInfo from '@ohos.deviceInfo';

export default function DeviceInfoTest() {
  describe('DeviceInfoTest', () => {
    /**
     * @tc.name   deviceInfoBrand_0100
     * @tc.number SUB_ARKUI_DEVICEINFO_BRAND_0100
     * @tc.desc   测试获取设备品牌信息
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('deviceInfoBrand_0100', Level.LEVEL0, async () => {
      let brand: string = deviceInfo.brand;
      expect(brand).assertNotNull();
      expect(brand.length).assertLarger(0);
    });

    /**
     * @tc.name   deviceInfoModel_0100
     * @tc.number SUB_ARKUI_DEVICEINFO_MODEL_0100
     * @tc.desc   测试获取设备型号信息
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('deviceInfoModel_0100', Level.LEVEL0, async () => {
      let model: string = deviceInfo.productModel;
      expect(model).assertNotNull();
      expect(model.length).assertLarger(0);
    });

    /**
     * @tc.name   deviceInfoOsVersion_0100
     * @tc.number SUB_ARKUI_DEVICEINFO_OS_VERSION_0100
     * @tc.desc   测试获取系统版本信息
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('deviceInfoOsVersion_0100', Level.LEVEL0, async () => {
      let osVersion: string = deviceInfo.osFullName;
      expect(osVersion).assertNotNull();
      expect(osVersion.length).assertLarger(0);
    });
  });
}
```

### 3. Preferences 数据存储测试

**测试目的**：验证首选项存储功能。

#### 测试侧（无需页面）

```typescript
import { describe, it, expect, Level } from '@ohos/hypium';
import preferences from '@ohos.data.preferences';

export default function PreferencesTest() {
  describe('PreferencesTest', () => {
    let preferencesStore: preferences.Preferences;

    beforeAll(async () => {
      // 初始化 preferences
      let context = getContext();
      preferencesStore = await preferences.getPreferences(context, 'test_preferences');
    });

    /**
     * @tc.name   preferencesPut_0100
     * @tc.number SUB_ARKUI_PREFERENCES_PUT_0100
     * @tc.desc   测试存储数据到首选项
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('preferencesPut_0100', Level.LEVEL0, async () => {
      await preferencesStore.put('test_key', 'test_value');
      await preferencesStore.flush();

      let value: string = await preferencesStore.get('test_key', 'default');
      expect(value).assertEqual('test_value');
    });

    /**
     * @tc.name   preferencesGet_0100
     * @tc.number SUB_ARKUI_PREFERENCES_GET_0100
     * @tc.desc   测试从首选项获取数据
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('preferencesGet_0100', Level.LEVEL0, async () => {
      let value: string = await preferencesStore.get('test_key', 'default');
      expect(value).assertEqual('test_value');
    });

    /**
     * @tc.name   preferencesDelete_0100
     * @tc.number SUB_ARKUI_PREFERENCES_DELETE_0100
     * @tc.desc   测试从首选项删除数据
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('preferencesDelete_0100', Level.LEVEL0, async () => {
      await preferencesStore.delete('test_key');
      await preferencesStore.flush();

      let value: string = await preferencesStore.get('test_key', 'default');
      expect(value).assertEqual('default');
    });
  });
}
```

### 4. HTTP 网络请求测试

**测试目的**：验证网络请求功能。

#### 测试侧（无需页面）

```typescript
import { describe, it, expect, Level } from '@ohos/hypium';
import http from '@ohos.net.http';

export default function HttpTest() {
  describe('HttpTest', () => {
    /**
     * @tc.name   httpRequest_0100
     * @tc.number SUB_ARKUI_HTTP_REQUEST_0100
     * @tc.desc   测试 HTTP GET 请求
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL1
     */
    it('httpRequest_0100', Level.LEVEL1, async (done: Function) => {
      let httpRequest = http.createHttp();

      httpRequest.request('https://example.com/api/test', {
        method: http.RequestMethod.GET,
        header: {
          'Content-Type': 'application/json'
        },
        readTimeout: 10000,
        connectTimeout: 10000
      }, (err: BusinessError, data: http.HttpResponse) => {
        if (!err) {
          expect(data.responseCode).assertEqual(200);
          expect(data.result).notBeNull();
        } else {
          expect(false).assertTrue();
        }
        httpRequest.destroy();
        done();
      });
    });
  });
}
```

---

## 测试注意事项

> **说明**：本节列出系统能力接口测试的特定注意事项。通用测试规范请参考 [_common.md](./_common.md)。

### 1. 无需创建页面

非 UI 接口测试通常**无需创建测试页面**，直接在 test.ets 中调用 API 并断言结果：

```typescript
// ✅ 正确：直接测试 API
it('apiTest', Level.LEVEL0, async () => {
  let result = await someApi.method();
  expect(result).assertEqual('expected');
});

// ❌ 错误：为非 UI API 创建页面（不必要）
```

### 2. 异步操作处理

系统 API 通常为异步，使用 `async/await` 或 `done` 回调：

```typescript
// ✅ 正确：使用 async/await
it('asyncTest', Level.LEVEL0, async () => {
  let result = await asyncApi.method();
  expect(result).assertEqual('expected');
});

// ✅ 正确：使用 done 回调
it('callbackTest', Level.LEVEL0, async (done: Function) => {
  asyncApi.method((err, data) => {
    expect(data).assertEqual('expected');
    done();
  });
});
```

### 3. 权限处理

系统能力测试可能需要特殊权限，在测试前确保已申请：

```typescript
beforeAll(async () => {
  // 确保必要权限已授予
  let context = getContext();
  // 权限检查逻辑
});
```

### 4. 错误处理

测试应包含成功和失败场景：

```typescript
/**
 * @tc.name   apiSuccess_0100
 * @tc.desc   测试 API 成功场景
 */
it('apiSuccess_0100', Level.LEVEL0, async () => {
  let result = await api.method();
  expect(result).assertEqual('expected');
});

/**
 * @tc.name   apiError_0100
 * @tc.desc   测试 API 错误场景
 */
it('apiError_0100', Level.LEVEL2, async () => {
  try {
    await api.method('invalid_param');
    expect(false).assertTrue();  // 不应该到达这里
  } catch (e) {
    expect(e.code).assertEqual(expectedErrorCode);
  }
});
```

### 5. 资源清理

系统资源（如 HTTP 连接）使用后需要清理：

```typescript
it('httpRequest_0100', Level.LEVEL1, async (done: Function) => {
  let httpRequest = http.createHttp();

  try {
    let response = await httpRequest.request('https://example.com');
    expect(response.responseCode).assertEqual(200);
  } finally {
    httpRequest.destroy();  // 确保资源清理
    done();
  }
});
```

---

## 系统能力测试模板

### 无页面 API 测试模板

```typescript
import { describe, beforeAll, afterAll, it, expect, Level } from '@ohos/hypium';
import { BusinessError } from '@ohos.base';
import systemApi from '@ohos.systemApi';

export default function SystemApiTest() {
  describe('SystemApiTest', () => {
    let apiInstance: systemApi.ApiType;

    beforeAll(async () => {
      // 初始化 API
      apiInstance = await systemApi.create();
    });

    afterAll(async () => {
      // 清理资源
      if (apiInstance) {
        await apiInstance.destroy();
      }
    });

    /**
     * @tc.name   systemApiMethod_0100
     * @tc.number SUB_ARKUI_SYSTEM_API_METHOD_0100
     * @tc.desc   测试 systemApi.method 方法
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL0
     */
    it('systemApiMethod_0100', Level.LEVEL0, async () => {
      let result: string = await apiInstance.method('param');
      expect(result).assertEqual('expected_value');
    });

    /**
     * @tc.name   systemApiMethod_0200
     * @tc.number SUB_ARKUI_SYSTEM_API_METHOD_0200
     * @tc.desc   测试 systemApi.method 方法的错误处理
     * @tc.type   FUNCTION
     * @tc.size   SMALLTEST
     * @tc.level  LEVEL2
     */
    it('systemApiMethod_0200', Level.LEVEL2, async () => {
      try {
        await apiInstance.method('invalid_param');
        expect(false).assertTrue();  // 不应该成功
      } catch (e: BusinessError) {
        expect(e.code).assertEqual(ErrorCode);
      }
    });
  });
}
```

---

## 与 UI 组件测试的区别

| 特性 | UI 组件测试 | 系统能力测试 |
|------|-----------|-------------|
| 是否需要页面 | 是 | 否 |
| 测试方式 | getInspectorByKey + UiTest | 直接调用 API |
| 断言方式 | 通过 $attrs 验证 | 直接断言返回值 |
| 主要工具 | @ohos.UiTest | 对应系统 API 模块 |
| 代码位置 | 需要创建页面和测试文件 | 只需测试文件 |

---

## 参考文档

- ArkUI 子系统通用配置：[_common.md](./_common.md)
- ArkUI 接口分类概览：[arkui.md](./arkui.md)
- HarmonyOS 系统API文档：[官方文档链接]
