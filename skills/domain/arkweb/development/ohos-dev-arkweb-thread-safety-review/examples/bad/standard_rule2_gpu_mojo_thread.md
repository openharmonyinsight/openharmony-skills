# standard_rule2 bad: GPU mojo callback handles GPU resource directly

Source: AI-generated illustrative example.

```cpp
class GpuBridge {
 public:
  void BindReceiverOnIpcThread(
      mojo::PendingReceiver<mojom::GpuBridge> receiver) {
    DCHECK(ipc_task_runner_->RunsTasksInCurrentSequence());
    receiver_.Bind(std::move(receiver));
  }

  void OnCreateSharedImage(const gpu::Mailbox& mailbox) override {
    DCHECK(ipc_task_runner_->RunsTasksInCurrentSequence());
    // BAD: the mojo callback runs on IPC but directly mutates GPU state.
    shared_image_manager_->CreateSharedImage(mailbox);
  }

 private:
  mojo::Receiver<mojom::GpuBridge> receiver_{this};
  scoped_refptr<base::SequencedTaskRunner> ipc_task_runner_;
  scoped_refptr<base::SequencedTaskRunner> gpu_task_runner_;
  raw_ptr<gpu::SharedImageManager> shared_image_manager_;
};
```

Violation evidence:
- receiver binding sequence: `BindReceiverOnIpcThread`
- callback sequence: IPC
- constrained object: `shared_image_manager_`
- missing transfer: no post to `gpu_task_runner_`

Mojo callbacks may run on an IPC sequence. GPU resource work must be forwarded to the matching GPU sequence.
