#!/usr/bin/env bash
# Re-fetch the source snapshot in sources/. Diff before trusting the result.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dst="$root/sources"

strip() {
  python3 -c "
import sys, re, html
raw = sys.stdin.read()
raw = re.sub(r'(?is)<(script|style|nav|footer)[^>]*>.*?</\1>', ' ', raw)
print(re.sub(r'[ \t]+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw))))"
}

fetch() {
  local url="$1" out="$2"
  local body; body="$(curl -sL --max-time 45 "$url")"
  if [ "${#body}" -lt 10000 ]; then
    echo "  SKIP (${#body} bytes) $out" >&2
    return
  fi
  printf '%s' "$body" | strip > "$out"
  echo "  ok $(basename "$out")"
}

echo "Google:"
curl -sL --max-time 45 https://developers.google.com/style/ui-elements \
  | grep -o 'href="/style/[a-z0-9-]*"' | sed 's/.*href="//;s/"//' | sort -u \
  | while read -r slug; do
      fetch "https://developers.google.com$slug" "$dst/google/$(basename "$slug").txt"
    done

echo "Microsoft:"
for p in top-10-tips-style-voice bias-free-communication numbers capitalization \
         punctuation/dashes-hyphens/ a-z-word-list-term-collections/p/please \
         global-communications/ punctuation/commas scannable-content/headings; do
  name="$(echo "$p" | tr '/' '-' | sed 's/-$//')"
  fetch "https://learn.microsoft.com/en-us/style-guide/$p" "$dst/microsoft/$name.txt"
done
