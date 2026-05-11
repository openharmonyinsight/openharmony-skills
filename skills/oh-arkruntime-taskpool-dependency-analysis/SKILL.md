---
name: taskpool-dependency-analysis
description: "Analyze, diagnose, and fix taskpool task dependency problems in static ArkTS — including circular dependency (10200026), missing dependency (10200027), dependent tasks not waking after dependency completion, cancel propagation through dependency chains, and illegal addDependency/removeDependency on periodic/group/seqRunner/asyncRunner/executed tasks. Use this skill whenever the user mentions taskpool dependencies, addDependency, removeDependency, circular dependency, dependency graph, task not executing after dependencies complete, cancel propagation, or any taskpool error codes 10200026, 10200027, 10200070, 10200071, 10200073, 10200074, 10200079, 10200097, 10200101, 10200113 — even if they don't explicitly say 'dependency' or 'taskpool'."
---

# Taskpool Dependency Analysis Skill

This skill helps you systematically diagnose and fix taskpool dependency problems in the static ArkTS runtime. It walks you through building a dependency graph from user code, detecting cycles, identifying illegal API call sequences, tracing notification/activation paths, and recommending fixes.

## Why this skill exists

Taskpool dependencies are not "just deadlock detection" — they are a bespoke task dependency model with its own state machine, notification mechanism, task-type restrictions, and cancel propagation rules. A task that depends on another task blocks via `waitForDependencies()` until its `taskDependenciesCount` reaches zero; when a prerequisite task finishes, it calls `notifyDependencies()` which decrements counters and re-enqueues ready dependents via `tryActivatePendingDependencyTask`. If any step in this chain breaks, dependent tasks silently hang or never execute, and the root cause is often not where the symptom appears.

## Source code bindings

When using this skill, read these source files for the authoritative implementation:

- **Static stdlib**: `runtime_core/static_core/plugins/ets/stdlib/std/concurrency/taskpool.ets`
  - `Task.addDependency` (line ~1238): validates task types, checks circular dependency via `hasTaskDFS`, builds edge in `dependentTasks` set
  - `Task.removeDependency` (line ~1284): validates state, removes edge, adjusts `taskDependenciesCount`
  - `Task.hasTaskDFS` (line ~1371): DFS cycle detection traversing `dependentTasks`
  - `InternalTask.waitForDependencies` (line ~718): blocks on `taskMutex`/`condVar` until `taskDependenciesCount == 0`
  - `InternalTask.notifyDependencies` (line ~731): decrements each dependent's count, signals condvar, activates ready tasks
  - `tryActivatePendingDependencyTask` (line ~3014): re-enqueues a task whose dependencies are all satisfied
  - `moveToPendingDependencyQueue` (line ~2993): stores task+priority in pending map when dequeued but still blocked

- **Dynamic reference**: `commonlibrary/ets_utils/js_concurrent_module/taskpool/task.cpp` and `task_manager.cpp`
  - `Task::AddDependency`, `Task::RemoveDependency`, `Task::CheckAddDependency`
  - `TaskManager::StoreTaskDependency`, `TaskManager::CheckCircularDependency`, `TaskManager::NotifyDependencyTaskInfo`, `TaskManager::RemoveTaskDependency`, `TaskManager::ClearDependentTask`

- **Test reference**: `runtime_core/static_core/plugins/ets/tests/ets-common-tests/taskpool/common_tasks.ets`
  - `dependentTasksTest`, `circularDependencyTest`, `dependencyExecutedTaskTest`, `dependencyCancelTaskTest`, `doubleCancelByDependencyTest`

For detailed reference on data structures, error codes, and the full lifecycle, read `references/dependency_reference.md` in this skill's directory.

## Analysis workflow

Follow these steps in order. Do not skip steps or merge them.

### Step 1: Classify the problem

Read the user's description or the failing test case and classify into one of these categories:

