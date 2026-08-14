#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

(
    # shellcheck source=./common.sh
    source "$SCRIPT_DIR/common.sh"
    [[ "$WIKI_AGENTIZER_REF" =~ ^[0-9a-f]{40}$ ]] || {
        echo "default WIKI_AGENTIZER_REF must be a pinned commit SHA" >&2
        exit 1
    }
)

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

cat > "$tmp_dir/git" <<'GIT'
#!/usr/bin/env bash
set -euo pipefail

case "$1" in
    clone)
        mkdir -p "$3/.git"
        : > "$3/pyproject.toml"
        ;;
    -C)
        case "$3" in
            checkout)
                echo "$4" > "$2/checked-out-ref"
                ;;
            rev-parse)
                echo "0000000000000000000000000000000000000000"
                ;;
            *)
                exit 2
                ;;
        esac
        ;;
    *)
        exit 2
        ;;
esac
GIT
chmod +x "$tmp_dir/git"

if PATH="$tmp_dir:$PATH" \
    GIT_BIN="$tmp_dir/git" \
    WIKI_AGENTIZER_DIR="$tmp_dir/wiki_agentizer" \
    WIKI_AGENTIZER_REPO="https://example.invalid/wiki_agentizer" \
    bash -c 'source "$1"; clone_wiki_agentizer' _ "$SCRIPT_DIR/common.sh" 2>"$tmp_dir/mismatch.err"; then
    echo "clone_wiki_agentizer must fail when checked out HEAD differs from pinned ref" >&2
    exit 1
fi

grep -q "wiki_agentizer HEAD mismatch" "$tmp_dir/mismatch.err"
