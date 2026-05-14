# standard_rule6 good: UI object access is posted and resolved by ID

```cpp
void PrintAdapter::OnStartLayoutWrite() {
  content::GetUIThreadTaskRunner({})->PostTask(
      FROM_HERE,
      base::BindOnce(&PrintAdapter::OnStartLayoutWriteOnUIThread,
                     rfh_id_));
}

void PrintAdapter::OnStartLayoutWriteOnUIThread(
    content::GlobalRenderFrameHostId rfh_id) {
  auto* rfh = content::RenderFrameHost::FromID(rfh_id);
  if (!rfh || !rfh->IsRenderFrameLive()) {
    return;
  }
  auto* web_contents = content::WebContents::FromRenderFrameHost(rfh);
}
```

The callback stores an ID, switches to UI, then resolves the live object there.
