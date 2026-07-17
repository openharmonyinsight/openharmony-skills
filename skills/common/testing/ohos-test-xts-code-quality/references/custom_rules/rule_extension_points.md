# 规则扩展点规范

> **版本**: 1.1.0
> **更新日期**: 2026-04-23

## 概述

本文档定义了每条内置规则支持的**扩展维度**，即该规则可以被用户从哪些角度追加额外检查。

**扩展来源不限**——无论用户的扩展诉求来自API文档分析、团队编码规范、代码评审结论还是任何其他业务约束，只要诉求的检查维度落在该规则的扩展点范围内，就可以通过生成规则扩展配置来追加检查。

模型收到用户的扩展诉求后：
1. 识别诉求对应哪条内置规则（base_rule）和哪个扩展维度
2. 读取该规则对应的扩展点定义，了解该维度需要什么格式的配置
3. 根据用户诉求（可能需要读取API文档、编码规范等参考资料）生成扩展配置
4. 将配置保存到 `.xts_scan/extensions/` 目录，扫描引擎自动加载执行

## 扩展维度分类

每条规则根据其检测本质，支持不同维度的扩展：

| 扩展维度 | 说明 | 适用规则 | 诉求示例 |
|---------|------|---------|---------|
| `resource_api` | 资源创建/释放配对检测 | R204 | "PixelMap用完必须release()" |
| `async_api` | 异步API需done/await | R201, R202 | "这个Kit的接口都是异步的" |
| `forbidden_api` | 禁止使用的API | R001, R006 | "我们子系统不许用xxxSync()" |
| `assertion_api` | 需要断言验证的API | R004 | "调用getPixelMap后必须验证返回值" |
| `deprecated_api` | 已废弃的API | R013 | "旧版本API不能再用" |
| `config_check` | 配置文件检查项 | R007, R010, R021 | "Test.json不允许配置timeout" |
| `event_listener` | 事件监听器注册/移除 | R204 | "on('xxx')必须配对off('xxx')" |
| `hook_pair` | 生命周期钩子配对 | R205 | "beforeAll建了数据库必须有afterAll关" |

## 各规则扩展点定义

### R001: 禁止使用getSync系统接口

**扩展点**: `forbidden_api`

**扩展逻辑**: 从API文档中识别同步阻塞API（方法名包含`Sync`后缀，或文档明确标注为同步调用），追加到禁止列表。

**提取规则**:
- 方法名以 `Sync` 结尾（如 `getSync`, `writeSync`, `readSync`）
- 文档中明确标注"同步"且非性能关键路径的API
- 文档明确标注"已废弃"或"不建议使用"的同步API

**自动生成示例**:
```json
{
  "type": "extension",
  "base_rule": "R001",
  "id": "R001_EXT_IMAGE_KIT",
  "name": "ImageKit-禁止同步阻塞API",
  "extension_point": "forbidden_api",
  "api_source": "apis-image-kit/",
  "patterns": [
    {
      "name": "ImageReceiver.getImageSync",
      "pattern": "\\bimageReceiver\\.getImageSync\\s*\\(",
      "suggestion": "请使用异步方法 getImage()"
    }
  ]
}
```

### R002: 错误码断言必须是number类型

**扩展点**: `assertion_api`

**扩展逻辑**: 从API文档中识别返回错误码的API，确认其错误码类型（number/string/BusinessError），追加到断言类型检查列表。

**提取规则**:
- API文档中 `@throws` 或 `@syscap` 标注的错误码
- 错误码参数类型为 `BusinessError` 的API
- 返回 `Promise<T>` 且可能reject的API

### R004: 测试用例缺少断言

**扩展点**: `assertion_api`

**扩展逻辑**: 从API文档中识别返回值的API，为其生成断言建议模板。

**提取规则**:
- 有明确返回值类型的API方法
- 返回值用于验证的API（如状态查询、属性获取）

