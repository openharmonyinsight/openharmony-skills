# standard_rule3 bad: compositor_gpu_thread_ is called directly

Source: AI-generated illustrative example.

```cpp
void DisplayScheduler::RequestComposite(const FrameSinkId& frame_sink_id) {
  compositor_gpu_thread_->ScheduleComposite(frame_sink_id);
}
```

`compositor_gpu_thread_` must not be accessed directly from arbitrary UI, IPC, or worker sequences.
