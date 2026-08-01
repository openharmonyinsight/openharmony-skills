# Host integration environment contract

The integration eval is valid only when `scripts/prepare_host_integration.py` produces an
`environment.json` with `ready: true`. The manifest must capture:

- OpenHarmony root and ace_engine revision;
- clean ace_engine working tree;
- successful attributed `host_product/ace_engine_test` build state after the pinned source;
- stripped and `exe.unstripped` paths, executable status, hashes, and matching Build IDs;
- exact gtest XML output path;
- the requested binary and exact gtest filter.

If preparation fails, record the integration case as `BLOCKED_ENVIRONMENT`; do not substitute
an older binary, an unpinned workspace, or prompt-provided assertions.
