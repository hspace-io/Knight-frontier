#!/usr/bin/env bash
set -euo pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RUNS_DIR="$SCRIPT_DIR/runs"
mkdir -p -- "$RUNS_DIR"
rm -rf -- "$RUNS_DIR"/* || true
random_hex_xxd() {
    local bytes=${1:-16}
    if ! command -v xxd >/dev/null 2>&1; then
        echo "ERROR: xxd not found in PATH" >&2
        return 2
    fi

    head -c "$bytes" /dev/urandom | xxd -p -c "$((bytes*2))"
}

KEY_BYTES=16

KEY1="$(random_hex_xxd "$KEY_BYTES")"
if [ $? -ne 0 ] || [ -z "$KEY1" ]; then
    echo "Failed to generate KEY1 via xxd" >&2
    exit 1
fi

KEY2="$(random_hex_xxd "$KEY_BYTES")"
if [ $? -ne 0 ] || [ -z "$KEY2" ]; then
    echo "Failed to generate KEY2 via xxd" >&2
    exit 1
fi

DIR_NAME="DIR-$KEY1"
FILE_NAME="flag-$KEY2"
TARGET_DIR="$RUNS_DIR/$DIR_NAME"
TARGET_FILE="$TARGET_DIR/$FILE_NAME"

mkdir -p -- "$TARGET_DIR"

{
    echo "HSKF{test_flag}"
} > "$TARGET_FILE"

chmod 666 "$TARGET_FILE" 2>/dev/null || true

