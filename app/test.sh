set -eux
chmod +x coverage.json
coverage json
COV=$(cat coverage.json)
PCT="$(echo "$COV" | python -c "import sys, json; print(json.load(sys.stdin)['totals']['percent_covered'])")"
echo "$PCT" | python -c "import sys; import json; print('Test coverage is fine') if json.load(sys.stdin) > 80 else sys.exit(1)"
coverage report
