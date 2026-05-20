# 基础 Collection 类型概述

本章介绍仓颉语言中常用的几种基础 Collection 类型，包括 Array、ArrayList、HashSet 和 HashMap。

可以在不同的场景中选择适合对应业务的类型：

- Array：不需要增加和删除元素，但需要修改元素
- ArrayList：需要频繁对元素增删查改
- HashSet：希望每个元素都是唯一的
- HashMap：希望存储一系列的映射关系

下表是这些类型的基础特性：

| 类型名称        | 元素可变 | 增删元素 | 元素唯一性 | 有序序列 |
| --------------- | -------- | -------- | ---------- | -------------- |
| `Array<T>`      | Y        | N        | N          | Y              |
| `ArrayList<T>`     | Y        | Y        | N          | Y              |
| `HashSet<T>`    | N       | Y        | Y          | N              |
| `HashMap<K, V>` | K: N, V: Y | Y        | K: Y, V: N | N              |
