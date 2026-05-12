# standard_rule7 good: mojo::Connector use returns to owner sequence

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
    io_task_runner_->PostTask(
        FROM_HERE,
        base::BindOnce(&MessageProxy::SendOnIoSequence,
                       weak_factory_.GetWeakPtr(), std::move(message)));
  }

 private:
  void SendOnIoSequence(mojo::Message message) {
    DCHECK(io_task_runner_->RunsTasksInCurrentSequence());
    connector_->Accept(&message);
  }

  scoped_refptr<base::SequencedTaskRunner> io_task_runner_;
  scoped_refptr<base::SequencedTaskRunner> worker_task_runner_;
  std::unique_ptr<mojo::Connector> connector_;
  base::WeakPtrFactory<MessageProxy> weak_factory_{this};
};
```

Safe evidence: worker entry only posts the message; `mojo::Connector` is touched by `SendOnIoSequence` on the creation sequence.
