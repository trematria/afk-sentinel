#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo '=== AFK SENTINEL SOURCE VERIFICATION ==='
sha256sum -c SHA256SUMS.txt
PYTHONPATH=src python3 -m compileall -q src tests
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m afk_sentinel --config config.example.json --check
PYTHONPATH=src python3 -m afk_sentinel --config config.example.json --retention-preview
echo '=== VERIFICATION COMPLETE — NO CAMERA ACCESSED ==='
