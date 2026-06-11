# SomeAPI

## 概述

SomeAPI 提供数据查询、更新和删除功能。

## 功能列表

1. 数据查询
2. 数据更新
3. 数据删除

## 使用说明

### 查询数据

```typescript
SomeAPI.query(options)
```

### 更新数据

```typescript
SomeAPI.update(id, newData)
```

### 删除数据

```typescript
SomeAPI.remove(id)
```

## 权限要求

使用此 API 需要申请以下权限：

- ohos.permission.DATA_READ
- ohos.permission.DATA_WRITE

## 约束说明

1. 查询操作每次最多返回 1000 条记录
2. 更新操作不支持批量更新
3. 删除操作不可撤销
