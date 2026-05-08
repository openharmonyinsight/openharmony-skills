#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_PATH="$SCRIPT_DIR/issue_output.json"

if [ ! -f "$JSON_PATH" ]; then
    echo "Error: issue_output.json not found"
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "Error: jq is required but not installed"
    exit 1
fi

TITLE=$(jq -r '.title // empty' "$JSON_PATH")
BODY=$(jq -r '.body // .content // empty' "$JSON_PATH")

if [ -z "$TITLE" ] || [ -z "$BODY" ]; then
    echo "Error: Missing title or body in issue_output.json"
    exit 1
fi

PAYLOAD=$(jq -n --arg title "$TITLE" --arg body "$BODY" '{"title": $title, "body": $body}')

WEBHOOK_URL="${WEBHOOK_URL:-http://42.193.17.157:8081/webhook}"

HEADERS=(-H "Content-Type: application/json" -H "Accept: application/json")
if [ -n "$WEBHOOK_SECRET" ]; then
    HEADERS+=(-H "X-Webhook-Secret: $WEBHOOK_SECRET")
fi

RESPONSE_FILE=$(mktemp)
HTTP_CODE=$(curl -s -o "$RESPONSE_FILE" -w "%{http_code}" "${HEADERS[@]}" -d "$PAYLOAD" "$WEBHOOK_URL")

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "Issue created successfully via webhook server."
    rm -f "$RESPONSE_FILE"
else
    echo "Error $HTTP_CODE: $(cat "$RESPONSE_FILE")"
    rm -f "$RESPONSE_FILE"
    exit 1
fi
