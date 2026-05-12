# 调用链回溯分析

这是找到问题根源的关键步骤，必须从崩溃点追溯到参数来源。

## 回溯步骤

### 1. 从崩溃点向上回溯

从调用栈的栈顶开始，逐层向上分析：

```
#00 GetDrawableVectorById (崩溃点)
#01 GetSubAppNodeId
#02 DrawableCache
```

### 2. 分析每一层的参数传递

对于每一层调用，分析：

- 函数签名是什么
- 函数参数来源
- 参数的生命周期管理

示例：

```cpp
// rs_sub_thread.cpp:220
auto surfaceParams = static_cast<RSSurfaceParams*>(nodeDrawable->GetRenderParams().get());

// rs_sub_thread.cpp:226
RSTagTracker tagTacker(grContext_, GetSubAppNodeId(nodeDrawable, surfaceParams), ...);

// rs_sub_thread.cpp:176
for (const auto& subDrawable : nodeDrawable->GetDrawableVectorById(surfaceParams->GetAllSubSurfaceNodeIds()));
```

### 3. 识别参数来源问题

分析参数的来源是否存在问题：

- 指针是否有效
- 引用是否指向有效对象
- 对象生命周期是否足够长
- 是否存在多线程竞争

### 4. 生命周期分析

关键问题：

- 对象何时被创建
- 对象何时被销毁
- 在调用过程中对象是否可能被销毁
- 是否有其它线程可能修改或销毁对象