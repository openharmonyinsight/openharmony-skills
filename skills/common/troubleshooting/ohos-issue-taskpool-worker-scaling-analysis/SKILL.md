---
name: ohos-issue-taskpool-worker-scaling-analysis
description: Diagnose ETS std.concurrency.taskpool task backlog, slow task execution, worker scaling failures, blocked workers, priority starvation, idle worker shrink issues, or worker close/join hangs. Use when logs, code, tests, or issue reports mention taskpool waiting tasks, tasks not executing, long tasks blocking short tasks, workers not expanding, workers shrinking unexpectedly, priority delays, global task queues, GlobalQueueWorker, managerWorker, blocked worker monitor, or taskpool shutdown hangs.
metadata:
  author: openharmony
  scope: common
  stage: troubleshooting
  domain: taskpool
  capability: worker-scaling-analysis
  version: 0.1.0
  status: draft
---

# Taskpool Worker Scaling Diagnostics

## Purpose

Use this skill to diagnose ETS `std.concurrency.taskpool` throughput and worker lifecycle problems by following the actual `taskpool.ets` scheduling model: enqueue, global priority queues, worker wakeup, worker expansion, blocked-worker compensation, shrink, and shutdown.

Keep dependency legality and taskpool error-code interpretation out of scope unless they directly explain queue buildup. Use a separate dependency/error-code skill for circular dependency, invalid task state, runner misuse, or taskpool error-code lookup.

## Source Map

Start from:

- `plugins/ets/stdlib/std/concurrency/taskpool.ets`

Use these anchors:

- `GlobalQueueWorker.workerBody`
- `InternalTask.enqueue`
- `initWorkerPoolSync`
- `tryTriggerExpand`
- `GlobalQueueWorker.triggerExpand`
- `GlobalQueueWorker.triggerShrink`
- `GlobalQueueWorker.triggerBlockedExpandMonitor`
- `GlobalQueueWorker.closeWorker`
- `getTaskFromGlobalQueue`
- `selectTaskByPriorityNonBlocking`
- `getGlobalTaskImplNonBlocking`
- `tryActivatePendingDependencyTask`

Read `references/scaling-model.md` for the taskpool worker model. Read `references/diagnostic-playbooks.md` for symptom-specific playbooks.

Optionally run `scripts/extract_taskpool_signals.py <log-file>` to summarize likely taskpool queue, worker, priority, blocked-worker, and shutdown clues from logs.

## Inputs To Gather

Ask for or infer:

- The symptom: task not executed, slow execution, backlog, no expansion, shutdown hang, priority delay, or worker churn.
- Logs around task submission, worker creation, task execution start/end, timeout, cancel, shutdown, and any taskpool errors.
- Whether `isUsingLaunch()` mode is enabled; if enabled, the GlobalQueueWorker path is bypassed.
- Task type mix: ordinary task, `LongTask`, periodic task, group task, `SequenceRunner`, `AsyncRunner`.
- Priority mix: `USER_INTERACTION`, `DEADLINE_REQUEST`, `HIGH`, `MEDIUM`, `LOW`, `IDLE`.
- Whether task bodies block synchronously for more than a few seconds.
- Any observed counts: waiting tasks, worker count, worker limit, idle worker count, running task count.
- Relevant code around `taskpool.execute`, `executeDelayed`, task creation, priority, cancel, and shutdown.

## Diagnostic Workflow

### 1. Classify The Execution Path

First determine whether the report uses launch mode or the managed GlobalQueueWorker pool.

- If `isTaskPoolUseLaunch` is true, focus on `launchImpl`: each task is executed through `launch(InternalTask.of(task).execute)` and `job.Await()`. Worker pool scaling, `globalTaskQueue`, `waitingTasksNum`, `managerWorker`, shrink, and blocked-worker monitor are not the primary path.
- If `isTaskPoolUseLaunch` is false, continue with the GlobalQueueWorker path.

When the mode is unknown, say which evidence would distinguish it and proceed with the GlobalQueueWorker hypothesis only as a hypothesis.

### 2. Trace Submission Into The Global Queue

For a backlog or "task never runs" report, verify that `InternalTask.enqueue` can reach the queue:

1. `initGlobalTaskQueues()` has initialized priority queues.
2. The task state is not already `CANCELED`.
3. `globalTaskQueue.get(normalizeTaskQueuePriority(priority))?.push(task)` runs.
4. `waitingTasksNum.fetchAdd(1)` increments waiting work.
5. `tryTriggerExpand()` is called when the previous waiting count is greater than `workers.size * 2`.
6. `condVarNotifyOne(globalTaskCondVar, globalTaskQueuesMutex)` wakes a worker.

If a task is queued but never selected, move to worker wakeup and priority selection.

### 3. Check Worker Wakeup And Queue Selection

Inspect `getTaskFromGlobalQueue(worker)`:

- It first calls `getTaskWithAttempts()` without blocking.
- If no task is found, it waits on `globalTaskCondVar` while active.
- It sets `worker.idleTime`, calls `Coroutine.Schedule()`, adds the worker to `idleWorkers`, then waits.
- After wakeup, it does not retry selection beyond the already computed `task` in that block; spurious wakeups can return `undefined` and loop in `workerBody`.

Inspect `selectTaskByPriorityNonBlocking()`:

- `USER_INTERACTION` and `DEADLINE_REQUEST` normalize to `HIGH`.
- `HIGH` and `MEDIUM` use `continuousExecutionCount` to avoid unlimited priority domination.
- `LOW` and `IDLE` are selected only when higher queues do not yield a task.
- Tasks with unresolved dependencies are moved to `pendingDependencyTasks` and are not executed yet.

