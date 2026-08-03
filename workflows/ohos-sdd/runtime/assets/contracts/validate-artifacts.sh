#!/usr/bin/env bash
# 兼容入口:委托给 ohos-sdd CLI 的源契约自检。
# 兼容新仓布局(runtime/assets/contracts/ + runtime/assets/cli/)和
# 发布布局(shared/ohos-sdd/contracts/ + bin/)。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 契约路径:优先与脚本同目录;回退 walk-up。
CONTRACT=""
for cand in "${SCRIPT_DIR}/artifacts.yaml" \
           "${SCRIPT_DIR}/../../contracts/artifacts.yaml"; do
  if [[ -f "$cand" ]]; then
    CONTRACT="$cand"; break
  fi
done
if [[ -z "$CONTRACT" ]]; then
  d="$SCRIPT_DIR"
  while [[ "$d" != "/" ]]; do
    for cand in "$d/runtime/assets/contracts/artifacts.yaml" "$d/contracts/artifacts.yaml"; do
      if [[ -f "$cand" ]]; then
        CONTRACT="$cand"; break 2
      fi
    done
    d="$(dirname "$d")"
  done
fi
if [[ -z "$CONTRACT" ]]; then
  echo "validate-artifacts: 找不到契约 artifacts.yaml" >&2
  exit 2
fi

# CLI 路径:新仓 runtime/assets/cli/ 或发布布局 bin/
CLI=""
for cand in "${SCRIPT_DIR}/../cli/ohos-sdd" \
           "${SCRIPT_DIR}/../../../bin/ohos-sdd" \
           "${SCRIPT_DIR}/../../bin/ohos-sdd" \
           "${SCRIPT_DIR}/../../shared/ohos-sdd/bin/ohos-sdd"; do
  [[ -x "$cand" ]] && { CLI="$cand"; break; }
done
if [[ -z "$CLI" ]]; then
  echo "validate-artifacts: 找不到 ohos-sdd CLI(先构建或安装插件)" >&2
  exit 2
fi

exec "$CLI" validate --source --contract "$CONTRACT"
