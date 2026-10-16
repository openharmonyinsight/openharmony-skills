# C-Utils / Parcel 组件使用陷阱

### U-01 Parcel 读写不对称
- 典型原因：写入与读取顺序/类型不一致；WriteBuffer 配 ReadBuffer 存在对齐问题（应配 ReadUnpadBuffer）；WriteBuffer 写字符串丢失结束符（应用 WriteString）；读 Object 后读基础类型被安全校验拦截。
- 典型影响：IPC 数据解析错乱、越界读、传输失败。
- 故障注入：构造字段错位/类型错配的 Parcel 数据。
- 日志/Trace：unmarshalling 失败日志；安全校验拦截日志。
- 消减建议：读写对称性单测；专用接口写字符串；Parcelable 正确实现 Marshalling/Unmarshalling。

### U-02 SafeMap / SafeQueue 误用
- 典型原因：SafeMap 用 operator[] 做写（返回引用非线程安全）；SafeBlockQueue 满后生产者永久阻塞、stop 后消费者仍阻塞未退出。
- 典型影响：数据竞争；线程挂起无法退出（线程泄漏）。
- 故障注入：多线程并发写 operator[]；队列满场景 stop。
- 日志/Trace：TSAN 报告；线程堆栈停在队列等待。
- 消减建议：写用 Insert/ChangeValueByLambda，读用 ReadVal；stop 后检查返回值退出。

### U-03 单例模式竞态
- 典型原因：懒汉单例无双检锁；构造与销毁顺序问题（静态销毁顺序未定义，单例先销毁后被使用）。
- 典型影响：多实例/半构造对象被使用；退出阶段崩溃。
- 故障注入：多线程并发首次获取；进程退出压测。
- 日志/Trace：偶发初始化相关崩溃栈。
- 消减建议：局部静态变量单例（C++11 线程安全）或双检锁；明确析构依赖。

### U-04 字符串 / 工具函数边界
- 典型原因：字符串处理函数目标缓冲区不足被截断未检查；日期时间解析未校验格式；路径拼接函数溢出。
- 典型影响：数据截断被采信（静默错误）；越界写。
- 故障注入：边界长度输入（恰好等于缓冲区大小）。
- 日志/Trace：截断告警（多数缺失）。
- 消减建议：检查返回值/截断标志；输入长度先校验。

### U-05 IOEventReactor / 事件处理生命周期
- 典型原因：Run 的线程在 Terminate 之前退出；事件在组件生命周期结束后仍被响应（未手动停止 Handler）。
- 典型影响：事件丢失或处理已销毁资源（UAF）。
- 故障注入：Terminate 与线程退出乱序；销毁后投递事件。
- 日志/Trace：事件处理异常日志；UAF crash 栈。
- 消减建议：Terminate 先于线程退出；生命周期结束手动停止事件响应。