| Category | Typical symptoms | Error codes |
|----------|-----------------|-------------|
| **Circular dependency** | `addDependency` throws immediately | 10200026 |
| **Missing/nonexistent dependency** | `removeDependency` throws | 10200027, 10200097 |
| **Dependent task never wakes** | Task submitted but never executes; hangs silently | None (no error thrown) |
| **Cancel propagation failure** | Canceling a prerequisite doesn't cancel dependents, or vice versa | None |
| **Illegal API sequence** | `addDependency`/`removeDependency` on wrong task type | 10200070, 10200071, 10200073, 10200074, 10200079, 10200113 |
| **Re-execution after dependency** | Re-executing a task that already ran with dependencies | 10200072 |
| **Timeout + dependency conflict** | `execute(task, {timeout})` on task with dependency | Custom error |

If the user provides a test case (.ets file), read it first and extract: task creation order, addDependency calls, execute calls, and expected vs actual behavior.

### Step 2: Build the dependency graph from user code

From the user's code or test case, extract every `Task` creation, `addDependency`, `removeDependency`, and `execute` call in order. Build a directed graph:

- **Nodes**: each `Task` instance (label with variable name + taskId if available)
- **Edges**: each `addDependency` creates an edge `dependent → prerequisite` (the dependent waits for the prerequisite)
- **Edge deletions**: each `removeDependency` removes that edge
- **Execution state**: mark nodes as `unexecuted`, `submitted`, `running`, `finished`, `canceled` based on `execute`/`cancel` calls

Represent the graph as text, e.g.:

```
task1 ──depends on──> task2 ──depends on──> task3
task4 ──depends on──> task2
```

If the graph has been modified by `removeDependency`, show the graph at each significant state change.

### Step 3: Detect cycles and illegal edges

Run these checks on the graph:

#### 3a: Cycle detection

Use DFS from each node. If any path returns to the starting node, it's a cycle. Report the exact cycle path:

```
Cycle detected: task1 → task2 → task3 → task1
Introduced by: task3.addDependency(task1) at line X
```

The static implementation uses `hasTaskDFS` which traverses the `dependentTasks` (reverse direction: from prerequisite towards its dependents). Make sure your cycle detection matches this traversal direction.

#### 3b: Illegal task-type edges

Check each node against these rules (these are the exact checks in `addDependency` and `removeDependency`):

| Task type | Can call addDependency? | Can be a dependency target? | Can call removeDependency? |
|-----------|------------------------|----------------------------|---------------------------|
| Unexecuted (TASK) | Yes | Yes | Yes (if isDependent) |
| Executed (COMMON_TASK, after execute) | No (10200070) | No (10200079) | No (10200071) |
| Periodic task | No (10200113) | No (10200113) | No (10200113) |
| Group task | No (10200073) | No (10200074) | N/A |
| SeqRunner task | No (10200070) | No (10200079) | No (10200071) |
| AsyncRunner task | No (10200070) | No (10200079) | No (10200071) |
| Timeout task | No | No | N/A |

Report any violations with the specific error code.

#### 3c: Missing dependency edges

For `removeDependency` errors: verify that the edge actually exists in the graph at the time of removal. If the user code calls `removeDependency(taskX)` but `taskX` is not a prerequisite of the caller, that's error 10200027.

### Step 4: Trace the notification/activation path

This is the most important step for "dependent task never wakes" problems. Trace the full path from when a prerequisite task finishes to when the dependent task should execute:

```
Prerequisite finishes
  → InternalTask.execute() finally block
    → notifyDependencies() called
      → Iterates over prerequisite.dependentTasks
        → For each dependent:
          - Locks dependent.taskMutex
          - Decrements dependent.taskDependenciesCount
          - Signals dependent.condVar
          - If taskDependenciesCount == 0:
            → tryActivatePendingDependencyTask(dependent)
              - Takes priority from pendingDependencyTasks map
              - Re-enqueues dependent into globalTaskQueue
              - Signals global condvar to wake a worker
```

Check each step for potential failure:

