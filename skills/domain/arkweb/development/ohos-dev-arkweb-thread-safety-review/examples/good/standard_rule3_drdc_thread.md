# standard_rule3 good: compositor work is posted to DrDC thread

Source: AI-generated illustrative example.

```cpp
void DisplayScheduler::RequestComposite(const FrameSinkId& frame_sink_id) {
  drdc_task_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(&DisplayScheduler::RequestCompositeOnDrDCThread,
                     weak_factory_.GetWeakPtr(), frame_sink_id));
}
```

The direct access to `compositor_gpu_thread_` is isolated to the DrDC sequence.
