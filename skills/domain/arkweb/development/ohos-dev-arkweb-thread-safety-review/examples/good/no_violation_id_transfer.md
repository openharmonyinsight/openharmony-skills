# no violation: cross-thread value transfer instead of UI object access

```cpp
void NavigationTracker::CollectOnUiThread(content::WebContents* web_contents) {
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);
  const int frame_tree_node_id =
      web_contents->GetPrimaryMainFrame()->GetFrameTreeNodeId();
  io_task_runner_->PostTask(
      FROM_HERE,
      base::BindOnce(&NavigationTracker::UseFrameIdOnIoThread,
                     weak_factory_.GetWeakPtr(), frame_tree_node_id));
}

void NavigationTracker::UseFrameIdOnIoThread(int frame_tree_node_id) {
  DCHECK_CURRENTLY_ON(content::BrowserThread::IO);
  RecordFrame(frame_tree_node_id);
}
```

Do not report rule6. `WebContents` and `RenderFrameHost` are accessed on the UI thread; only an integer id crosses to IO, so there is no cross-thread UI object dereference in this file.

Correct result: no violation.
