# taskpool Worker Scaling Diagnostic Playbooks

## Table Of Contents

- Task never starts
- Workers do not expand
- Short tasks are delayed by long tasks
- Priority task is delayed
- Worker close or shutdown hangs
- Workers shrink unexpectedly
- Dependency handoff looks stuck
- Minimum reproduction patterns

## Task Never Starts

Use when the user says a task is waiting forever or `taskpool.execute` returns a promise that never resolves.

Check in order:

1. Determine whether launch mode is active. If launch mode is active, switch to coroutine launch/await diagnostics.
2. Confirm `initWorkerPoolSync()` has run.
3. Confirm `InternalTask.enqueue()` pushes into `globalTaskQueue`.
4. Confirm the task is not already canceled before enqueue.
5. Confirm `waitingTasksNum` increments.
6. Confirm a worker is notified through `globalTaskCondVar`.
7. Confirm `getTaskFromGlobalQueue()` selects the task.
8. If selection returns undefined, check whether the task has unresolved dependencies and was moved to `pendingDependencyTasks`.

Likely conclusions:

- Task was canceled before execution.
- Task is dependency-pending, not worker-starved.
- Worker is asleep and notify did not happen or was missed.
- Worker pool did not initialize because launch mode is active.

## Workers Do Not Expand

Use when waiting tasks increase but worker count stays flat.

Check:

- `workers.size >= workersLimit`
- `waitingTasksNum.fetchAdd(1)` threshold: expansion is attempted only when the previous waiting count is greater than `workers.size * 2`
- `managerWorker` exists
- idle workers are enough for computed `targetNum`
- `totalExecCount` and `totalExecTime` make average duration small
- launch mode bypasses GlobalQueueWorker scaling

Suggested evidence to collect:

- workers size
- workers limit
- waitingTasksNum before/after enqueue
- totalExecCount
- totalExecTime
- idleWorkersNum
- targetNum
- expansion step

## Short Tasks Are Delayed By Long Tasks

Use when long synchronous task bodies occupy workers and short tasks wait.

Check:

- `executingTaskBodyStartTime` is non-zero for busy workers.
- elapsed time exceeds `blockedWorkerThresholdMs`.
- `triggerBlockedExpandMonitor()` is running.
- `workers.size < workersLimit`.
- `blockedExpandedWorkerIds` does not already contain the blocked worker id.

Likely conclusions:

- Compensation worker cannot be created because the pool is at limit.
- Monitor is not active because launch mode is active.
- The task is blocking outside the synchronous window captured by `executingTaskBodyStartTime`.
- Long task should be split, moved, or changed to a more appropriate task type.

## Priority Task Is Delayed

Use when high-priority tasks do not execute as expected.

Check:

- `USER_INTERACTION` and `DEADLINE_REQUEST` normalize to `HIGH`.
- `HIGH` and `MEDIUM` use `continuousExecutionCount`, so a lower priority queue can occasionally run.
- A HIGH task with unresolved dependencies can be moved to `pendingDependencyTasks`.
- Worker native priority is updated in `workerBody()` through `setCurrentTaskpoolWorkerPriority`.
- Current task priority is only updated when the worker starts executing the task.

Likely conclusions:

- Delay is due to dependency pending, not priority.
- Priority affects selection and native worker priority, not cancellation of already running lower priority tasks.
- Lower priority execution after several high-priority tasks can be expected because of the continuous execution cap.

## Worker Close Or Shutdown Hangs

Use when close, shrink, or taskpool shutdown waits indefinitely.

Check:

- `closeWorker()` sets active false.
- It notifies all workers waiting on `globalTaskCondVar`.
- It calls `join()`.
- A worker inside a long task body cannot observe active false until the task returns.
- A worker blocked in native/interop code can delay join.

Suggested evidence:

- worker id
- active flag transition
- join start/end log
- current task id/name
- task execution start time
- stack trace of the worker thread

## Workers Shrink Unexpectedly

Use when users interpret worker shrink as task loss.

Check:

- Shrink only closes idle workers.
- It waits for `idleThreshold`.
- It keeps at least `WORKERS_MINIMUM`.
- Running workers are counted in target.
- Waiting demand is added to target.

Likely conclusions:

- Shrink is expected after idle threshold.
- If tasks are waiting while shrink happens, collect targetNum, waitingTasksNum, and queue sizes.
- If a worker is closed while still needed, inspect idle bookkeeping and queue notification.

## Dependency Handoff Looks Stuck

Use only to separate worker scaling from dependency diagnostics.

Check:

- First task reaches `finally`.
- `notifyDependencies()` is posted to main.
- Dependent task enters `tryActivatePendingDependencyTask`.
- It is requeued only when dependency count reaches zero.
- Canceled pending dependency tasks are finished instead of requeued.

If dependency counts, circular dependencies, or invalid dependency types are involved, route to a taskpool dependency skill.

## Minimum Reproduction Patterns

Backlog:

- Create more tasks than `workers.size * 2`.
- Make each task perform measurable synchronous work.
- Log enqueue time and execution start time.

Blocked worker compensation:

- Submit tasks whose body blocks synchronously beyond `blockedWorkerThresholdMs`.
- Set worker limit high enough to allow compensation.
- Log worker count before and after the monitor interval.

Priority delay:

- Submit a mix of HIGH, MEDIUM, LOW, and IDLE tasks.
- Add task ids and start order logs.
- Include dependency-free tasks first, then repeat with dependencies.

Shutdown hang:

- Submit one blocking task.
- Trigger worker close/shutdown.
- Capture worker stack and join timing.
