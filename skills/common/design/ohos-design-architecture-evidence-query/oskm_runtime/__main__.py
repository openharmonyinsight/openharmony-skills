"""`python3 -m oskm_runtime`，与 `python3 bootstrap.py` 等价。"""
from .bootstrap import main

if __name__ == '__main__':
    raise SystemExit(main())
