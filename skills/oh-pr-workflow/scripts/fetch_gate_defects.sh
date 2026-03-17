#!/usr/bin/env bash
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# fetch_gate_defects.sh — Fetch all codecheck defects from DCP gate CI
# Automatically paginates to retrieve ALL defects.
#
# Usage: fetch_gate_defects.sh <eventId> <taskId> [date]
# Output: JSON array of all defects to stdout, progress to stderr

set -uo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: fetch_gate_defects.sh <eventId> <taskId> [date]" >&2
    exit 1
fi

EVENT_ID="$1"
TASK_ID="$2"
DATE="${3:-}"
API_URL="https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/${EVENT_ID}/codecheck/task/${TASK_ID}"

python3 - "${API_URL}" "${DATE}" <<'PYEOF'
import sys, json, subprocess

api_url = sys.argv[1]
date = sys.argv[2]
page_size = 100
page_num = 1
total_count = 0
all_items = []

while True:
    body = json.dumps({
        "pageNum": page_num, "pageSize": page_size, "date": date,
        "defectStatus": "0", "defectLevel": "", "filePath": "",
        "fileName": "", "ruleSystemTags": "", "checkType": "",
        "rule": "", "trigger": "", "defectContent": "", "ruleName": ""
    })

    result = subprocess.run(
        ["curl", "-s", "--max-time", "30", "-X", "POST", api_url,
         "-H", "Content-Type: application/json", "-d", body],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"Error: curl failed on page {page_num}", file=sys.stderr)
        if all_items:
            break
        sys.exit(1)

    try:
        resp = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error: invalid JSON on page {page_num}", file=sys.stderr)
        if all_items:
            break
        sys.exit(1)

    if resp.get("code") != "20000":
        print(f"Error: API code={resp.get('code')} on page {page_num}: {resp.get('message','')}", file=sys.stderr)
        if all_items:
            break
        sys.exit(1)

    data = resp["data"]
    if page_num == 1:
        total_count = data["count"]
        print(f"Total defects: {total_count}", file=sys.stderr)

    defects = data["defects"]
    for defect in defects:
        detail = defect["defectDetailList"][0]
        all_items.append({
            "filepath": detail.get("filepath", ""),
            "lineNumber": detail.get("lineNumber", ""),
            "ruleName": detail.get("ruleName", ""),
            "defectContent": detail.get("defectContent", ""),
            "defectLevel": detail.get("defectLevel", ""),
            "defectStatus": detail.get("defectStatus", ""),
            "fragment": detail.get("fragment", []),
        })

    print(f"Fetched page {page_num}: {len(defects)} defects ({len(all_items)}/{total_count})", file=sys.stderr)

    if len(all_items) >= total_count or len(defects) < page_size:
        break

    page_num += 1

json.dump(all_items, sys.stdout, ensure_ascii=False, indent=2)
print()
PYEOF
