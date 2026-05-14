# standard_rule4 good: external NDK callback is dispatched to UI thread

```cpp
void BrowserHost::OnColorResult(bool success, uint32_t color) {
  if (!CEF_CURRENTLY_ON_UIT()) {
    CEF_POST_TASK(CEF_UIT,
        base::BindOnce(&BrowserHost::OnColorResult,
                       weak_factory_.GetWeakPtr(), success, color));
    return;
  }
  if (!listener_) {
    return;
  }
  success ? listener_->ColorSelected(color)
          : listener_->ColorSelectionCanceled();
}
```

The method returns after posting to UI, then invokes the external callback only on UI.
