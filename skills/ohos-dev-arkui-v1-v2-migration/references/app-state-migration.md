# 应用级状态迁移

## 渐进迁移原则：保留 V1 API，只新增 V2 API

渐进迁移过程中，**不得删除原有的 V1 状态管理 API 调用**，只在其旁边新增 V2 对应调用。原因：

1. 同一 `.ts` 文件中可能包含多个 key 的 V1 API 调用，其中部分 key 仍被未迁移的 V1 组件使用
2. 删除 V1 API 会导致未迁移的组件运行时找不到数据

**正确做法**：参照 `component_analyzer.py` 的 `stateApiByKey` 输出，确认某个 key 的所有 `decoratorUsage`（即所有使用该 key 的组件装饰器）均已迁移到 V2 后，才可移除该 key 对应的 V1 API 调用。

```typescript
// 迁移前（model.ts）
AppStorage.setOrCreate('count', 42);
AppStorage.setOrCreate('theme', 'dark');

// 迁移 'count' 组件后 —— 只新增 V2 API，不删除 V1
AppStorage.setOrCreate('count', 42);               // V1 保留
AppStorage.setOrCreate('theme', 'dark');             // V1 保留
const countStorage = AppStorageV2.connect(           // V2 新增
  CountStorage, 'count', () => new CountStorage()
)!;

// 后续当 'theme' 也迁移完成后，才可删除 AppStorage.setOrCreate('theme', ...)
// 当所有 key 都迁移完成后，才可删除全部 AppStorage 调用
```

## AppStorage -> AppStorageV2

### 核心差异

| 维度 | V1 AppStorage | V2 AppStorageV2 |
|------|---------------|-----------------|
| 数据模型 | string key → 任意类型值（松散） | Type + key → 类型化对象（严格） |
| 绑定方式 | 装饰器 `@StorageLink`/`@StorageProp` | `connect()` 方法 + `@Local` |
| 同步方向 | 区分单向（@StorageProp）和双向（@StorageLink） | 统一双向同步，单向需 @Monitor 辅助 |
| 观测机制 | 自动观测属性变化 | 需 `@ObservedV2` + `@Trace` 显式标注 |
| 返回类型 | `SubscribedAbstractProperty<T>` 包装类，需手动 `aboutToBeDeleted()` | 直接返回 `T` 对象，无需手动释放 |
| API 版本 | API 7+（驼峰 API 10+） | API 12+ |

### 装饰器映射

| V1 | V2 | 说明 |
|----|-----|------|
| `@StorageLink('key') var: Type` | `@Local var: Type = AppStorageV2.connect(Type, 'key', () => default)!` | 双向同步。V2 通过 connect 获取对象引用，修改 @Trace 属性自动同步 |
| `@StorageProp('key') var: Type` | `@Local var: Type` + `@Monitor` 监听变化覆盖本地值 | V2 无单向绑定。用 @Local 存本地副本，@Monitor 监听 connect 对象变化后覆盖 |

### API 方法映射

#### 初始化与读写

| V1 AppStorage | V2 AppStorageV2 | 说明 |
|---|---|---|
| `setOrCreate('key', value)` | `connect(Type, 'key', () => new Type())` | V1 存原始值，V2 存类型化对象。首次 connect 调用创建，后续返回已有实例 |
| `get('key')` | `connect(Type, 'key')?.prop` | V2 返回整个对象，通过 @Trace 属性访问具体值 |
| `set('key', newValue)` | 直接修改 connected 对象的 `@Trace` 属性 | V2: `obj.prop = newValue` 即触发观测更新 |

#### 绑定与引用

| V1 AppStorage | V2 AppStorageV2 | 说明 |
|---|---|---|
| `link('key')` → `SubscribedAbstractProperty<T>` | `connect(Type, 'key')` → `T` | V1 返回包装类需手动释放；V2 返回对象本身 |
| `setAndLink('key', default)` | `connect(Type, 'key', () => new Type())` | 不存在则自动创建 |
| `prop('key')` → `SubscribedAbstractProperty<T>` | `connect(Type, 'key')` + `@Monitor` | V1 单向绑定；V2 无单向概念，需 @Monitor 辅助实现 |
| `setAndProp('key', default)` | `connect(Type, 'key', () => default)` + `@Monitor` | 同上 |
| `ref('key')` → `AbstractProperty<T>` (API 12+) | `connect(Type, 'key')` | V1 ref 无需手动释放；V2 connect 同样无需 |
| `setAndRef('key', default)` (API 12+) | `connect(Type, 'key', () => default)` | 不存在则自动创建 |

#### 查询与管理

| V1 AppStorage | V2 AppStorageV2 | 说明 |
|---|---|---|
| `has('key')` | `keys().includes('key')` | V2 无 has()，用 keys 判断 |
| `delete('key')` | `remove('key')` 或 `remove(Type)` | V2 支持按 key 或按类型删除 |
| `keys()` → `IterableIterator<string>` | `keys()` → `Array<string>` | 返回类型不同 |
| `clear()` | 遍历 `keys()` 逐个 `remove()` | V2 无 clear() |
| `size()` | `keys().length` | V2 无 size() |

#### 废弃 API（PascalCase，API 7+，已废弃）

