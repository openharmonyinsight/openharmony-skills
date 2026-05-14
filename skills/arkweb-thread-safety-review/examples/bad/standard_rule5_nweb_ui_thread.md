# standard_rule5 bad: NWeb-related state is updated from an unknown thread

```cpp
class PreferenceMigrator {
 public:
  void StartFromWorker(std::string path, bool value) {
    DCHECK(worker_task_runner_->RunsTasksInCurrentSequence());
    WriteBrowserPreference(path, value);
  }

 private:
  void WriteBrowserPreference(std::string path, bool value) {
    // BAD: Browser process preferences are touched from the worker entry.
    g_browser_process->local_state()->SetBoolean(path, value);
    g_browser_process->local_state()->CommitPendingWrite();
  }

  scoped_refptr<base::SequencedTaskRunner> worker_task_runner_;
};
```

Violation evidence:
- entry sequence: `StartFromWorker`
- constrained object: browser preference state behind `g_browser_process->local_state()`
- missing transfer: no UI thread check or `PostTask` to UI before access

Browser process preferences and NWeb-adjacent state must be accessed on the UI thread.
