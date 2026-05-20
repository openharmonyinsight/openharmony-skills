# std.collection.concurrent

## 功能介绍

collection.concurrent 包提供了并发安全的集合类型实现。

本包实现了以下几种并发安全的集合类型：

- [ArrayBlockingQueue](./collection_concurrent_package_api/collection_concurrent_class.md#class-arrayblockingqueuee)：以数组的形式实现的具有固定大小的有界队列。

- [ConcurrentHashMap](./collection_concurrent_package_api/collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)：线程安全的哈希表实现，支持高并发的读写操作。

- [ConcurrentLinkedQueue](./collection_concurrent_package_api/collection_concurrent_class.md#class-concurrentlinkedqueuee)：一种线程安全的队列数据结构，特点是在添加元素时，如果当前的尾部 Block 已满，那么会创建一个新的 Block，而不是阻塞等待。这样可以保证在多线程环境下，队列的操作不会因为阻塞而导致线程的阻塞，从而提高了程序的性能。

- [LinkedBlockingQueue](./collection_concurrent_package_api/collection_concurrent_class.md#class-linkedblockingqueuee)：一种阻塞队列，它支持在队列为空时阻塞获取元素的操作，以及在队列已满时阻塞添加元素的操作。

## API 列表

### 类型别名

| 类型别名                                                       | 功能                          |
| ------------------------------------------------------------ | ----------------------------- |
| [BlockingQueue\<E> <sup>(deprecated)</sup>](./collection_concurrent_package_api/collection_concurrent_types.md#type-blockingqueuee-deprecated) | LinkedBlockingQueue 的别名。 |
| [NonBlockingQueue\<E> <sup>(deprecated)</sup>](./collection_concurrent_package_api/collection_concurrent_types.md#type-nonblockingqueuee-deprecated) | ConcurrentLinkedQueue 的别名。 |

### 接口

| 接口名 | 功能 |
| -------- | --------- |
| [ConcurrentMap\<K, V>](./collection_concurrent_package_api/collection_concurrent_interface.md#interface-concurrentmapk-v) | 保证线程安全和操作原子性的 Map 接口定义。 |

### 类

|  类名 | 功能  |
| ------------ | ------------ |
| [ArrayBlockingQueue\<E>](./collection_concurrent_package_api/collection_concurrent_class.md#class-arrayblockingqueuee) | 基于数组实现的 Blocking Queue 数据结构及相关操作函数。 |
| [ConcurrentHashMapIterator\<K, V> where K <: Hashable & Equatable\<K>](./collection_concurrent_package_api/collection_concurrent_class.md#class-concurrenthashmapiteratork-v-where-k--hashable--equatablek) | 此类主要实现 Concurrent HashMap 的迭代器功能。 |
| [ConcurrentHashMap\<K, V> where K <: Hashable & Equatable\<K>](./collection_concurrent_package_api/collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) | 此类用于实现并发场景下线程安全的哈希表 ConcurrentHashMap 数据结构及相关操作函数。 |
| [ConcurrentLinkedQueue\<E>](./collection_concurrent_package_api/collection_concurrent_class.md#class-concurrentlinkedqueuee) | 提供一个线程安全的队列，可以在多线程环境下安全地进行元素的添加和删除操作。 |
| [LinkedBlockingQueue\<E>](./collection_concurrent_package_api/collection_concurrent_class.md#class-linkedblockingqueuee) | 实现是带阻塞机制并支持用户指定容量上界的并发队列。 |
