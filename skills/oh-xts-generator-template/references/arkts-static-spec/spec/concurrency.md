# ArkTS Concurrency Reference

## async/await

### Async Functions

```typescript
async function fetchData(url: string): Promise<string> {
  const response = await fetch(url)
  return await response.text()
}
```

**Return type:** Always `Promise<T>`

### Await Expression

```typescript
async function main(): Promise<void> {
  const data: string = await fetchData("https://example.com")
  console.log(data)
}
```

**Rules:**
- `await` only allowed in `async` functions
- Pauses execution until Promise resolves
- Can only `await` values of type `Promise<T>` or `T`

---

## Promise Type

```typescript
class Promise<T> {
  constructor(executor: (resolve: (value: T) => void, reject: (error: Error) => void) => void)

  then<U>(onFulfilled: (value: T) => U): Promise<U>
  catch(onRejected: (error: Error) => void): Promise<T>
  finally(onFinally: () => void): Promise<T>
}
```

---

## TaskPool

Execute tasks in thread pool:

```typescript
import taskpool from '@ohos.taskpool'

@Concurrent
function heavyTask(data: number): number {
  return data * data
}

async function execute(): Promise<void> {
  let task: taskpool.Task = new taskpool.Task(heavyTask, 42)
  let result: number = await taskpool.execute(task)
  console.log(result)
}
```

---

## Workers

```typescript
import worker from '@ohos.worker'

// Main thread
let worker: worker.ThreadWorker = new worker.Worker("worker.js")
worker.postMessage({ data: "hello" })
worker.onmessage = (event: MessageEvent) => {
  console.log(event.data)
}
```

---

## Key Rules

1. **async functions**: Must have `async` modifier
2. **await restriction**: Only in async functions
3. **Promise types**: Generic over resolved value type
4. **@Concurrent**: Required for TaskPool functions
