#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://127.0.0.1:5000}"
echo "GET /api"
curl -fsS "$BASE_URL/api"
echo
echo "POST /submittodoitem"
curl -fsS -X POST "$BASE_URL/submittodoitem" \
  -H 'Content-Type: application/json' \
  -d '{"itemName":"Git practice","itemDescription":"Test API submission"}'
echo
echo "GET /items"
curl -fsS "$BASE_URL/items"
echo
