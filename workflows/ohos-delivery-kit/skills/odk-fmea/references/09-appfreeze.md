# 主线程卡死 / AppFreeze 故障模式

### A-01 主线程执行耗时任务
- 典型原因：在主线程做大粒度计算、文件/数据库 IO、同步网络请求；事件队列被长任务独占，watchdog 判活任务无法执行。
- 典型影响：THREAD_BLOCK_3S 告警 → THREAD_BLOCK_6S 故障事件，系统杀应用并生成 AppFreeze 日志。
- 故障注入：主线程注入 sleep/大循环；慢速设备压测。
- 日志/Trace：AppFreeze 日志（THREAD_BLOCK_6S）；主线程堆栈；HiAppEvent 冻屏事件。
- 消减建议：耗时任务移工作线程（taskpool/FFRT）；长任务拆分让出事件循环；关键路径耗时埋点。

### A-02 主线程同步网络 / 资源加载
- 典型原因：Image 组件设置 syncLoad=true 同步下载网络图片；主线程同步等待资源。
- 典型影响：网络不佳时主线程阻塞至 AppFreeze。
- 故障注入：弱网/丢包环境加载网络图片。
- 日志/Trace：AppFreeze 主线程栈含 DownloadSync/PerformDownload（libace_network）。
- 消减建议：禁用 syncLoad；异步加载+占位图；网络请求设超时。

### A-03 跨线程同步任务互锁
- 典型原因：工作线程 PostSyncTask 到主线程并等待完成，而主线程也在同步等待该工作线程（或经 IPC 形成多进程互锁环）。
- 典型影响：双方/多方永久互等，AppFreeze 或系统级卡死；堆栈仅是互锁环的一部分，无法从单点打破。
- 故障注入：构造双向同步等待场景。
- 日志/Trace：AppFreeze 日志中主线程与非主线程堆栈（WaitUntilComplete/PostSyncTask）；增强日志的对端进程信息。
- 消减建议：同步等待改异步回调；绘制线程等待关系图找互锁环；分析对端线程在处理什么任务。

### A-04 输入响应超时（APP_INPUT_BLOCK）
- 典型原因：点击事件 5s（nolog）/8s（log）未响应；输入分发依赖的线程被阻塞。
- 典型影响：用户点击无反应，系统报 APP_INPUT_BLOCK 并杀应用。
- 故障注入：阻塞输入处理线程后点击。
- 日志/Trace：AppFreeze 日志 APP_INPUT_BLOCK 特有字段（输入事件信息）。
- 消减建议：输入路径零阻塞；输入到响应全链路埋点。

### A-05 同步等待无超时保护
- 典型原因：同步调用（IPC/锁/条件变量/future.get）不设超时；超时设得过大（超过 watchdog 6s 窗口）。
- 典型影响：故障从"可恢复的错误"升级为"进程被杀"。
- 故障注入：对端不响应场景下测量等待时长。
- 日志/Trace：等待点堆栈 + 无超时日志。
- 消减建议：所有同步等待带超时（且小于 watchdog 窗口）；超时后降级并上报事件。
> 应用生命周期超时、透明窗口、输入分发超时、事件队列卡死等 APP 层业务可靠性故障，参见 `12-app-framework.md` 中 AF-01 ~ AF-06、AF-15 ~ AF-17、AF-23 ~ AF-24。