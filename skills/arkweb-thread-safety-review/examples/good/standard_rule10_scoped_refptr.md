# standard_rule10 good: cross-thread ref-counted object uses RefCountedThreadSafe

```cpp
class BackendFactory
    : public base::RefCountedThreadSafe<BackendFactory> {
 public:
  void CreateBackend();

 private:
  friend class base::RefCountedThreadSafe<BackendFactory>;
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

Safe evidence: cross-thread ownership is backed by a thread-safe reference count. Object methods still need their own sequence-safety guarantees, so this example only clears the refcount/lifetime part of rule10.
