# 二进制资源来源与校验

本 Skill 随包发布的二进制资源，其来源、版本与 SHA-256 校验值如下，供审查与可追溯。

## hilogtool.exe

| 项 | 值 |
|---|---|
| 文件 | `tools/hilogtool.exe` |
| 用途 | HiLog 加密日志（`hilog.*.gz`）解密工具，输出明文 `.txt` 供 `filter_hilog.py` 解析 |
| 来源 | HarmonyOS SDK（DevEco Studio）自带工具，非本项目原创 |
| 官方说明 | https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hilog-tool |
| 大小 | 1,029,632 字节 |
| SHA-256 | `f51bd7ad984655e217df625045a07fa9a27d8d55dbcf3387ca911924988d34e0` |
| 许可 | 随 HarmonyOS SDK 分发，遵循华为 SDK 许可协议 |
| 运行 | Windows 原生执行；Linux 经 `wine64` 运行（详见 `references/hilogtool-guide.md`） |

校验命令：

```bash
sha256sum tools/hilogtool.exe
# 期望: f51bd7ad984655e217df625045a07fa9a27d8d55dbcf3387ca911924988d34e0
```

## xts_rules.db

| 项 | 值 |
|---|---|
| 文件 | `data/xts_rules.db` |
| 用途 | XTS 测试日志定界规则库（`rules`/`so_mapping`/`kit_module` 等 21 张表），供 `query_db.py`、`analyze_crash_stack.py` 查询 |
| 来源 | 从 OpenHarmony 源码自动构建并随包预置；各表数据来源见 `docs/database-schema.md` 对应"数据来源"段（如 `/interface/sdk-js/kits/@kit.*.d.ts`、`/base/hiviewdfx/hilog/services/hilogd/log_domains.cpp`） |
| 版本 | `v3.0`（异常状态识别增强，2026-07-02；见 `db_version` 表） |
| 大小 | 1,785,856 字节 |
| SHA-256 | `81ed32d85f45c7e96241ad4d35c3fbdc4eb6f5f5bc20e42170f7cad7ee42696d` |
| 构建 | 预构建数据库，无独立 `init_db.py` 脚本；升级随 Skill 版本更新发布 |
| 许可 | 本项目构建产物；规则与映射数据源自 OpenHarmony 开源代码（Apache License 2.0） |

校验命令：

```bash
sha256sum data/xts_rules.db
# 期望: 81ed32d85f45c7e96241ad4d35c3fbdc4eb6f5f5bc20e42170f7cad7ee42696d
```

## 完整性核验

重新获取 Skill 包后，若上述 SHA-256 与本文档不一致，视为资源被篡改，应停止使用并重新获取官方 Skill 包。
