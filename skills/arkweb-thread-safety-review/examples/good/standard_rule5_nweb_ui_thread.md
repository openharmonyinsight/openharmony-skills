# standard_rule5 good: NWeb-related state is updated on UI thread

```cpp
class PreferenceMigrator {
 public:
  void StartFromWorker(std::string path, bool value) {
    DCHECK(worker_task_runner_->RunsTasksInCurrentSequence());
    content::GetUIThreadTaskRunner({})->PostTask(
        FROM_HERE,
        base::BindOnce(&PreferenceMigrator::WriteBrowserPreferenceOnUi,
                       weak_factory_.GetWeakPtr(), std::move(path), value));
  }

 private:
  void WriteBrowserPreferenceOnUi(std::string path, bool value) {
    DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
    g_browser_process->local_state()->SetBoolean(path, value);
    g_browser_process->local_state()->CommitPendingWrite();
  }

  scoped_refptr<base::SequencedTaskRunner> worker_task_runner_;
  base::WeakPtrFactory<PreferenceMigrator> weak_factory_{this};
};
```

Safe evidence: worker entry posts to UI and only the UI helper touches browser preference state.
