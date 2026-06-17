# Taskpool Worker Scaling Analysis

## 用途

诊断 ETS `std.concurrency.taskpool` 的 worker 扩缩容问题，包括：
- 任务积压（backlog）
- worker 不扩张
- 长任务阻塞短任务
- 优先级饥饿
- worker 关闭/挂起
- shutdown hang

## 依赖路径

主要依赖 OpenHarmony 主仓中的 taskpool 实现：

```
arkcompiler_runtime_core/static_core/plugins/ets/stdlib/std/concurrency/taskpool.ets
```

关键锚点：
- `GlobalQueueWorker.workerBody` - worker 主循环
- `InternalTask.enqueue` - 任务入队
- `tryTriggerExpand` / `triggerExpand` - worker 扩张逻辑
- `triggerBlockedExpandMonitor` - 阻塞 worker 补偿
- `triggerShrink` / `closeWorker` - worker 缩容

## 脚本工具

### extract_taskpool_signals.py

从日志文件中提取 taskpool 相关线索：

```bash
python3 scripts/extract_taskpool_signals.py <log-file>
```

参数：
- `--context N` - 显示匹配行前后 N 行上下文（默认 0）
- `--limit N` - 每类最多显示 N 行（默认 12）

输出分类：
- queue - 任务队列相关
- worker - worker 相关
- expand - 扩张相关
- blocked - 阻塞相关
- priority - 优先级相关
- shutdown - 关闭/缩容相关
- dependency - 依赖相关
- launch - launch 模式相关

## 参考文档

- `references/scaling-model.md` - taskpool worker 扩缩容模型详解
- `references/diagnostic-playbooks.md` - 按症状分类的诊断手册