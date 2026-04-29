# 应用内分屏适配指南

## 目录

1. [核心概念](#核心概念)
2. [前置条件](#前置条件)
3. [跨 Ability 数据通信架构](#跨-ability-数据通信架构)
4. [数据流时序](#数据流时序)
5. [关键代码](#关键代码)
6. [目标页面复用已有 NavDestination](#目标页面复用已有-navdestination)
7. [注意事项](#注意事项)
8. [常见问题](#常见问题)

---

## 核心概念

应用内分屏是通过 `startAbility` + `StartOptions` 启动另一个 UIAbility 并自动形成分屏的多窗口方案。两个窗口各自拥有独立的生命周期和窗口实例，可独立操作。

### 与平行视界（EasyGo）的区别

| | 应用内分屏（本指南） | 平行视界（EasyGo） |
|---|---|---|
| 实现方式 | `startAbility` + `StartOptions` | `easy_go.json` 配置文件 |
| 窗口实例 | 两个独立 UIAbility，各自有独立窗口和生命周期 | 同一个 UIAbility 内页面分栏，共享窗口 |
| 触发方式 | 代码调用（用户点击按钮） | 系统根据配置自动生效 |
| 适用场景 | 需要两个独立窗口并行操作 | 宽屏/大屏设备的兼容分栏 |

### 关键术语

- **UIAbility**: HarmonyOS 应用的基本组成单元，每个 UIAbility 拥有独立的窗口实例和生命周期
- **分屏**: 两个 UIAbility 的窗口在屏幕上各占一侧（左右或上下）同时显示
- **StartOptions**: 启动 Ability 时携带的窗口选项，用于控制目标窗口的显示模式
- **LocalStorage**: UIAbility 级别的键值对存储，通过 `loadContent(path, storage)` 传递给页面

---

## 前置条件

1. 应用至少有两个 UIAbility
2. 目标 UIAbility 在 `module.json5` 中声明支持分屏（`supportWindowMode` 包含 `"split"`）
3. 目标 UIAbility 设置 `"launchType": "singleton"` 确保后续调用触发 `onNewWant`

---

## 跨 Ability 数据通信架构

```
┌─────────────────────────────────────────────────────────────┐
│                    主 UIAbility (EntryAbility)               │
│                                                             │
│  Index 页面                                                 │
│  ┌──────────────────┐    ┌────────────────────────────┐     │
│  │ @State selectedItem│   │  分屏按钮 onClick          │     │
│  │ @State itemList    │   │  startAbility(want, opts)  │     │
│  └──────────────────┘    │  want.parameters = {        │     │
│                          │    itemId, itemTitle, itemDesc  │     │
│  列表项 onClick:         │  }                           │     │
│  selectedItem = item     │  options.windowMode =         │     │
│  pathStack.pushPath(...) │    SPLIT_SECONDARY           │     │
│                          └────────────┬───────────────┘     │
└──────────────────────────────────────┼──────────────────────┘
                                       │ startAbility (Want)
                                       ▼
┌──────────────────────────────────────────────────────────────┐
│                  目标 UIAbility (EntryAbility1)               │
│                                                              │
│  ┌─────────────────────────────────────────────┐             │
│  │ LocalStorage (new LocalStorage(para))        │             │
│  │   itemId: number                             │             │
│  │   itemTitle: string                          │             │
│  │   itemDesc: string                           │             │
│  └──────────────────┬──────────────────────────┘             │
│                     │ loadContent(path, storage)             │
│                     ▼                                         │
│  ┌─────────────────────────────────────────────┐             │
│  │ DetailPage (@Entry useSharedStorage: true)   │             │
│  │   @LocalStorageLink('itemId') ←─────────┐   │             │
│  │   @LocalStorageLink('itemTitle') ←──────┤   │             │
│  │   @LocalStorageLink('itemDesc') ←───────┘   │             │
│  │                                             │             │
│  │  生命周期：                                   │             │
│  │   onCreate   → writeParamsToStorage(want)   │             │
│  │   onNewWant  → writeParamsToStorage(want)   │             │
│  │   onWindowStageCreate → loadContent(page, storage)        │
│  └─────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

---

## 数据流时序

```
首次分屏:
  Index.onClick(分屏) → startAbility(want+parameters, SPLIT_SECONDARY)
    → EntryAbility1.onCreate(want) → writeParamsToStorage(want)
    → EntryAbility1.onWindowStageCreate → loadContent('DetailPage', storage)
    → DetailPage.aboutToAppear → @LocalStorageLink 绑定 storage 值

分屏已存在，点击新列表项:
  Index.onClick(列表项) → selectedItem = item
  Index.onClick(分屏) → startAbility(want+新parameters, SPLIT_SECONDARY)
    → EntryAbility1.onNewWant(want) → writeParamsToStorage(want)
    → @LocalStorageLink 自动刷新 UI
```

---

## 关键代码

### module.json5 — 声明分屏支持

```json5
{
  "abilities": [
    {
      "name": "EntryAbility"
    },
    {
      "name": "EntryAbility1",
      "srcEntry": "./ets/entryability1/EntryAbility1.ets",
      "exported": true,
      "launchType": "singleton",
      "supportWindowMode": ["fullscreen", "split", "floating"]
    }
  ]
}
```

### 主 Ability 页面 — 分屏启动 + 传递参数

```typescript
import { AbilityConstant, common, StartOptions, Want } from '@kit.AbilityKit'

@Entry
@Component
struct Index {
  @State selectedItem: ItemModel | null = null

  // 分屏按钮点击
  startSplitMode() {
    let context = this.getUIContext().getHostContext();
    if (context) {
      let uiAbilityContext = context as common.UIAbilityContext;
      let item = this.selectedItem
      let want: Want = {
        bundleName: uiAbilityContext.abilityInfo.bundleName,
        abilityName: 'EntryAbility1',
        parameters: {
          itemId: item?.id ?? 0,
          itemTitle: item?.title ?? '',
          itemDesc: item?.description ?? ''
        }
      }
      let options: StartOptions = {
        windowMode: AbilityConstant.WindowMode.WINDOW_MODE_SPLIT_SECONDARY
      }
      uiAbilityContext.startAbility(want, options)
    }
  }

  // 列表项点击 — 仅记录选中项 + 页内导航
  ListItemBuilder(item: ItemModel) {
    Row() { /* ... */ }
      .onClick(() => {
        this.selectedItem = item
        this.pathStack.pushPath(new NavPathInfo('DetailPage',
          new DetailParam(item.id, item.title, item.description)))
      })
  }
}
```

### 目标 UIAbility — Want.parameters → LocalStorage → loadContent

```typescript
import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit';
import { window } from '@kit.ArkUI';

export default class EntryAbility1 extends UIAbility {
  private para: Record<string, Object> = {
    'itemId': 0,
    'itemTitle': '',
    'itemDesc': ''
  }
  private storage: LocalStorage = new LocalStorage(this.para)

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    this.writeParamsToStorage(want);
  }

  // 分屏已存在时，后续 startAbility 触发此回调
  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    this.writeParamsToStorage(want);
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/DetailPage', this.storage, (err) => {
      if (err.code) {
        hilog.error(0x0000, 'EntryAbility1', 'Failed: %{public}s', JSON.stringify(err));
      }
    });
  }

  private writeParamsToStorage(want: Want): void {
    const id = want.parameters?.['itemId'] as number ?? 0
    const title = want.parameters?.['itemTitle'] as string ?? ''
    const desc = want.parameters?.['itemDesc'] as string ?? ''
    this.storage.setOrCreate('itemId', id)
    this.storage.setOrCreate('itemTitle', title)
    this.storage.setOrCreate('itemDesc', desc)
  }
}
```

### 目标页面 — useSharedStorage + LocalStorageLink 绑定

```typescript
@Entry({ useSharedStorage: true })
@Component
export struct DetailPage {
  @LocalStorageLink('itemId') itemId: number = 0
  @LocalStorageLink('itemTitle') itemTitle: string = ''
  @LocalStorageLink('itemDesc') itemDesc: string = ''
  @State itemParam: DetailParam = new DetailParam()

  aboutToAppear(): void {
    if (this.itemId !== 0 || this.itemTitle !== '') {
      this.itemParam = {
        id: this.itemId,
        title: this.itemTitle,
        description: this.itemDesc
      }
    }
  }

  build() {
    NavDestination() {
      Column() {
        Text(this.itemParam.title || this.itemTitle)
        Text((this.itemParam.id || this.itemId).toString())
        Text(this.itemParam.description || this.itemDesc)
      }
    }
  }
}
```

### windowMode 取值

| 值 | 说明 |
|----|------|
| `WINDOW_MODE_SPLIT_PRIMARY` | 目标 UIAbility 显示在主侧（左侧/上侧） |
| `WINDOW_MODE_SPLIT_SECONDARY` | 目标 UIAbility 显示在副侧（右侧/下侧） |

### preferMultiWindowOrientation 取值

| 配置值 | 说明 | 效果 |
|--------|------|------|
| `default` | 缺省值 | 手机上下分屏；折叠屏展开态左右分屏 |
| `portrait` | 竖向布局 | 悬浮窗竖向，折叠屏展开态左右分屏 |
| `landscape` | 横向布局 | 支持横向悬浮窗和上下分屏 |
| `landscape_auto` | 动态横向 | 需配合 `enableLandscapeMultiWindow` / `disableLandscapeMultiWindow` API |

---

## 注意事项

- `@Entry({ useSharedStorage: true })` 是页面接收 `loadContent(path, storage)` 传入的 LocalStorage 的必要条件，缺少此声明 `@LocalStorageLink` 将无法绑定。
- 外层 Navigation 须加 `.hideTitleBar(true)` 避免与 NavDestination 标题栏产生双标题栏空白。
- `onNewWant` 必须实现，否则分屏已存在时后续 `startAbility` 不会更新数据。
- `launchType: "singleton"` 确保目标 UIAbility 单例运行，后续调用走 `onNewWant` 而非创建新实例。
- `supportWindowMode` 合法值为 `"fullscreen"`、`"split"`、`"floating"`，不是 `"splitScreen"`。
- pageMap 中访问 param 前必须做空值保护，EasyGo 分栏场景下 param 可能为 null。

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 启动后目标 UIAbility 全屏显示，未分屏 | `startAbility` 未传 `StartOptions` | 必须传入 `StartOptions` 并指定 `windowMode` |
| 使用 `WINDOW_MODE_FLOATING` 编译报错 | 枚举中不存在此值 | 使用 `WINDOW_MODE_SPLIT_SECONDARY` 或 `WINDOW_MODE_SPLIT_PRIMARY` |
| 分屏启动不生效 | 未声明 `"split"` | 在 `module.json5` 中添加 `"supportWindowMode": ["split", "fullscreen"]` |
| 分屏启动不生效 | `bundleName` 或 `abilityName` 不正确 | 检查并修正为与 `module.json5` 一致的值 |
| 分屏后两侧内容相同 | 两个 UIAbility 加载了同一个页面 | 目标 UIAbility 加载独立页面 |
| `supportWindowMode` 编译报错 | `"splitScreen"` 不是合法枚举值 | 合法值为 `"fullscreen"`、`"split"`、`"floating"` |
| 分屏页面接收不到 Want 参数 | `@Entry` 未声明 `useSharedStorage: true` | 页面须使用 `@Entry({ useSharedStorage: true })` |
| 分屏后更新参数不生效 | 未处理 `onNewWant` | 在 `onNewWant` 中更新 LocalStorage |
| 分屏页面左侧存在较大空白 | 外层 Navigation 与 NavDestination 双标题栏 | 外层 Navigation 添加 `.hideTitleBar(true)` |
| `getUIContext()` 报错 window state abnormal | `loadContent` 之前调用了 `getUIContext()` | 先 `loadContent`，UI 加载后再调用 |
| `LocalStorage \| undefined` 类型不匹配 | `getSharedLocalStorage()` 返回 `undefined` | 使用 `new LocalStorage(para)` + `loadContent(path, storage)` 模式 |
