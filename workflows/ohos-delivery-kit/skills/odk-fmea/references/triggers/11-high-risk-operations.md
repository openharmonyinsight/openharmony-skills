# 高危操作故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../11-high-risk-operations.md](../11-high-risk-operations.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| H-01 | 业务路径误触进程退出 | 代码或三方依赖中存在 exit/abort/quick_exit/_Exit/APPSPAWN_CHECK 类终止调用，且位于库函数、工具函数或错误处理深层路径（非入口层统一退出点） |
| H-02 | 自杀式降级设计失控 | 存在"连续失败 N 次即退出/重启进程"的自恢复逻辑，且计数为全局维度或未评估 critical/看门狗联动后果 |
| H-03 | kill 目标校验不足 / pid 复用误杀 | kill(pid, SIGKILL) 的 pid 来源于历史记录/IPC 消息/配置而非刚孵化子进程，kill 前无 pidfd 或 /proc/\<pid\>/cmdline+启动时间身份校验；或对进程组整体 kill |
| H-04 | 异常清理路径的连锁 kill | 超时/失败清理路径 kill 子进程后无 wait/pidfd 回收确认；或单发 SIGTERM 无 SIGKILL 兜底；或 kill 与状态机迁移不配对 |
| H-05 | 删除非本模块创建的数据 | 清理/卸载/重置路径按路径模式或通配符删除文件目录，目标可能含他模块创建的数据，且无 owner/magic 标识校验或删除白名单 |
| H-06 | 直接操作非本模块创建的数据库 | 绕过数据 owner 服务直接打开他模块数据库文件（sqlite/RDB/Preferences）读写；跨模块共享数据未走 DataShare/IPC 接口 |
| H-07 | 内存申请与释放不在同一模块 | 跨 so/模块接口传递裸堆指针（malloc/new 后由对端 free/delete）；或异步回调中的释放与申请方生命周期脱钩 |
| H-08 | 其他非配对资源操作 | mount/umount、lock/unlock、register/unregister、open/close 等配对操作跨模块或跨线程执行（如 A 线程加锁 B 解锁、注册方未注销即模块卸载） |
