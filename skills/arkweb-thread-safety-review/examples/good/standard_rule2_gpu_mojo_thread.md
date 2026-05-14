# standard_rule2 good: GPU work is posted to GPU thread

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
    gpu_task_runner_->PostTask(
        FROM_HERE,
        base::BindOnce(&GpuBridge::CreateSharedImageOnGpuThread,
                       weak_factory_.GetWeakPtr(), mailbox));
  }

 private:
  void CreateSharedImageOnGpuThread(const gpu::Mailbox& mailbox) {
    DCHECK(gpu_task_runner_->RunsTasksInCurrentSequence());
    shared_image_manager_->CreateSharedImage(mailbox);
  }

  mojo::Receiver<mojom::GpuBridge> receiver_{this};
  scoped_refptr<base::SequencedTaskRunner> ipc_task_runner_;
  scoped_refptr<base::SequencedTaskRunner> gpu_task_runner_;
  raw_ptr<gpu::SharedImageManager> shared_image_manager_;
  base::WeakPtrFactory<GpuBridge> weak_factory_{this};
};
```

Safe evidence: the mojo callback only forwards work from IPC; GPU resources are touched on the GPU task runner.
