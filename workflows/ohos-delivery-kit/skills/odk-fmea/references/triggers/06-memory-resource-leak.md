# 内存与资源泄漏故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../06-memory-resource-leak.md](../06-memory-resource-leak.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| M-01 | Native 内存泄漏 | new/malloc 与 delete/free 不配对（异常分支跳过释放）；循环持续分配无释放点；无 RAII/智能指针管理 |
| M-02 | JS 堆内存泄漏 | 全局对象/单例持引用、闭包捕获大对象；监听器/订阅/定时器未随页面销毁移除；大缓存无上限 |
| M-03 | RefBase 引用计数误用 | sptr 与裸指针混用；用裸指针构造 sptr（未用 MakeSptr）；栈上构造 RefBase 对象；双向 sptr 循环引用；无 sptr 单独用 wptr |
| M-04 | Ashmem / 映射资源泄漏 | Ashmem/MappedFile 的 Map/Unmap、Create/Close 未严格配对（映射需手动释放）；fd 未用 UniqueFd 管理 |
| M-05 | 内存水位失控（无上限设计） | 缓存/队列/对象池无容量上限与 LRU；大图/大数据常驻内存；未订阅系统低内存通知主动释放 |
