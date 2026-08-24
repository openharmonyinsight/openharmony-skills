#!/usr/bin/env bash
# SELinux 策略提交自检扫描脚本（自动可检项）
# 用法：
#   bash scan.sh <git-ref>           # 扫描某 commit/branch 的 sepolicy diff
#   bash scan.sh <base>..<head>      # 扫描区间
#   bash scan.sh - < file.diff       # 从 stdin 读 diff
#   echo "$DIFF" | bash scan.sh -    # 从管道读 diff
# 退出码：0 正常完成（不等于无违规，需人工看输出）

set -euo pipefail

emit() { printf '\n=== %s ===\n' "$1"; }

if [[ "${1:-}" == "-" ]]; then
    DIFF="$(cat)"
    REF_DESC="stdin"
else
    REF="${1:-HEAD}"
    DIFF="$(git show "$REF" -- sepolicy/ 2>/dev/null || git diff "${REF}" -- sepolicy/ 2>/dev/null || true)"
    REF_DESC="$REF"
fi

if [[ -z "$DIFF" ]]; then
    echo "ERROR: empty diff for target '$REF_DESC'. 检查 git ref 或 sepolicy 路径。" >&2
    exit 1
fi

echo "扫描目标: $REF_DESC"
echo "涉及 sepolicy 文件: $(echo "$DIFF" | grep -cE '^\+\+\+ b/sepolicy/')"
echo "新增规则行(allow/allowxperm/neverallow): $(echo "$DIFF" | grep -cE '^\+(allow|allowxperm|neverallow)[[:space:]]')"

emit "S1 敏感词（非 license 行的 + 行；无输出=通过）"
echo "$DIFF" | grep '^+' | grep -viE 'apache|license' | grep -iE 'password|passwd|secret|token|private[ _-]?key|backdoor|debug_backdoor' || true

emit "S2-A 向 sepolicy/base 新增策略（有输出=违反）"
echo "$DIFF" | grep -E '^\+\+\+ b/sepolicy/base/' || true
emit "S2-B 涉及的 ohos_policy/<子系统>/<部件> 目录（≥2 行=建议集中/拆分 MR）"
echo "$DIFF" | grep -E '^\+\+\+ b/sepolicy/ohos_policy/' | sed -E 's#^\+\+\+ b/sepolicy/ohos_policy/##' | sed -E 's#/(public|system|vendor)/.*##' | sort -u || true

emit "S3 新增参数标签 parameter_attr（有输出=需 init 责任田确认）"
echo "$DIFF" | grep '^+' | grep -E 'type[[:space:]]+[^,]+,[[:space:]]*parameter_attr' || true

emit "S4/S11 neverallow 新增/修改（有输出=S4 落点建议 + S11 需安全评审确认）"
echo "$DIFF" | grep '^+' | grep -nE 'neverallow' || true

emit "S5/S6 SA 服务 / 系统参数（有输出=S5 需确认 neverallow 看护 / S6 需确认）"
echo "$DIFF" | grep '^+' | grep -E 'sa_service_attr|parameter_service' || true

emit "S8 file_contexts 新增 bin 标签（人工核验是否用独立 type）"
echo "$DIFF" | grep '^+' | grep -E '/system/bin/|/vendor/bin/' || true

emit "S9/S10/S13 debug_only / developer_only 隔离宏位置（辅助定位包裹范围）"
echo "$DIFF" | grep -nE 'debug_only\(|developer_only\(' || true

emit "S11a 单条 neverallow 多个同类 violator 豁免（有输出=可能违反唯一性，人工核验语义）"
echo "$DIFF" | grep '^+' | grep -E 'neverallow' | grep -E '(-[a-z0-9_]*violator_).*(-[a-z0-9_]*violator_)|(-rgm_violater_).*(-rgm_violater_)' || true

emit "S12 sh 作为主体（有输出=需 DFX + 安全评审）"
echo "$DIFF" | grep '^+' | grep -E '^\+allow[[:space:]]+sh[[:space:]]' || true

