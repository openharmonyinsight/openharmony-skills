# 接口

## interface ConcurrentMap\<K, V>

```cangjie
public interface ConcurrentMap<K, V> {
    func add(key: K, value: V): ?V
    func addIfAbsent(key: K, value: V): ?V
    func entryView(key: K, fn: (MapEntryView<K, V>) -> Unit): ?V
    func get(key: K): ?V
    func contains(key: K): Bool
    func put(key: K, value: V): ?V
    func putIfAbsent(key: K, value: V): ?V
    func remove(key: K): ?V
    func remove(key: K, predicate: (V) -> Bool): ?V
    func replace(key: K, value: V): ?V
    func replace(key: K, eval: (V) -> V): ?V
    func replace(key: K, predicate: (V) -> Bool, eval: (V) -> V): ?V
    operator func [](key: K): V
    operator func [](key: K, value!: V): Unit
}
```

功能：保证线程安全和操作原子性的 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 接口定义。

[ConcurrentMap](collection_concurrent_interface.md#interface-concurrentmapk-v) 接口中声明了并发场景下线程安全的 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 必须保证**原子性**的方法，我们希望定义的线程安全 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 类都能实现 [ConcurrentMap](collection_concurrent_interface.md#interface-concurrentmapk-v) 接口。例如我们在该包中定义的 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 就实现了 [ConcurrentMap](collection_concurrent_interface.md#interface-concurrentmapk-v) 接口，并提供了 [ConcurrentMap](collection_concurrent_interface.md#interface-concurrentmapk-v) 中所声明方法的保证原子性的实现。

[ConcurrentMap](collection_concurrent_interface.md#interface-concurrentmapk-v) 接口中声明了并发 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 在并发场景下需要保证原子性的方法。

并发 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 为“键”到“值”的映射，其中 K 为键的类型，V 为值的类型。

### func add(K, V)

```cangjie
func add(key: K, value: V): ?V
```

功能：将指定的值 value 与此 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中指定的键 key 关联。如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中已经包含键 key 的关联，则旧值将被替换；如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不包含键 key 的关联，则添加键 key 与值 value 的关联。

参数：

- key: K - 要放置的键。
- value: V - 要关联的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回旧的值 Some(V)；当赋值前 key 不存在时，返回 None。

### func addIfAbsent(K, V)

```cangjie
func addIfAbsent(key: K, value: V): ?V
```

功能：当此 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不存在键 key 时，在 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中添加指定的值 value 与指定的键 key 的关联。如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 已经包含键 key，则不执行赋值操作。

参数：

- key: K - 要放置的键。
- value: V - 要分配的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回当前 key 对应的值 Some(V)，且不执行赋值操作；当赋值前 key 不存在时，返回 None。

### func contains(K)

```cangjie
func contains(key: K): Bool
```

功能：判断 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中是否包含指定键 key 的关联。

参数：

- key: K - 传递要判断的 key。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当 key 存在时返回 true；当 key 不存在时返回 false。

### func entryView(K, (MapEntryView\<K, V>) -> Unit)

```cangjie
func entryView(key: K, fn: (MapEntryView<K, V>) -> Unit): ?V
```

功能：根据指定键 key 获取当前映射中相应的键值对视图 entryView，并调用函数 fn 对该键值对进行增、删、改操作，并返回最终映射中键 key 对应的值。

如果当前映射中不包含键 key，则将获取一个空视图 entryView，如果将其 value 置为非 None 值，则将在当前映射中增加 key-value 键值对。

如果当前映射中包含键 key，则将获取 key-value 的视图，如果将 value 置为 None，则相当于从当前映射中删除该键值对；如果将 value 置为新的非 None 值，则相当于修改当前映射中键 key 对应的值。

参数：

- key: K - 待获取其相应视图的键。
- fn: ([MapEntryView](../../collection/collection_package_api/collection_package_interface.md#interface-mapentryviewk-v)\<K, V>) -> [Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 对指定视图进行的自定义操作，可用于对映射中键值对进行增、删、改操作。

返回值：

- ?V - 函数 fn 调用结束后当前映射中键 key 对应的值，如果 key 不存在，返回 None。

### func get(K)

```cangjie
func get(key: K): ?V
```

功能：返回 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中键 key 所关联的值。

参数：

- key: K - 传递 key，获取 value。

返回值：

- ?V - 当 key 存在时，返回其关联的值 Some(V)；当 key 不存在时，返回 None。

### func put(K, V) <sup>(deprecated)</sup>

```cangjie
func put(key: K, value: V): ?V
```

功能：将指定的值 value 与此 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中指定的键 key 关联。如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中已经包含键 key 的关联，则旧值将被替换；如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不包含键 key 的关联，则添加键 key 与值 value 的关联。

> **注意：**
>
> 未来版本即将废弃，使用 [add(K, V)](#func-addk-v) 替代。

参数：

- key: K - 要放置的键。
- value: V - 要关联的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回旧的值 Some(V)；当赋值前 key 不存在时，返回 None。

### func putIfAbsent(K, V) <sup>(deprecated)</sup>

```cangjie
func putIfAbsent(key: K, value: V): ?V
```

功能：当此 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不存在键 key 时，在 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中添加指定的值 value 与指定的键 key 的关联。如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 已经包含键 key，则不执行赋值操作。

> **注意：**
>
> 未来版本即将废弃，使用 [addIfAbsent(K, V)](#func-addifabsentk-v) 替代。

参数：

- key: K - 要放置的键。
- value: V - 要分配的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回当前 key 对应的值 Some(V)，且不执行赋值操作；当赋值前 key 不存在时，返回 None。

### func remove(K)

```cangjie
func remove(key: K): ?V
```

功能：从此映射中删除指定键 key 的映射（如果存在）。

参数：

- key: K - 传入要删除的 key。

返回值：

- ?V - 如果移除之前 key 存在，则返回 key 对应的值 Some(V)；当移除时 key 不存在时，返回 None。

### func remove(K, (V) -> Bool) <sup>(deprecated)</sup>

```cangjie
func remove(key: K, predicate: (V) -> Bool): ?V
```

功能：如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中存在键 key 且 key 所关联的值 v 满足条件 predicate，则从 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中删除 key 的关联。

> **注意：**
>
> 未来版本即将废弃，使用 [entryView(K, (MapEntryView\<K, V>) -> Unit)](#func-entryviewk-mapentryviewk-v---unit) 替代。

参数：

- key: K - 传入要删除的 key。
- predicate: (V) ->[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传递一个 lambda 表达式进行判断。

返回值：

- ?V - 如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中存在 key，则返回 key 对应的旧值 Some(V)；当 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不存在 key 时，或者 key 关联的值不满足 predicate 时，返回 None。

### func replace(K, (V) -> Bool, (V) -> V) <sup>(deprecated)</sup>

```cangjie
func replace(key: K, predicate: (V) -> Bool, eval: (V) -> V): ?V
```

功能：如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中存在键 key（假设其关联的值为 v），且 v 满足条件 predicate，则将 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中键 key 关联的值替换为 eval(v) 的计算结果；如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不存在键 key，或者存在键 key 但关联的值不满足 predicate，则不对 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 做任何修改。

> **注意：**
>
> 未来版本即将废弃，使用 [entryView(K, (MapEntryView\<K, V>) -> Unit)](#func-entryviewk-mapentryviewk-v---unit) 替代。

参数：

- key: K - 传入要替换所关联值的键。
- predicate: (V) ->[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传递一个 lambda 表达式进行判断。
- eval: (V) ->V - 传入计算用于替换的新值的函数。

返回值：

- ?V - 如果 key 存在，则返回 key 对应的旧值 Some(V)；当 key 不存在时，或者 key 关联的值不满足 predicate 时，返回 None。

### func replace(K, (V) -> V) <sup>(deprecated)</sup>

```cangjie
func replace(key: K, eval: (V) -> V): ?V
```

功能：如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中存在键 key（假设其关联的值为 v），则将 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中键 key 关联的值替换为 eval(v) 的计算结果；如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不存在键 key，则不对 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 做任何修改。

> **注意：**
>
> 未来版本即将废弃，使用 [entryView(K, (MapEntryView\<K, V>) -> Unit)](#func-entryviewk-mapentryviewk-v---unit) 替代。

参数：

- key: K - 传入要替换所关联值的键。
- eval: (V) ->V - 传入计算用于替换的新值的函数。

返回值：

- ?V - 如果 key 存在，则返回 key 对应的旧值 Some(V)；当 key 不存在时，返回 None。

### func replace(K, V)

```cangjie
func replace(key: K, value: V): ?V
```

功能：如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中存在 key，则将 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中键 key 关联的值替换为 value；如果 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 中不存在 key，则不对 [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v) 做任何修改。

参数：

- key: K - 传入要替换所关联值的键。
- value: V - 传入要替换成的新值。

返回值：

- ?V - 如果 key 存在，则返回 key 对应的旧值 Some(V)；当 key 不存在时，返回 None。

### operator func \[](K)

```cangjie
operator func [](key: K): V
```

功能：根据指定键 key 获取值。如果键 key 存在，返回对应的值；如果不存在，抛出异常。

参数：

- key: K - 待获取其值的键。

返回值：

- V - 键 key 对应的值。

异常：

- [NoneValueException](../../core/core_package_api/core_package_exceptions.md#class-nonevalueexception) - 当前映射中不存在键 key。

### operator func \[](K, V)

```cangjie
operator func [](key: K, value!: V): Unit
```

功能：设置指定键 key 的值为 value。如果键 key 存在，新 value 覆盖旧 value；如果键不存在，添加此键值对。

参数：

- key: K - 待设置其值的键。
- value!: V - 待设置的值。
