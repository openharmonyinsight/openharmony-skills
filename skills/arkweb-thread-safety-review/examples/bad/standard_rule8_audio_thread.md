# standard_rule8 bad: audio stream lifecycle is restarted from a callback thread

```cpp
class AudioOutputStream {
 public:
  void OnUiResume() {
    DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
    if (callback_) {
      // BAD: Start mutates the audio stream lifecycle from the UI thread.
      Start(weak_factory_.GetWeakPtr(), callback_);
    }
  }

 private:
  void Start(base::WeakPtr<AudioOutputStream> stream,
             AudioCallback* callback);

  AudioCallback* callback_ = nullptr;
  base::WeakPtrFactory<AudioOutputStream> weak_factory_{this};
};
```

Violation evidence:
- entry thread: `OnUiResume` is on the UI thread
- constrained operation: `Start` changes the Audio lifecycle
- missing transfer: no post to `audio_task_runner_`

Audio start, pause, stop, and close operations must run on the Audio thread.