| V1 废弃 API | → V1 驼峰 API | → V2 替代 |
|---|---|---|
| `AppStorage.SetOrCreate('key', val)` | `setOrCreate` | `connect(Type, 'key', () => val)` |
| `AppStorage.Set('key', val)` | `set` | 修改 connected 对象属性 |
| `AppStorage.Get('key')` | `get` | `connect(Type, 'key')?.prop` |
| `AppStorage.Link('key')` | `link` | `connect(Type, 'key')` |
| `AppStorage.SetAndLink('key', val)` | `setAndLink` | `connect(Type, 'key', () => val)` |
| `AppStorage.Prop('key')` | `prop` | `connect(Type, 'key')` + @Monitor |
| `AppStorage.SetAndProp('key', val)` | `setAndProp` | `connect(Type, 'key', () => val)` + @Monitor |
| `AppStorage.Has('key')` | `has` | `keys().includes('key')` |
| `AppStorage.Delete('key')` | `delete` | `remove('key')` |
| `AppStorage.Keys()` | `keys` | `keys()` |
| `AppStorage.Clear()` / `staticClear()` | `clear` | 遍历 `remove()` |
| `AppStorage.IsMutable('key')` | (始终返回 true) | 无对应，V2 对象始终可变 |
| `AppStorage.Size()` | `size` | `keys().length` |

### 迁移示例

#### @StorageLink 双向绑定迁移

```typescript
// V1
@Entry @Component
struct Page1 {
  @StorageLink('count') count: number = 0;
  build() { Text(`${this.count}`) }
}
// 初始化（通常在 EntryAbility 或其他文件中）
AppStorage.setOrCreate('count', 42);
```

```typescript
// V2
import { AppStorageV2 } from '@kit.ArkUI';

@ObservedV2
export class CountStorage {
  @Trace public count: number = 0;
}

@Entry @ComponentV2
struct Page1 {
  @Local storage: CountStorage = AppStorageV2.connect(
    CountStorage, 'count', () => new CountStorage()
  )!;
  build() { Text(`${this.storage.count}`) }
}
```

#### @StorageProp 单向绑定迁移

```typescript
// V1
@Component
struct Child {
  @StorageProp('count') count: number = 0;
  build() { Text(`${this.count}`) }
}
```

```typescript
// V2 — @Local 存本地副本 + @Monitor 监听覆盖
@ComponentV2
struct Child {
  @Local localCount: number = 0;
  storage: CountStorage = AppStorageV2.connect(
    CountStorage, 'count', () => new CountStorage()
  )!;
  @Monitor('storage.count')
  onCountChange(mon: IMonitor) {
    this.localCount = this.storage.count;
  }
  build() { Text(`${this.localCount}`) }
}
```

#### API 调用迁移

迁移 API 调用时，**保留原有 V1 调用，在其旁边新增 V2 调用**。只有当所有使用该 key 的组件都已迁移到 V2 后，才可移除 V1 调用。

```typescript
// === 迁移前（model.ts）===
AppStorage.setOrCreate('count', 42);          // V1 初始化
let val = AppStorage.get('count');             // V1 读取
AppStorage.set('count', 100);                  // V1 写入
AppStorage.setOrCreate('theme', 'dark');       // 其他 key 的 V1 调用

// === 迁移 'count' 后（保留 V1，新增 V2）===
AppStorage.setOrCreate('count', 42);          // V1 保留（其他 V1 组件可能仍在使用）
AppStorage.setOrCreate('theme', 'dark');       // V1 保留（'theme' 尚未迁移）

// V2 新增
let storage = AppStorageV2.connect(
  CountStorage, 'count', () => new CountStorage()
)!;
let val = storage.count;                       // V2 读取
storage.count = 100;                           // V2 写入（@Trace 自动触发更新）

// === 最终清理（所有组件迁移完成后）===
// 此时方可删除 AppStorage.setOrCreate('count', 42) 等残留的 V1 调用
```

## LocalStorage -> @ObservedV2/@Trace 单例

V2将观察能力内嵌到数据本身，不再和View层耦合。用 @ObservedV2/@Trace 创建可导出的单例类替代 LocalStorage。

```typescript
// V2替代方案
@ObservedV2
export class MyStorage {
  public static singleton_: MyStorage;
  static instance() {
    if (!MyStorage.singleton_) { MyStorage.singleton_ = new MyStorage(); }
    return MyStorage.singleton_;
  }
  @Trace public count: number = 47;
}

// 页面中使用
import { MyStorage } from './storage';
@Entry @ComponentV2
struct Page1 {
  storage: MyStorage = MyStorage.instance();
  build() { Text(`${this.storage.count}`) }
}
```

### @LocalStorageProp效果（本地修改不同步回源）
用 @Local + @Monitor 实现：
```typescript
@Local count: number = this.storage.count;
@Monitor('storage.count')
onCountChange(mon: IMonitor) { this.count = this.storage.count; }
```

## Environment -> 直接获取系统环境变量

V2不再需要Environment，直接通过 UIAbilityContext.config 获取：

```typescript
// EntryAbility.ets
env.language = this.context.config.language;
env.colorMode = this.context.config.colorMode;

// 页面中使用
import { env } from '../pages/Env';
Text(`languageCode: ${env.language}`)
```

## PersistentStorage -> PersistenceV2

V2自动持久化 @Trace 属性，不再与 AppStorage 耦合：

```typescript
import { PersistenceV2, Type } from '@kit.ArkUI';

@ObservedV2
class Sample {
  @Type(V2Data) @Trace public num: number = 1;
  @Trace public V2: V2Data = new V2Data();
}

@Local p: Sample = PersistenceV2.globalConnect({
  type: Sample, key: 'connect2', defaultCreator: () => new Sample()
})!;
```

**注意**：迁移时同样保留 `PersistentStorage.persistProp()` 等 V1 调用，只新增 `PersistenceV2.globalConnect()`。只有当所有使用该 key 的组件都迁移到 V2 后，才可移除对应的 `persistProp` 调用。

### 数据迁移函数
从PersistentStorage迁移数据到PersistenceV2时，需要编写一次性迁移函数：
1. 读取PersistentStorage数据
2. 写入PersistenceV2
3. 删除PersistentStorage数据
4. 设置迁移完成标志
