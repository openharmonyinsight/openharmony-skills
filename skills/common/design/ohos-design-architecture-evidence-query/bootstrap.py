#!/usr/bin/env python3
"""skill 的唯一入口。

    python3 bootstrap.py doctor
    python3 bootstrap.py install --runtime-root ~/.oskm
    python3 bootstrap.py refresh --runtime-root ~/.oskm

查询不归它管，直接调装好的 CLI：

    python3 ~/.oskm/oskm-cli.pyz --db ~/.oskm/knowledge.db arch overview

这个文件只做一件事：把**自己所在目录**放到 `sys.path` 最前面，然后交给
`oskm_runtime.bootstrap:main`。自举放在这里而不是让使用者设 `PYTHONPATH`，
是因为 skill 会被解压到宿主工具决定的任意目录（`.claude/skills/…`、
`${CODEX_HOME}/skills/…`），任何"先 cd 到某处"的前提都会在某个宿主上失效。

Windows 把 `python3` 换成 `py -3`。不要求 Bash，也不要求 Git。
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from oskm_runtime.bootstrap import main  # noqa: E402  (需要先补 sys.path)

if __name__ == '__main__':
    raise SystemExit(main())
