#!/usr/bin/env bash
set -euo pipefail

# -------------------------------------------------------
# makeflag.sh
# - xxd 만 사용하여 랜덤 hex 생성
# - runs 디렉토리 초기화 후 runs/<KEY1>/flag-<KEY2> 생성
# - cron (root) 환경에서 안전하게 동작하도록 절대경로/환경 설정 포함
# -------------------------------------------------------

# PATH 명시 (cron 환경에서 안전)
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# 스크립트 위치 기준으로 동작
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"



# runs 디렉토리 (root가 만들고 관리)
RUNS_DIR="$SCRIPT_DIR/runs"
mkdir -p -- "$RUNS_DIR"

# 기존 내용 전부 삭제 (RUNS_DIR 내부만)
rm -rf -- "$RUNS_DIR"/* || true

# ---- xxd 전용 랜덤 hex 생성 함수 ----
random_hex_xxd() {
    local bytes=${1:-16}

    # xxd 가 있는지 확인
    if ! command -v xxd >/dev/null 2>&1; then
        echo "ERROR: xxd not found in PATH" >&2
        return 2
    fi

    # head -c 바이트 -> xxd (hexdump 옵션 없이 순수 hex)
    head -c "$bytes" /dev/urandom | xxd -p -c "$((bytes*2))"
}

# 키 바이트 길이 (필요 시 변경)
KEY_BYTES=16

# 생성
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

# 디렉토리 생성
mkdir -p -- "$TARGET_DIR"

# 파일 내용 작성
{
    echo "HSKF{p1z_1eak_urand0m_val}"
} > "$TARGET_FILE"

# 권한 설정 (root가 생성하므로 소유자/권한 요구에 따라 조정 가능)
chmod 666 "$TARGET_FILE" 2>/dev/null || true

