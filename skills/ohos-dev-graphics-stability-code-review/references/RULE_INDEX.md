# 稳定性规则总索引

本文件列出所有可用的稳定性规则及其配置信息。

## 规则统计

| 大类 | 规则数量 | 严重程度分布 |
|------|----------|--------------|
| 异常处理 | 2 | MEDIUM: 2 |
| 并发稳定性 | 1 | HIGH: 1 |
| 资源管理 | 5 | HIGH: 3, MEDIUM: 2 |
| 边界条件 | 14 | CRITICAL: 2, HIGH: 8, MEDIUM: 4 |
| 图形稳定性 | 12 | HIGH: 12 |
| **总计** | **34** | CRITICAL: 2, HIGH: 24, MEDIUM: 8, LOW: 0 |

---

## 规则列表

### CRITICAL (2)

| 规则 ID | 名称 | 分类 | 描述 |
|---------|------|------|------|
| StabilityCodeReview_BoundaryCondition_001 | Parcel数据不可作为循环或递归条件 | 边界条件 | Parcel 数据作为循环条件可能导致无限循环或拒绝服务 |
| StabilityCodeReview_BoundaryCondition_002 | Parcel数据不可直接作为数组下标 | 边界条件 | Parcel 数据直接作为数组下标可能导致内存越界访问 |

### HIGH (24)

| 规则 ID | 名称 | 分类 | 描述 |
|---------|------|------|------|
| StabilityCodeReview_ConcurrencyStability_001 | RenderNodeDrawable全局变量写入问题 | 并发稳定性 | RenderNodeDrawable全局变量在多线程场景写入未加锁保护 |
| StabilityCodeReview_ResourceManagement_001 | 反序列化内存泄漏 | 资源管理 | 反序列化过程中的内存泄漏风险 |
| StabilityCodeReview_ResourceManagement_002 | dlopen需配对dlclose | 资源管理 | dlopen 后未配对调用 dlclose 导致动态库资源泄漏 |
| StabilityCodeReview_ResourceManagement_004 | 文件描述符泄漏 | 资源管理 | open/socket/epoll 等文件描述符在错误路径上未关闭 |
| StabilityCodeReview_BoundaryCondition_003 | Parcel数据不可直接作为内存申请大小 | 边界条件 | Parcel 数据直接作为内存申请大小可能导致 OOM 或整数溢出 |
| StabilityCodeReview_BoundaryCondition_004 | 容器size增长的对外接口应限制上限 | 边界条件 | 容器 size 增长的对外接口未限制上限可能导致 OOM |
| StabilityCodeReview_BoundaryCondition_006 | Parcel序列化和反序列化必须匹配 | 边界条件 | Parcel 序列化和反序列化不匹配导致数据处理错误 |
| StabilityCodeReview_BoundaryCondition_007 | 外部数据类型转换需范围检查 | 边界条件 | 外部数据类型转换未做范围检查导致数据截断或溢出 |
| StabilityCodeReview_BoundaryCondition_008 | 加减乘除运算应避免类型溢出或回绕 | 边界条件 | 加减乘除运算未考虑类型溢出或回绕导致计算错误 |
| StabilityCodeReview_BoundaryCondition_011 | 类型强制转换未校验，可能导致越界读 | 边界条件 | 类型强制转换未校验范围导致越界读取 |
| StabilityCodeReview_BoundaryCondition_012 | 数组下标的计算应避免整数回绕导致内存越界访问 | 边界条件 | 数组下标计算发生整数回绕导致内存越界访问 |
| StabilityCodeReview_BoundaryCondition_014 | JSON解析安全风险 | 边界条件 | JSON 解析过程中的安全风险 |
| StabilityCodeReview_GraphicsStability_001 | VulkanCleanupHelper引用计数管理 | 图形稳定性 | VulkanCleanupHelper 引用计数管理不当导致资源泄漏 |
| StabilityCodeReview_GraphicsStability_002 | VulkanCleanUpHelper与SharedContext引用计数混用 | 图形稳定性 | VulkanCleanUpHelper 与 SharedContext 引用计数混用导致资源管理混乱 |
| StabilityCodeReview_GraphicsStability_003 | RS主线程禁止使用RenderNodeDrawable | 图形稳定性 | RS 主线程使用 RenderNodeDrawable 导致线程安全风险 |
| StabilityCodeReview_GraphicsStability_004 | RSUniRenderThread禁止访问RenderNode | 图形稳定性 | RSUniRenderThread 访问 RenderNode 导致线程安全风险 |
| StabilityCodeReview_GraphicsStability_005 | RS主线程禁止GPU Context操作 | 图形稳定性 | RS 主线程执行 GPU Context 操作导致线程安全风险 |
| StabilityCodeReview_GraphicsStability_006 | Surface/Image跨线程跨Context操作风险 | 图形稳定性 | Surface/Image 跨线程跨 Context 操作导致资源管理混乱 |
| StabilityCodeReview_GraphicsStability_007 | Surface/Image创建和释放线程一致性 | 图形稳定性 | Surface/Image 创建和释放线程不一致导致资源泄漏 |
| StabilityCodeReview_GraphicsStability_008 | GetBackendTexture线程限制 | 图形稳定性 | GetBackendTexture 在非创建线程调用导致线程安全风险 |
| StabilityCodeReview_GraphicsStability_009 | RSRenderNodeMap线程访问限制 | 图形稳定性 | RSRenderNodeMap 在多线程访问未加锁保护 |
| StabilityCodeReview_GraphicsStability_010 | 回调函数执行进程限制 | 图形稳定性 | 回调函数在错误进程执行导致功能异常 |
| StabilityCodeReview_GraphicsStability_011 | Vulkan信号量导出fd生命周期管理 | 图形稳定性 | Vulkan 信号量导出 fd 生命周期管理不当导致 fd 泄漏 |
| StabilityCodeReview_GraphicsStability_012 | SyncFence智能指针缓存管理 | 图形稳定性 | SyncFence 智能指针缓存管理不当导致资源泄漏 |

