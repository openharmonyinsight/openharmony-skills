# standard_rule6 bad: WebContents is accessed from a non-UI callback

```cpp
void PrintAdapter::OnStartLayoutWrite() {
  auto* web_contents = content::WebContents::FromRenderFrameHost(rfh_);
  if (web_contents) {
    title_ = web_contents->GetTitle();
  }
}
```

`RenderFrameHost` and `WebContents` are UI-thread objects. Raw pointers can also become stale across async work.