Report priority starvation only after checking queue sizes, continuous execution counters, and dependency pending.

### 4. Check Worker Expansion

For "workers did not expand", check both normal expansion and blocked-worker compensation.

Normal expansion path:

1. `initWorkerPoolSync()` creates `managerWorker` and `initialWorkersNumber` workers unless launch mode is active.
2. `tryTriggerExpand()` returns early if `workers.size >= workersLimit`.
3. `triggerExpand()` estimates `targetNum`:
   - If execution history exists: `averageDuration = totalExecTime / totalExecCount`; `targetNum = min((averageDuration * waitingTasksNum) / TASK_DURATION, waitingTasksNum)`.
   - Otherwise: `targetNum = min(waitingTasksNum, STEP_SIZE)`.
4. Expansion occurs only when `workers.size < workersLimit` and `idleWorkersNum < targetNum`.

Common conclusions:

- No expansion because workers are at `workersLimit`.
- No expansion because idle workers already satisfy `targetNum`.
- Delayed expansion because `waitingTasksNum.fetchAdd(1)` compares the previous count to `workers.size * 2`.
- Target too low because average duration is small or history is absent.
- Launch mode bypasses the worker pool.

### 5. Check Blocked Worker Compensation

Use this path when long synchronous task bodies block worker threads.

In `workerBody`, `executingTaskBodyStartTime` is set before `internalTask.execute(this)` and reset in `finally`.

`triggerBlockedExpandMonitor()`:

- Runs only for the manager worker.
- Is not started when launch mode is active.
- Checks workers every `blockedWorkerMonitorIntervalMs`.
- Treats a worker as blocked when elapsed synchronous execution time is at least `blockedWorkerThresholdMs`.
- Creates at most one compensation worker per newly blocked worker, limited by `workersLimit`.
- Tracks handled blocked workers in `blockedExpandedWorkerIds` and clears records when a worker is no longer blocked.

Common conclusions:

- Compensation cannot happen in launch mode.
- Compensation cannot happen at worker limit.
- A task is async-waiting rather than synchronously blocking, so `executingTaskBodyStartTime` may not explain it.
- A long task blocks correctly, but compensation is limited and not a substitute for moving long work to a better task type or splitting work.

### 6. Check Task Completion And Dependency Notification

For "task ran but downstream work did not start", verify completion cleanup:

- `workerBody` resolves or rejects `currentDeferred`.
- `executingTaskBodyStartTime` is reset in `finally`.
- `EAWorker.postToMain(() => setTimeout(() => internalTask.notifyDependencies(), 1))` runs.
- `notifyDependencies()` activates pending dependent tasks through `tryActivatePendingDependencyTask`.
- `tryActivatePendingDependencyTask` requeues the task and notifies `globalTaskCondVar`.

If the blocker is dependency state or cancellation, state that this skill can identify the handoff point but the dependency-specific root cause belongs in a taskpool dependency diagnostic.

### 7. Check Shrink And Shutdown

For worker churn, unexpected shrink, or close/join hangs:

- `triggerShrink()` runs every `triggerInterval`.
- It computes `targetNum` from running workers plus estimated waiting demand.
- It never shrinks below `WORKERS_MINIMUM`.
- It only closes workers whose `idleTime` is non-zero and older than `idleThreshold`.
- `closeWorker()` sets active false, notifies all on `globalTaskCondVar`, then calls `join()`.

Common conclusions:

- Close/join can wait for a task body that is still executing.
- A worker that never becomes idle will not be selected for shrink.
- Idle bookkeeping may be stale if a worker is not removed from `idleWorkers` when it starts work.
- Shrink is expected after idle threshold, not a task loss by itself.

## Output Format

Return:

1. **Diagnosis**: one sentence naming the most likely cause.
2. **Path**: launch mode or GlobalQueueWorker path.
3. **Evidence**: logs, code snippets, counters, and taskpool.ets anchors.
4. **Queue/Worker State**: queued priorities, waiting count, worker count, idle/running/blocked workers.
5. **Reasoning**: concise walk through enqueue -> wakeup -> select -> execute -> complete/shrink.
6. **Fix or Next Probe**: code change, logging point, reproduction, or metric to collect.

Prefer concrete hypotheses over vague "thread pool issue" language.

## Useful Probes

When logs are insufficient, suggest adding temporary logs around:

- `InternalTask.enqueue`: priority, waiting count before/after, workers size, workers limit.
- `tryTriggerExpand`: workers size, workers limit.
- `triggerExpand`: average duration, waiting tasks, target number, idle worker number, expansion step.
- `getTaskFromGlobalQueue`: selected priority, undefined selection, wait entry, wakeup.
- `workerBody`: worker id, task id/name, priority, execute start/end, exception, duration.
- `triggerBlockedExpandMonitor`: worker id, elapsed ms, threshold, compensation count.
- `triggerShrink`: target count, running workers, idle duration, closed worker ids.
- `closeWorker`: active flag change, notify all, join start/end.

## Guardrails

- Do not claim a deadlock from queue backlog alone. Require a wait cycle, blocked worker evidence, or stack traces.
- Do not treat reader-visible task slowness as worker expansion failure until priority, dependency pending, and launch mode are checked.
- Do not recommend increasing worker limits before checking long synchronous task bodies and dependency pending.
- Do not conflate taskpool dependency errors with worker scaling; route dependency legality to the dependency diagnostic workflow.