# standard_rule9 good: Web instance is checked before CEF_POST_TASK

```cpp
void NWebDelegate::NotifyScreenInfoChanged(RotationType rotation) {
  auto browser = GetBrowser();
  if (!browser || !browser->GetHost()) {
    return;
  }
  CEF_POST_TASK(CEF_UIT,
      base::BindOnce(&NWebDelegate::SetRotationType,
                     weak_factory_.GetWeakPtr(), rotation));
}
```

The task is posted only after confirming the target Web instance exists.
