# standard_rule4 bad: external NDK callback is invoked without UI-thread dispatch

```cpp
void BrowserHost::OnColorResult(bool success, uint32_t color) {
  if (success) {
    listener_->ColorSelected(color);
  } else {
    listener_->ColorSelectionCanceled();
  }
}
```

The callback may run off the UI thread, but `listener_` represents an external interface that must be called on UI.
