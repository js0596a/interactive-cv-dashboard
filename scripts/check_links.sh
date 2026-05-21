#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TMP_FILE="/tmp/cv_links_$$.txt"
trap 'rm -f "$TMP_FILE"' EXIT

python3 - <<'PY' > "$TMP_FILE"
from pathlib import Path
import re

text = Path("cv_data.py").read_text(encoding="utf-8")
urls = sorted(set(re.findall(r"https?://[^\"'\n]+", text)))
for url in urls:
    print(url)
PY

if [[ ! -s "$TMP_FILE" ]]; then
  echo "No URLs found in cv_data.py"
  exit 1
fi

echo "Checking links from cv_data.py..."
failed=0
while IFS= read -r url; do
  code="$(curl -L -s -o /dev/null -w "%{http_code}" "$url" || echo "000")"
  if [[ "$code" =~ ^2|3 ]]; then
    echo "OK  [$code] $url"
  elif [[ "$code" == "999" && "$url" == *"linkedin.com"* ]]; then
    echo "WARN[999] $url (blocked by provider bot protection)"
  else
    echo "BAD [$code] $url"
    failed=1
  fi
done < "$TMP_FILE"

if [[ $failed -eq 1 ]]; then
  echo "\nOne or more links failed."
  exit 1
fi

echo "\nAll links responded successfully."
