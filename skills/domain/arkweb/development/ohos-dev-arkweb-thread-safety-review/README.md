# ohos-dev-arkweb-thread-safety-review

ArkWeb/Chromium C++ 线程安全与生命周期审查 Skill，用于检查跨线程访问、异步回调生命周期、GPU/Audio 线程约束、NDK/UI 回调、mojo 使用、WebContents/Profile 访问和 scoped_refptr 风险。

## 目录位置

```text
skills/domain/arkweb/development/ohos-dev-arkweb-thread-safety-review/
```

## 命名与元数据

- `scope`: `domain`
- `stage`: `development`
- `domain`: `arkweb`
- `capability`: `thread-safety-review`

## 使用场景

当需要对 ArkWeb/Chromium C++ 单文件进行线程安全、生命周期和跨线程访问风险审查时，使用本 Skill。
