# taskpool Worker Scaling Model

## Table Of Contents

- Source anchors
- GlobalQueueWorker path
- Launch mode
- Priority queues
- Expansion model
- Blocked-worker compensation
- Shrink model
- Completion handoff

## Source Anchors

Primary file:

- `plugins/ets/stdlib/std/concurrency/taskpool.ets`

Important implementation anchors:

- `GlobalQueueWorker.workerBody`
- `InternalTask.enqueue`
- `initWorkerPoolSync`
- `tryTriggerExpand`
- `GlobalQueueWorker.triggerExpand`
- `GlobalQueueWorker.triggerShrink`
- `GlobalQueueWorker.triggerBlockedExpandMonitor`
- `getTaskFromGlobalQueue`
- `selectTaskByPriorityNonBlocking`
- `getGlobalTaskImplNonBlocking`
- `tryActivatePendingDependencyTask`

## GlobalQueueWorker Path

The managed worker-pool path is used when `isTaskPoolUseLaunch` is false.

Initialization:

- `initWorkerPoolSync()` returns immediately if workers are already initialized or launch mode is active.
- It creates `managerWorker` if absent.
- It starts shrink monitoring through `managerWorker.retriggerShrink()`.
- It starts blocked-worker expansion monitoring through `managerWorker.retriggerBlockedExpandMonitor()`.
- It creates `initialWorkersNumber` `GlobalQueueWorker` instances.

Worker execution:

- `workerBody()` loops while `isWorkerActive()` is true.
- It obtains a task with `getTaskFromGlobalQueue(this)`.
- It removes itself from `idleWorkers`.
- It updates native worker priority from taskpool priority.
- It records the current task in `currentTasks`.
- It stores `executingTaskBodyStartTime` before running the task.
- It resolves or rejects the current deferred.
- It resets `executingTaskBodyStartTime` in `finally`.
- It posts dependency notification to main using `EAWorker.postToMain` and `setTimeout(..., 1)`.

## Launch Mode

When `isTaskPoolUseLaunch` is true, the GlobalQueueWorker scaling path is not the main executor path.

In `launchImpl(task, priority?)`:

- The task executes through `launch(InternalTask.of(task).execute)`.
- The returned job is awaited with `job.Await()`.

In this mode, do not focus on:

- `globalTaskQueue`
- `waitingTasksNum`
- worker expansion/shrink
- blocked-worker compensation

Instead, route the issue to coroutine launch, await, or runtime scheduling diagnostics.

## Priority Queues

Global task queues are initialized for:

- `HIGH`
- `MEDIUM`
- `LOW`
- `IDLE`

`USER_INTERACTION` and `DEADLINE_REQUEST` currently normalize to `HIGH`.

Selection order:

1. `HIGH`, capped by `continuousExecutionCount`
2. `MEDIUM`, capped by `continuousExecutionCount`
3. `LOW`
4. `IDLE`

This means LOW/IDLE delay is expected while higher priority queues keep yielding tasks, but HIGH/MEDIUM counters are intended to avoid unlimited domination.

## Expansion Model

Expansion starts from enqueue:

- `InternalTask.enqueue()` pushes the task to the normalized global priority queue.
- It increments `waitingTasksNum`.
- If the previous waiting count is greater than `workers.size * 2`, it calls `tryTriggerExpand()`.
- It notifies one worker through `globalTaskCondVar`.

`tryTriggerExpand()` returns if `workers.size >= workersLimit`; otherwise it delegates to `managerWorker?.triggerExpand()`.

`triggerExpand()` estimates target idle capacity:

- With history: `averageDuration = totalExecTime / totalExecCount`
- `targetNum = min((averageDuration * waitingTasksNum) / TASK_DURATION, waitingTasksNum)`
- Without history: `targetNum = min(waitingTasksNum, STEP_SIZE)`

It expands only when:

- `workers.size < workersLimit`
- `idleWorkersNum < targetNum`

The expansion step is capped by remaining worker capacity and target demand.

## Blocked-Worker Compensation

This is separate from normal backlog expansion.

`workerBody()` records a synchronous task body start time in `executingTaskBodyStartTime`. The manager monitor treats a worker as blocked when:

- start time is non-zero
- elapsed milliseconds are at least `blockedWorkerThresholdMs`

The monitor:

- runs every `blockedWorkerMonitorIntervalMs`
- creates compensation workers within `workersLimit`
- records each already compensated worker id in `blockedExpandedWorkerIds`
- clears that record when the worker is no longer blocked

This mechanism compensates for synchronous task bodies that occupy worker threads. It does not prove the task is deadlocked, and it does not replace task design fixes for long blocking work.

## Shrink Model

`triggerShrink()` periodically computes a target worker number:

- Start from workers currently running tasks.
- Add estimated demand from waiting tasks and average duration.
- Do not shrink below `WORKERS_MINIMUM`.
- Close up to `SHRINK_STEP` idle workers per tick.

Only workers with `idleTime != 0` and idle duration exceeding `idleThreshold` are closed.

`closeWorker()`:

- sets active false
- notifies all on `globalTaskCondVar`
- joins the worker

If join hangs, suspect the worker is still executing a task body, blocked in native/interop work, or cannot reach the loop condition.

## Completion Handoff

After task execution:

- `currentDeferred` is resolved or rejected under `taskMutex`.
- `pendingDeferreds` may be shifted into `currentDeferred`.
- `notifyDependencies()` is scheduled via main worker timeout.

Dependent tasks are activated by:

- `notifyDependencies()`
- `tryActivatePendingDependencyTask()`
- requeue into global priority queue
- `condVarNotifyOne(globalTaskCondVar, globalTaskQueuesMutex)`

If downstream tasks do not start, inspect dependency state after confirming the worker completed the first task.
