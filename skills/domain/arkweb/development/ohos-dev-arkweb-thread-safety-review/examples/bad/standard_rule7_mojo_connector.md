# standard_rule7 bad: mojo::Connector is used on another thread

Source: AI-generated illustrative example.

```cpp
class MessageProxy {
 public:
  void BindOnIoSequence(mojo::ScopedMessagePipeHandle handle) {
    DCHECK(io_task_runner_->RunsTasksInCurrentSequence());
    connector_ = std::make_unique<mojo::Connector>(std::move(handle));
  }

  void SendFromWorker(mojo::Message message) {
    DCHECK(worker_task_runner_->RunsTasksInCurrentSequence());
    // BAD: connector_ was created on the IO sequence but is used on worker.
    connector_->Accept(&message);
  }

 private:
  scoped_refptr<base::SequencedTaskRunner> io_task_runner_;
  scoped_refptr<base::SequencedTaskRunner> worker_task_runner_;
  std::unique_ptr<mojo::Connector> connector_;
};
```

Violation evidence:
- creation/binding sequence: `BindOnIoSequence`
- use sequence: `SendFromWorker`
- unsafe operation: `connector_->Accept(&message)` runs on a different sequence

`mojo::Connector` is sequence-affine and must be used on the sequence where it was created.
