#!/bin/bash

set -e

dir="$(dirname "$(realpath "$0")")"
postgres="$1"

if [ -z "$postgres" ]; then
	# read from config.toml
	postgres="$(PYTHONPATH="$dir/.." python3 -c "from config import config; print(config['db']['url'])")"
fi

psql "$postgres" -1 -f "$dir/update-score.sql"
psql "$postgres" -1 -f "$dir/fill-season.sql"
python "$dir/problems.py" "$postgres"
psql "$postgres" -1 -f "$dir/assign-problems.sql"

