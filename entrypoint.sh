#!/bin/sh
set -e  # прерываемся при любой ошибке

echo "=== INIT DB ==="
python rss_collector.py --init-only || { echo "Failed to init DB"; exit 1; }

echo "=== START COLLECTOR ==="
python rss_collector.py &

echo "=== START API ==="
exec python api.py
