# Output Examples

Read this file only when JSON field filling is ambiguous. The `rule_level` table in `SKILL.md` is authoritative; if any example conflicts with that table, follow `SKILL.md`.

All examples in this file use the complete top-level JSON shape. Do not copy only a `violations` array or a single violation object as final output.

## No Violation

Use this shape when evidence is weak, even if the code looks suspicious:

```json
{
  "scan_info": {
    "file_path": "/path/to/file.cc",
    "skill": "arkweb-thread-safety-review"
  },
  "summary": {
    "total_violations": 0,
    "by_rule": {},
    "by_team": {}
  },
  "violations": []
}
```

Do not add `uncertain`, `notes`, `risk`, or any custom field.

## Rejected Output Patterns

Never use these shapes as final output:
- A JSON object with `uncertain`, `note`, `risk`, `finding`, or any custom field outside the schema.
- A violation for ID/value transfer only, such as frame tree node id, routing id, URL, or string snapshot crossing threads.
- A violation based only on missing thread checks, without visible object, thread/sequence path, async boundary, and missing guard evidence.
- A `required_fix` value that invents helper names, task runners, file paths, or ownership not visible in the current file.

## Minimal Violation

When exact replacement code is not visible, keep `required_fix` directional and do not invent helper names:

```json
{
  "scan_info": {
    "file_path": "/path/to/refresh_listener.cc",
    "skill": "arkweb-thread-safety-review"
  },
  "summary": {
    "total_violations": 1,
    "by_rule": {
      "standard_rule1": 1
    },
    "by_team": {
      "交互安全": 1
    }
  },
  "violations": [
    {
      "id": 1,
      "rule_id": "standard_rule1",
      "rule_name": "异步任务裸 this 生命周期约束",
      "rule_level": "P1",
      "location": {
        "file": "refresh_listener.cc",
        "line": 42,
        "function": "RefreshListener::ScheduleRepeat"
      },
      "issue": "异步 PostTask 使用 base::Unretained(this)，当前文件可见 Stop 可能在任务执行前销毁对象，缺少 WeakPtr 或取消机制。",
      "anti_pattern": "base::BindOnce(&RefreshListener::OnAnimationRepeat, base::Unretained(this), delta)",
      "required_fix": "改用 WeakPtr 或在销毁前取消未执行任务；不要继续把裸 this 绑定到异步任务。",
      "impact": "任务延迟执行时可能解引用已销毁对象，导致 UAF。",
      "team": "交互安全"
    }
  ]
}
```

## Multi-Rule Conflict

If one code path appears to match multiple rules, report only the most specific root cause. Example: a GPU mojo callback directly touches GPU state and also uses a mojo receiver. If the unsafe operation is GPU state access on the IPC callback, report `standard_rule2`; do not also report `standard_rule7` unless the same file proves `mojo::Connector` itself is used across sequences.

## Three-Rule Overlap

When a callback appears to match three rules, split only the independently proven root causes. In this example, GPU state access and connector sequence misuse are both visible; raw `this` is not reported because the file does not prove the task can outlive the object.

```json
{
  "scan_info": {
    "file_path": "/path/to/gpu_message_bridge.cc",
    "skill": "arkweb-thread-safety-review"
  },
  "summary": {
    "total_violations": 2,
    "by_rule": {
      "standard_rule2": 1,
      "standard_rule7": 1
    },
    "by_team": {
      "渲染合成": 1,
      "基础框架": 1
    }
  },
  "violations": [
    {
      "id": 1,
      "rule_id": "standard_rule2",
      "rule_name": "GPU mojo 任务线程约束",
      "rule_level": "P1",
      "location": {
        "file": "gpu_message_bridge.cc",
        "line": 73,
        "function": "GpuMessageBridge::OnMessage"
      },
      "issue": "IPC 回调线程直接更新 GPU 状态，当前文件未显示投递到 GPU task runner。",
      "anti_pattern": "gpu_state_->Apply(message)",
      "required_fix": "将 GPU 状态访问投递到 GPU task runner 后执行。",
      "impact": "GPU 资源在错误线程访问，可能导致竞态或状态破坏。",
      "team": "渲染合成"
    },
    {
      "id": 2,
      "rule_id": "standard_rule7",
      "rule_name": "mojo::Connector 跨线程约束",
      "rule_level": "P1",
      "location": {
        "file": "gpu_message_bridge.cc",
        "line": 75,
        "function": "GpuMessageBridge::OnMessage"
      },
      "issue": "connector_ 在 UI sequence 绑定，但在 IPC 回调 sequence 发送消息，当前文件可见创建和使用 sequence 不一致。",
      "anti_pattern": "connector_->Accept(&reply)",
      "required_fix": "将 connector 操作投递回绑定 sequence，或保证 connector 只在 owner sequence 使用。",
      "impact": "破坏 mojo::Connector sequence-affinity，可能导致 DCHECK、消息乱序或竞态崩溃。",
      "team": "基础框架"
    }
  ]
}
```

## Raw this + scoped_refptr Conflict

When an async task captures both `base::Unretained(this)` and `scoped_refptr<T>`, report `standard_rule1` if the concrete hazard is the receiver object's lifetime. Do not add `standard_rule10` unless `T` itself has visible non-thread-safe refcount/destruction evidence.

```json
{
  "scan_info": {
    "file_path": "/path/to/bridge.cc",
    "skill": "arkweb-thread-safety-review"
  },
  "summary": {
    "total_violations": 1,
    "by_rule": {
      "standard_rule1": 1
    },
    "by_team": {
      "基础框架": 1
    }
  },
  "violations": [
    {
      "id": 1,
      "rule_id": "standard_rule1",
      "rule_name": "异步任务裸 this 生命周期约束",
      "rule_level": "P1",
      "location": {
        "file": "bridge.cc",
        "line": 88,
        "function": "Bridge::Schedule"
      },
      "issue": "异步任务使用 base::Unretained(this)，当前文件未显示对象生命周期覆盖任务执行；scoped_refptr 参数不是本次上报根因。",
      "anti_pattern": "base::BindOnce(&Bridge::Run, base::Unretained(this), holder)",
      "required_fix": "将 this 改为 WeakPtr，或在销毁前取消任务；不要因同一代码片段重复报告 rule10。",
      "impact": "对象销毁后任务仍可能执行，导致 UAF。",
      "team": "基础框架"
    }
  ]
}
```

## Low-Confidence Team

When team ownership is not obvious after reading `team_mapping.md`, choose the nearest owner and state the basis in `issue`.

```json
{
  "scan_info": {
    "file_path": "/path/to/message_proxy.cc",
    "skill": "arkweb-thread-safety-review"
  },
  "summary": {
    "total_violations": 1,
    "by_rule": {
      "standard_rule7": 1
    },
    "by_team": {
      "基础框架": 1
    }
  },
  "violations": [
    {
      "id": 1,
      "rule_id": "standard_rule7",
      "rule_name": "mojo::Connector 跨线程约束",
      "rule_level": "P1",
      "location": {
        "file": "message_proxy.cc",
        "line": 64,
        "function": "MessageProxy::SendFromWorker"
      },
      "issue": "mojo::Connector 在 IO sequence 创建但在 worker sequence 使用；按 team_mapping 中 mojo/IPC plumbing 归属，选择基础框架。",
      "anti_pattern": "connector_->Accept(&message)",
      "required_fix": "将 connector 操作投递回创建 sequence，或保证 connector 只在 owner sequence 使用。",
      "impact": "破坏 mojo::Connector sequence-affinity，可能导致竞态或崩溃。",
      "team": "基础框架"
    }
  ]
}
```
