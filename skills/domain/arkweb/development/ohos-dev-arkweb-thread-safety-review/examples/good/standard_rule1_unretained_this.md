# standard_rule1 good: async task uses WeakPtr

```cpp
class RefreshListener {
 public:
  explicit RefreshListener(scoped_refptr<base::SequencedTaskRunner> ui_runner)
      : ui_runner_(std::move(ui_runner)) {}

  void ScheduleRepeat(float delta) {
    ui_runner_->PostTask(
        FROM_HERE,
        base::BindOnce(&RefreshListener::OnAnimationRepeat,
                       weak_factory_.GetWeakPtr(), delta));
  }

  void Stop() {
    weak_factory_.InvalidateWeakPtrs();
    delete this;
  }

 private:
  void OnAnimationRepeat(float delta);

  scoped_refptr<base::SequencedTaskRunner> ui_runner_;
  base::WeakPtrFactory<RefreshListener> weak_factory_{this};
};
```

Safe evidence: the async boundary still exists, but `WeakPtr` invalidation prevents the callback from running on a destroyed object.
