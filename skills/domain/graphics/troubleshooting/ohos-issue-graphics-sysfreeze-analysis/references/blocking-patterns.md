# 常见阻塞模式

**重要提示：模式中的函数需解栈确认**

## 锁和同步原语阻塞

| 阻塞函数 | 说明 | 分析方法 |
|------|------|------|
| pthread_cond_timedwait | 等待信号量/条件变量 | 根据上层业务分析条件由哪个线程业务出发，再分析对应线程栈 |
| pthread_mutex_timedlock_inner | 等待互斥锁 | 根据上层业务分析确定等待的锁资源，再分析当前锁被哪个线程持有，分析对应线程栈 |

示例：

```
Tid:54719, Name:OS_IPC_40_54719
#00 pc 001d4338 /system/lib64/ld-musl-aarch64.so.1(__timedwait_cp)
#01 pc 001da37c /system/lib64/ld-musl-aarch64.so.1(__pthread_mutex_timedlock_inner)
#02 pc 000c76ac /system/lib64/chipset-sdk-sp/libc++.so(std::__h::mutex::lock)
#03 pc 000654c4 /system/lib64/libapsmgr.z.so(OHOS:Rosen::SwingFrameRate::SetSceneInfo)
#04 pc 00044744 /system/lib64/libapsmgr.z.so(OHOS:Rosen::FrameRateControl::NotifyPkgChange)
#05 pc 00046f18 /system/lib64/libapsmgr.z.so(OHOS:Rosen::FrameRateControl::SetSceneInfo)
#06 pc 000460a0 /system/lib64/libapsmgr.z.so(OHOS:Rosen::FrameRateControl::SetScene)
#07 pc 0003c5b0 /system/lib64/libapsmgr.z.so(OHOS:Rosen::ApsManagerService::SetScene)
#07 pc 0005f374 /system/lib64/libapsmgr.z.so(OHOS:Rosen::ApsManagerStub::OnRemoteRequest)

Tid:5566, Name:OS_IPC_42_5566
#00 pc 001d4338 /system/lib64/ld-musl-aarch64.so.1(__timedwait_cp)
#01 pc 001da37c /system/lib64/ld-musl-aarch64.so.1(__pthread_mutex_timedlock_inner)
#02 pc 000c7830 /system/lib64/chipset-sdk-sp/libc++.so(std::__h::recursive_mutex::lock)
#06 pc 0004582c /system/lib64/libapsmgr.z.so(OHOS:Rosen::FrameRateControl::SetScene)
#07 pc 0003c5b0 /system/lib64/libapsmgr.z.so(OHOS:Rosen::ApsManagerService::SetScene)
#07 pc 0005f374 /system/lib64/libapsmgr.z.so(OHOS:Rosen::ApsManagerStub::OnRemoteRequest)

Tid:61947, Name:OS_IPC_33_61947
#00 pc 00191e0c /system/lib64/ld-musl-aarch64.so.1(ioctl)
#01 pc 0000f030 /system/lib64/platformsdk/libipc_common.z.so(OHOS::BinerConnector::WriteBinder)
#02 pc 00071c54 /system/lib64/platformsdk/libipc_single.z.so(OHOS::BinerInvoker::TransactWithDriver)
#03 pc 00070654 /system/lib64/platformsdk/libipc_single.z.so(OHOS::BinerInvoker::WaitForCompletion)
#04 pc 0006fb24 /system/lib64/platformsdk/libipc_single.z.so(OHOS::BinerInvoker::SendRequest)
#05 pc 00048c74 /system/lib64/platformsdk/libipc_single.z.so(OHOS::IPCObjectProxy::SendRequestInner)
#06 pc 00049690 /system/lib64/platformsdk/libipc_single.z.so(OHOS::IPCObjectProxy::SendRequest)
#07 pc 0005ea98 /system/lib64/libapsmgr.z.so
#08 pc 000639c0 /system/lib64/libapsmgr.z.so(OHOS:Rosen::SwingFrameRate::RegiterSystemCallback)
#09 pc 0005fbc4 /system/lib64/libapsmgr.z.so(OHOS:Rosen::ApsManagerStub::OnRemoteRequest)
```

5566线程等锁，根据类名推知FrameRateControl持锁；查看其它线程调用栈，54719线程下层栈为FrameRateControl且也处于SetScene调用，上层栈SwingFrameRate等锁，推知线程持FrameRateControl锁，等SwingFrameRate锁；同理，分析61947线程持SwingFrameRate锁，正在等待ipc请求完成。因此完整的阻塞链：5566->54719->61947->ipc对端线程。

## 同步/异步任务阻塞

| 阻塞函数 | 说明 | 分析方法 |
|------|------|------|
| OHOS::Rosen::RSDrawFrame::PostAndWait | render_service主线程等RSUniRenderThread线程 | 分析RSUniRenderThread线程 |
| `X`Thread::PostSyncTask | 向X线程抛同步任务被阻塞 | 分析对应X线程 |
| DDGR::GrDrawOp::DoExecute -> std::future::get | DrawOp异步任务等待 | 线程等待DrawOp异步任务在DDGRTask线程完成，分析DDGRTask线程 |
| OHOS::BinderInvoker::SendRequest -> ioctl | 线程发起IPC请求 | 查看Binder信息，分析当前线程ipc的对端线程 |

## 工作线程状态分析

| 函数/状态 | 说明 | 分析方法 |
|------|------|------|
| 栈顶OHOS::AppExecFwk::EventQueueBase::GetEvent | EventRunner线程空闲，无任务执行 | 检查任务队列，确认是否有任务提交 |
| OHOS::BinderInvoker::StartWorkLoop -> ioctl | IPC工作线程空闲，未处理IPC请求 | 检查BinderCatcher信息，确认IPC通信状态 |
