#!/bin/bash
# Export Jobs to CSV
cd "$(dirname "$0")"
python3 multi_platform_search.py export jobs_$(date +%Y%m%d).csv
echo "Jobs exported to jobs_$(date +%Y%m%d).csv"
