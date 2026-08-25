# 安全 (Security)

安全子系统相关技能，涵盖权限管理、数据安全、安全审查、威胁检测等。

## 细分主题域

- **seharmony** — SELinux 策略子域，属于 security namespace 下的细分主题域，对应 `metadata.domain=seharmony`、`namespace=security`。

## Development

| Skill | Description |
| --- | --- |
| `ohos-dev-seharmony-policy-review` | OpenHarmony SELinux 策略提交自检扫描。依据 selinux_adapter 仓库的自检项，扫描 commit/PR diff 中新增的 .te、file_contexts、service_contexts、attributes、*_whitelist.json 等策略文件，逐条判定并输出报告（含 ROM 增量估算）。 |

> **注**：`evals/` 目录为测试资产（fixture + 断言），非运行时资源，仅供 skill 质量评估使用。
