# 字体缩放与显示密度适配指南

## 目录

1. [适配设计原理](#适配设计原理)
2. [字体缩放适配](#字体缩放适配)
3. [显示密度适配](#显示密度适配)
4. [环境变量监听](#环境变量监听)

---

## 适配设计原理

字体缩放(fontSizeScale)和显示密度(screenDensity)是系统级环境变量，用户在「设置」中修改后会全局生效。应用若未正确处理，将出现组件遮挡、截断、布局错乱等问题。

### 核心概念

- **字体缩放 (fontSizeScale)**: 用户在设置中调整字体大小后，系统传递的字体缩放倍数
- **显示密度 (screenDensity)**: 用户在设置中调整显示大小后，系统传递的屏幕像素密度变化
- **maxFontScale**: 组件级属性，限制文本最大字体缩放倍数
- **fontSizeMaxScale**: 应用级配置，在 `base/profile/configuration.json` 中设置全局字体最大缩放倍数

### 为什么需要适配？

**原则一: 适老化支持**
> 系统字体放大后，应用应确保布局不错乱、组件不重叠，保障无障碍体验。

**原则二: 布局稳定性**
> 显示密度变化等同于窗口尺寸变化，应用需要动态调整组件尺寸和布局结构。

**原则三: 全局一致性**
> 环境变量变化时，所有页面应同步响应，不能出现部分页面适配、部分页面未适配的情况。

---

## 字体缩放适配

### 方案 A — 应用级限制: `app.json5` + `configuration.json` 配置

`app.json5` 中的 `configuration` 标签是一个 profile 文件资源引用，指向独立的配置文件，而非内联 JSON 对象。

**步骤一：在 `app.json5` 中引用配置文件**

```json
{
  "app": {
    "bundleName": "com.example.myapplication",
    "vendor": "example",
    "versionCode": 1000000,
    "versionName": "1.0.0",
    "icon": "$media:app_icon",
    "label": "$string:app_name",
    "configuration": "$profile:configuration"
  }
}
```

**步骤二：创建 `base/profile/configuration.json` 配置文件**

```json
{
  "configuration": {
    "fontSizeScale": "followSystem",
    "fontSizeMaxScale": "1.3"
  }
}
```

| 配置项 | 取值 | 说明 |
|--------|------|------|
| `fontSizeScale` | `"followSystem"` | 表示应用字体大小跟随系统缩放；不配置时默认不跟随系统字体变化 |
| `fontSizeMaxScale` | `"1.0"` ~ `"3.2"` | 字体最大缩放倍数，字符串格式。取值对应系统字体档位（见下方档位表），常用值为 `"1.3"`、`"1.45"`、`"1.75"` |

**系统字体档位对照表**

| 档位 | 字体大小 | 字体粗细 | 说明 |
|------|---------|---------|------|
| 标准 | 1.0 倍 | 1.0 倍 | 默认档位 |
| 大1档 | 1.15 倍 | 1.0 倍 | |
| 大2档 | 1.3 倍 | 1.1 倍 | |
| 大3档 | 1.45 倍 | 1.1 倍 | |
| 大4档 | 1.75 倍 | 1.25 倍 | 建议应用最大应调整至此档位 |
| 大5档 | 2.0 倍 | 1.25 倍 | 部分组件可调整至此档位 |
| 大6档 | 3.2 倍 | 1.25 倍 | 最大档位 |

> **推荐实践**：应用最大应调整至 1.75 倍（大4档），部分组件可通过 `maxFontScale` 属性单独放宽至 2.0 倍。

### 方案 B — 组件级限制: `maxFontScale` 属性

对单个 Text 组件限制最大字体缩放倍数。当 Text 组件配置了 `maxFontScale` 时，将采用组件设置的最大放大倍数，而非应用级 `fontSizeMaxScale` 的值。

```typescript
// 示例：应用级 fontSizeMaxScale 设为 1.75，但该组件允许放大到 2 倍
Text('hello world!')
  .fontSize($r('sys.float.Body_M'))
  .maxFontScale(2)
  .fontColor($r('sys.color.font_secondary'))
```

| 属性 | 取值范围 | 说明 |
|------|---------|------|
| `maxFontScale(number)` | 1.0 ~ 3.2 | 限制该 Text 组件的最大字体缩放倍数；当系统字体大于此值时，字体大小被截断到此倍数 |
| 适用范围 | - | 仅影响字体大小，不影响整体显示缩放；图标及图片不会随字体变化而变化 |

### 方案 C — 应用内自行管理

不跟随系统字体，在应用内提供独立的字体大小调节功能。适用于有自定义字体设置需求的应用。

### 方案选择建议

| 场景 | 推荐方案                                                         |
|------|--------------------------------------------------------------|
| 全局限裁，防止字体溢出 | 方案 A (`configuration.json` 配置 `fontSizeMaxScale` 为 `"1.75"`) |
| 特定组件限制 | 方案 B (`maxFontScale` 属性值设置，如 1.15)                           |
| 应用有独立字体设置体系 | 方案 C (不配置 `configuration`，应用内自行管理)                           |

---

## 显示密度适配

### 密度变化的影响

| 概念 | 说明 |
|------|------|
| **densityUpdate** | 监听屏幕像素密度变化事件，设置中「显示大小」缩放变化时触发 |
| **onSizeChange** | 组件尺寸变化事件，仅响应布局变化导致的尺寸变化 |
| **px2vp / vp2px** | 物理像素与虚拟像素的单位换算工具方法 |
| **constraintSize** | 限制组件最大/最小尺寸，避免超出容器 |

### 监听密度变化 + 动态调整布局

使用 `UIObserver.on('densityUpdate', ...)` 监听屏幕密度变化：

```typescript
aboutToAppear(): void {
  this.getUIContext().getUIObserver().on('densityUpdate', (info) => {
    // 更新断点或根据 density 计算组件尺寸
    this.maxWidth = (windowWidth / 2 - this.parentPadding) / 2;
  });
}
```

### 使用 constraintSize 限制组件尺寸

```typescript
build() {
  Row() {
    Text('布局测试')
      .constraintSize({ maxWidth: this.maxWidth })  // 限制最大宽度
  }
  .onSizeChange((oldSize: SizeOptions, newSize: SizeOptions) => {
    // 响应尺寸变化，调整布局
  })
}
```

### 布局适配策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| `constraintSize` | 设置最大/最小宽高 | 固定容器内文字不溢出 |
| 响应式布局 | 结合断点系统动态切换布局 | 密度变化导致断点迁移 |
| `px2vp` / `vp2px` | 单位换算 | 需要精确像素计算的布局 |
| `onSizeChange` | 监听组件尺寸变化 | 父容器尺寸依赖子组件的场景 |

---

## 环境变量监听

### ⚠️ 重要原则：必须订阅环境变量变化

系统配置变化（字体缩放、显示密度）通过 `onConfigurationUpdate` 回调传递，应用必须订阅并同步到全局状态，否则所有页面将保持初始值。

```typescript
// ❌ 错误: 未订阅环境变量，页面始终使用初始值
let fontScale: number = 1.0;  // 永远是 1.0

// ✅ 推荐方案: 在 EntryAbility 中订阅 + AppStorage 全局同步
onConfigurationUpdate(newConfig: Configuration): void {
  AppStorage.setOrCreate('FontSizeScale', newConfig.fontSizeScale);
  AppStorage.setOrCreate('ScreenDensity', newConfig.screenDensity);
}
```

### 推荐方案详细用法

在 `EntryAbility.ets` 中订阅环境变量，组件通过 `@StorageProp` 响应变化：

```typescript
// EntryAbility.ets
onConfigurationUpdate(newConfig: Configuration): void {
  AppStorage.setOrCreate('FontSizeScale', newConfig.fontSizeScale);
  AppStorage.setOrCreate('ScreenDensity', newConfig.screenDensity);
  // 根据断点或具体值调整布局
}

// 页面组件中
@StorageProp('FontSizeScale') fontScale: number = 1.0;
@StorageProp('ScreenDensity') screenDensity: number = 1.0;
```

### 密度变化监听详细用法

使用 `UIObserver` 监听密度变化，适用于需要精细计算组件尺寸的场景：

```typescript
aboutToAppear(): void {
  this.getUIContext().getUIObserver().on('densityUpdate', (info) => {
    // density 变化后重新计算组件尺寸
    this.maxWidth = (windowWidth / 2 - this.parentPadding) / 2;
  });
}
```

### 组件尺寸变化监听

使用 `onSizeChange` 监听组件自身尺寸变化：

```typescript
build() {
  Column() {
    // 子组件
  }
  .onSizeChange((oldSize: SizeOptions, newSize: SizeOptions) => {
    // 响应布局变化，调整子组件排列或显隐
  })
}
```

---

## 完整文件结构

| 文件 | 职责 |
|------|------|
| `app.json5` | 通过 `"configuration": "$profile:configuration"` 引用字体缩放配置文件 |
| `base/profile/configuration.json` | 配置 `fontSizeScale` 和 `fontSizeMaxScale`，定义字体跟随策略 |
| `EntryAbility.ets` | 订阅 `onConfigurationUpdate`，同步 fontSizeScale / screenDensity 到 AppStorage |
| 页面组件 | 通过 `@StorageProp` 获取全局状态，响应字体缩放和密度变化 |
| 密度监听组件 | 使用 `UIObserver.on('densityUpdate')` 监听密度变化，动态计算组件尺寸 |
| 字体限制组件 | 使用 `maxFontScale` 限制单个组件的字体缩放 |

---

## 关键要点

1. **必须订阅 `onConfigurationUpdate`**，在其中同步字体缩放和屏幕密度到全局状态
2. **使用 `maxFontScale` 或 `fontSizeMaxScale`** 限制字体最大缩放，防止布局溢出
3. **监听 `densityUpdate` 事件**，在显示缩放变化时动态调整组件尺寸
4. **使用 `constraintSize`** 限制组件最大/最小尺寸，避免超出容器
5. **推荐响应式布局**，结合断点系统适配不同 DPI 和字体大小

---

## 常见问题对照表

| 问题现象 | 根因 | 修复方案 |
|---------|------|---------|
| 文字超出容器 | 未限制字体缩放倍数 | 使用 `maxFontScale` 或 `fontSizeMaxScale` |
| 组件遮挡/重叠 | 未响应字体或密度变化 | 订阅 `onConfigurationUpdate` + 动态布局 |
| 布局在不同设备显示大小下错乱 | 未监听 `densityUpdate` | 使用 `UIObserver.on('densityUpdate')` |
| 部分页面适配不一致 | 未全局同步环境变量 | 通过 `AppStorage` + `@StorageProp` 全局同步 |
| 组件尺寸计算不随密度变化 | 使用固定 px 值 | 使用 `px2vp` / `vp2px` 动态换算 |
