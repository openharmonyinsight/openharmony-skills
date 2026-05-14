# standard_rule10 bad: scoped_refptr crosses threads with non-thread-safe ref count

```cpp
class BackendFactory : public base::RefCounted<BackendFactory> {
 public:
  void CreateBackend();

 private:
  friend class base::RefCounted<BackendFactory>;
  ~BackendFactory() = default;
};

scoped_refptr<BackendFactory> factory_;

void Service::CreateOnWorker() {
  DCHECK(ui_task_runner_->RunsTasksInCurrentSequence());
  worker_task_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(&BackendFactory::CreateBackend, factory_));
}
```

Violation evidence:
- `factory_` is owned on the UI sequence but captured into a worker task
- `BackendFactory` uses `base::RefCounted`, not `base::RefCountedThreadSafe`
- current file has no proof that destruction or method access is confined to one sequence

The risk is not the `scoped_refptr` spelling alone; it is cross-thread ownership of an object whose refcount/destruction model is not thread-safe.