### R006: 禁止基于设备类型差异化

**扩展点**: `forbidden_api`

**扩展逻辑**: 从API文档中识别设备差异化API（屏幕尺寸、设备型号、CPU架构等），追加到禁止列表。

**提取规则**:
- 涉及屏幕尺寸/分辨率的API
- 涉及设备型号/CPU架构的API
- 文档标注"不同设备表现不同"的API

### R007: Test.json禁止配置项

**扩展点**: `config_check`

**扩展逻辑**: 从API文档中识别子系统特有的配置要求，追加到Test.json检查列表。

### R010: part_name/subsystem_name不匹配

**扩展点**: `config_check`

**扩展逻辑**: 从API文档中识别子系统名称，追加到子系统映射表。

### R012: 签名证书APL等级

**扩展点**: `config_check`

**扩展逻辑**: 从API文档中识别API的系统能力要求（systemCapability），判断是否需要高级别签名证书。

### R014: 测试HAP命名不规范

**扩展点**: `config_check`

**扩展逻辑**: 从API文档中识别子系统标识，用于HAP命名校验。

### R017: syscap.json配置多个能力

**扩展点**: `config_check`

**扩展逻辑**: 从API文档中提取 `SystemCapability` 声明，用于syscap.json检查。

### R021: hypium版本号

**扩展点**: `config_check`

**扩展逻辑**: 从API文档中识别最低API版本要求，判断hypium版本是否满足。

### R204: 资源创建后未释放

**扩展点**: `resource_api` (核心扩展点)

**扩展逻辑**: 从API文档中识别**需要手动释放资源的API**，提取创建/释放方法对，追加到资源管理检测列表。

**提取规则**:
1. **创建模式识别**: 文档中以下关键词对应的API方法
   - `create` - 工厂方法创建实例
   - `new` - 构造函数创建实例
   - `open` - 打开连接/流
   - `connect` - 建立连接
   - `on` - 注册事件监听
   - `subscribe` / `register` - 订阅/注册
   - `start` / `begin` - 启动任务

2. **释放模式识别**: 文档中以下关键词对应的API方法
   - `release` - 释放资源
   - `close` - 关闭连接/流
   - `destroy` - 销毁实例
   - `off` / `removeEventListener` - 移除事件监听
   - `unsubscribe` / `unregister` - 取消订阅
   - `stop` / `end` - 停止任务
   - `disconnect` - 断开连接

3. **文档线索识别**: 文档中以下描述表明该API需要资源释放
   - "使用完成后应主动调用...释放"
   - "需要调用...方法释放内存"
   - "使用完毕后需要调用...释放"
   - "不再使用时应调用...释放"
   - "占用内存较大，应...释放"

**自动生成示例** (基于 ImageKit API文档):
```json
{
  "type": "extension",
  "base_rule": "R204",
  "id": "R204_EXT_IMAGE_KIT",
  "name": "ImageKit-资源管理API检测",
  "extension_point": "resource_api",
  "api_source": "apis-image-kit/",
  "resource_pairs": [
    {
      "class": "ImageReceiver",
      "create": "image.createImageReceiver",
      "release": ".release()",
      "doc_hint": "使用完成后应主动调用release方法及时释放内存",
      "patterns": {
        "create": "\\bimage\\.createImageReceiver\\s*\\(",
        "release": "\\.release\\s*\\("
      }
    },
    {
      "class": "ImagePacker",
      "create": "image.createImagePacker",
      "release": ".release()",
      "doc_hint": "使用完毕后需要调用release方法释放",
      "patterns": {
        "create": "\\bimage\\.createImagePacker\\s*\\(",
        "release": "\\.release\\s*\\("
      }
    },
    {
      "class": "ImageSource",
      "create": "image.createImageSource",
      "release": ".release()",
      "doc_hint": "不再使用时应调用release方法释放",
      "patterns": {
        "create": "\\bimage\\.createImageSource\\s*\\(",
        "release": "\\.release\\s*\\("
      }
    },
    {
      "class": "PixelMap",
      "create": ".createPixelMap",
      "release": ".release()",
      "doc_hint": "PixelMap对象使用完毕后需要调用release释放",
      "patterns": {
        "create": "\\.createPixelMap\\s*\\(",
        "release": "\\.release\\s*\\("
      }
    }
  ]
}
```

