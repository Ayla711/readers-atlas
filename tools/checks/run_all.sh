#!/bin/sh
# Run every page check against the repo root (this script's grandparent). Fast ones first.
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
node tools/validate.js
for s in check_labels check_cjk check_contrast check_contrast_pixels check_wave check_name_dots flags_check_slow flags_check_zh_slow; do
  echo "== $s"; python3 -I "tools/checks/$s.py" "$ROOT" | tail -3
done