| Failure point | Symptom | Root cause pattern |
|---------------|---------|--------------------|
| `notifyDependencies` not called | Dependent never wakes | Task type is not COMMON_TASK (dynamic: TriggerTask only calls NotifyDependencyTaskInfo for common tasks); or task was canceled (isCancel=true skips notification) |
| `dependentTasks` set is empty | No dependents notified | Edge was removed before execution, or addDependency was called after execute |
| `taskDependenciesCount` doesn't reach 0 | Dependent wakes but re-waits | Some prerequisite finished without decrementing this dependent's count (race: count was incremented after the notification ran) |
| `pendingDependencyTasks` has no entry for the dependent | tryActivatePendingDependencyTask returns false | Task was never moved to pending queue (e.g., it was dequeued and started waitForDependencies before all prerequisites finished) |
| Task is CANCELED in tryActivatePendingDependencyTask | Promise rejected with cancel error | Another thread/task canceled the dependent between notification and activation |
| Global condvar not signaled | Worker doesn't pick up re-enqueued task | Race between enqueue and worker sleep |

When diagnosing "never wakes" issues, **add logging** at these points:
1. `notifyDependencies`: log each dependent task's taskId and the new `taskDependenciesCount`
2. `tryActivatePendingDependencyTask`: log whether priority was found, whether task is CANCELED, whether re-enqueue succeeded
3. `waitForDependencies`: log when entering wait and when exiting (with final `taskDependenciesCount`)
4. `moveToPendingDependencyQueue`: log when a task is moved to pending vs when it's skipped (dependencies already cleared)

### Step 5: Trace cancel propagation

When a task is canceled, its dependents should also be canceled. Trace this path:

```
cancel(task) called
  → task state -> CANCELED (CAS)
  → tryCancelDependentTasks(task)
    → Iterates over InternalTask.of(task).dependentTasks
      → For each dependent:
        - calls cancel(dependent) (silently catches errors)
  → cleanupCanceledPendingDependencyTask(task)
    → Takes priority from pendingDependencyTasks
    → If found: finishCanceledPendingDependencyTask (rejects promises)
```

Check for:
- **Dependents not canceled**: `dependentTasks` set was empty or the edge was already removed
- **Dependents stuck in WAITING state**: They were in the global queue and cancel didn't remove them (this should be handled by `RemoveDependTaskByTaskId` in dynamic, `tryCancelDependentTasks` in static)
- **Double cancel race**: Two tasks in the same dependency chain are canceled concurrently — check whether `cancel()` has proper CAS on state transition

### Step 6: Produce the diagnostic report

Output a structured report with these sections:

#### Dependency Graph

```
Nodes: [task1 (unexecuted), task2 (finished), task3 (submitted, isDependent=true)]
Edges:
  task3 → task2  (task3 depends on task2)
  task1 → task3  (task1 depends on task3)
```

#### Issues Found

For each issue, provide:
- **Issue type**: circular / illegal-edge / missing-edge / notification-failure / cancel-failure
- **Error code** (if applicable)
- **Exact source location** (file:line)
- **The affected edge or path**
- **Root cause explanation**

#### Recommended Fix

For each issue, recommend one of:
- **Reorder addDependency calls**: declare all dependencies before execute
- **Remove the problematic edge**: use removeDependency before the task type changes
- **Split the task**: create a new unexecuted task instead of reusing an executed one
- **Replace task type**: don't use periodic/group/seqRunner/asyncRunner where dependencies are needed
- **Add synchronization**: if the issue is a race in notification/activation, identify the specific race window and the fix (do not suggest sleep/retry/timeout)
- **Fix the notification path**: if notifyDependencies is not being called, identify why and fix the condition

#### Refactored Code Sketch

If the user's code has structural issues (e.g., adding dependencies after execute, self-referencing cycles, group tasks in dependency chains), provide a sketch of the corrected code showing the proper order of operations.

## Key invariant checklist

When analyzing any taskpool dependency problem, verify these invariants hold. If any is violated, that's your root cause or contributing factor:

1. **Edge direction invariant**: `addDependency(taskA, taskB)` means taskA waits for taskB. The edge is stored in `taskB.dependentTasks` (reverse mapping). If you traverse `dependentTasks`, you're going from prerequisite towards dependents, not from dependents towards prerequisites.