### R205: beforeAll/beforeEach配对缺失

**扩展点**: `resource_api` (与R204联动)

**扩展逻辑**: 与R204共享资源API列表。如果R204扩展中识别了需要释放的资源，R205也会检查对应资源在beforeAll中的创建是否有afterAll释放。

### R201: 异步用例缺少done/await

**扩展点**: `async_api`

**扩展逻辑**: 从API文档中识别异步API（返回Promise、使用callback、标注async），追加到异步检测列表。

**提取规则**:
- 方法签名包含 `Promise<T>` 返回值
- 方法签名包含 `AsyncCallback<T>` 参数
- 文档标注"异步调用"或"回调方式"
- 方法名不包含 `Sync` 后缀的变体

### R202: 异步回调/Promise未正确处理错误

**扩展点**: `async_api`

**扩展逻辑**: 与R201共享异步API列表，额外检查错误处理。

### R203: 并发调用无隔离

**扩展点**: `async_api`

**扩展逻辑**: 从API文档中识别不支持并发调用的API（文档标注"不支持并发"或"需串行调用"）。

## 扩展生成流程

```
用户诉求（任意来源）
─────────────────────────────────────
"R204还要检查PixelMap是否调用了release()"
"我们子系统不许用xxxSync()"
"评审发现beforeAll建数据库没afterAll关"
"这个Kit的接口都是异步的要await"
                                         │
    ┌────────────────────────────────────┘
    │
    ├─→ 模型识别: 诉求 → 规则(R204) + 扩展维度(resource_api)
    │
    ├─→ 模型查阅: rule_extension_points.md 了解该维度需要的配置格式
    │
    ├─→ 模型分析: 根据诉求提取检查模式
    │   如果涉及API文档 → 可用 extension_generator.py 辅助提取
    │   如果是规范/评审结论 → 直接根据描述生成
    │
    ├─→ 模型生成: 扩展配置JSON
    │   → .xts_scan/extensions/R204_EXT_{标识}.json
    │
    └─→ 扫描引擎自动加载执行
        内置扫描器 + 扩展扫描器 并行
        结果合并到统一报告
```

## 扩展配置的 resource_pairs 格式

对于 `resource_api` 类型的扩展（如R204），除了常规的 `patterns` 数组外，还支持 `resource_pairs` 字段，提供更精确的创建/释放配对检测：

```json
{
  "type": "extension",
  "base_rule": "R204",
  "id": "R204_EXT_{KIT}",
  "resource_pairs": [
    {
      "class": "ClassName",
      "create": "factory.createXxx",
      "release": ".release()",
      "doc_hint": "文档中的释放提示原文",
      "patterns": {
        "create": "正则匹配创建调用",
        "release": "正则匹配释放调用"
      },
      "import_check": {
        "module": "@kit.XxxKit",
        "symbol": "ClassName"
      }
    }
  ]
}
```

`resource_pairs` 字段会被 `common.py` 的 `execute_custom_rules()` 函数识别，执行更精确的配对检测（而非简单正则匹配）。

## 已知限制

1. **文档格式依赖**: 扩展生成依赖API文档的格式规范（Markdown+JSDoc），非标准格式可能需要手动调整
2. **语义理解局限**: 自动提取基于关键词匹配，无法完全理解API语义，生成结果建议人工审核
3. **跨Kit引用**: 如果API文档中引用了其他Kit的API（如ImageReceiver引用Camera），跨Kit的资源释放关系需要手动补充
