#!/usr/bin/env bash
# 兼容入口:委托给 ohos-sdd CLI 的源契约自检。
# 历史上用 ruby -ryaml 解析 artifacts.yaml;现由 ohos_sdd_engine.py(mini yaml)承担。
# 兼容源仓布局(openharmony/contracts/ + openharmony/tools/cli/)和
# 发布布局(shared/ohos-sdd/contracts/ + bin/)。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 契约路径:优先与脚本同目录(源仓和发布布局均为 contracts/ 兄弟);
# 回退源仓 walk-up(openharmony/contracts/artifacts.yaml)。
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
    if [[ -f "$d/openharmony/contracts/artifacts.yaml" ]]; then
      CONTRACT="$d/openharmony/contracts/artifacts.yaml"; break
    fi
    d="$(dirname "$d")"
  done
fi
if [[ -z "$CONTRACT" ]]; then
  echo "validate-artifacts: 找不到契约 artifacts.yaml" >&2
  exit 2
fi

# CLI 路径:兼容源仓(tools/cli/)和发布布局(bin/)。
# 源仓: contracts/../tools/cli/ohos-sdd
# 发布: shared/ohos-sdd/contracts/../../../bin/ohos-sdd
CLI=""
for cand in "${SCRIPT_DIR}/../tools/cli/ohos-sdd" \
           "${SCRIPT_DIR}/../../../bin/ohos-sdd" \
           "${SCRIPT_DIR}/../../bin/ohos-sdd" \
           "${SCRIPT_DIR}/../cli/ohos-sdd" \
           "${SCRIPT_DIR}/../../shared/ohos-sdd/bin/ohos-sdd"; do
  [[ -x "$cand" ]] && { CLI="$cand"; break; }
done
if [[ -z "$CLI" ]]; then
  echo "validate-artifacts: 找不到 ohos-sdd CLI(先构建或安装插件)" >&2
  exit 2
fi
# 判断布局:源仓布局有 openharmony/ 目录,发布布局没有。
# --source 模式校验 contract 结构(模板存在性、标题完整性等),两种布局都支持。
# CLI validate_contract_source 已兼容源仓(openharmony/contracts/)和发布布局(contracts/)。
SOURCE_FLAG="--source"
d="$SCRIPT_DIR"
while [[ "$d" != "/" ]]; do
  if [[ -d "$d/openharmony" ]]; then
    break
  fi
  d="$(dirname "$d")"
done

exec "$CLI" validate $SOURCE_FLAG --contract "$CONTRACT"