emit "S13 su 主体（默认放行，冗余但不违规）/ 客体（需 debug_only）"
echo "$DIFF" | grep '^+' | grep -E '^\+allow[[:space:]]+su[[:space:]]' || true
echo "$DIFF" | grep '^+' | grep -E '^\+allow[[:space:]]+[a-z0-9_]+[[:space:]]+su:' || true

emit "S14 新增 ioctl 权限 / 配套 allowxperm（二者需配对，人工核对一一对应）"
echo "$DIFF" | grep '^+' | grep -E '^\+allow[[:space:]].*\{[[:space:]]*ioctl' || true
echo "$DIFF" | grep '^+' | grep -E '^\+allowxperm' || true

emit "S15 hap 权限（人工核验 hap_domain vs 具体 type 范围）"
echo "$DIFF" | grep '^+' | grep -E 'hap_domain|hap_file|data_app_' || true

emit "S16 禁用默认标签（有输出=违反）"
echo "$DIFF" | grep '^+' | grep -E 'limit_domain|default_param|default_service|default_hdf_service' || true

emit "S17 新增 allow/allowxperm 行数 vs #avc: 注释行数（数量应匹配；代码库写法 '# avc:' 带空格）"
allow_cnt=$(echo "$DIFF" | grep -cE '^\+[[:space:]]*allow(xperm)?[[:space:]]' || true)
avc_cnt=$(echo "$DIFF" | grep -cE '^\+.*#[[:space:]]*avc' || true)
echo "allow/allowxperm + 行: $allow_cnt    #avc: 注释 + 行: $avc_cnt"
echo "$DIFF" | grep '^+' | grep -E '^\+[[:space:]]*allow(xperm)?[[:space:]]' || true
echo "--- #avc: ---"
echo "$DIFF" | grep '^+' | grep -E '#[[:space:]]*avc[[:space:]]*:' || true

emit "S18-A public/ 下新增 allow（有输出=违反）/ S18-B/C allow 目录与主体（人工判断 system/vendor 落点）"
echo "$DIFF" | awk '/^\+\+\+ b\// {f=$2} /^\+[[:space:]]*allow/ && f ~ /\/public\// {print "[public违反] "f" => "$0}' || true
echo "$DIFF" | awk '/^\+\+\+ b\// {f=$2} /^\+[[:space:]]*allow/ && f !~ /^\+\+\+/ {print "[落点] "f" => "$0}' || true

emit "S19 相邻 allow 块缺空行（有 '缺空行' 输出=违反；跨文件不误报；rename 重构按步骤2判定基调处理）"
echo "$DIFF" | awk '
  /^diff --git/ { last="newfile"; next }
  /^\+\+\+ b\// { last="newfile"; next }
  /^\+[[:space:]]*#[[:space:]]*avc/ { next }
  /^\+[[:space:]]*allow(xperm)?[[:space:]]/ { if (last=="allow") print "缺空行: "$0; last="allow"; next }
  /^\+[[:space:]]*$/ { last="blank"; next }
  /^-/ { next }
  /^\+/ { last="other"; next }
' || true

emit "S20 allow 客体为 appdat（有输出=建议改用 normal_app_data）"
echo "$DIFF" | grep '^+' | grep -E '^\+[[:space:]]*allow[[:space:]]+[a-z0-9_]+[[:space:]]+appdat:' || true

emit "ROM 增量估算（A=新增规则行 D=删减规则行 M=access_vector变更）"
added=$(echo "$DIFF" | grep -cE '^\+(allow|allowxperm|neverallow)[[:space:]]' || true)
removed=$(echo "$DIFF" | grep -cE '^-(allow|allowxperm|neverallow)[[:space:]]' || true)
modcnt=$(echo "$DIFF" | grep -E '^[+-](allow|allowxperm)[[:space:]]' | sed -E 's/^[-+]//' | sed -E 's/[[:space:]]*\{.*//' | sort | uniq -d | wc -l)
echo "A=$added  D=$removed  M=$modcnt"
echo "ROM 增量估算 = (A - D + M) × 100B = $(( (added - removed + modcnt) * 100 )) B"

echo
echo "=== 自动检测完成。以上需人工判定项：S2-B定性 / S4落点 / S5看护 / S6范围 / S7写执行 / S9-S10隔离 / S11评审 / S18-B/C落点 / S17一一对应 ==="
