# Taskpool Dependency Reference

## Table of Contents

1. [Data Structures](#1-data-structures)
2. [Full Error Code Registry](#2-full-error-code-registry)
3. [Dependency Lifecycle State Machine](#3-dependency-lifecycle-state-machine)
4. [Static vs Dynamic Implementation Differences](#4-static-vs-dynamic-implementation-differences)
5. [Task Type Restriction Matrix](#5-task-type-restriction-matrix)
6. [Notification Flow Detail](#6-notification-flow-detail)
7. [Cancel Propagation Flow Detail](#7-cancel-propagation-flow-detail)

---

## 1. Data Structures

### Static ArkTS (InternalTask)

| Field | Type | Description |
|-------|------|-------------|
| `dependentTasks` | `containers.ConcurrentSet<Task>` | Tasks that depend on THIS task (reverse mapping: "who waits for me") |
| `taskDependenciesCount` | `int` | Number of prerequisites THIS task waits for (forward count) |
| `isDependent` | `boolean` | Whether task has any dependencies (`taskDependenciesCount != 0`) |
| `isRunning` | `boolean` | Whether an instance is currently executing (single-instance constraint) |
| `taskMutex` | managed Object | Protects `taskDependenciesCount`, `isRunning`, `condVar` wait state |
| `condVar` | managed Object | Wait/signal for dependency completion |

Global:
| Field | Type | Description |
|-------|------|-------------|
| `pendingDependencyTasks` | `Map<Task, Priority>` | Blocked tasks storing original priority for re-enqueue |
| `pendingDependencyTasksMutex` | Object | Protects `pendingDependencyTasks` |

### Dynamic C++ (TaskManager)

| Field | Type | Description |
|-------|------|-------------|
| `dependTaskInfos_` | `unordered_map<taskId, set<dependentTaskId>>` | Forward: taskId -> tasks it depends on |
| `dependentTaskInfos_` | `unordered_map<dependentTaskId, set<taskId>>` | Reverse: dependentId -> tasks that depend on it |
| `pendingTaskInfos_` | `unordered_map<taskId, Priority>` | Pending dependent tasks with priorities |
| `dependTaskInfosMutex_` | `shared_mutex` | Protects `dependTaskInfos_` |
| `dependentTaskInfosMutex_` | `shared_mutex` | Protects `dependentTaskInfos_` |
| `pendingTaskInfosMutex_` | `shared_mutex` | Protects `pendingTaskInfos_` |

### Edge direction convention

**Critical**: `addDependency(taskA, taskB)` means taskA DEPENDS ON taskB (taskA waits for taskB).

- **Static**: Edge is stored as `taskA` added to `taskB.dependentTasks` (reverse: "taskB knows who waits for it"). `taskA.taskDependenciesCount` increments.
- **Dynamic**: Edge stored in both `dependTaskInfos_[taskA] = {..., taskB}` (forward) and `dependentTaskInfos_[taskB] = {..., taskA}` (reverse).

---

## 2. Full Error Code Registry

### Static ArkTS Error Codes

| Code | Constant | Message | Trigger |
|------|----------|---------|---------|
| 10200026 | TASKPOOL_ERROR_CIRCULAR_DEPENDENCY | "There is a circular dependency" | Self-dep or cycle via hasTaskDFS |
| 10200027 | TASKPOOL_ERROR_DEPENDENCY_NOT_EXIST | "The dependency does not exist" | removeDependency on non-edge |
| 10200070 | TASKPOOL_ERROR_EXECUTED_TASK_ADD_DEPENDENCY | "asyncRunnerTask or seqRunnerTask or executedTask cannot addDependency" | addDependency on executed/runner |
| 10200071 | TASKPOOL_ERROR_EXECUTED_TASK_REMOVE_DEPENDENCY | "executedTask cannot removeDependency" | removeDependency on executed task |
| 10200073 | TASKPOOL_ERROR_GROUP_TASK_ADD_DEPENDENCY | "groupTask cannot addDependency" | Group task calling addDependency |
| 10200074 | TASKPOOL_ERROR_GROUP_TASK_RELIED_ON | "groupTask cannot be relied on" | Group task as dependency target |
| 10200079 | TASKPOOL_ERROR_SEQ_RUNNER_OR_ASYNC_RUNNER_TASK_RELIED_ON | "asyncRunnerTask or seqRunnerTask or executedTask cannot be relied on" | Runner task as dependency target |
| 10200097 | TASKPOOL_ERROR_NO_DEPENDENCY | "task has no dependency" | removeDependency on task with no deps |
| 10200101 | TASKPOOL_ERROR_NO_PARAMS | "addDependency/removeDependency has no params" | Empty argument list |
| 10200113 | TASKPOOL_ERROR_PERIODIC_TASK_ADD_DEPENDENCY | "the periodic task cannot have a dependency" | Periodic task involved |

### Dynamic C++ Error Codes

| Code | Constant | Message |
|------|----------|---------|
| 10200026 | ERR_CIRCULAR_DEPENDENCY | "There is a circular dependency" |
| 10200027 | ERR_INEXISTENT_DEPENDENCY | "The dependency does not exist" |
| 10200025 | ERR_ADD_DEPENDENT_TASK_TO_SEQRUNNER | "dependent task not allowed." |
| 10200052 | ERR_TASK_HAVE_DEPENDENCY | "The periodic task cannot have a dependency." |
| 10200056 | ERR_ASYNCRUNNER_TASK_HAVE_DEPENDENCY | "The task has been executed by AsyncRunner." |

---

## 3. Dependency Lifecycle State Machine

### Task states (InternalState)

| State | Value | Description |
|-------|-------|-------------|
| NOT_FOUND | 0 | Task not yet submitted |
| WAITING | 1 | Task in queue |
| RUNNING | 2 | Task executing |
| CANCELED | 3 | Task canceled |
| DELAYED | 4 | Task delayed (timer) |
| FINISHED | 5 | Task completed |
| ENDING | 6 | Task ending |
| TIMEOUT | 7 | Task timed out |

### State transitions with dependencies

```
[Created] state=NOT_FOUND, count=0, isDependent=false

[addDependency] validate -> check cycle -> add edge -> count++, isDependent=true

[execute] state -> WAITING, task pushed to globalTaskQueue

[Worker dequeues] if count>0: moveToPendingDependencyQueue (store priority)
                  if count==0: proceed to execution

[Prerequisite finishes] notifyDependencies -> count-- -> signal condvar
                         if count==0: tryActivatePendingDependencyTask -> re-enqueue

[Worker dequeues again] removePendingDependencyTask -> waitForDependencies
                         lock taskMutex, wait until count==0
                         if CANCELED during wait: notifyDependencies, throw
                         set isRunning=true, execute task function

[Task finishes] notifyDependencies -> for each in dependentTasks: count--, signal
                isRunning=false, signal condvar

[Cancel] state -> CANCELED (CAS)
          tryCancelDependentTasks (recursively cancel dependents)
          cleanupCanceledPendingDependencyTask (reject promises)
```

---

## 4. Static vs Dynamic Implementation Differences

| Aspect | Static (ArkTS 1.2) | Dynamic (C++/NAPI) |
|--------|---------------------|-------------------|
| Data storage | Distributed: each InternalTask holds own dependentTasks + count | Centralized: TaskManager holds bidirectional maps |
| Cycle detection | DFS on task objects via `hasTaskDFS` | Graph traversal on `dependTaskInfos_` via `CheckCircularDependency` |
| Synchronization | Managed mutex/condvar per task | `shared_mutex` on central maps; per-task recursive `taskMutex_` |
| Pending tasks | `pendingDependencyTasks` map (Task -> Priority) | `pendingTaskInfos_` map (taskId -> Priority) |
| Notification | `notifyDependencies()` directly decrements and signals | `NotifyDependencyTaskInfo()` via TaskManager, dequeues and re-enqueues |
| Cancel propagation | `tryCancelDependentTasks()` recursively calls `cancel()` | `ClearDependentTask()` recursively removes from maps/queues |
| Execution wait | `waitForDependencies()` blocks on taskMutex/condvar | Task stays in pending until notification re-enqueues it |

---

## 5. Task Type Restriction Matrix

| TaskType | addDependency (caller) | addDependency (target) | removeDependency | Dependency notification |
|----------|----------------------|----------------------|-----------------|----------------------|
| TASK (unexecuted) | YES | YES | YES (if isDependent) | No (not yet common) |
| COMMON_TASK (after execute) | NO (10200070) | NO (10200079) | NO (10200071) | YES (notifyDependencies) |
| SEQRUNNER_TASK | NO (10200070) | NO (10200079) | NO (10200071) | No (handled by SequenceRunnerManager) |
| GROUP_TASK | NO (10200073) | NO (10200074) | N/A | No (handled by TaskGroupManager) |
| FUNCTION_TASK | YES | YES | YES | No (one-shot) |
| ASYNCRUNNER_TASK | NO (10200070) | NO (10200079) | NO (10200071) | No (handled by AsyncRunnerManager) |
| Periodic task | NO (10200113) | NO (10200113) | NO (10200113) | No (never finishes normally) |
| Timeout task | NO | NO | N/A | N/A |

---

## 6. Notification Flow Detail

### When a prerequisite (COMMON_TASK) finishes

```
InternalTask.execute() finally block:
  → notifyDependencies()
    → for each task in this.dependentTasks:
      1. Lock dependent.taskMutex
      2. Decrement dependent.taskDependenciesCount
      3. shouldActivate = (taskDependenciesCount == 0)
      4. Signal dependent.condVar
      5. Unlock
      6. If shouldActivate:
         → tryActivatePendingDependencyTask(dependent)
           a. Lock task.taskMutex -> verify count==0
           b. Take priority from pendingDependencyTasks (under pendingDependencyTasksMutex)
           c. If task is CANCELED: finishCanceledPendingDependencyTask -> reject promises, return false
           d. Push task into globalTaskQueue at stored priority
           e. Signal global condvar -> wake a worker
           f. Return true
    → Set this.isRunning = false
    → Signal this.condVar (for single-instance waiters)
```

### When a prerequisite is NOT a COMMON_TASK

SeqRunner, AsyncRunner, and Group tasks do NOT call `notifyDependencies`. If a task depends on one of these, it will wait forever. This is why these task types are rejected by `addDependency` validation.

### When a prerequisite is canceled

In dynamic: `TriggerTask(task, isCancel=true)` skips `NotifyDependencyTaskInfo`.
In static: `cancel()` calls `tryCancelDependentTasks` which recursively cancels all dependents, so they don't need to wait.

### Key race windows

1. **count increment vs notification**: If `addDependency` increments `taskDependenciesCount` AFTER a prerequisite has already called `notifyDependencies`, the dependent may see count > 0 even though all prerequisites have finished. This is prevented in static by requiring `addDependency` before `execute`.

2. **pending map insertion vs activation**: If `tryActivatePendingDependencyTask` reads the pending map before `moveToPendingDependencyQueue` has stored the entry, the task won't be found and won't be re-enqueued. This is prevented by: pending insertion happens during deque (under global queue mutex), and activation happens during notification (under task mutex + pending mutex).

3. **cancel vs notification**: If `cancel()` and `notifyDependencies()` run concurrently on the same task, both modify `taskDependenciesCount` and `condVar`. The CAS on state (WAITING -> CANCELED) ensures cancel wins; `tryActivatePendingDependencyTask` checks CANCELED state before re-enqueue.

---

## 7. Cancel Propagation Flow Detail

### Static ArkTS

```
cancel(task):
  1. CAS task state -> CANCELED (if not already CANCELED/FINISHED)
  2. tryCancelDependentTasks(task):
     → for each dependent in InternalTask.of(task).dependentTasks:
       → call cancel(dependent) (silently catch errors)
  3. cleanupCanceledPendingDependencyTask(task):
     → takePendingDependencyTaskPriority(task)
     → if found: finishCanceledPendingDependencyTask(task)
       - decrement waitingTasksNum
       - remove from allTasks
       - reject current and pending deferred promises with cancel error
```

### Dynamic C++

```
Task::CancelInner():
  1. Clear delayed timers, cancel pending
  2. If HasDependency():
     → TaskManager::ClearDependentTask(taskId)
       → RemoveDependTaskByTaskId(taskId) // forward edges
       → DequeuePendingTaskInfo(taskId)   // remove from pending
       → RemoveDependentTaskByTaskId(taskId) // reverse edges + recursive cleanup
         → For each dependent:
           - DequeuePendingTaskInfo
           - RemoveDependencyById
           - EraseWaitingTaskId (if in queue)
           - Cleanup task lifecycle
           - RemoveDependTaskByTaskId (recursive)
```

### Cancel invariant

All tasks in `dependentTasks` of the canceled task must also be canceled. If any is not, it will wait forever for a prerequisite that will never finish (since canceled tasks don't call `notifyDependencies`).