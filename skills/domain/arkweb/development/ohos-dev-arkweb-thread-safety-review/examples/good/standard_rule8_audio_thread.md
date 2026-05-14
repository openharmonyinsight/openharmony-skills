# standard_rule8 good: audio stream lifecycle is posted to Audio thread

```cpp
class AudioOutputStream {
 public:
  void OnUiResume() {
    DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
    if (callback_ && audio_task_runner_) {
      audio_task_runner_->PostTask(
          FROM_HERE,
          base::BindOnce(&AudioOutputStream::StartOnAudioThread,
                         weak_factory_.GetWeakPtr(), callback_));
    }
  }

 private:
  void StartOnAudioThread(AudioCallback* callback) {
    DCHECK(audio_task_runner_->RunsTasksInCurrentSequence());
    Start(weak_factory_.GetWeakPtr(), callback);
  }

  void Start(base::WeakPtr<AudioOutputStream> stream,
             AudioCallback* callback);

  AudioCallback* callback_ = nullptr;
  scoped_refptr<base::SequencedTaskRunner> audio_task_runner_;
  base::WeakPtrFactory<AudioOutputStream> weak_factory_{this};
};
```

Safe evidence: UI entry does not mutate the stream directly; lifecycle work runs after transfer to the Audio task runner.
