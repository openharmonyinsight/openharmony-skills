# C-Utils / Parcel 组件使用陷阱 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../10-cutils-parcel.md](../10-cutils-parcel.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| U-01 | Parcel 读写不对称 | Parcel 写入与读取顺序/类型不一致；WriteBuffer 配 ReadBuffer（对齐问题）或写字符串丢结束符；读 Object 后读基础类型未按契约 |
| U-02 | SafeMap / SafeQueue 误用 | SafeMap 写场景用 operator[]（返回引用非线程安全）；SafeBlockQueue 满后生产者永久阻塞、stop 后消费者未退出 |
| U-03 | 单例模式竞态 | 懒汉单例无双检锁（非局部静态变量）；静态对象销毁顺序未定义（单例先销毁后被使用） |
| U-04 | 字符串 / 工具函数边界 | 字符串处理目标缓冲区不足被截断且未检查返回值；日期/路径拼接等工具函数输入长度未校验 |
| U-05 | IOEventReactor / 事件处理生命周期 | Run 线程可能在 Terminate 之前退出；组件生命周期结束后事件仍被响应（未手动停止 Handler） |