### MEDIUM (8)

| 规则 ID | 名称 | 分类 | 描述 |
|---------|------|------|------|
| StabilityCodeReview_ExceptionHandling_001 | 禁止异常处理机制 | 异常处理 | 使用 C++ 异常处理机制（try/catch/throw）违反编码规范 |
| StabilityCodeReview_ExceptionHandling_002 | 异常分支应正确处理 | 异常处理 | 异常分支处理不当导致错误传播或状态不一致 |
| StabilityCodeReview_ResourceManagement_003 | 谨慎使用static_pointer_cast | 资源管理 | static_pointer_cast 使用不当导致类型安全问题 |
| StabilityCodeReview_ResourceManagement_005 | JSON对象未关闭泄漏 | 资源管理 | JSON 对象未正确关闭导致资源泄漏 |
| StabilityCodeReview_BoundaryCondition_005 | Parcel整数转枚举需校验有效性 | 边界条件 | Parcel 整数转枚举未校验有效性导致无效枚举值 |
| StabilityCodeReview_BoundaryCondition_009 | 使用json库获取键值内容前应先判断类型是否匹配、键值是否存在 | 边界条件 | 使用 json 库获取键值内容前未判断类型或键值是否存在导致解析失败 |
| StabilityCodeReview_BoundaryCondition_010 | 使用json库获取键值后，在进行类型转换前应先校验参数类型 | 边界条件 | 使用 json 库获取键值后未校验参数类型导致类型转换失败 |
| StabilityCodeReview_BoundaryCondition_013 | 返回值类型不匹配风险 | 边界条件 | 返回值类型不匹配导致数据截断或溢出 |

---

## 规则模板与开发指南

- 新增规则模板请参考 [RULE_TEMPLATE.md](./RULE_TEMPLATE.md)
- 完整开发指南请参考 [RULE_DEVELOPMENT_GUIDE.md](./RULE_DEVELOPMENT_GUIDE.md)