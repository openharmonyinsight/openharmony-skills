# standard_rule9 bad: CEF_POST_TASK is used before Web instance checks

```cpp
void NWebDelegate::NotifyScreenInfoChanged(RotationType rotation) {
  CEF_POST_TASK(CEF_UIT,
      base::BindOnce(&NWebDelegate::SetRotationType,
                     weak_factory_.GetWeakPtr(), rotation));
}
```

The posted task may depend on a browser/Web instance that has not been created yet.
