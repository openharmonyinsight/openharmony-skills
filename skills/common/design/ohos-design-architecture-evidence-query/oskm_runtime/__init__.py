"""skill 的运行时装配层：把 CLI、DB、SDK 装到位，并把查询转给 CLI。

**这个包不实现任何查询，也不再自己校验 schema。** 查询能力全在独立产物
`oskm-cli`（`packages/oskm/cli/`）里；schema 契约也只有那一处
（`oskm_cli/database.py`）。这里的 `validate-db` 是转发，不是第二份实现——
两份清单一定会漂，历史上 `runtime.REQUIRED_COLUMNS` 就是第二份。

模块划分：

    environment.py   端点与 .env（DB/SDK 归档 + CLI 产物）
    db_download.py   HTTP、安全解压、SQLite 校验、原子替换
    cli_install.py   定位 / 下载 / 结构校验 / 载入 CLI 产物
    state.py         .oskm-runtime.json 读写、廉价刷新判定
    install.py       安装与回滚、源码树探测（向上找 OpenHarmony 源码根）、
                     源码树内 DB/CLI/SDK 本地运行时候选
    doctor.py        环境自检
    bootstrap.py     唯一入口：只负责装，不负责查

**查询不在这里。** `bootstrap.py` 只实现 doctor / install / refresh /
update-cli / download-db / validate-db / cli-path 七条命令；`ask/arch/diff/sql`
一律直接调 `<runtime-root>/oskm-cli.pyz`。

CLI 与 `knowledge.db` 同类：**固定文件名、不记版本**。装在
`<runtime-root>/oskm-cli.pyz`，完整性靠结构校验（`verify_pyz`：shebang +
是 zip + 有 `__main__.py` 与 `oskm_cli/cli.py` + CRC 完好），与 DB 那侧的
`verify_sqlite` 同一思路；摘要只写进状态文件当出处记录，不作为期望值。

包名刻意不叫裸 `runtime`：顶层名太容易和宿主工具里的其它模块撞上，
而 `bootstrap.py` 是靠 `sys.path` 自举的，撞名会静默加载错东西。
"""

__all__ = ['bootstrap', 'cli_install', 'db_download', 'doctor', 'environment',
           'install', 'state']