2. **taskDependenciesCount invariant**: For any task T, `T.taskDependenciesCount` must equal the number of prerequisite edges pointing into T. If `taskDependenciesCount > 0`, T must be in `pendingDependencyTasks` (if dequeued from global queue) or in the global queue (if just submitted). If `taskDependenciesCount == 0`, T must NOT be in `pendingDependencyTasks`.

3. **Task type restriction invariant**: Only unexecuted TASK type and FUNCTION_TASK can participate in `addDependency`. Periodic, group, seqRunner, asyncRunner, and executed (COMMON_TASK) types are prohibited in both directions.

4. **Notification invariant**: When a COMMON_TASK finishes (not canceled), `notifyDependencies()` must be called, and it must traverse ALL entries in `this.dependentTasks`. If any entry is missing, some dependent will never wake.

5. **Cancel propagation invariant**: When a task is canceled, ALL tasks in its `dependentTasks` must also be canceled (recursively). If any dependent is not canceled, it will either hang forever (waiting for a canceled prerequisite) or execute with missing prerequisite results.

6. **Single-instance invariant**: `waitForDependencies()` checks `isRunning` after dependencies are satisfied. If another instance of the same task is running, the current instance waits. `notifyDependencies()` sets `isRunning = false` and signals `condVar` to unblock the next instance.

7. **Pending-queue consistency**: A task moves from global queue → `pendingDependencyTasks` (when dequeued but blocked) → global queue (when re-enqueued by `tryActivatePendingDependencyTask`). It must not be in both the global queue and `pendingDependencyTasks` simultaneously. The `removePendingDependencyTask` call at the start of `execute()` ensures cleanup.

## Anti-patterns to watch for

These patterns in user code are almost always bugs. Flag them immediately:

1. **addDependency after execute**: `task.addDependency(other)` after `taskpool.execute(task)` — throws 10200070
2. **Self-dependency**: `task.addDependency(task)` — throws 10200026
3. **Periodic task in dependency chain**: `periodicTask.addDependency(x)` or `x.addDependency(periodicTask)` — throws 10200113
4. **Group task in dependency chain**: group tasks cannot add or receive dependencies — throws 10200073/10200074
5. **Missing prerequisite notification**: if a prerequisite is executed via seqRunner/asyncRunner/group, it will never call `notifyDependencies`, so dependents hang forever
6. **Re-execution after dependency completion**: `taskpool.execute(task)` after the task already ran with dependencies — throws 10200072
7. **removeDependency on wrong task**: removing a dependency that doesn't exist — throws 10200027
8. **Cancel without propagation**: canceling a prerequisite but expecting dependents to still run — they will be canceled too

## Error code quick reference

| Code | Constant | Meaning | Typical fix |
|------|----------|---------|-------------|
| 10200026 | CIRCULAR_DEPENDENCY | Cycle in dependency graph | Remove the edge that closes the cycle |
| 10200027 | DEPENDENCY_NOT_EXIST | removeDependency on non-edge | Only remove edges that were actually added |
| 10200070 | EXECUTED_TASK_ADD_DEPENDENCY | addDependency on executed/runner task | Declare dependencies before execute |
| 10200071 | EXECUTED_TASK_REMOVE_DEPENDENCY | removeDependency on executed task | Don't modify dependencies after execution |
| 10200073 | GROUP_TASK_ADD_DEPENDENCY | Group task calling addDependency | Remove group task from dependency chain |
| 10200074 | GROUP_TASK_RELIED_ON | Group task as dependency target | Use regular task instead of group task |
| 10200079 | SEQ/ASYNC_RUNNER_TASK_RELIED_ON | SeqRunner/AsyncRunner as dependency target | Use regular task instead |
| 10200097 | NO_DEPENDENCY | removeDependency on task with no deps | Ensure addDependency was called first |
| 10200101 | NO_PARAMS | addDependency/removeDependency with no args | Provide task arguments |
| 10200113 | PERIODIC_TASK_ADD_DEPENDENCY | Periodic task in dependency | Remove periodic task from dependency chain |