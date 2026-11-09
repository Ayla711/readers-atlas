#!/bin/sh
# Run from the repository root. The final validator requires these independent copies.
set -eu
mkdir -p tools/us-work/shared/fresh-gutenberg
for id in 24 203 205 233 242 245 416 514 1298 2147 2701 2809 3177 7345 8813 11228 19146 64317; do
  curl -fL --max-time 60 "https://www.gutenberg.org/cache/epub/$id/pg$id.txt" \
    -o "tools/us-work/shared/fresh-gutenberg/pg$id.txt"
done
