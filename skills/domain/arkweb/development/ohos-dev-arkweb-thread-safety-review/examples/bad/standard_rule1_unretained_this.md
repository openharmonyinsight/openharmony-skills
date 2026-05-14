# standard_rule1 bad: async task captures raw this

```cpp
class RefreshListener {
 public:
  explicit RefreshListener(scoped_refptr<base::SequencedTaskRunner> ui_runner)
      : ui_runner_(std::move(ui_runner)) {}

  void ScheduleRepeat(float delta) {
    ui_runner_->PostTask(
        FROM_HERE,
        base::BindOnce(&RefreshListener::OnAnimationRepeat,
                       base::Unretained(this), delta));
  }

  void Stop() {
    delete this;
  }

 private:
  void OnAnimationRepeat(float delta);

  scoped_refptr<base::SequencedTaskRunner> ui_runner_;
};
```

Violation evidence:
- async boundary: `ui_runner_->PostTask`
- unsafe capture: `base::Unretained(this)`
- visible lifetime risk: `Stop` can destroy the object before the posted task runs
- missing guard: no `WeakPtr`, cancellation, or owner lifetime guarantee in this file

`this` is captured by an asynchronous task. If the object is destroyed before the task runs, the callback can dereference freed memory.
