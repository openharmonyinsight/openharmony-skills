# no violation: suspicious API without thread ownership evidence

```cpp
class AudioController {
 public:
  void ResumeIfNeeded() {
    if (stream_) {
      stream_->Start();
    }
  }

 private:
  std::unique_ptr<AudioStream> stream_;
};
```

Do not report rule8 from this file alone. The method name is suspicious, but the current file does not show the entry thread, the Audio task runner, or whether `ResumeIfNeeded` already runs on the Audio sequence.

Correct result: no violation.
