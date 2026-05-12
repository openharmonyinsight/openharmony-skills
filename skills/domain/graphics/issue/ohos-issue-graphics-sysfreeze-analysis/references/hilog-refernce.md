# 常见流水日志

## 异常日志

- `GetSaWrap SA:10`：获取SA超时，10是render_service，说明render_service启动超时（未发布服务）
- `bootevent.render_service_ready`：render_service的启动投票
- `vsync signal is not processed in time`/`RequestNextVsync too many times`：vsync处理超时，render_service丢帧或者freeze
- `task too long`：render_service的某个任务耗时
- `MemoryOverflow`：应用内存超限出发内存查杀
- `IDisplayComposer`：hdi的ipc请求耗时（会输出时长）
- `init.*ohos.servicectrl.stop.render_service`：通过sevicectrl命令终止了render_service服务，render_service进程不再被拉起

## 场景分析日志

- `TransactionDataStatistics`：应用发送较大绘制指令，可能导致高负载（注意区分日志出现在freeze前还是freeze后）
- `PostPlayback`/`PostPlaybackInCorrespondThread`：CanvasDrawing节点绘制，可能与后续freeze有关
- `SetIsOnTheTree`：应用节点（窗口）上下树信息（分析应用场景）
- `OcclusionInfo`：应用窗口可见性，0-可见，1-部分可见，2-不可见（分析应用场景）

## 系统日志

- `ReclaimAvailBuffer`：LMK打印系统内存信息，表示可用内存
- `Total ION`/`Total GPU`：LMK内存信息dump，可以拆解ion/gpu内存信息
